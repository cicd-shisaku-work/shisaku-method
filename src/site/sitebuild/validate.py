"""Quality gate run on the finished output, before anything is published (DESIGN.md §16.1).

It reads only the output directory, so it checks what readers would get,
not what the builder meant to produce. Any violation stops the build.
"""

from __future__ import annotations

import posixpath
import re
import struct
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

from . import rules


_LINK_ATTRS = {"a": "href", "link": "href", "img": "src", "script": "src"}


@dataclass
class _PageFacts:
    lang: str | None = None
    title: str = ""
    description: str | None = None
    canonical: str | None = None
    alternates: dict[str, str] = field(default_factory=dict)
    og_image: str | None = None
    links: list[str] = field(default_factory=list)
    sitemap_links: list[str] = field(default_factory=list)
    has_generated: bool = False


class _Scanner(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.facts = _PageFacts()
        self._in_title = False
        self._sitemap_depth = 0
        self._in_footer_generated = False
        self._saw_time = False
        self._saw_commit = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        f = self.facts
        if tag == "html":
            f.lang = a.get("lang") or None
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and a.get("name") == "description":
            f.description = a.get("content", "")
        elif tag == "meta" and a.get("property") == "og:image":
            f.og_image = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            f.canonical = a.get("href")
        elif tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            f.alternates[a["hreflang"]] = a.get("href", "")
        elif tag == "nav":
            if self._sitemap_depth:
                self._sitemap_depth += 1
            elif "sitemap" in a.get("class", "").split():
                self._sitemap_depth = 1
        elif tag == "p" and "generated" in a.get("class", "").split():
            self._in_footer_generated = True
        elif tag == "time" and self._in_footer_generated and a.get("datetime"):
            self._saw_time = True

        attr = _LINK_ATTRS.get(tag)
        if tag == "link" and a.get("rel") != "stylesheet":
            attr = None
        value = a.get(attr) if attr else None
        if value:
            f.links.append(value)
            if self._sitemap_depth and tag == "a":
                f.sitemap_links.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag == "nav" and self._sitemap_depth:
            self._sitemap_depth -= 1
        elif tag == "p" and self._in_footer_generated:
            if self._saw_time and self._saw_commit:
                self.facts.has_generated = True
            self._in_footer_generated = False
            self._saw_time = False
            self._saw_commit = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.facts.title += data
        if self._in_footer_generated and "commit" in data:
            self._saw_commit = True


def _scan(path: Path) -> _PageFacts:
    scanner = _Scanner()
    text = path.read_text(encoding="utf-8")
    scanner.feed(text)
    scanner.close()
    return scanner.facts


def page_url(out: Path, path: Path) -> str:
    rel = path.relative_to(out).as_posix()
    return "/" if rel == "index.html" else "/" + rel


def _target(base: str, link: str) -> str | None:
    """The output-relative path a link points to, or None if it leaves the site."""
    parts = urlsplit(link)
    if parts.scheme or parts.netloc or link.startswith("#"):
        return None
    path = parts.path
    if not path:
        return None
    if not path.startswith("/"):
        path = posixpath.join(posixpath.dirname(base), path)
    path = posixpath.normpath(path)
    if path == "/" or path.endswith("/"):
        path = path.rstrip("/") + "/index.html"
    return path


def validate(out: Path, base_url: str) -> list[str]:
    violations: list[str] = []
    html_files = sorted(out.rglob("*.html"))
    pages = {page_url(out, p): p for p in html_files}
    facts = {url: _scan(path) for url, path in pages.items()}

    def exists(path: str) -> bool:
        return (out / path.lstrip("/")).is_file()

    covered: set[str] = set()
    image_ok: dict[str, bool] = {}
    for url, f in facts.items():
        where = url
        if not f.lang:
            violations.append(f"{where}: missing <html lang>")
        if not f.title.strip():
            violations.append(f"{where}: empty <title>")
        if not (f.description or "").strip():
            violations.append(f"{where}: empty meta description")
        if f.canonical != base_url + url:
            violations.append(f"{where}: canonical is {f.canonical!r}, expected {base_url + url!r}")
        if not f.og_image or not f.og_image.startswith(base_url + "/"):
            violations.append(f"{where}: og:image missing or outside the site")
        elif not exists(f.og_image[len(base_url):]):
            violations.append(f"{where}: og:image {f.og_image} does not exist")
        else:
            image = f.og_image[len(base_url):]
            if image not in image_ok:
                image_ok[image] = _png_size(out / image.lstrip("/")) == rules.OG_IMAGE_SIZE
            if not image_ok[image]:
                w, h = rules.OG_IMAGE_SIZE
                violations.append(f"{where}: og:image {image} is not a {w}x{h} PNG")
        if not f.has_generated:
            violations.append(f"{where}: footer lacks the build time and commit")
        for link in f.links:
            target = _target(url if url != "/" else "/index.html", link)
            if target is not None and not exists(target):
                violations.append(f"{where}: broken link {link}")
        for lang, href in f.alternates.items():
            if not href.startswith(base_url):
                violations.append(f"{where}: hreflang {lang} points outside the site")
                continue
            other = href[len(base_url):]
            back = facts.get(other)
            if back is None:
                violations.append(f"{where}: hreflang {lang} target {other} does not exist")
            elif back.alternates.get(f.lang or "") != base_url + url:
                violations.append(f"{where}: hreflang {lang} is not reciprocated by {other}")
        for link in f.sitemap_links:
            target = _target(url if url != "/" else "/index.html", link)
            if target:
                covered.add("/" if target == "/index.html" else target)

    for url in pages:
        if url != "/" and url not in covered:
            violations.append(f"{url}: not listed in any HTML sitemap")

    violations += _check_sitemap_xml(out, base_url, set(pages))
    if not (out / "robots.txt").is_file():
        violations.append("robots.txt is missing")
    return violations


def _png_size(path: Path) -> tuple[int, int] | None:
    """Width and height from a PNG header, or None if it is not a PNG."""
    with path.open("rb") as fh:
        head = fh.read(24)
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", head[16:24])


def _check_sitemap_xml(out: Path, base_url: str, pages: set[str]) -> list[str]:
    path = out / "sitemap.xml"
    if not path.is_file():
        return ["sitemap.xml is missing"]
    locs = re.findall(r"<loc>(.*?)</loc>", path.read_text(encoding="utf-8"))
    listed = {loc[len(base_url):] for loc in locs if loc.startswith(base_url)}
    problems = []
    if len(listed) != len(locs):
        problems.append("sitemap.xml has entries outside the site")
    problems += [f"sitemap.xml lacks {u}" for u in sorted(pages - listed)]
    problems += [f"sitemap.xml lists missing page {u}" for u in sorted(listed - pages)]
    return problems
