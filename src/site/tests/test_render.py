import unittest

from sitebuild.render import describe, first_h1, make_parser, render_document

MD = make_parser()

# Description rule (DESIGN.md §4.3). Each case reproduces a pattern found in the
# published documents, so a rule change shows here as a failing expectation.
DESCRIPTION_CASES = [
    ("canon with an upstream line",
     "# 題\n\n**上流依存：** A → B\n\nこれは、ヒト種を対象とする理論である。\n",
     "これは、ヒト種を対象とする理論である。"),
    ("supplement with a related line",
     "# 題\n\n関連：原典／姉妹補足\n\nこれは理論ではなく、補足資料である。\n",
     "これは理論ではなく、補足資料である。"),
    ("english metadata block",
     "# Title\n\nAuthor: shisaku\nStatus: draft\nVersion: v0.1\nDate: 2026/06/05\n\n本文書は記録である。\n",
     "本文書は記録である。"),
    ("bold metadata",
     "# 題\n\n* **Author:** shisaku\n* **Version:** v0.2\n\n本書は解釈である。\n",
     "本書は解釈である。"),
    ("ledger note",
     "# 題\n\n帳簿注記（2026-09-07）: 裁定済み。\n\n本資料は地図である。\n",
     "本資料は地図である。"),
    ("list as first paragraph",
     "# 題\n\n- これは着眼の枠組みである。\n- 型はない。\n",
     "これは着眼の枠組みである。 型はない。"),
    ("inline markup is flattened",
     "# 題\n\n**本書**は[リンク](x.md)と`code`を含む。\n",
     "本書はリンクとcodeを含む。"),
    ("long text cut at a sentence end",
     "# 題\n\n" + "あ" * 50 + "。" + "い" * 100 + "。\n",
     "あ" * 50 + "。"),
    ("long text without a sentence end is cut with an ellipsis",
     "# 題\n\n" + "う" * 200 + "\n",
     "う" * 120 + "…"),
    ("nothing usable", "# 題\n\n## 見出しだけ\n", ""),
]


class DescriptionTest(unittest.TestCase):
    def test_cases(self):
        for name, text, expected in DESCRIPTION_CASES:
            with self.subTest(name):
                self.assertEqual(describe(MD, text), expected)


class RenderTest(unittest.TestCase):
    def render(self, text, resolve=None, fallback=None):
        return render_document(
            MD, text,
            repo_path="concepts/c/x/ja/x.md",
            resolve=resolve or (lambda p: None),
            fallback_link=fallback or (lambda p: None),
            fallback_title="x",
        )

    def test_title_is_plain_h1(self):
        r = self.render("# **強調**された`題`\n\n本文。\n")
        self.assertEqual(r.title, "強調された題")

    def test_title_falls_back(self):
        self.assertEqual(self.render("本文だけ。\n").title, "x")
        self.assertIsNone(first_h1(MD, MD.parse("## 二段目\n")))

    def test_description_falls_back_to_title(self):
        self.assertEqual(self.render("# 題\n").description, "題")

    def test_text_is_not_rewritten(self):
        text = "# 題\n\n「引用」と——記号…そのまま。\n"
        self.assertIn("「引用」と——記号…そのまま。", self.render(text).body)

    def test_relative_link_is_resolved(self):
        r = self.render("[y](../../y/ja/y.md#節)", resolve={"concepts/c/y/ja/y.md": "/ja/y.html"}.get)
        self.assertIn('href="/ja/y.html#%E7%AF%80"', r.body)
        self.assertEqual(r.unresolved, [])

    def test_unresolved_link_goes_to_fallback_and_is_reported(self):
        r = self.render("[z](z.md)", fallback=lambda p: f"https://gh.example/{p}")
        self.assertIn('href="https://gh.example/concepts/c/x/ja/z.md"', r.body)
        self.assertEqual(r.unresolved, ["concepts/c/x/ja/x.md: z.md"])

    def test_external_and_anchor_links_are_untouched(self):
        r = self.render("[a](https://example.com/p) [b](#k) [c](mailto:a@example.com)")
        self.assertIn('href="https://example.com/p"', r.body)
        self.assertIn('href="#k"', r.body)
        self.assertIn('href="mailto:a@example.com"', r.body)
        self.assertEqual(r.unresolved, [])

    def test_headings_get_unique_ids(self):
        body = self.render("# 題\n\n## 定義\n\n## 定義\n").body
        self.assertIn('id="定義"', body)
        self.assertIn('id="定義-1"', body)


if __name__ == "__main__":
    unittest.main()
