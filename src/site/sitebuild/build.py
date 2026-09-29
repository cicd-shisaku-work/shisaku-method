"""The build pipeline: discover -> render -> write -> validate (DESIGN.md §16.4).

This module owns the order of the stages. File writes happen only in
``_write``; everything before it works on in-memory values.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
from pathlib import Path

from markdown_it import MarkdownIt

from . import assets, fonts, nav, order, page, rules, seo
from .cards import Card, Painter
from .config import Config
from .discover import discover
from .model import Concept, Corpus, Doc, Figure
from .render import Rendered, make_parser, render_document, render_plain_page
from .validate import validate

CONTENT = Path(__file__).resolve().parent.parent / "content"


class BuildError(Exception):
    pass


@dataclass
class BuildResult:
    pages: list[str]
    excluded: tuple[str, ...]
    unresolved: list[str]
    violations: list[str]
    warnings: tuple[str, ...]
    files: int = 0
    upstream_unmatched: list[str] = field(default_factory=list)
    share_cards: bool = False   # per-page title cards were drawn (fonts present and verified)

    @property
    def ok(self) -> bool:
        return not self.violations

    def report(self) -> str:
        lines = [
            f"pages: {len(self.pages)}  files: {self.files}",
            f"excluded concepts ({len(self.excluded)}): {', '.join(self.excluded) or '-'}",
            f"share cards: {'per page' if self.share_cards else 'default image only'}",
        ]
        lines += [f"unresolved link: {u}" for u in self.unresolved]
        lines += [f"upstream outside the site: {u}" for u in self.upstream_unmatched]
        lines += [f"warning: {w}" for w in self.warnings]
        lines += [f"violation: {v}" for v in self.violations]
        return "\n".join(lines)


@dataclass
class _Page:
    url: str
    lang: str
    html: str
    card: Card | None = None   # drawn to rules.card_path(url) when set


@dataclass
class _Context:
    cfg: Config
    corpus: Corpus
    md: MarkdownIt
    painter: Painter
    titles: dict[str, str] = field(default_factory=dict)
    rendered: dict[str, Rendered] = field(default_factory=dict)
    unresolved: list[str] = field(default_factory=list)
    ordered: list[Concept] = field(default_factory=list)     # upstream to downstream
    warnings: list[str] = field(default_factory=list)
    upstream_unmatched: list[str] = field(default_factory=list)


def build(cfg: Config) -> BuildResult:
    if cfg.out.exists() and any(cfg.out.iterdir()):
        raise BuildError(f"output directory is not empty: {cfg.out}")

    found, why_not = fonts.locate(cfg.font_dir)
    ctx = _Context(cfg=cfg, corpus=discover(cfg.src), md=make_parser(), painter=Painter(found))
    if found is None:
        ctx.warnings.append(f"share cards omitted ({why_not}); every page uses the default image")
    readme = _render_sources(ctx)
    _order_concepts(ctx)
    pages = _pages(ctx, readme)

    files = _write(cfg.out, pages, ctx.corpus, cfg.base_url, ctx.painter)
    violations = validate(cfg.out, cfg.base_url)
    return BuildResult(
        pages=[p.url for p in pages],
        excluded=ctx.corpus.excluded,
        unresolved=ctx.unresolved,
        violations=violations,
        warnings=cfg.warnings + tuple(ctx.warnings),
        files=files,
        upstream_unmatched=ctx.upstream_unmatched,
        share_cards=ctx.painter.can_draw_text,
    )


# --- stage: render the sources ----------------------------------------------------

def _render_sources(ctx: _Context) -> dict[str, Rendered]:
    corpus, cfg = ctx.corpus, ctx.cfg
    link_map = {d.repo_path: d.url for d in corpus.docs()}
    link_map.update({f.repo_path: f.url for f in corpus.figures()})
    link_map[rules.README_FILE] = f"/{rules.PRIMARY_LANG}/readme.html"

    def render(text: str, repo_path: str, fallback_title: str) -> Rendered:
        r = render_document(
            ctx.md, text,
            repo_path=repo_path,
            resolve=link_map.get,
            fallback_link=cfg.blob_url,
            fallback_title=fallback_title,
        )
        ctx.unresolved.extend(r.unresolved)
        return r

    for doc in corpus.docs():
        r = render(_read(doc.source), doc.repo_path, doc.rel)
        ctx.rendered[doc.url] = r
        ctx.titles[doc.url] = r.title
    for fig in corpus.figures():
        ctx.titles[fig.url] = fig.name

    readme: dict[str, Rendered] = {}
    for lang, text in zip(("ja", "en"), split_readme(_read(corpus.readme))):
        if text is not None:
            readme[lang] = render(text, rules.README_FILE, rules.README_LABEL)
            ctx.titles[f"/{lang}/readme.html"] = rules.README_LABEL
    return readme


def _order_concepts(ctx: _Context) -> None:
    """Upstream first, read from each canon's own "上流依存" line (DESIGN.md §4.5)."""
    canons: dict[str, str] = {}
    titles: dict[str, str] = {}
    by_name: dict[str, Concept] = {}
    for concept in ctx.corpus.concepts:
        by_name[concept.name] = concept
        canon = next(d for d in concept.docs[rules.PRIMARY_LANG] if d.is_canon)
        canons[concept.name] = _read(canon.source)
        titles[concept.name] = ctx.titles[canon.url]
    result = order.concept_order(canons, titles)
    ctx.ordered = [by_name[name] for name in result.concepts]
    ctx.upstream_unmatched = result.unmatched
    if result.cycle:
        ctx.warnings.append(f"upstream cycle; placed by name: {', '.join(result.cycle)}")


def split_readme(text: str) -> tuple[str, str | None]:
    """Split the bilingual README at the English H1 line."""
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.rstrip("\r\n") == rules.README_EN_H1:
            return _strip_trailing_rules("".join(lines[:i])), "".join(lines[i:])
    return text, None


def _strip_trailing_rules(text: str) -> str:
    lines = text.rstrip().splitlines()
    while lines and (not lines[-1].strip() or set(lines[-1].strip()) <= set("-*_")):
        lines.pop()
    return "\n".join(lines) + "\n"


# --- stage: compose pages ------------------------------------------------------------

def _pages(ctx: _Context, readme: dict[str, Rendered]) -> list[_Page]:
    corpus = ctx.corpus
    urls = ["/"] + [f"/{lang}/readme.html" for lang in ("ja", "en") if lang in readme]
    urls += [d.url for d in corpus.docs()] + [f.url for f in corpus.figures()]
    url_set = set(urls)

    pages = [_top_page(ctx, url_set)]
    pages += [_readme_page(ctx, lang, r, url_set) for lang, r in readme.items()]
    for concept in corpus.concepts:
        for lang in concept.langs():
            pages += [_doc_page(ctx, concept, d, url_set) for d in concept.docs.get(lang, ())]
            pages += [_figure_page(ctx, concept, f, url_set) for f in concept.figures.get(lang, ())]
    return pages


def _alternates(url: str, url_set: set[str]) -> dict[str, str]:
    for lang in rules.LANGS:
        prefix = f"/{lang}/"
        if url.startswith(prefix):
            rest = url[len(prefix):]
            return {l: f"/{l}/{rest}" for l in rules.LANGS if f"/{l}/{rest}" in url_set}
    return {}


def _finish(ctx: _Context, url: str, lang: str, title: str, description: str, og_type: str,
            content: str, footer_lines: list[str], url_set: set[str],
            breadcrumb: str = "", local_nav: str = "", tail: str = "",
            card: Card | None = None) -> _Page:
    """Assemble a page. ``main`` = content, then the share links, then ``tail`` (a sitemap).

    With a ``card`` (and fonts to draw it) the page gets its own share image.
    """
    cfg = ctx.cfg
    if card is not None and not ctx.painter.can_draw_text:
        card = None
    if card is not None:
        missing = ctx.painter.missing_glyphs(card)
        if missing:
            ctx.warnings.append(f"{url}: share card font has no glyph for {' '.join(missing)}")
        image, image_alt = rules.card_path(url), title
    else:
        image, image_alt = rules.OG_IMAGE_PATH, rules.LABELS[lang]["og_image_alt"]
    main = "\n".join(part for part in (content, page.share(lang, cfg.base_url + url, title), tail) if part)
    alternates = _alternates(url, url_set)
    other = next((u for l, u in alternates.items() if l != lang), None)
    parts = page.PageParts(
        lang=lang,
        title=title,
        description=description,
        canonical=cfg.base_url + url,
        head_meta=seo.head_meta(
            base_url=cfg.base_url, url=url, lang=lang, title=title,
            description=description, og_type=og_type, alternates=alternates,
            image_url=cfg.base_url + image, image_alt=image_alt,
        ),
        main=main,
        footer=page.footer(footer_lines),
        breadcrumb=breadcrumb,
        local_nav=local_nav,
        lang_switch=page.lang_switch(lang, other),
    )
    return _Page(url=url, lang=lang, html=page.compose(parts, cfg.ga_id), card=card)


def _generated(ctx: _Context, lang: str) -> str:
    cfg = ctx.cfg
    return page.generated_line(lang, cfg.fetched_at, cfg.commit_short, cfg.commit_url)


def _top_page(ctx: _Context, url_set: set[str]) -> _Page:
    sections, description = [], ""
    for lang in ("ja", "en"):
        html, first = render_plain_page(ctx.md, _read(CONTENT / f"landing.{lang}.md"))
        description = description or first
        sections.append(f'<section class="landing" lang="{lang}">\n{html}</section>')
    extra = [(u, label) for u, label in (
        ("/ja/readme.html", "README（日本語）"),
        ("/en/readme.html", "README (English)"),
    ) if u in url_set]
    return _finish(
        ctx, "/", "ja", rules.TOP_TITLE, description, "website", "\n".join(sections),
        [_generated(ctx, "ja"), _generated(ctx, "en")], url_set,
        tail=nav.sitemap("ja", ctx.ordered, ctx.titles, extra),
    )


def _readme_page(ctx: _Context, lang: str, r: Rendered, url_set: set[str]) -> _Page:
    url = f"/{lang}/readme.html"
    labels = rules.LABELS[lang]
    has_concepts = any(c.docs.get(lang) for c in ctx.corpus.concepts)
    extra = [] if has_concepts else [(url, rules.README_LABEL)]
    crumbs = nav.breadcrumb(lang, [(labels["home"], "/"), (rules.README_LABEL, None)])
    return _finish(
        ctx, url, lang, rules.README_LABEL + rules.TITLE_SUFFIX, r.description, "article",
        _article(lang, r.body), [_generated(ctx, lang)], url_set, breadcrumb=crumbs,
        tail=nav.sitemap(lang, ctx.ordered, ctx.titles, extra),
    )


def _doc_page(ctx: _Context, concept: Concept, doc: Doc, url_set: set[str]) -> _Page:
    r = ctx.rendered[doc.url]
    labels = rules.LABELS[doc.lang]
    crumbs = nav.breadcrumb(doc.lang, nav.trail_for(doc.lang, concept, ctx.titles, doc.url, r.title))
    if doc.is_canon:
        card = Card(title=r.title, kind=labels["canon"])
    else:
        card = Card(title=r.title, kind=labels["card_supplement"], context=_concept_title(ctx, concept, doc.lang))
    return _finish(
        ctx, doc.url, doc.lang, r.title + rules.TITLE_SUFFIX, r.description, "article",
        _article(doc.lang, r.body), [_generated(ctx, doc.lang)], url_set,
        breadcrumb=crumbs,
        local_nav=nav.local_nav(doc.lang, concept, ctx.titles, doc.url),
        card=card,
    )


def _figure_page(ctx: _Context, concept: Concept, fig: Figure, url_set: set[str]) -> _Page:
    lang, cfg = fig.lang, ctx.cfg
    labels = rules.LABELS[lang]
    concept_title = _concept_title(ctx, concept, lang)
    of = labels["figure_of"].format(concept=concept_title)
    description = f"{fig.name}（{of}）" if lang == "ja" else f"{fig.name} ({of})"
    blob = cfg.blob_url(fig.repo_path)
    source = (f'<a href="{escape(blob)}">{escape(blob)}</a>' if blob
              else f"<code>{escape(fig.repo_path)}</code>")
    main = (
        f'<figure class="figure-page">\n'
        f'<img src="{escape(fig.name)}.svg" alt="{escape(fig.name)}">\n'
        f"<figcaption>{escape(fig.name)}</figcaption>\n</figure>\n"
        f'<dl class="figure-source">\n'
        f'<dt>{escape(labels["license"])}</dt><dd><a href="{rules.LICENSE_URL}">{rules.LICENSE_NAME}</a></dd>\n'
        f'<dt>{escape(labels["source"])}</dt><dd>{source}</dd>\n</dl>'
    )
    crumbs = nav.breadcrumb(lang, nav.trail_for(lang, concept, ctx.titles, fig.url, fig.name))
    return _finish(
        ctx, fig.url, lang, fig.name + rules.TITLE_SUFFIX, description, "article",
        main, [_generated(ctx, lang)], url_set,
        breadcrumb=crumbs,
        local_nav=nav.local_nav(lang, concept, ctx.titles, fig.url),
        card=Card(title=fig.name, kind=labels["card_figure"], context=concept_title),
    )


def _concept_title(ctx: _Context, concept: Concept, lang: str) -> str:
    return ctx.titles.get(concept.entry(lang).url, concept.name)


def _article(lang: str, body: str) -> str:
    return f'<article class="origin" data-origin="github" lang="{lang}">\n{body}</article>'


# --- stage: write --------------------------------------------------------------------

def _write(out: Path, pages: list[_Page], corpus: Corpus, base_url: str, painter: Painter) -> int:
    count = 0
    for p in pages:
        target = out / ("index.html" if p.url == "/" else p.url.lstrip("/"))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(p.html, encoding="utf-8")
        count += 1
        if p.card is not None:
            _write_bytes(out, rules.card_path(p.url), painter.card(p.card, p.lang))
            count += 1
    _write_bytes(out, rules.OG_IMAGE_PATH, painter.default())
    count += 1
    count += assets.copy_static(out)
    for fig in corpus.figures():
        assets.copy_figure(out, fig)
        count += 1
    (out / "sitemap.xml").write_text(seo.sitemap_xml(base_url, [p.url for p in pages]), encoding="utf-8")
    (out / "robots.txt").write_text(seo.robots_txt(base_url), encoding="utf-8")
    return count + 2


def _write_bytes(out: Path, url_path: str, data: bytes) -> None:
    target = out / url_path.lstrip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")
