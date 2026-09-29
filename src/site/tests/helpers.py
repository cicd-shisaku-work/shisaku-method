"""Shared test helpers. Tests run with unittest and the pinned requirements only.

Tests that draw title cards need the pinned fonts: point SITE_FONTS at a
directory filled by fetch_fonts.py (CI does). Without it they are skipped.
"""

from __future__ import annotations

import os
from pathlib import Path

from sitebuild import fonts
from sitebuild.config import from_env

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "repo"
COMMIT = "0123456789abcdef0123456789abcdef01234567"
ENV = {"BASE_URL": "https://site.example", "SOURCE_REPO": "example/repo"}


FONT_DIR = Path(os.environ["SITE_FONTS"]).expanduser() if os.environ.get("SITE_FONTS") else None
FONTS, _ = fonts.locate(FONT_DIR)
NO_FONTS = "SITE_FONTS does not point at the pinned fonts"


def config(out: Path, env: dict[str, str] | None = None, src: Path = FIXTURE, font_dir: Path | None = None):
    return from_env(ENV if env is None else env, src=src, out=out, commit=COMMIT, font_dir=font_dir)
