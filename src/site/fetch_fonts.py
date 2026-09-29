#!/usr/bin/env python3
"""Fetch the share-card fonts, pinned by commit and SHA-256 (DESIGN.md §9).

    python3 src/site/fetch_fonts.py --dest ~/fonts

Run it when packaging the Lambda function and in CI, not at build time.
Files already present and verified are left alone. Exit status 1 on failure.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from sitebuild.fonts import FontError, fetch  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fetch the pinned share-card fonts.")
    parser.add_argument("--dest", type=Path, required=True, help="directory to place the fonts in")
    args = parser.parse_args(argv)
    try:
        fetched = fetch(args.dest.expanduser())
    except (FontError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"fetched: {', '.join(fetched)}" if fetched else "fonts already in place")
    return 0


if __name__ == "__main__":
    sys.exit(main())
