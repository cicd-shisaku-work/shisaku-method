"""Compose a full HTML page from its parts using the files in ../templates."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from html import escape
from pathlib import Path
from string import Template
from urllib.parse import urlencode

from . import rules

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"


@lru_cache(maxsize=None)
def _template(name: str) -> Template:
    return Template((TEMPLATES / name).read_text(encoding="utf-8"))


@dataclass(frozen=True)
class PageParts:
    lang: str
    title: str
    description: str
    canonical: str
    head_meta: str
    main: str
    footer: str
    breadcrumb: str = ""
    local_nav: str = ""
    lang_switch: str = ""


def compose(parts: PageParts, ga_id: str | None) -> str:
    analytics = _template("analytics.html").substitute(ga_id=ga_id) if ga_id else ""
    return _template("base.html").substitute(
        lang=parts.lang,
        title=escape(parts.title),
        description=escape(parts.description),
        canonical=escape(parts.canonical),
        head_meta=parts.head_meta,
        analytics=analytics,
        skip_label=escape(rules.LABELS[parts.lang]["skip"]),
        lang_switch=parts.lang_switch,
        breadcrumb=parts.breadcrumb,
        layout_class=" has-local-nav" if parts.local_nav else "",
        main=parts.main,
        local_nav=parts.local_nav,
        footer=parts.footer,
        site_name=escape(rules.SITE_NAME),
        site_name_ja=escape(rules.SITE_NAME_JA),
    )


def lang_switch(lang: str, other_url: str | None) -> str:
    if not other_url:
        return ""
    other = "en" if lang == "ja" else "ja"
    return (
        f'<a class="lang-switch" href="{escape(other_url)}" hreflang="{other}" lang="{other}">'
        f'{escape(rules.LABELS[lang]["switch"])}</a>'
    )


def share(lang: str, absolute_url: str, text: str) -> str:
    """Links to the X and Facebook share dialogs for this page."""
    labels = rules.LABELS[lang]
    targets = [
        ("share-x", labels["share_x"], f"{rules.SHARE_X}?{urlencode({'text': text, 'url': absolute_url})}"),
        ("share-facebook", labels["share_facebook"], f"{rules.SHARE_FACEBOOK}?{urlencode({'u': absolute_url})}"),
    ]
    links = "".join(
        f'<li><a class="{cls}" href="{escape(href)}" target="_blank" rel="noopener noreferrer">{escape(label)}</a></li>'
        for cls, label, href in targets
    )
    return f'<nav class="share" aria-label="{escape(labels["share"])}"><ul>{links}</ul></nav>'


def generated_line(lang: str, fetched_at: datetime, commit_short: str, commit_url: str | None) -> str:
    """'Fetched from GitHub and built: <time> (commit <sha>)' in the page's timezone."""
    tz, tz_name = rules.TIMEZONES[lang]
    local = fetched_at.astimezone(tz)
    stamp = (
        f'<time datetime="{local.isoformat()}">'
        f'{local.strftime("%Y-%m-%d %H:%M")} {tz_name}</time>'
    )
    sha = escape(commit_short)
    commit = f'<a href="{escape(commit_url)}">{sha}</a>' if commit_url else sha
    if lang == "ja":
        return f'<p class="generated">{rules.LABELS[lang]["generated"]}：{stamp}（commit {commit}）</p>'
    return f'<p class="generated">{rules.LABELS[lang]["generated"]}: {stamp} (commit {commit})</p>'


def footer(lines: list[str]) -> str:
    return (
        f'<p class="footer-site"><a href="/">{escape(rules.SITE_NAME)}</a>'
        f' <span lang="ja">（{escape(rules.SITE_NAME_JA)}）</span></p>' + "".join(lines)
    )
