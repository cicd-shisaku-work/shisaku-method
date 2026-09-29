import io
import tarfile
import tempfile
import unittest
from pathlib import Path

from sitebuild.fetch import FetchError, extract, fetch, tarball_url

SHA = "3a349a9587fb9dd58783a4423ae6b7ded809d923"


def make_tarball(path: Path, members: dict[str, bytes], comment: str | None = SHA) -> None:
    pax = {"comment": comment} if comment else {}
    with tarfile.open(path, "w:gz", format=tarfile.PAX_FORMAT, pax_headers=pax) as tf:
        for name, data in members.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))


class FetchTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)

    def test_url(self):
        self.assertEqual(tarball_url("o/r", "main"), "https://codeload.github.com/o/r/tar.gz/refs/heads/main")

    def test_commit_comes_from_the_pax_header(self):
        archive = self.tmp / "a.tar.gz"
        make_tarball(archive, {"repo-main/README.md": b"# r\n", "repo-main/concepts/x.md": b"x"})
        root, commit = extract(archive, self.tmp / "x")
        self.assertEqual(root.name, "repo-main")
        self.assertEqual(commit, SHA)
        self.assertTrue((root / "README.md").is_file())

    def test_missing_header_gives_unknown(self):
        archive = self.tmp / "a.tar.gz"
        make_tarball(archive, {"repo-main/README.md": b"# r\n"}, comment=None)
        self.assertEqual(extract(archive, self.tmp / "x")[1], "unknown")

    def test_path_traversal_is_rejected(self):
        archive = self.tmp / "a.tar.gz"
        make_tarball(archive, {"repo-main/README.md": b"# r\n", "repo-main/../../evil.txt": b"x"})
        with self.assertRaises(FetchError):
            extract(archive, self.tmp / "x")
        self.assertFalse((self.tmp / "evil.txt").exists())

    def test_readme_is_required(self):
        archive = self.tmp / "a.tar.gz"
        make_tarball(archive, {"repo-main/other.md": b"x"})
        with self.assertRaises(FetchError):
            extract(archive, self.tmp / "x")

    def test_fetch_from_a_url(self):
        archive = self.tmp / "a.tar.gz"
        make_tarball(archive, {"repo-main/README.md": b"# r\n"})
        source = fetch(archive.as_uri(), self.tmp / "work", attempts=1)
        self.assertEqual(source.commit, SHA)
        self.assertIsNotNone(source.fetched_at.tzinfo)

    def test_fetch_failure_is_reported(self):
        with self.assertRaises(FetchError):
            fetch((self.tmp / "absent.tar.gz").as_uri(), self.tmp / "work", attempts=2, backoff=0)


if __name__ == "__main__":
    unittest.main()
