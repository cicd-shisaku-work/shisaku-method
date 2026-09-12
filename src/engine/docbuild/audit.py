# -*- coding: utf-8 -*-
"""監査の材料を出す（判定はしない）。思想と設計は AUDIT.md。

出すもの:
  - 粒度の分布（モジュールごとの文字数）
  - 位置依存の参照（「前述」「次節」など。名前参照へ変換できない書き方）
  - 参照グラフ（参照している先・されている側）と、相互参照が密な対
  - 孤立モジュール（参照も被参照もゼロ）
"""
import re

SHARED_MARK = "shared/"

POSITIONAL = re.compile(r"前述|後述|先述|上記|下記|前掲|次節|前節|上の節|下の節|以下に述べ|上で述べ")
REF = re.compile(r"\{\{(?:sec|num|title):([^}]+)\}\}")


def collect(blocks):
    """(モジュール一覧, 参照グラフ) を返す。共有モジュールは shared: 付きの id で入る。"""
    mods = []
    for block, groups, _secmap in blocks:
        for entries in groups:
            for mod, _shift, _prefix in entries:
                mods.append((block.lang, mod))
    out_refs = {}
    for lang, mod in mods:
        out_refs[(lang, mod.id)] = [m for m in REF.findall(mod.body)]
    in_refs = {}
    for (lang, mid), targets in out_refs.items():
        for t in targets:
            in_refs.setdefault((lang, t), []).append(mid)
    return mods, out_refs, in_refs


def report(doc_id, blocks):
    mods, out_refs, in_refs = collect(blocks)
    lines = [f"== 監査の材料: {doc_id} =="]

    # 粒度
    sizes = sorted(((len(m.body), lang, m.id) for lang, m in mods), reverse=True)
    if sizes:
        lines.append("")
        lines.append(f"-- 粒度（{len(sizes)} モジュール・文字数）")
        mid = sizes[len(sizes) // 2][0]
        lines.append(f"   最大 {sizes[0][0]} / 最小 {sizes[-1][0]} / 中央 {mid}"
                     f"（散らばり 最大÷中央 = {sizes[0][0] / mid:.1f} 倍）")
        for n, lang, mid in sizes[:3]:
            lines.append(f"   大きい: {lang}/{mid} ({n})")
        for n, lang, mid in sizes[-3:]:
            lines.append(f"   小さい: {lang}/{mid} ({n})")

    # 位置依存の参照
    hits = []
    for lang, mod in mods:
        for m in POSITIONAL.finditer(mod.body):
            s = max(0, m.start() - 12)
            hits.append(f"   {lang}/{mod.id}: …{mod.body[s:m.end() + 8]}…".replace("\n", " "))
    lines.append("")
    lines.append(f"-- 位置依存の参照（{len(hits)} 件）")
    lines.extend(hits if hits else ["   なし"])

    # 参照グラフ
    total = sum(len(v) for v in out_refs.values())
    lines.append("")
    if not total:
        lines.append("-- 参照")
        lines.append("   この文書は節参照のトークンを持たない。参照にもとづく材料"
                     "（被参照・相互参照・孤立）は、この文書では測れない。")
        lines.append("   節どうしを本文で指し合う文書でなければ、これは異常ではない。")
        return "\n".join(lines)
    lines.append("-- 参照（被参照の多い順）")
    counts = sorted(((len(v), k) for k, v in in_refs.items()), reverse=True)
    for n, (lang, mid) in counts[:8]:
        lines.append(f"   {lang}/{mid} ← {n} 件")

    # 相互参照が密な対
    pairs = {}
    for (lang, a), targets in out_refs.items():
        for b in targets:
            back = out_refs.get((lang, b), [])
            if a in back:
                key = (lang, *sorted((a, b)))
                pairs[key] = (targets.count(b), back.count(a))
    lines.append("")
    lines.append(f"-- 相互に参照し合う対（{len(pairs)} 組・割ってはいけないものを割った疑い）")
    for (lang, a, b), (x, y) in sorted(pairs.items(), key=lambda kv: -(kv[1][0] + kv[1][1])):
        lines.append(f"   {lang}/{a} ↔ {lang}/{b}（{x} / {y} 回）")
    if not pairs:
        lines.append("   なし")

    # 孤立（定型＝共有モジュールは除く。定型は参照を持たないのが正常）
    lonely, fixed = [], 0
    for lang, m in mods:
        if out_refs.get((lang, m.id)) or in_refs.get((lang, m.id)):
            continue
        if m.path.startswith(SHARED_MARK) or "/shared/" in m.path:
            fixed += 1
            continue
        lonely.append(f"   {lang}/{m.id}")
    lines.append("")
    lines.append(f"-- 参照も被参照も無いモジュール（{len(lonely)} 件・定型 {fixed} 件は除いた）")
    lines.extend(lonely if lonely else ["   なし"])
    return "\n".join(lines)


def refs(doc_id, blocks, target):
    mods, out_refs, in_refs = collect(blocks)
    lines = [f"== 影響半径: {target}（{doc_id}）=="]
    found = False
    for lang, mod in mods:
        if mod.id != target:
            continue
        found = True
        outs = out_refs.get((lang, mod.id), [])
        ins = in_refs.get((lang, mod.id), [])
        lines.append(f"-- {lang}/{mod.id}")
        lines.append(f"   参照している先: {', '.join(sorted(set(outs))) or 'なし'}")
        lines.append(f"   参照している側（直す前に突き合わせる）: {', '.join(sorted(set(ins))) or 'なし'}")
    if not found:
        lines.append("   そのモジュールは無い")
    return "\n".join(lines)


# --- 収録前（まだモジュールでない文書）に当てる ------------------------

SELF_REF = re.compile(r"第[0-9]+(?:\.[0-9]+)?節")
DOC_REF = re.compile(r"〔([^〕]+)〕")
NUMBERED_H2 = re.compile(r"(?m)^## (\d+(?:\.\d+)*)[.\s]")


def report_file(path):
    """ビルドに載っていない Markdown に、構造点検の材料を出す。"""
    text = open(path, encoding="utf-8").read()
    lines = [f"== 監査の材料（収録前）: {path} =="]

    secs = re.split(r"(?m)^(?=## )", text)
    bodies = secs[1:]
    sizes = sorted(((len(b), b.split(chr(10))[0][3:40]) for b in bodies), reverse=True)
    h2 = len(re.findall(r"(?m)^## ", text))
    h3 = len(re.findall(r"(?m)^### ", text))
    lines.append("")
    lines.append(f"-- 見出し: H2={h2} H3={h3}／全体 {len(text)} 字")
    if sizes:
        mid = sizes[len(sizes) // 2][0]
        lines.append(f"-- 節の長さ: 最大 {sizes[0][0]} / 中央 {mid} / 最小 {sizes[-1][0]}"
                     f"（散らばり 最大÷中央 = {sizes[0][0] / mid:.1f} 倍）")
        lines.append(f"   最大: {sizes[0][1]}")
        lines.append(f"   最小: {sizes[-1][1]}")

    hits = [f"   …{text[max(0, m.start()-12):m.end()+8]}…".replace("\n", " ")
            for m in POSITIONAL.finditer(text)]
    lines.append("")
    lines.append(f"-- 位置依存の参照（{len(hits)} 件）")
    lines.extend(hits[:10] if hits else ["   なし"])
    if len(hits) > 10:
        lines.append(f"   …他 {len(hits) - 10} 件")

    nums = NUMBERED_H2.findall(text)
    lines.append("")
    lines.append(f"-- 採番: 番号つき H2 {len(nums)} / 番号なし H2 {h2 - len(nums)}")
    if nums:
        depths = {len(n.split('.')) for n in nums}
        lines.append(f"   番号の深さ: {sorted(depths)}（混在は書式のずれの疑い）")
    if nums and h2 - len(nums):
        lines.append("   番号あり・なしが同居している。どこまでを番号つきにするかの規則が要る。")

    lines.append("")
    lines.append(f"-- 自節参照（第N節の形）: {len(SELF_REF.findall(text))} 件")
    refs = DOC_REF.findall(text)
    lines.append(f"-- 他文書への参照〔…〕: {len(refs)} 件"
                 + (f"（{', '.join(sorted(set(refs))[:5])} …）" if refs else ""))
    lines.append("   ※ 他文書参照は位置依存ではないが、配置換えで壊れる。")
    return "\n".join(lines)


def impact(doc_id, doc_dir, blocks, changed_paths):
    """変更されたモジュールの影響半径をまとめて出す（編集前・PR 前の必須調査）。"""
    mods, out_refs, in_refs = collect(blocks)
    by_path = {}
    for lang, mod in mods:
        by_path[mod.path] = (lang, mod)

    hits = [p for p in changed_paths if p in by_path]
    if not hits:
        return None

    detailed, quiet = [], []
    for p in sorted(hits):
        lang, mod = by_path[p]
        ins = sorted(set(in_refs.get((lang, mod.id), [])))
        outs = sorted(set(out_refs.get((lang, mod.id), [])))
        (detailed if (ins or outs) else quiet).append((lang, mod, ins, outs))

    lines = [f"== 影響半径（変更されたモジュール）: {doc_id} =="]
    for lang, mod, ins, outs in detailed:
        lines.append("")
        lines.append(f"-- {lang}/{mod.id}")
        lines.append(f"   参照している先: {', '.join(outs) or 'なし'}")
        if ins:
            cross = [i for i in ins if i.split("/")[0] != mod.id.split("/")[0]]
            lines.append(f"   参照している側（要突き合わせ）: {', '.join(ins)}")
            if cross:
                lines.append(f"   ※ 役をまたぐ波及: {', '.join(cross)}")
        else:
            lines.append("   参照している側: なし")
    if quiet:
        lines.append("")
        lines.append(f"-- 参照関係を持たないモジュール（{len(quiet)} 件・突き合わせ不要）")
        lines.append("   " + ", ".join(f"{l}/{m.id}" for l, m, _i, _o in quiet[:8])
                     + (" …" if len(quiet) > 8 else ""))
    return "\n".join(lines)
