"""Static assets: the stylesheet and the SVG figures. Share images are drawn in cards.py."""

from __future__ import annotations

import shutil
from pathlib import Path

from .model import Figure

ASSETS = Path(__file__).resolve().parent.parent / "assets"


STATIC = ("site.css",)


def copy_static(out: Path) -> int:
    """The stylesheet, into /assets/."""
    target_dir = out / "assets"
    target_dir.mkdir(parents=True, exist_ok=True)
    for name in STATIC:
        shutil.copyfile(ASSETS / name, target_dir / name)
    return len(STATIC)


def copy_figure(out: Path, figure: Figure) -> Path:
    target = out / figure.svg_url.lstrip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(figure.source, target)
    return target
