"""Publish the output directory to S3 (DESIGN.md §8, §16.2).

Only a validated output reaches this module. Uploads and updates all finish
before any deletion, and a sudden shrink of the site is refused unless
explicitly allowed.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from . import rules


class DeployError(Exception):
    pass


class S3Client(Protocol):
    def list_objects_v2(self, **kwargs: Any) -> dict: ...
    def put_object(self, **kwargs: Any) -> dict: ...
    def delete_objects(self, **kwargs: Any) -> dict: ...


@dataclass
class Plan:
    puts: list[str] = field(default_factory=list)      # keys to upload
    deletes: list[str] = field(default_factory=list)   # keys to remove
    unchanged: int = 0


@dataclass(frozen=True)
class LocalFile:
    path: Path
    md5: str
    size: int


def scan_local(out: Path) -> dict[str, LocalFile]:
    files = {}
    for path in sorted(p for p in out.rglob("*") if p.is_file()):
        data = path.read_bytes()
        files[path.relative_to(out).as_posix()] = LocalFile(path, hashlib.md5(data).hexdigest(), len(data))
    return files


def list_remote(s3: S3Client, bucket: str) -> dict[str, tuple[str, int]]:
    remote: dict[str, tuple[str, int]] = {}
    kwargs: dict[str, Any] = {"Bucket": bucket}
    while True:
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp.get("Contents", []):
            remote[obj["Key"]] = (obj["ETag"].strip('"'), int(obj["Size"]))
        if not resp.get("IsTruncated"):
            return remote
        kwargs["ContinuationToken"] = resp["NextContinuationToken"]


def make_plan(local: dict[str, LocalFile], remote: dict[str, tuple[str, int]]) -> Plan:
    plan = Plan()
    for key, f in local.items():
        if remote.get(key) == (f.md5, f.size):
            plan.unchanged += 1
        else:
            plan.puts.append(key)
    plan.deletes = sorted(k for k in remote if k not in local)
    return plan


def check_shrink(local: dict[str, LocalFile], remote: dict[str, tuple[str, int]], allow: bool) -> None:
    live = sum(1 for k in remote if k.endswith(".html"))
    new = sum(1 for k in local if k.endswith(".html"))
    if live and new < live * rules.SHRINK_RATIO and not allow:
        raise DeployError(
            f"refusing to publish {new} pages over {live} live pages "
            f"(below {rules.SHRINK_RATIO:.0%}); set ALLOW_SHRINK=1 to allow once"
        )


def headers_for(key: str) -> dict[str, str]:
    suffix = Path(key).suffix.lower()
    return {
        "ContentType": rules.CONTENT_TYPES.get(suffix, rules.DEFAULT_CONTENT_TYPE),
        "CacheControl": rules.CACHE_CONTROL.get(suffix, rules.DEFAULT_CACHE_CONTROL),
    }


def deploy(out: Path, bucket: str, s3: S3Client, *, allow_shrink: bool = False) -> Plan:
    local = scan_local(out)
    remote = list_remote(s3, bucket)
    check_shrink(local, remote, allow_shrink)
    plan = make_plan(local, remote)

    for key in plan.puts:  # all uploads first ...
        s3.put_object(Bucket=bucket, Key=key, Body=local[key].path.read_bytes(), **headers_for(key))
    for start in range(0, len(plan.deletes), 1000):  # ... deletions last
        batch = plan.deletes[start:start + 1000]
        resp = s3.delete_objects(Bucket=bucket, Delete={"Objects": [{"Key": k} for k in batch], "Quiet": True})
        if resp.get("Errors"):
            raise DeployError(f"delete failed: {resp['Errors'][:3]}")
    return plan


def invalidate(cloudfront: Any, distribution_id: str, reference: str | None = None) -> str:
    resp = cloudfront.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            "Paths": {"Quantity": 1, "Items": ["/*"]},
            "CallerReference": reference or str(time.time()),
        },
    )
    return resp["Invalidation"]["Id"]
