import shutil
import tempfile
import unittest
from pathlib import Path

from sitebuild.build import build
from sitebuild.validate import validate

from .helpers import config

BASE = "https://site.example"


class ValidateTest(unittest.TestCase):
    """Start from a valid build, break one thing, and expect the gate to say so."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.good = Path(cls._tmp.name) / "good"
        assert build(config(cls.good)).ok

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.out = Path(tmp.name) / "dist"
        shutil.copytree(self.good, self.out)

    def edit(self, rel, old, new):
        path = self.out / rel
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def assertViolation(self, fragment):
        violations = validate(self.out, BASE)
        self.assertTrue(any(fragment in v for v in violations), violations)

    def test_clean_output_passes(self):
        self.assertEqual(validate(self.out, BASE), [])

    def test_broken_internal_link(self):
        (self.out / "ja/concepts/human/alpha/alpha-map.html").unlink()
        self.assertViolation("broken link /ja/concepts/human/alpha/alpha-map.html")

    def test_missing_asset(self):
        (self.out / "ja/concepts/human/alpha/figures/alpha-figure.svg").unlink()
        self.assertViolation("broken link alpha-figure.svg")

    def test_empty_title(self):
        self.edit("ja/readme.html", "<title>README", "<title>")
        self.edit("ja/readme.html", " | shisaku-method （シサクメソッド）</title>", "</title>")
        self.assertViolation("/ja/readme.html: empty <title>")

    def test_missing_share_image(self):
        (self.out / "assets/og-default.png").unlink()
        self.assertViolation("og:image https://site.example/assets/og-default.png does not exist")

    def test_share_image_that_is_not_a_png(self):
        (self.out / "assets/og-default.png").write_bytes(b"GIF89a" + bytes(20))
        self.assertViolation("og:image /assets/og-default.png is not a 1200x630 PNG")

    def test_wrong_canonical(self):
        self.edit("ja/readme.html", 'rel="canonical" href="https://site.example/ja/readme.html"',
                  'rel="canonical" href="https://site.example/other.html"')
        self.assertViolation("/ja/readme.html: canonical")

    def test_missing_footer_stamp(self):
        self.edit("ja/concepts/universal/gamma/gamma.html", '<p class="generated">', '<p>')
        self.assertViolation("gamma.html: footer lacks")

    def test_one_sided_hreflang(self):
        self.edit("en/readme.html", 'hreflang="ja"', 'hreflang="xx"')
        self.assertViolation("/ja/readme.html: hreflang en is not reciprocated")

    def test_page_missing_from_html_sitemaps(self):
        (self.out / "ja/extra.html").write_text(
            (self.out / "ja/readme.html").read_text(encoding="utf-8").replace(
                "/ja/readme.html\"", "/ja/extra.html\"", 1), encoding="utf-8")
        self.assertViolation("/ja/extra.html: not listed in any HTML sitemap")
        self.assertViolation("sitemap.xml lacks /ja/extra.html")

    def test_sitemap_xml_lists_a_missing_page(self):
        (self.out / "ja/concepts/universal/gamma/notes/gamma-note.html").unlink()
        self.assertViolation("sitemap.xml lists missing page /ja/concepts/universal/gamma/notes/gamma-note.html")


if __name__ == "__main__":
    unittest.main()
