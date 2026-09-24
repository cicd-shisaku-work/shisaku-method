import unittest

from sitebuild import rules
from sitebuild.cards import Card, Painter, truncate, wrap

from .helpers import FONTS, NO_FONTS


def one(text):
    """Every character is one unit wide."""
    return float(len(text))


def png_size(data: bytes):
    import struct
    return struct.unpack(">II", data[16:24])


class WrapTest(unittest.TestCase):
    def test_japanese_breaks_between_characters(self):
        self.assertEqual(wrap("あいうえおかきくけこ", one, 4), ["あいうえ", "おかきく", "けこ"])

    def test_closing_punctuation_hangs(self):
        self.assertEqual(wrap("あいうえ。おか", one, 4), ["あいうえ。", "おか"])

    def test_opening_bracket_moves_down(self):
        self.assertEqual(wrap("あいう（えお）", one, 4), ["あいう", "（えお）"])

    def test_latin_words_stay_whole(self):
        self.assertEqual(wrap("model of change", one, 9), ["model of", "change"])

    def test_hyphenated_words_break_after_the_hyphen(self):
        self.assertEqual(wrap("shisaku-prediction-model", one, 19), ["shisaku-prediction-", "model"])

    def test_a_word_wider_than_the_line_is_cut(self):
        self.assertEqual(wrap("abcdefghij", one, 4), ["abcd", "efgh", "ij"])

    def test_whitespace_is_collapsed(self):
        self.assertEqual(wrap("  a   b\n c ", one, 10), ["a b c"])

    def test_truncate(self):
        self.assertEqual(truncate("あいうえお", one, 10), "あいうえお")
        self.assertEqual(truncate("あいうえお", one, 4), "あいう…")


class PainterWithoutFontsTest(unittest.TestCase):
    def test_default_image_needs_no_fonts(self):
        data = Painter(None).default()
        self.assertEqual(png_size(data), rules.OG_IMAGE_SIZE)

    def test_title_cards_need_fonts(self):
        with self.assertRaises(RuntimeError):
            Painter(None).card(Card("x", "原典"), "ja")


@unittest.skipUnless(FONTS, NO_FONTS)
class PainterTest(unittest.TestCase):
    def setUp(self):
        self.painter = Painter(FONTS)

    def test_sizes(self):
        self.assertEqual(png_size(self.painter.default()), rules.OG_IMAGE_SIZE)
        card = Card("アルファ 補足 ― 地図", "補足", "アルファ理論")
        self.assertEqual(png_size(self.painter.card(card, "ja")), rules.OG_IMAGE_SIZE)

    def test_drawing_is_deterministic(self):
        card = Card("シサク・ヒト変容理論", "原典")
        self.assertEqual(Painter(FONTS).card(card, "ja"), self.painter.card(card, "ja"))
        self.assertEqual(Painter(FONTS).default(), self.painter.default())

    def test_text_changes_the_image(self):
        self.assertNotEqual(self.painter.card(Card("A", "原典"), "ja"), self.painter.card(Card("B", "原典"), "ja"))

    def test_missing_glyphs_after_substitution(self):
        self.assertEqual(self.painter.missing_glyphs(Card("補足資料 ― 地図～", "補足", "理論")), [])
        self.assertEqual(self.painter.missing_glyphs(Card("𠮷", "原典")), ["𠮷"])

    def test_an_overlong_title_is_cut_to_fit(self):
        size, lines = self.painter._fit_title("長いタイトル" * 60, 1040, 316)
        self.assertEqual(size, rules.CARD_TITLE_SIZES[-1])
        self.assertTrue(lines[-1].endswith("…"))
        self.assertLessEqual(len(lines) * size * rules.CARD_TITLE_LEADING, 316)


if __name__ == "__main__":
    unittest.main()
