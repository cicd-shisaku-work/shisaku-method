"""Fetch the source repository as a tarball (used where git is unavailable).

GitHub serves a branch as ``codeload.github.com/<repo>/tar.gz/refs/heads/<branch>``.
The archive's top directory is named after the branch, not the commit; the
commit SHA is carried in the tar's global pax header (``comment``).
"""

from __future__ import annotations

import re
import tarfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from . import rules

USER_AGENT = "shisaku-method-site-builder"
_SHA = re.compile(r"^[0-9a-f]{40}$")


class FetchError(Exception):
    pass


@dataclass(frozen=True)
class Source:
    root: Path
    commit: str
    fetched_at: datetime


def tarball_url(repo: str, branch: str) -> str:
    return f"https://codeload.github.com/{repo}/tar.gz/refs/heads/{branch}"


def fetch(
    url: str,
    dest: Path,
    *,
    token: str | None = None,
    timeout: float = 60,
    attempts: int = 3,
    backoff: float = 2.0,
) -> Source:
    dest.mkdir(parents=True, exist_ok=True)
    archive = dest / "source.tar.gz"
    _download(url, archive, token=token, timeout=timeout, attempts=attempts, backoff=backoff)
    fetched_at = datetime.now(timezone.utc).replace(microsecond=0)
    root, commit = extract(archive, dest / "source")
    return Source(root=root, commit=commit, fetched_at=fetched_at)


def _download(url: str, target: Path, *, token: str | None, timeout: float,
              attempts: int, backoff: float) -> None:
    headers = {"User-Agent": USER_AGENT}
    if token:
        headers["Authorization"] = f"token {token}"
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=timeout) as response:
                target.write_bytes(response.read())
            return
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code < 500 and exc.code != 429:
                break  # a client error will not fix itself
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = exc
        if attempt < attempts:
            time.sleep(backoff * attempt)
    raise FetchError(f"download failed: {url}: {last}")


def extract(archive: Path, dest: Path) -> tuple[Path, str]:
    """Extract safely; return (repository root, commit SHA or "unknown")."""
    try:
        with tarfile.open(archive, "r:*") as tf:
            comment = tf.pax_headers.get("comment", "")
            tops = {Path(m.name).parts[0] for m in tf.getmembers() if m.name and m.name != "pax_global_header"}
            if len(tops) != 1:
                raise FetchError(f"archive must have one top directory, found {sorted(tops)}")
            dest.mkdir(parents=True, exist_ok=True)
            tf.extractall(dest, filter="data")  # rejects absolute paths, "..", devices, outside links
    except tarfile.TarError as exc:
        raise FetchError(f"cannot extract archive: {exc}") from exc

    root = dest / tops.pop()
    if not (root / rules.README_FILE).is_file():
        raise FetchError(f"{rules.README_FILE} not found in the archive")
    commit = comment if _SHA.match(comment) else "unknown"
    return root, commit
