#!/usr/bin/env python3
"""Build the static site from a repository checkout (DESIGN.md §10).

    python3 src/site/build_site.py --src . --out dist --fonts ~/fonts --report

Share cards need the pinned fonts (fetch them once with fetch_fonts.py); without
``--fonts`` every page uses the text-free default image and a warning is printed.

Exit status: 0 on success; 1 when the build fails or the quality gate finds a
violation. Missing environment variables only produce warnings.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import os
import shutil
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from sitebuild.build import BuildError, BuildResult, build  # noqa: E402
from sitebuild.config import from_env  # noqa: E402
from sitebuild.discover import DiscoveryError  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the shisaku-method static site.")
    parser.add_argument("--src", type=Path, default=Path("."), help="repository root (default: .)")
    parser.add_argument("--out", type=Path, default=Path("dist"), help="output directory (default: dist)")
    parser.add_argument("--clean", action="store_true", help="remove the output directory first")
    parser.add_argument("--commit", help="commit SHA shown in the footer (default: git HEAD)")
    parser.add_argument("--fetched-at", type=datetime.fromisoformat,
                        help="ISO 8601 time with offset shown in the footer (default: now)")
    parser.add_argument("--fonts", type=Path, help="directory holding the share-card fonts (see fetch_fonts.py)")
    parser.add_argument("--report", action="store_true", help="print a summary of the build")
    args = parser.parse_args(argv)

    if args.clean and args.out.exists():
        shutil.rmtree(args.out)
    try:
        cfg = from_env(os.environ, src=args.src.resolve(), out=args.out.resolve(),
                       commit=args.commit, fetched_at=args.fetched_at,
                       font_dir=args.fonts.expanduser().resolve() if args.fonts else None)
        result = build(cfg)
    except (BuildError, DiscoveryError, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return _finish(result, args.report)


def _finish(result: BuildResult, report: bool) -> int:
    for w in result.warnings:
        print(f"warning: {w}", file=sys.stderr)
    if report:
        print(result.report())
    elif result.violations:
        for v in result.violations:
            print(f"violation: {v}", file=sys.stderr)
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
