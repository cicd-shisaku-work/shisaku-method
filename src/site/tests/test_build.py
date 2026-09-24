import re
import struct
import tempfile
import unittest
from pathlib import Path

from sitebuild.build import BuildError, build, split_readme

from .helpers import ENV, FONT_DIR, FONTS, NO_FONTS, config


class BuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls._tmp.name) / "dist"
        cls.result = build(config(cls.out))

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def read(self, rel):
        return (self.out / rel).read_text(encoding="utf-8")

    def test_passes_the_quality_gate(self):
        self.assertEqual(self.result.violations, [])

    def test_pages(self):
        self.assertEqual(sorted(self.result.pages), sorted([
            "/", "/ja/readme.html", "/en/readme.html",
            "/ja/concepts/human/alpha/alpha.html",
            "/ja/concepts/human/alpha/alpha-map.html",
            "/ja/concepts/human/alpha/figures/alpha-figure.html",
            "/ja/concepts/universal/gamma/gamma.html",
            "/ja/concepts/universal/gamma/notes/gamma-note.html",
        ]))
        self.assertFalse((self.out / "ja/concepts/human/beta").exists())

    def test_titles(self):
        self.assertIn("<title>アルファ理論 | shisaku-method （シサクメソッド）</title>", self.read("ja/concepts/human/alpha/alpha.html"))
        self.assertIn("<title>README | shisaku-method （シサクメソッド）</title>", self.read("ja/readme.html"))
        self.assertIn("<title>shisaku-method （シサクメソッド）</title>", self.read("index.html"))
        self.assertIn("<title>alpha-figure | shisaku-method （シサクメソッド）</title>",
                      self.read("ja/concepts/human/alpha/figures/alpha-figure.html"))

    def test_body_is_one_origin_block(self):
        html = self.read("ja/concepts/human/alpha/alpha-map.html")
        self.assertEqual(html.count('data-origin="github"'), 1)
        article = re.search(r'<article[^>]*data-origin="github"[^>]*>(.*?)</article>', html, re.S).group(1)
        self.assertIn("これは理論ではなく、アルファ理論の補足資料である。", article)
        self.assertNotIn("local-nav", article)
        self.assertNotIn("breadcrumb", article)

    def test_footer_time_and_commit(self):
        ja = self.read("ja/concepts/human/alpha/alpha.html")
        self.assertIn("2026-09-23 09:30 JST", ja)
        self.assertIn('https://github.com/example/repo/commit/0123456789abcdef0123456789abcdef01234567', ja)
        self.assertIn(">0123456<", ja)
        en = self.read("en/readme.html")
        self.assertIn("2026-09-23 00:30 UTC", en)
        top = self.read("index.html")
        self.assertIn("JST", top)
        self.assertIn("UTC", top)

    def test_readme_split_and_pairing(self):
        ja, en = self.read("ja/readme.html"), self.read("en/readme.html")
        self.assertIn("このリポジトリは何か", ja)
        self.assertNotIn("What is this repository?", ja)
        self.assertIn("What is this repository?", en)
        self.assertIn('hreflang="en" href="https://site.example/en/readme.html"', ja)
        self.assertIn('hreflang="ja" href="https://site.example/ja/readme.html"', en)
        self.assertIn('class="lang-switch" href="/en/readme.html"', ja)

    def test_split_readme_strips_the_boundary_rules(self):
        ja, en = split_readme("# a\n\nx\n\n---\n\n---\n\n# shisaku-method (English)\n\ny\n")
        self.assertEqual(ja, "# a\n\nx\n")
        self.assertTrue(en.startswith("# shisaku-method (English)"))
        self.assertEqual(split_readme("# only\n"), ("# only\n", None))

    def test_sitemaps(self):
        top = self.read("index.html")
        for url in ("/ja/readme.html", "/en/readme.html", "/ja/concepts/universal/gamma/notes/gamma-note.html",
                    "/ja/concepts/human/alpha/figures/alpha-figure.html"):
            self.assertIn(f'href="{url}"', top)
        # upstream first: alpha declares gamma as its upstream, so gamma leads
        self.assertLess(top.index('href="/ja/concepts/universal/gamma/gamma.html"'),
                        top.index('href="/ja/concepts/human/alpha/alpha.html"'))
        self.assertEqual(self.result.upstream_unmatched, ["alpha: ベータ理論"])
        en = self.read("en/readme.html")
        self.assertNotIn("/ja/concepts/", en)  # the English sitemap lists English pages only
        xml = self.read("sitemap.xml")
        self.assertEqual(len(re.findall("<loc>", xml)), len(self.result.pages))
        self.assertIn("Sitemap: https://site.example/sitemap.xml", self.read("robots.txt"))

    def test_breadcrumb_and_local_nav(self):
        canon = self.read("ja/concepts/human/alpha/alpha.html")
        crumbs = re.search(r'<nav class="breadcrumb".*?</nav>', canon).group(0)
        self.assertEqual(crumbs.count("アルファ理論"), 1)  # not repeated on the entry page
        supplement = self.read("ja/concepts/human/alpha/alpha-map.html")
        self.assertIn('<li aria-current="page">アルファ 補足 ― 地図</li>', supplement)
        self.assertIn('<span class="badge">原典</span>', supplement)
        self.assertIn('href="/ja/concepts/human/alpha/alpha-map.html" aria-current="page"', supplement)

    def test_supplements_and_figures_sit_under_the_canon(self):
        top = self.read("index.html")
        alpha = re.search(r'<a href="/ja/concepts/human/alpha/alpha.html">.*?</ul></li>', top).group(0)
        self.assertIn('<ul class="sub">', alpha)
        self.assertIn('href="/ja/concepts/human/alpha/alpha-map.html"', alpha)
        self.assertIn('href="/ja/concepts/human/alpha/figures/alpha-figure.html"', alpha)
        nav = re.search(r'<aside class="local-nav".*?</aside>', self.read("ja/concepts/human/alpha/alpha-map.html")).group(0)
        self.assertRegex(nav, r'alpha\.html">アルファ理論</a> <span class="badge">原典</span><ul class="sub"><li><a href="[^"]*alpha-map\.html" aria-current="page">')

    def test_share_links_on_every_page(self):
        for page in self.out.rglob("*.html"):
            html = page.read_text(encoding="utf-8")
            with self.subTest(page.relative_to(self.out).as_posix()):
                self.assertIn('<nav class="share"', html)
                self.assertIn('href="https://x.com/intent/tweet?text=', html)
                self.assertIn('href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fsite.example%2F', html)
                self.assertIn('target="_blank" rel="noopener noreferrer"', html)
                self.assertNotIn("<script", html)  # no third-party script without an analytics ID
        doc = self.read("ja/concepts/human/alpha/alpha.html")
        self.assertIn("url=https%3A%2F%2Fsite.example%2Fja%2Fconcepts%2Fhuman%2Falpha%2Falpha.html", doc)
        self.assertIn("X でシェア", doc)
        self.assertIn("Share on X", self.read("en/readme.html"))

    def test_without_fonts_every_page_uses_the_default_image(self):
        self.assertFalse(self.result.share_cards)
        self.assertTrue(any("share cards omitted (no font directory given)" in w for w in self.result.warnings))
        self.assertFalse((self.out / "assets/og").exists())
        self.assertTrue((self.out / "assets/og-default.png").is_file())
        for page in self.out.rglob("*.html"):
            html = page.read_text(encoding="utf-8")
            with self.subTest(page.relative_to(self.out).as_posix()):
                self.assertIn('<meta property="og:image" content="https://site.example/assets/og-default.png">', html)
                self.assertIn('<meta property="og:image:width" content="1200">', html)
                self.assertIn('<meta property="og:image:height" content="630">', html)
                self.assertIn('<meta name="twitter:card" content="summary_large_image">', html)
                self.assertIn('<meta property="og:image:alt" content="shisaku-method', html)

    def test_figure_page_carries_license_and_source(self):
        html = self.read("ja/concepts/human/alpha/figures/alpha-figure.html")
        self.assertIn('<img src="alpha-figure.svg" alt="alpha-figure">', html)
        self.assertIn("https://creativecommons.org/licenses/by/4.0/", html)
        self.assertIn("https://github.com/example/repo/blob/main/concepts/human/alpha/ja/figures/alpha-figure.svg", html)
        self.assertTrue((self.out / "ja/concepts/human/alpha/figures/alpha-figure.svg").is_file())

    def test_no_analytics_without_id(self):
        self.assertNotIn("googletagmanager", self.read("index.html"))


@unittest.skipUnless(FONTS, NO_FONTS)
class ShareCardBuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls._tmp.name) / "dist"
        cls.result = build(config(cls.out, font_dir=FONT_DIR))

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def read(self, rel):
        return (self.out / rel).read_text(encoding="utf-8")

    def test_passes_the_quality_gate(self):
        self.assertEqual(self.result.violations, [])
        self.assertTrue(self.result.share_cards)
        self.assertFalse(any("share card" in w for w in self.result.warnings), self.result.warnings)

    def test_concept_pages_get_their_own_card(self):
        for url in ("/ja/concepts/human/alpha/alpha.html", "/ja/concepts/human/alpha/alpha-map.html",
                    "/ja/concepts/human/alpha/figures/alpha-figure.html"):
            with self.subTest(url):
                card = "assets/og" + url[:-5] + ".png"
                self.assertIn(f'<meta property="og:image" content="https://site.example/{card}">', self.read(url[1:]))
                head = (self.out / card).read_bytes()[:24]
                self.assertEqual(struct.unpack(">II", head[16:24]), (1200, 630))
        self.assertIn('<meta property="og:image:alt" content="アルファ 補足 ― 地図 | shisaku-method （シサクメソッド）">',
                      self.read("ja/concepts/human/alpha/alpha-map.html"))

    def test_top_and_readme_keep_the_default_image(self):
        for rel in ("index.html", "ja/readme.html", "en/readme.html"):
            self.assertIn('content="https://site.example/assets/og-default.png"', self.read(rel))

    def test_one_card_per_concept_page(self):
        cards = sorted(p.relative_to(self.out / "assets/og").as_posix() for p in (self.out / "assets/og").rglob("*.png"))
        pages = sorted(u[1:-5] + ".png" for u in self.result.pages if u.startswith("/ja/concepts/"))
        self.assertEqual(cards, pages)


class BuildVariantsTest(unittest.TestCase):
    def build_to(self, env):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        out = Path(tmp.name) / "dist"
        return out, build(config(out, env))

    def test_analytics_is_injected_from_the_environment(self):
        out, result = self.build_to({**ENV, "GA_MEASUREMENT_ID": "G-TEST1234"})
        self.assertTrue(result.ok, result.violations)
        for page in out.rglob("*.html"):
            self.assertIn("gtag/js?id=G-TEST1234", page.read_text(encoding="utf-8"), page)

    def test_malformed_analytics_id_is_dropped(self):
        out, result = self.build_to({**ENV, "GA_MEASUREMENT_ID": "G-1');alert(1)//"})
        self.assertNotIn("googletagmanager", (out / "index.html").read_text(encoding="utf-8"))
        self.assertTrue(any("GA_MEASUREMENT_ID" in w for w in result.warnings))

    def test_gate_stops_a_broken_link(self):
        # Without SOURCE_REPO the unresolvable link stays relative and breaks.
        _, result = self.build_to({"BASE_URL": "https://site.example"})
        self.assertFalse(result.ok)
        self.assertTrue(any("broken link missing.md" in v for v in result.violations), result.violations)

    def test_output_is_deterministic(self):
        a, _ = self.build_to(ENV)
        b, _ = self.build_to(ENV)
        files_a = sorted(p.relative_to(a) for p in a.rglob("*") if p.is_file())
        files_b = sorted(p.relative_to(b) for p in b.rglob("*") if p.is_file())
        self.assertEqual(files_a, files_b)
        for rel in files_a:
            self.assertEqual((a / rel).read_bytes(), (b / rel).read_bytes(), rel)

    def test_refuses_a_non_empty_output_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            (out / "stale.html").write_text("x")
            with self.assertRaises(BuildError):
                build(config(out))


if __name__ == "__main__":
    unittest.main()
