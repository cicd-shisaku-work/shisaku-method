"""Share images (og:image), drawn with Pillow at build time (DESIGN.md §9).

Two kinds of 1200x630 PNG:

- the default image, used by the top page, README and any page without a card;
- a title card for each concept page: badge (canon / supplement / figure),
  the concept it belongs to, the title, and the site name.

Drawing is deterministic: the same text, fonts and Pillow version give the same
bytes, so the daily deploy leaves unchanged cards alone. Text layout uses
Pillow's basic engine so the result does not depend on optional libraries.
Without fonts only the text-free default image can be drawn.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from io import BytesIO
from typing import Callable

from PIL import Image, ImageDraw, ImageFont

from . import rules
from .fonts import Fonts

W, H = rules.OG_IMAGE_SIZE
C = rules.CARD_COLORS
M = rules.CARD_MARGIN
ELLIPSIS = "…"

# A Latin word stays on one line, but may break after a hyphen; everything else breaks per character.
_TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9.,:;'’&+/_]*-?|\s+|.", re.S)


@dataclass(frozen=True)
class Card:
    title: str
    kind: str          # badge text
    context: str = ""  # the concept a supplement or figure belongs to


# --- text layout (pure; takes a width function so it can be tested without fonts) ---

def wrap(text: str, measure: Callable[[str], float], width: float) -> list[str]:
    """Break ``text`` into lines no wider than ``width``.

    Japanese breaks between characters, Latin words stay whole unless a word
    alone is too wide, closing punctuation never starts a line (it hangs at the
    end of the previous one) and opening brackets never end one.
    """
    lines: list[str] = []
    cur = ""
    for tok in _TOKEN.findall(" ".join(text.split())):
        if tok.isspace():
            if cur and measure(cur + tok) <= width:
                cur += tok
            elif cur:
                lines.append(cur.rstrip())
                cur = ""
            continue
        if measure(cur + tok) <= width:
            cur += tok
            continue
        if cur and tok[0] in rules.NO_LINE_START:
            cur += tok  # hang the punctuation
            continue
        carry = ""
        if len(cur) > 1 and cur[-1] in rules.NO_LINE_END:
            cur, carry = cur[:-1], cur[-1]
        if cur.strip():
            lines.append(cur.rstrip())
        cur = carry + tok
        while measure(cur) > width and len(cur) > 1:  # a single word wider than the line
            cut = len(cur) - 1
            while cut > 1 and measure(cur[:cut]) > width:
                cut -= 1
            lines.append(cur[:cut])
            cur = cur[cut:]
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def truncate(text: str, measure: Callable[[str], float], width: float) -> str:
    """``text`` shortened with an ellipsis until it fits ``width``."""
    if measure(text) <= width:
        return text
    while text and measure(text + ELLIPSIS) > width:
        text = text[:-1]
    return text.rstrip() + ELLIPSIS


# --- drawing -------------------------------------------------------------------------

class Painter:
    def __init__(self, fonts: Fonts | None) -> None:
        self.fonts = fonts
        self._cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}

    @property
    def can_draw_text(self) -> bool:
        return self.fonts is not None

    def missing_glyphs(self, card: Card) -> list[str]:
        """Characters of ``card`` the fonts cannot draw, even after substitution."""
        if not self.can_draw_text:
            return []
        found = set()
        for weight, text in (("bold", card.title), ("medium", card.kind + card.context)):
            font = self._font(weight, rules.CARD_LABEL_SIZE)
            notdef = font.getmask("\ue000")
            for ch in set(_substitute(text)):
                if ch.isspace():
                    continue
                mask = font.getmask(ch)
                if mask.size == notdef.size and bytes(mask) == bytes(notdef):
                    found.add(ch)
        return sorted(found)

    def _font(self, weight: str, size: int) -> ImageFont.FreeTypeFont:
        key = (weight, size)
        if key not in self._cache:
            assert self.fonts is not None
            path = self.fonts.bold if weight == "bold" else self.fonts.medium
            self._cache[key] = ImageFont.truetype(str(path), size, layout_engine=ImageFont.Layout.BASIC)
        return self._cache[key]

    def default(self) -> bytes:
        img, draw = _canvas()
        if not self.can_draw_text:
            _motif(draw, (W - 257) // 2, 168, 1.0)
            return _png(img)
        _motif(draw, 868, 168, 1.0)
        draw.text((96, 250), rules.SITE_NAME, font=self._font("bold", 84), fill=C["fg"], anchor="ls")
        draw.text((100, 350), rules.SITE_NAME_JA, font=self._font("medium", 44), fill=C["muted"], anchor="ls")
        draw.rounded_rectangle((96, 388, 168, 396), radius=4, fill=C["accent"])
        draw.text((96, 468), rules.CARD_TAGLINE, font=self._font("medium", 34), fill=C["fg"], anchor="ls")
        return _png(img)

    def card(self, card: Card, lang: str) -> bytes:
        if not self.can_draw_text:
            raise RuntimeError("title cards need fonts")
        card = Card(_substitute(card.title), _substitute(card.kind), _substitute(card.context))
        img, draw = _canvas()
        right = W - M

        # header: badge, then the concept it belongs to
        label = self._font("medium", rules.CARD_LABEL_SIZE)
        pad_x, pad_y = 20, 10
        badge_w = label.getlength(card.kind) + pad_x * 2
        badge_h = rules.CARD_LABEL_SIZE + pad_y * 2
        draw.rounded_rectangle((M, M, M + badge_w, M + badge_h), radius=badge_h // 2, fill=C["accent_soft"])
        draw.text((M + pad_x, M + badge_h / 2), card.kind, font=label, fill=C["accent"], anchor="lm")
        if card.context:
            x = M + badge_w + 20
            text = truncate(card.context, label.getlength, right - x)
            draw.text((x, M + badge_h / 2), text, font=label, fill=C["muted"], anchor="lm")

        # title: the largest size whose lines fit the band; the smallest truncates
        top, bottom = M + badge_h + 36, H - 150
        size, lines = self._fit_title(card.title, right - M, bottom - top)
        lead = size * rules.CARD_TITLE_LEADING
        y = top + (bottom - top - lead * len(lines)) / 2 + lead / 2
        title_font = self._font("bold", size)
        for line in lines:
            draw.text((M, y), line, font=title_font, fill=C["fg"], anchor="lm")
            y += lead

        # footer: rule, site name, small motif
        draw.line((M, H - 118, right, H - 118), fill=C["line"], width=2)
        site = rules.LABELS[lang]["card_site"]
        draw.text((M, H - 62), site, font=self._font("medium", rules.CARD_SITE_SIZE), fill=C["muted"], anchor="lm")
        _motif(draw, right - 257 * 0.28, H - 62 - 282 * 0.28 / 2, 0.28)
        return _png(img)

    def _fit_title(self, title: str, width: float, height: float) -> tuple[int, list[str]]:
        for size in rules.CARD_TITLE_SIZES:
            font = self._font("bold", size)
            lines = wrap(title, font.getlength, width)
            if len(lines) * size * rules.CARD_TITLE_LEADING <= height:
                return size, lines
        size = rules.CARD_TITLE_SIZES[-1]
        font = self._font("bold", size)
        keep = max(1, int(height // (size * rules.CARD_TITLE_LEADING)))
        lines = wrap(title, font.getlength, width)
        if len(lines) > keep:
            last = lines[keep - 1]
            while last and font.getlength(last + ELLIPSIS) > width:
                last = last[:-1]
            lines = lines[: keep - 1] + [last.rstrip() + ELLIPSIS]
        return size, lines


def _substitute(text: str) -> str:
    return "".join(rules.CARD_GLYPH_SUBSTITUTES.get(ch, ch) for ch in text)


def _canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), C["bg"])
    return img, ImageDraw.Draw(img)


def _motif(draw: ImageDraw.ImageDraw, x: float, y: float, scale: float) -> None:
    """Stepped bars with a stem: upstream at the top, flowing down. 257 x 282 at scale 1."""
    s = scale
    draw.line((x + 18 * s, y + 18 * s, x + 18 * s, y + 264 * s), fill=C["line"], width=max(2, round(4 * s)))
    bars = ((0, 236), (40, 196), (80, 176), (80, 150), (120, 128))
    for i, ((dx, w), color) in enumerate(zip(bars, C["bars"])):
        top = y + i * 62 * s
        box = (x + dx * s, top, x + (dx + w) * s, top + 34 * s)
        draw.rounded_rectangle(box, radius=17 * s, fill=color)


def _png(img: Image.Image) -> bytes:
    buf = BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()
