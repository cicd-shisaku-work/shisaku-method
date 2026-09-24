"""Fonts for the share cards: fetch once at packaging time, verify at every build.

The files come from google/fonts on GitHub at a pinned commit and must match
the SHA-256 held in ``rules.FONT_FILES``; anything else is treated as absent.
"""

from __future__ import annotations

import hashlib
import os
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from . import rules

_TIMEOUT = 60  # seconds per file


@dataclass(frozen=True)
class Fonts:
    bold: Path
    medium: Path


class FontError(Exception):
    pass


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def locate(font_dir: Path | None) -> tuple[Fonts | None, str | None]:
    """The verified fonts in ``font_dir``, or ``(None, reason)``."""
    if font_dir is None:
        return None, "no font directory given"
    for name, digest in rules.FONT_FILES.values():
        path = font_dir / name
        if not path.is_file():
            return None, f"{path} is missing"
        if _sha256(path) != digest:
            return None, f"{path} does not match the pinned SHA-256"
    return Fonts(
        bold=font_dir / rules.FONT_FILES["bold"][0],
        medium=font_dir / rules.FONT_FILES["medium"][0],
    ), None


def fetch(dest: Path, source: str = rules.FONT_SOURCE) -> list[str]:
    """Download every pinned file into ``dest``; files already verified are kept.

    Returns the names downloaded. Raises FontError on a hash mismatch, in which
    case nothing is left behind for that file.
    """
    dest.mkdir(parents=True, exist_ok=True)
    fetched = []
    for name, digest in rules.FONT_FILES.values():
        target = dest / name
        if target.is_file() and _sha256(target) == digest:
            continue
        fd, tmp_name = tempfile.mkstemp(dir=dest, prefix=f".{name}.")
        tmp = Path(tmp_name)
        try:
            with os.fdopen(fd, "wb") as out, urllib.request.urlopen(source + name, timeout=_TIMEOUT) as resp:
                for chunk in iter(lambda: resp.read(1 << 20), b""):
                    out.write(chunk)
            actual = _sha256(tmp)
            if actual != digest:
                raise FontError(f"{name}: SHA-256 {actual} does not match the pinned {digest}")
            tmp.replace(target)
            fetched.append(name)
        finally:
            tmp.unlink(missing_ok=True)
    return fetched
