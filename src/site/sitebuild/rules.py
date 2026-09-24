"""Site rules held as data in one place.

Anything that decides *what* is published or *how* it is labelled lives here,
so that changing a rule means touching this file only (DESIGN.md §16.3).
"""

from __future__ import annotations

import re
from datetime import timedelta, timezone
from pathlib import Path

# --- scope -----------------------------------------------------------------

LANGS: tuple[str, ...] = ("ja", "en")
PRIMARY_LANG = "ja"
FIGURES_DIR = "figures"


def is_target_concept(concept_dir: Path) -> bool:
    """A concept is published only when it holds a canon named after itself."""
    return (concept_dir / PRIMARY_LANG / f"{concept_dir.name}.md").is_file()


def is_canon(concept: str, rel: str) -> bool:
    """The canon is the document whose stem equals the concept directory name."""
    return rel == concept


# --- upstream order (DESIGN.md §4.5) ------------------------------------------

# Each canon states its upstream near the top, e.g.
#   **上流依存：シサク・ヒト変容理論（SHTT）→ 前提優位理論（Premise Primacy）／最上流：シサク・世界解釈**
UPSTREAM_SCAN_LINES = 20
UPSTREAM_LINE = re.compile(r"上流依存\s*[:：]\s*(.+)")
UPSTREAM_SEGMENT_SEP = re.compile(r"／")
UPSTREAM_CHAIN_SEP = re.compile(r"\s*(?:→|->)\s*")
UPSTREAM_ROOT = re.compile(r"^最上流\s*[:：]\s*(.+)$")
UPSTREAM_NAME_NOISE = re.compile(r"[（(][^）)]*[）)]|\s*v\d+(?:\.\d+)*\s*$")


def order_key(concept: str) -> tuple[int, str]:
    """Among concepts that can be placed at the same time: interpretations first, then by name."""
    return (0 if concept.endswith("-interpretation") else 1, concept)


# --- README ------------------------------------------------------------------

README_FILE = "README.md"
README_EN_H1 = "# shisaku-method (English)"

# --- naming ------------------------------------------------------------------

SITE_NAME = "shisaku-method"
SITE_NAME_JA = "シサクメソッド"
TITLE_SUFFIX = f" | {SITE_NAME} （{SITE_NAME_JA}）"
TOP_TITLE = f"{SITE_NAME} （{SITE_NAME_JA}）"
README_LABEL = "README"

# --- description ---------------------------------------------------------------

DESC_MAX = 120          # characters
DESC_MIN_SENTENCE = 40  # shortest first sentence accepted as a cut point
META_LINE = re.compile(
    r"^(Author|Status|Version|Date|Upstream|Canonical|License)\b"
    r"|^(上流依存|最上流|関連|関連資料|バージョン|姉妹補足|系列|帳簿注記)"
    r"|^[^\s：]{1,10}："
)
LIST_MARKER = re.compile(r"^(?:[-*+]|\d+[.)])\s+")
SENTENCE_END = re.compile(r"^(.*?[。．.!?！？])")

# --- time --------------------------------------------------------------------

TIMEZONES = {
    "ja": (timezone(timedelta(hours=9)), "JST"),
    "en": (timezone.utc, "UTC"),
}

# --- labels ----------------------------------------------------------------------

LABELS: dict[str, dict[str, str]] = {
    "ja": {
        "home": "Home",
        "skip": "本文へ移動",
        "breadcrumb": "パンくずリスト",
        "local_nav": "この概念のドキュメント",
        "docs": "ドキュメント",
        "figures": "図版",
        "canon": "原典",
        "sitemap": "サイトマップ",
        "generated": "GitHub から取得・生成",
        "license": "ライセンス",
        "source": "GitHub",
        "switch": "English",
        "figure_of": "{concept}の図版",
        "share": "シェア",
        "share_x": "X でシェア",
        "share_facebook": "Facebook でシェア",
        "og_image_alt": "shisaku-method（シサクメソッド）",
        "card_supplement": "補足",
        "card_figure": "図版",
        "card_site": "shisaku-method（シサクメソッド）",
    },
    "en": {
        "home": "Home",
        "skip": "Skip to content",
        "breadcrumb": "Breadcrumb",
        "local_nav": "Documents in this concept",
        "docs": "Documents",
        "figures": "Figures",
        "canon": "Canon",
        "sitemap": "Sitemap",
        "generated": "Fetched from GitHub and built",
        "license": "License",
        "source": "GitHub",
        "switch": "日本語",
        "figure_of": "Figure of {concept}",
        "share": "Share",
        "share_x": "Share on X",
        "share_facebook": "Share on Facebook",
        "og_image_alt": "shisaku-method",
        "card_supplement": "Supplement",
        "card_figure": "Figure",
        "card_site": "shisaku-method",
    },
}
LOCALES = {"ja": "ja_JP", "en": "en_US"}

# --- licence (figure pages only; documents carry their own) ---------------------

LICENSE_NAME = "CC BY 4.0"
LICENSE_URL = "https://creativecommons.org/licenses/by/4.0/"

# --- share images (DESIGN.md §9) ---------------------------------------------------

OG_IMAGE_PATH = "/assets/og-default.png"   # README, the top page, and any page without a card
OG_IMAGE_SIZE = (1200, 630)
TWITTER_CARD = "summary_large_image"
CARD_ROOT = "/assets/og"                   # a page's card mirrors its path: /ja/x/y.html -> /assets/og/ja/x/y.png


def card_path(page_url: str) -> str:
    return CARD_ROOT + page_url[: -len(".html")] + ".png"


# Card drawing. The palette follows site.css (light scheme).
CARD_COLORS = {
    "bg": "#fbfaf7",
    "fg": "#2b2a27",
    "muted": "#6d6a62",
    "line": "#e5e1d8",
    "accent": "#2c6e7c",
    "accent_soft": "#e5f0f1",
    "bars": ("#2c6e7c", "#5b95a1", "#8fb6be", "#b7d2d7", "#d7e7ea"),
}
CARD_MARGIN = 80
CARD_TAGLINE = "原典と補足で読む、シサクの理論群"   # default image only (provisional wording)
CARD_TITLE_SIZES = (64, 58, 52, 46, 42)    # largest that fits wins; the last one truncates with "…"
CARD_TITLE_LEADING = 1.4
CARD_LABEL_SIZE = 28
CARD_SITE_SIZE = 30
NO_LINE_START = set("、。，．,.:;：；!?！？)]}）」』】〕〉》ー々ゝゞ・…‥ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮヵヶ")
NO_LINE_END = set("([{（「『【〔〈《")
# Characters the card font lacks, drawn with the nearest glyph it has.
CARD_GLYPH_SUBSTITUTES = {"―": "—", "～": "〜", "‒": "–"}

# Fonts are fetched at packaging time from google/fonts on GitHub, pinned to one
# commit and verified by SHA-256; they are never committed here (SIL OFL 1.1).
FONT_SOURCE = "https://raw.githubusercontent.com/google/fonts/e44c4b011a820c2cbe2fd2cfa8052037d7edb571/ofl/zenmarugothic/"
FONT_FILES = {
    "bold": ("ZenMaruGothic-Bold.ttf", "fe24426b9c8b5523a0146a8235c8674eccf0493af354a53ec895c3596d9eb745"),
    "medium": ("ZenMaruGothic-Medium.ttf", "3cfdb98a13571ede17fcc769f5093a97c38b80a7b9b2ab754a26b4d822092b3b"),
    "license": ("OFL.txt", "2a20cf7ce1909d8ee1e949095d340f7d7656705f7c810a2d6faf56800ad0cb3d"),
}

# --- share (plain links; no third-party script is loaded) -------------------------

SHARE_X = "https://x.com/intent/tweet"                      # params: text, url
SHARE_FACEBOOK = "https://www.facebook.com/sharer/sharer.php"  # param: u

# --- analytics -------------------------------------------------------------------

GA_ID_PATTERN = re.compile(r"^G-[A-Z0-9]{4,20}$")

# --- deploy ------------------------------------------------------------------------

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".svg": "image/svg+xml",
    ".xml": "application/xml",
    ".txt": "text/plain; charset=utf-8",
    ".png": "image/png",
}
DEFAULT_CONTENT_TYPE = "application/octet-stream"
CACHE_CONTROL = {
    ".html": "public, max-age=3600",
    ".xml": "public, max-age=3600",
    ".txt": "public, max-age=3600",
    ".css": "public, max-age=86400",
    ".svg": "public, max-age=86400",
    ".png": "public, max-age=86400",
}
DEFAULT_CACHE_CONTROL = "public, max-age=3600"
SHRINK_RATIO = 0.5  # refuse to publish fewer than half of the live HTML pages
