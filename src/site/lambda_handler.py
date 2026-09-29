"""AWS Lambda entry point: fetch -> build -> validate -> deploy (DESIGN.md §8, §16.2).

Fail-closed: if any step before deployment fails, S3 is not touched and the
live site stays as it was. Errors are raised so the invocation fails.

Environment (values are set in the Lambda console, never in the repository):
SOURCE_REPO, SOURCE_BRANCH, BASE_URL, GA_MEASUREMENT_ID, S3_BUCKET,
CLOUDFRONT_DISTRIBUTION_ID, ALLOW_SHRINK, GITHUB_TOKEN (only for a private source).

The share-card fonts travel in the package under ``fonts/`` (OPERATIONS.md);
a package without them is refused rather than publishing plain images.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import logging
import os
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONT_DIR = HERE / "fonts"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from sitebuild import deploy as deploy_mod  # noqa: E402
from sitebuild.build import build  # noqa: E402
from sitebuild.config import DEFAULT_BRANCH, from_env  # noqa: E402
from sitebuild.fetch import fetch, tarball_url  # noqa: E402

log = logging.getLogger()
log.setLevel(logging.INFO)


class ConfigurationError(Exception):
    pass


def handler(event: dict | None = None, context: object = None) -> dict:
    env = os.environ
    repo = env.get("SOURCE_REPO", "").strip()
    bucket = env.get("S3_BUCKET", "").strip()
    if not repo or not bucket:
        raise ConfigurationError("SOURCE_REPO and S3_BUCKET must be set")
    branch = env.get("SOURCE_BRANCH", "").strip() or DEFAULT_BRANCH

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        source = fetch(tarball_url(repo, branch), work / "fetch", token=env.get("GITHUB_TOKEN") or None)
        log.info("fetched %s@%s commit=%s", repo, branch, source.commit)

        cfg = from_env(env, src=source.root, out=work / "dist",
                       commit=source.commit, fetched_at=source.fetched_at, font_dir=FONT_DIR)
        result = build(cfg)
        for w in result.warnings:
            log.warning(w)
        log.info("built pages=%d files=%d excluded=%d", len(result.pages), result.files, len(result.excluded))
        if not result.share_cards:
            raise RuntimeError("share-card fonts are missing or altered in the package; nothing published")
        if not result.ok:
            for v in result.violations:
                log.error("violation: %s", v)
            raise RuntimeError(f"quality gate failed with {len(result.violations)} violation(s); nothing published")

        import boto3  # provided by the Lambda runtime

        plan = deploy_mod.deploy(cfg.out, bucket, boto3.client("s3"),
                                 allow_shrink=env.get("ALLOW_SHRINK", "") == "1")
        log.info("deployed put=%d delete=%d unchanged=%d", len(plan.puts), len(plan.deletes), plan.unchanged)

        invalidation = None
        dist_id = env.get("CLOUDFRONT_DISTRIBUTION_ID", "").strip()
        if dist_id and (plan.puts or plan.deletes):
            invalidation = deploy_mod.invalidate(boto3.client("cloudfront"), dist_id, source.commit + source.fetched_at.isoformat())
            log.info("invalidation %s", invalidation)

    return {
        "commit": source.commit,
        "pages": len(result.pages),
        "put": len(plan.puts),
        "delete": len(plan.deletes),
        "unchanged": plan.unchanged,
        "invalidation": invalidation,
    }
