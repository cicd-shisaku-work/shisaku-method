import tempfile
import unittest
from pathlib import Path

from sitebuild.discover import DiscoveryError, discover

from .helpers import FIXTURE


class DiscoverTest(unittest.TestCase):
    def setUp(self):
        self.corpus = discover(FIXTURE)

    def test_scope_is_concepts_with_a_self_named_canon(self):
        names = [f"{c.category}/{c.name}" for c in self.corpus.concepts]
        self.assertEqual(names, ["human/alpha", "universal/gamma"])
        self.assertEqual(self.corpus.excluded, ("human/beta",))

    def test_canon_comes_first_then_by_name(self):
        alpha = self.corpus.concepts[0]
        self.assertEqual([d.rel for d in alpha.docs["ja"]], ["alpha", "alpha-map"])
        self.assertTrue(alpha.docs["ja"][0].is_canon)
        self.assertFalse(alpha.docs["ja"][1].is_canon)

    def test_nested_documents_keep_their_path(self):
        gamma = self.corpus.concepts[1]
        self.assertEqual([d.url for d in gamma.docs["ja"]], [
            "/ja/concepts/universal/gamma/gamma.html",
            "/ja/concepts/universal/gamma/notes/gamma-note.html",
        ])

    def test_figures_and_empty_language_directories(self):
        alpha = self.corpus.concepts[0]
        self.assertEqual([f.name for f in alpha.figures["ja"]], ["alpha-figure"])
        self.assertNotIn("en", alpha.docs)  # only .gitkeep
        self.assertEqual(alpha.langs(), ("ja",))

    def test_missing_readme_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(DiscoveryError):
                discover(Path(tmp))


if __name__ == "__main__":
    unittest.main()
