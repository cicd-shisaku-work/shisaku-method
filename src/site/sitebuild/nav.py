"""Site-generated navigation: breadcrumb, local menu and HTML sitemap.

All of it sits outside ``<article data-origin="github">`` (DESIGN.md §4.4).
"""

from __future__ import annotations

from collections.abc import Sequence
from html import escape

from . import rules
from .model import Concept

Titles = dict[str, str]  # page URL -> title


def breadcrumb(lang: str, trail: list[tuple[str, str | None]]) -> str:
    """``trail`` items are (label, url); the last item is the current page."""
    labels = rules.LABELS[lang]
    items = []
    for n, (label, url) in enumerate(trail):
        text = escape(label)
        if n == len(trail) - 1:
            items.append(f'<li aria-current="page">{text}</li>')
        elif url:
            items.append(f'<li><a href="{escape(url)}">{text}</a></li>')
        else:
            items.append(f"<li>{text}</li>")
    return (
        f'<nav class="breadcrumb" aria-label="{escape(labels["breadcrumb"])}">'
        f'<ol>{"".join(items)}</ol></nav>'
    )


def trail_for(lang: str, concept: Concept, titles: Titles,
              current_url: str, current_label: str) -> list[tuple[str, str | None]]:
    """Home / README / category / concept / current page.

    On the concept's own entry page the concept is the current page, so the
    trail ends there instead of repeating it.
    """
    labels = rules.LABELS[lang]
    entry = concept.entry(lang)
    trail: list[tuple[str, str | None]] = [
        (labels["home"], "/"),
        (rules.README_LABEL, f"/{lang}/readme.html"),
        (concept.category, None),
        (titles.get(entry.url, concept.name), entry.url),
    ]
    if current_url != entry.url:
        trail.append((current_label, None))
    return trail


def local_nav(lang: str, concept: Concept, titles: Titles, current_url: str) -> str:
    labels = rules.LABELS[lang]
    docs = concept.docs.get(lang, ())
    figures = concept.figures.get(lang, ())
    parts = [
        f'<aside class="local-nav" aria-label="{escape(labels["local_nav"])}">',
        f'<p class="local-nav-title">{escape(titles.get(concept.entry(lang).url, concept.name))}</p>',
    ]
    if docs:
        parts.append(f'<h2>{escape(labels["docs"])}</h2>')
        parts.append(_nested(lang, list(docs), [], titles, current_url))
    if figures:
        parts.append(f'<h2>{escape(labels["figures"])}</h2><ul>')
        parts.extend(_item(f.url, titles[f.url], current_url, None) for f in figures)
        parts.append("</ul>")
    parts.append("</aside>")
    return "".join(parts)


def sitemap(lang: str, concepts: Sequence[Concept], titles: Titles,
            extra: list[tuple[str, str]] | None = None) -> str:
    """HTML sitemap of one language: concepts upstream to downstream, each with its documents and figures.

    ``concepts`` arrives already ordered; the category is shown as a label, not
    as a grouping, because upstream and downstream cross categories.
    """
    labels = rules.LABELS[lang]
    parts = [
        f'<nav class="sitemap" aria-label="{escape(labels["sitemap"])}">',
        f'<h2>{escape(labels["sitemap"])}</h2>',
    ]
    if extra:
        parts.append('<ul class="sitemap-extra">')
        parts.extend(f'<li><a href="{escape(url)}">{escape(label)}</a></li>' for url, label in extra)
        parts.append("</ul>")

    listed = [c for c in concepts if c.docs.get(lang) or c.figures.get(lang)]
    if listed:
        parts.append('<ol class="sitemap-tree">')
        for concept in listed:
            entry = concept.entry(lang)
            parts.append(
                f'<li><span class="sitemap-concept">{escape(titles.get(entry.url, concept.name))}</span>'
                f' <span class="sitemap-category">{escape(concept.category)}</span>'
            )
            parts.append(_nested(lang, list(concept.docs.get(lang, ())), list(concept.figures.get(lang, ())), titles, None))
            parts.append("</li>")
        parts.append("</ol>")
    parts.append("</nav>")
    return "".join(parts)


def _nested(lang: str, docs: list, figures: list, titles: Titles, current_url: str | None) -> str:
    """The canon at the top level; supplements and figures one level below it.

    Without a canon in this language, everything stays at one level.
    """
    labels = rules.LABELS[lang]
    canon = docs[0] if docs and docs[0].is_canon else None
    rest = [_item(d.url, titles[d.url], current_url, None) for d in docs if d is not canon]
    rest += [_item(f.url, titles[f.url], current_url, labels["figures"]) for f in figures]
    if canon is None:
        return f'<ul>{"".join(rest)}</ul>'
    head = _item(canon.url, titles[canon.url], current_url, labels["canon"], close=not rest)
    if rest:
        head += f'<ul class="sub">{"".join(rest)}</ul></li>'
    return f"<ul>{head}</ul>"


def _item(url: str, title: str, current_url: str | None, badge: str | None, close: bool = True) -> str:


    mark = f' <span class="badge">{escape(badge)}</span>' if badge else ""
    current = ' aria-current="page"' if url == current_url else ""
    end = "</li>" if close else ""
    return f'<li><a href="{escape(url)}"{current}>{escape(title)}</a>{mark}{end}'
