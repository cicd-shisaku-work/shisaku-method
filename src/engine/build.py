#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""モジュール群から文書を組み立てる。設計は DESIGN.md、運用は OPERATIONS.md。

使い方:
    python3 src/engine/build.py                                   # 全文書をビルド
    python3 src/engine/build.py shisaku-human-idion-structure     # 文書を指定
    python3 src/engine/build.py --check                           # 出力先との一致を検査
    python3 src/engine/build.py --lint-only                       # 静的検査のみ
    python3 src/engine/build.py --audit                           # 監査の材料を出す
    python3 src/engine/build.py --audit-file <path>               # 収録前の文書に材料を出す
    python3 src/engine/build.py --impact                          # 変更したモジュールの影響半径
    python3 src/engine/build.py <doc> --refs <モジュールid>        # 影響半径
"""
import sys

sys.dont_write_bytecode = True  # __pycache__ を作らない

import argparse
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docbuild.assemble import build_document, resolve_output
from docbuild.index import Index, load_paths
from docbuild.audit import impact as audit_impact, refs as audit_refs, report as audit_report, report_file as audit_file
from docbuild.lint import check

ENGINE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(ENGINE)
ROOT = os.path.dirname(SRC)
PATHS = os.path.join(SRC, "paths.toml")


DOCS = os.path.join(SRC, "docs")


def documents():
    """src/docs/ 以下の index.toml を持つディレクトリが 1 文書。名は出力の語幹と同じ。"""
    out = []
    for root, dirs, files in os.walk(DOCS):
        if "index.toml" in files:
            out.append((os.path.basename(root), root))
            dirs[:] = []
    return sorted(out)


def main():
    ap = argparse.ArgumentParser(description="文書ビルド")
    ap.add_argument("docs", nargs="*", help="文書 id（＝ディレクトリ名・省略時は全部）")
    ap.add_argument("--check", action="store_true", help="出力先との一致を検査する")
    ap.add_argument("--lint-only", action="store_true", help="静的検査だけ行う")
    ap.add_argument("--audit", action="store_true", help="監査の材料を出す（判定はしない）")
    ap.add_argument("--refs", metavar="ID", help="そのモジュールの影響半径を出す")
    ap.add_argument("--audit-file", metavar="PATH", help="まだ載せていない文書に、収録前の材料を出す")
    ap.add_argument("--impact", action="store_true",
                    help="変更されたモジュール（git 差分）の影響半径を出す。直す前・PR 前の必須調査")
    args = ap.parse_args()

    if args.audit_file:
        print(audit_file(args.audit_file))
        sys.exit(0)

    base_url, paths = load_paths(PATHS) if os.path.exists(PATHS) else ("", {})

    changed = []
    if args.impact:
        import subprocess
        r = subprocess.run(["git", "diff", "--name-only", "HEAD", "--", "src/docs"],
                           capture_output=True, text=True, cwd=ROOT)
        changed = [os.path.join(ROOT, line) for line in r.stdout.split("\n") if line.strip()]
        r2 = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "src/docs"],
                            capture_output=True, text=True, cwd=ROOT)
        changed += [os.path.join(ROOT, line) for line in r2.stdout.split("\n") if line.strip()]

    targets = [(n, d) for n, d in documents() if not args.docs or n in args.docs]
    if not targets:
        sys.exit(f"[FATAL] 対象の文書が無い: {args.docs}")

    failed = False
    used_shared = set()
    for name, doc_dir in targets:
        idx = Index(os.path.join(doc_dir, "index.toml"))
        for block in idx.blocks:
            used_shared |= {m[len("shared:"):] for g in block.groups for m in g if m.startswith("shared:")}
        errors = []
        text, unused, blocks = build_document(idx, SRC, doc_dir, paths, base_url, errors)
        if args.impact:
            out = audit_impact(idx.id, doc_dir, blocks, changed)
            if out:
                print(out)
                print()
            continue

        if args.audit or args.refs:
            print(audit_refs(idx.id, blocks, args.refs) if args.refs else audit_report(idx.id, blocks))
            print()
            continue

        lint_errors, warnings = check(idx, SRC, doc_dir, ROOT, paths, blocks, unused)
        errors = list(dict.fromkeys(errors + lint_errors))

        for w in warnings:
            print(f"  [warn] {idx.id}: {w}")
        if errors:
            failed = True
            print(f"[NG] {idx.id}: 検査に通らなかった")
            for e in errors:
                print(f"    - {e}")
            continue

        out_errors = []
        out_rel = resolve_output(idx, paths, base_url, out_errors)
        if out_errors:
            failed = True
            print(f"[NG] {idx.id}: 出力先が解決できない")
            for e in out_errors:
                print(f"    - {e}")
            continue
        out_path = os.path.join(ROOT, out_rel)
        if args.lint_only:
            print(f"[OK] {idx.id}: 検査に通った")
            continue
        if args.check:
            current = open(out_path, encoding="utf-8").read() if os.path.exists(out_path) else None
            if current == text:
                print(f"[OK] {idx.id}: 出力先と一致（{os.path.relpath(out_path, ROOT)}）")
            else:
                failed = True
                print(f"[NG] {idx.id}: 出力先と一致しない（{os.path.relpath(out_path, ROOT)}）")
                _report_diff(current, text)
            continue
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[OK] {idx.id}: 書き出した（{os.path.relpath(out_path, ROOT)}・{len(text)} bytes）")

    if not args.docs:  # 全文書を見たときだけ、呼ばれていない共有モジュールを報告する
        shared_dir = os.path.join(SRC, "shared")
        for root, _dirs, files in os.walk(shared_dir):
            for fn in files:
                if not fn.endswith((".md", ".xml")):
                    continue
                mid = os.path.relpath(os.path.join(root, fn), shared_dir).rsplit(".", 1)[0]
                if mid not in used_shared:
                    print(f"  [warn] どの文書からも呼ばれていない共有モジュール: shared:{mid}")

    sys.exit(1 if failed else 0)


def _report_diff(current, text):
    if current is None:
        print("    - 出力先のファイルが無い")
        return
    import difflib

    diff = list(difflib.unified_diff(current.split("\n"), text.split("\n"),
                                     "現在の出力先", "組み立て結果", lineterm="", n=1))
    for line in diff[:40]:
        print("    " + line)
    if len(diff) > 40:
        print(f"    … 他 {len(diff) - 40} 行")


if __name__ == "__main__":
    main()
