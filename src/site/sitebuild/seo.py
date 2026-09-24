"""Search-engine facing output: head metadata, sitemap.xml and robots.txt (DESIGN.md §9)."""

from __future__ import annotations

from html import escape
from xml.sax.saxutils import escape as xml_escape

from . import rules


def head_meta(
    *,
    base_url: str,
    url: str,
    lang: str,
    title: str,
    description: str,
    og_type: str,
    alternates: dict[str, str],
    image_url: str,
    image_alt: str,
) -> str:
    """OGP, card and hreflang tags. ``alternates`` maps language -> URL, including this page."""
    width, height = rules.OG_IMAGE_SIZE
    tags = [
        f'<meta property="og:title" content="{escape(title)}">',
        f'<meta property="og:description" content="{escape(description)}">',
        f'<meta property="og:url" content="{escape(base_url + url)}">',
        f'<meta property="og:site_name" content="{escape(rules.SITE_NAME)}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:locale" content="{rules.LOCALES[lang]}">',
        f'<meta property="og:image" content="{escape(image_url)}">',
        f'<meta property="og:image:width" content="{width}">',
        f'<meta property="og:image:height" content="{height}">',
        f'<meta property="og:image:alt" content="{escape(image_alt)}">',
        f'<meta name="twitter:card" content="{rules.TWITTER_CARD}">',
    ]
    if len(alternates) > 1:
        for alt_lang in sorted(alternates):
            tags.append(
                f'<link rel="alternate" hreflang="{alt_lang}" href="{escape(base_url + alternates[alt_lang])}">'
            )
    return "\n".join(tags)


def sitemap_xml(base_url: str, urls: list[str]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    lines.extend(f"  <url><loc>{xml_escape(base_url + u)}</loc></url>" for u in urls)
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def robots_txt(base_url: str) -> str:
    return f"User-agent: *\nAllow: /\n\nSitemap: {base_url}/sitemap.xml\n"
