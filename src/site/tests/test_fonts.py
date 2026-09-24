import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from sitebuild import fonts, rules

FILES = {"bold": b"bold font", "medium": b"medium font", "license": b"licence text"}


def pinned(contents):
    return {key: (f"{key}.bin", hashlib.sha256(data).hexdigest()) for key, data in contents.items()}


class FontsTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.source = self.tmp / "source"
        self.source.mkdir()
        for key, data in FILES.items():
            (self.source / f"{key}.bin").write_bytes(data)
        patcher = mock.patch.dict(rules.FONT_FILES, pinned(FILES), clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_nothing_given(self):
        self.assertEqual(fonts.locate(None), (None, "no font directory given"))

    def test_fetch_then_locate(self):
        dest = self.tmp / "fonts"
        got = fonts.fetch(dest, source=self.source.as_uri() + "/")
        self.assertEqual(sorted(got), ["bold.bin", "license.bin", "medium.bin"])
        found, why = fonts.locate(dest)
        self.assertIsNone(why)
        self.assertEqual(found.bold, dest / "bold.bin")
        self.assertEqual(fonts.fetch(dest, source=self.source.as_uri() + "/"), [])  # already in place

    def test_a_missing_file(self):
        dest = self.tmp / "fonts"
        fonts.fetch(dest, source=self.source.as_uri() + "/")
        (dest / "license.bin").unlink()
        found, why = fonts.locate(dest)
        self.assertIsNone(found)
        self.assertIn("license.bin is missing", why)

    def test_an_altered_file_is_not_used(self):
        dest = self.tmp / "fonts"
        fonts.fetch(dest, source=self.source.as_uri() + "/")
        (dest / "bold.bin").write_bytes(b"something else")
        found, why = fonts.locate(dest)
        self.assertIsNone(found)
        self.assertIn("does not match the pinned SHA-256", why)

    def test_a_download_with_the_wrong_hash_leaves_nothing_behind(self):
        (self.source / "medium.bin").write_bytes(b"tampered")
        dest = self.tmp / "fonts"
        with self.assertRaises(fonts.FontError):
            fonts.fetch(dest, source=self.source.as_uri() + "/")
        self.assertFalse((dest / "medium.bin").exists())
        self.assertEqual([p.name for p in dest.iterdir() if p.name.startswith(".")], [])


if __name__ == "__main__":
    unittest.main()
