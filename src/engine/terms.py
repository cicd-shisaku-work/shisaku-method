# -*- coding: utf-8 -*-
"""用語の関門。台帳（正本）と本文の目印を突き合わせる。

`terminology-policy.md` 第11条が要求する検査を実装する。
判定できるものだけを判定し、できないものは数えて出す（`AUDIT.md` の分界）。
標準ライブラリのみ（`DESIGN.md` §15）。
"""
import os
import re
import sys

sys.dont_write_bytecode = True   # DESIGN.md §15

try:
    import tomllib
except ModuleNotFoundError:  # 3.11 未満
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        sys.exit("[FATAL] Python 3.11 以上、または tomli が要る（DESIGN.md §15）")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEDGER = os.path.join(ROOT, "terminology-ledger.md")
MARK = re.compile(r"<!--\s*machinery-def:\s*(.+?)\s*-->")
HEAD = re.compile(r"^(#+)\s+(.*)$")
HEAD_M = re.compile(r"^(#+)\s+(.*)$", re.M)


def _rows(text, start, end):
    """`## start` から `end` までの最初の表の行を返す（ヘッダーと区切りを除く）。"""
    i = text.index(start)
    j = text.index(end, i)
    out, seen_sep = [], False
    for line in text[i:j].split("\n"):
        if not line.startswith("|"):
            if seen_sep and out:
                break          # 表が終わった
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if set("".join(cells)) <= set("-: "):
            seen_sep = True
            continue
        if not seen_sep:
            continue           # ヘッダー行
        out.append(cells)
    return out


def load_ledger():
    t = open(LEDGER, encoding="utf-8").read()
    heads = list(HEAD_M.finditer(t))
    words = []      # (語, 軸, 定義位置, 節)
    for k, m in enumerate(heads):
        name = m.group(2)
        if not re.match(r"^[1-8]\. ", name):
            continue            # §9 境界は適用範囲外・§10/§11 は別扱い
        b = heads[k + 1].start() if k + 1 < len(heads) else len(t)
        block = t[m.start():b]
        seen_sep = False
        for line in block.split("\n"):
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                seen_sep = True
                continue
            if not seen_sep or len(cells) < 4:
                continue
            words.append((cells[0], cells[1], cells[3], name))

    bundles = _rows(t, "## 10. バンドル", "### 10.1")
    machinery = _rows(t, "## 11. 仕組みの語", "## License")
    return words, bundles, machinery


def generated_outputs():
    """インデックスの出力先。`{{path:…}}` は `src/paths.toml` で解く。"""
    with open(os.path.join(ROOT, "src", "paths.toml"), "rb") as f:
        paths = tomllib.load(f).get("paths", {})
    out = set()
    src = os.path.join(ROOT, "src", "docs")
    for base, _d, files in os.walk(src):
        if "index.toml" in files:
            with open(os.path.join(base, "index.toml"), "rb") as f:
                idx = tomllib.load(f)
            o = idx.get("doc", {}).get("output")
            if o:
                o = re.sub(r"\{\{path:([^}]+)\}\}", lambda m: paths.get(m.group(1), m.group(0)), o)
                out.add(os.path.normpath(os.path.join(ROOT, o)))
    return out


def scan_marks():
    """(名, ファイル, 節の見出し, 節の本文) を集める。生成物は除く。"""
    skip = generated_outputs()
    hits = []
    for sub in ("concepts", "src/docs"):
        for base, _d, files in os.walk(os.path.join(ROOT, sub)):
            for fn in files:
                if not fn.endswith(".md"):
                    continue
                p = os.path.join(base, fn)
                if os.path.normpath(p) in skip:
                    continue
                lines = open(p, encoding="utf-8").read().split("\n")
                for i, line in enumerate(lines):
                    m = MARK.search(line)
                    if not m:
                        continue
                    lvl, head = 0, ""
                    for j in range(i, -1, -1):
                        hm = HEAD.match(lines[j])
                        if hm:
                            lvl, head = len(hm.group(1)), hm.group(2)
                            start = j
                            break
                    end = len(lines)
                    for j in range(start + 1, len(lines)):
                        hm = HEAD.match(lines[j])
                        if hm and len(hm.group(1)) <= lvl:
                            end = j
                            break
                    hits.append((m.group(1), os.path.relpath(p, ROOT), head,
                                 "\n".join(lines[start:end])))
    return hits


def main():
    words, bundles, machinery = load_ledger()
    marks = scan_marks()
    err, warn, note = [], [], []

    bnames = {b[0]: b for b in bundles}
    mnames = {}
    for name, path, head, body in marks:
        mnames.setdefault(name, []).append((path, head, body))

    # C2 目印の名が台帳にあるか
    for name in mnames:
        if name not in bnames:
            err.append(f"[C2] 本文の目印「{name}」が台帳に無い（{mnames[name][0][0]}）")
    # C2' 台帳の行に目印があるか
    for name in bnames:
        if name not in mnames:
            err.append(f"[C2'] 台帳の「{name}」に本文の目印が無い")
    # C1 正本の位置が実在するか（節名が見出しに含まれるか）
    for name, hits in mnames.items():
        row = bnames.get(name)
        if not row:
            continue
        want = re.findall(r"「([^」]+)」", row[4])
        if not want:
            note.append(f"[C1] 「{name}」の正本の位置に節名が無い（照合できない）")
            continue
        if not any(any(w in h for w in want) for _p, h, _b in hits):
            err.append(f"[C1] 「{name}」の正本の位置『{want[0]}』が、目印のある節（{hits[0][2][:24]}）と一致しない")
    # C3 台帳の要素が本文に在るか
    for name, hits in mnames.items():
        row = bnames.get(name)
        if not row:
            continue
        for el in [e.strip() for e in row[1].split("／") if e.strip()]:
            if "〜" in el:
                note.append(f"[C3] 「{name}」の要素『{el}』は範囲表記。照合できない")
                continue
            if not any(el in b for _p, _h, b in hits):
                warn.append(f"[C3] 「{name}」の要素『{el}』が本文に見つからない")
    # C6 開閉の書き落とし
    for b in bundles:
        if "closed" not in b[2] and "open" not in b[2]:
            err.append(f"[C6] 「{b[0]}」に開閉の宣言が無い")
    # C4 一語一軸
    axes = {}
    for w, ax, _loc, _sec in words:
        axes.setdefault(w, set()).add(ax)
    for w, a in axes.items():
        if len(a) > 1:
            err.append(f"[C4] 「{w}」が二つ以上の軸に乗っている（{'／'.join(sorted(a))}）")
    # C5 バンドル名が、裸の登録語と同じでないか
    wset = {w for w, *_ in words}
    for b in bundles:
        if b[0] in wset:
            err.append(f"[C5] バンドル名「{b[0]}」が、語としても登録されている")
    # C7 別名の衝突
    alias = {}
    for b in bundles:
        for a in [x.strip() for x in b[3].split("／") if x.strip()]:
            alias.setdefault(a, []).append(b[0])
    for a, owners in alias.items():
        if len(owners) > 1:
            warn.append(f"[C7] 裸形「{a}」が {len(owners)} 件のバンドルを指す（{'／'.join(owners)}）")
    # C8 仕組みの語と原典の語の重なり（第12条）
    for m in machinery:
        if m[0] in wset:
            err.append(f"[C8] 仕組みの語「{m[0]}」が原典の語と重なっている")
        elif any(m[0] in w for w in wset):
            warn.append(f"[C8] 仕組みの語「{m[0]}」が原典の語に含まれる")

    print(f"== 用語の関門 ==")
    print(f"台帳：語 {len(words)} 件／バンドル {len(bundles)} 件／仕組みの語 {len(machinery)} 件")
    print(f"本文：目印 {len(marks)} 件")
    for label, items in (("エラー", err), ("警告", warn), ("判定できない", note)):
        print(f"\n-- {label}（{len(items)} 件）")
        for x in items:
            print("   " + x)
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
