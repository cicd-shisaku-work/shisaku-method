import hashlib
import tempfile
import unittest
from pathlib import Path

from sitebuild.deploy import DeployError, deploy, headers_for


class FakeS3:
    """In-memory stand-in for the boto3 S3 client; records the call order."""

    def __init__(self, objects=None, page_size=2):
        self.objects = dict(objects or {})  # key -> bytes
        self.calls = []
        self.page_size = page_size
        self.headers = {}

    def list_objects_v2(self, Bucket, ContinuationToken=None):
        keys = sorted(self.objects)
        start = int(ContinuationToken or 0)
        page = keys[start:start + self.page_size]
        resp = {"Contents": [{"Key": k, "ETag": f'"{hashlib.md5(self.objects[k]).hexdigest()}"',
                              "Size": len(self.objects[k])} for k in page]}
        if start + self.page_size < len(keys):
            resp.update(IsTruncated=True, NextContinuationToken=str(start + self.page_size))
        return resp

    def put_object(self, Bucket, Key, Body, ContentType, CacheControl):
        self.calls.append(("put", Key))
        self.objects[Key] = Body
        self.headers[Key] = (ContentType, CacheControl)
        return {}

    def delete_objects(self, Bucket, Delete):
        for obj in Delete["Objects"]:
            self.calls.append(("delete", obj["Key"]))
            self.objects.pop(obj["Key"], None)
        return {}


class DeployTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.out = Path(tmp.name)
        self.files = {"index.html": b"top", "ja/a.html": b"a", "ja/b.html": b"b", "assets/site.css": b"css"}
        for rel, data in self.files.items():
            (self.out / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.out / rel).write_bytes(data)

    def test_first_publish_uploads_everything(self):
        s3 = FakeS3()
        plan = deploy(self.out, "bucket", s3)
        self.assertEqual(sorted(plan.puts), sorted(self.files))
        self.assertEqual(s3.objects, self.files)

    def test_only_changes_are_uploaded_and_deletions_come_last(self):
        s3 = FakeS3({"index.html": b"top", "ja/a.html": b"old", "ja/b.html": b"b",
                     "assets/site.css": b"css", "ja/gone.html": b"x"})
        plan = deploy(self.out, "bucket", s3)
        self.assertEqual(plan.puts, ["ja/a.html"])
        self.assertEqual(plan.deletes, ["ja/gone.html"])
        self.assertEqual(plan.unchanged, 3)
        self.assertEqual(s3.calls, [("put", "ja/a.html"), ("delete", "ja/gone.html")])

    def test_shrink_is_refused_unless_allowed(self):
        live = {f"ja/p{i}.html": b"x" for i in range(10)}
        with self.assertRaises(DeployError):
            deploy(self.out, "bucket", FakeS3(live))
        s3 = FakeS3(live)
        self.assertEqual(s3.calls, [])  # nothing touched
        plan = deploy(self.out, "bucket", s3, allow_shrink=True)
        self.assertEqual(len(plan.deletes), 10)

    def test_content_type_and_cache_control(self):
        s3 = FakeS3()
        deploy(self.out, "bucket", s3)
        self.assertEqual(s3.headers["ja/a.html"], ("text/html; charset=utf-8", "public, max-age=3600"))
        self.assertEqual(s3.headers["assets/site.css"], ("text/css; charset=utf-8", "public, max-age=86400"))
        self.assertEqual(headers_for("x/fig.svg")["ContentType"], "image/svg+xml")
        self.assertEqual(headers_for("sitemap.xml")["ContentType"], "application/xml")
        self.assertEqual(headers_for("assets/og-default.png"), {"ContentType": "image/png", "CacheControl": "public, max-age=86400"})


if __name__ == "__main__":
    unittest.main()
