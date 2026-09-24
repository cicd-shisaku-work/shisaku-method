"""Build settings, read once at the entry points and passed down.

Modules below the entry points never touch ``os.environ`` (DESIGN.md §16.4).
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

from . import rules

DEFAULT_BASE_URL = "http://localhost:8000"
DEFAULT_BRANCH = "main"


@dataclass(frozen=True)
class Config:
    src: Path                # repository root to read
    out: Path                # output directory
    base_url: str            # absolute site origin, no trailing slash
    source_repo: str | None  # "owner/name" on GitHub
    source_branch: str
    ga_id: str | None
    commit: str              # full SHA or "unknown"
    fetched_at: datetime     # timezone-aware
    font_dir: Path | None = None  # share-card fonts (DESIGN.md §9); None draws the default image only
    warnings: tuple[str, ...] = ()

    @property
    def commit_short(self) -> str:
        return self.commit[:7] if self.commit != "unknown" else self.commit

    @property
    def commit_url(self) -> str | None:
        if self.source_repo and self.commit != "unknown":
            return f"https://github.com/{self.source_repo}/commit/{self.commit}"
        return None

    def blob_url(self, repo_path: str) -> str | None:
        if self.source_repo:
            return f"https://github.com/{self.source_repo}/blob/{self.source_branch}/{repo_path}"
        return None


def from_env(
    env: Mapping[str, str],
    *,
    src: Path,
    out: Path,
    commit: str | None = None,
    fetched_at: datetime | None = None,
    font_dir: Path | None = None,
) -> Config:
    warnings: list[str] = []

    base_url = (env.get("BASE_URL") or "").strip().rstrip("/")
    if not base_url:
        base_url = DEFAULT_BASE_URL
        warnings.append(f"BASE_URL is not set; using {DEFAULT_BASE_URL}")

    source_repo = (env.get("SOURCE_REPO") or "").strip() or None
    if source_repo is None:
        warnings.append("SOURCE_REPO is not set; commit and GitHub links are omitted")

    ga_id = (env.get("GA_MEASUREMENT_ID") or "").strip() or None
    if ga_id and not rules.GA_ID_PATTERN.match(ga_id):
        warnings.append("GA_MEASUREMENT_ID has an unexpected form; analytics is omitted")
        ga_id = None

    if fetched_at is None:
        fetched_at = datetime.now(timezone.utc).replace(microsecond=0)
    elif fetched_at.tzinfo is None:
        raise ValueError("fetched_at must be timezone-aware")

    return Config(
        src=src,
        out=out,
        base_url=base_url,
        source_repo=source_repo,
        source_branch=(env.get("SOURCE_BRANCH") or "").strip() or DEFAULT_BRANCH,
        ga_id=ga_id,
        commit=commit or _local_commit(src) or "unknown",
        fetched_at=fetched_at,
        font_dir=font_dir,
        warnings=tuple(warnings),
    )


def _local_commit(src: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(src), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10, check=True,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    sha = result.stdout.strip()
    return sha if len(sha) == 40 else None
