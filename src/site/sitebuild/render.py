"""Markdown to HTML, plus the title and description taken from a document.

The body is rendered as written: the site never rewrites the text. The only
change is that relative links are pointed at their published location
(DESIGN.md §5).
"""

from __future__ import annotations

import html
import posixpath
import re
from dataclasses import dataclass, field
from typing import Callable
from urllib.parse import urlsplit

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.footnote import footnote_plugin

from . import rules

# Given a repository path (POSIX, normalised), return the site URL or None.
Resolver = Callable[[str], "str | None"]


def make_parser() -> MarkdownIt:
    md = MarkdownIt("commonmark", {"html": True})
    md.enable(["table", "strikethrough"])
    md.use(footnote_plugin)
    md.use(anchors_plugin, min_level=1, max_level=6)
    return md


@dataclass
class Rendered:
    body: str
    title: str
    description: str
    unresolved: list[str] = field(default_factory=list)


def render_document(
    md: MarkdownIt,
    text: str,
    *,
    repo_path: str,
    resolve: Resolver,
    fallback_link: Callable[[str], "str | None"],
    fallback_title: str,
) -> Rendered:
    env: dict = {}
    tokens = md.parse(text, env)
    unresolved: list[str] = []
    _rewrite_links(tokens, repo_path, resolve, fallback_link, unresolved)
    body = md.renderer.render(tokens, md.options, env)
    title = first_h1(md, tokens) or fallback_title
    return Rendered(
        body=body,
        title=title,
        description=describe(md, text) or title,
        unresolved=unresolved,
    )


def render_plain_page(md: MarkdownIt, text: str) -> tuple[str, str]:
    """Render site-owned Markdown (landing copy); return (html, first paragraph)."""
    return md.render(text), describe(md, text)


# --- title ---------------------------------------------------------------------

def first_h1(md: MarkdownIt, tokens: list[Token]) -> str | None:
    for i, tok in enumerate(tokens):
        if tok.type == "heading_open" and tok.tag == "h1" and i + 1 < len(tokens):
            return plain_text(md, tokens[i + 1].content) or None
    return None


def plain_text(md: MarkdownIt, inline_markdown: str) -> str:
    rendered = md.renderInline(inline_markdown)
    text = html.unescape(re.sub(r"<[^>]+>", "", rendered))
    return re.sub(r"\s+", " ", text).strip()


# --- description (DESIGN.md §4.3) -------------------------------------------------

def describe(md: MarkdownIt, text: str) -> str:
    """First prose paragraph after the H1, skipping metadata lines."""
    lines = text.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].startswith("# "):
        i += 1

    para: list[str] = []
    in_fence = False
    while i < len(lines):
        raw = lines[i].strip()
        i += 1
        if raw.startswith(("```", "~~~")):
            in_fence = not in_fence
            if para:
                break
            continue
        if in_fence:
            continue
        if not raw:
            if para:
                break
            continue
        if raw.startswith("#") or _is_rule(raw) or raw.startswith("|"):
            if para:
                break
            continue
        line = rules.LIST_MARKER.sub("", raw.lstrip("> ").strip())
        plain = plain_text(md, line)
        if not plain:
            continue
        if not para and rules.META_LINE.match(plain):
            continue
        para.append(plain)

    return _trim(" ".join(para))


def _is_rule(line: str) -> bool:
    return len(line) >= 3 and set(line) <= set("-*_ ")


def _trim(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= rules.DESC_MAX:
        return text
    m = rules.SENTENCE_END.match(text[: rules.DESC_MAX])
    if m and len(m.group(1)) >= rules.DESC_MIN_SENTENCE:
        return m.group(1)
    return text[: rules.DESC_MAX].rstrip() + "…"


# --- links -------------------------------------------------------------------------

def _rewrite_links(
    tokens: list[Token],
    repo_path: str,
    resolve: Resolver,
    fallback_link: Callable[[str], "str | None"],
    unresolved: list[str],
) -> None:
    for tok in tokens:
        if tok.children:
            _rewrite_links(tok.children, repo_path, resolve, fallback_link, unresolved)
        attr = "href" if tok.type == "link_open" else "src" if tok.type == "image" else None
        if attr is None:
            continue
        value = tok.attrGet(attr)
        if not isinstance(value, str):
            continue
        new = _relink(value, repo_path, resolve, fallback_link, unresolved)
        if new is not None:
            tok.attrSet(attr, new)


def _relink(
    href: str,
    repo_path: str,
    resolve: Resolver,
    fallback_link: Callable[[str], "str | None"],
    unresolved: list[str],
) -> str | None:
    parts = urlsplit(href)
    if parts.scheme or parts.netloc or href.startswith("#") or not parts.path:
        return None
    if parts.path.startswith("/"):
        target = posixpath.normpath(parts.path.lstrip("/"))
    else:
        target = posixpath.normpath(posixpath.join(posixpath.dirname(repo_path), parts.path))
    fragment = f"#{parts.fragment}" if parts.fragment else ""
    url = resolve(target)
    if url is not None:
        return url + fragment
    unresolved.append(f"{repo_path}: {href}")
    external = fallback_link(target)
    return external + fragment if external else None
