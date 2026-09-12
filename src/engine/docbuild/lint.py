# -*- coding: utf-8 -*-
"""静的検査。エラーはビルドを止め、警告は報告のみ。"""
import os
import re

VERSION_RE = re.compile(r"^v0\.\d+(\.\d+)?$")
DATE_RE = re.compile(r"^\d{4}/\d{2}/\d{2}$")


def check(idx, src_root, doc_dir, repo_root, paths, blocks, unused_meta):
    errors, warnings = [], []

    # 文書の識別子は、置き場のディレクトリ名（＝出力の語幹）と一致する。別名を作らない。
    if idx.id != os.path.basename(doc_dir):
        errors.append(f"[doc] id ({idx.id}) とディレクトリ名 ({os.path.basename(doc_dir)}) が違う")

    # [meta] の書式（CONTRIBUTING の版の規約の機械担保）
    v = idx.meta.get("version")
    if v is not None and not VERSION_RE.match(str(v)):
        errors.append(f"version が v0.x[.y] でない、または括弧書きが付いている: {v!r}")
    date = idx.meta.get("date")
    if date is not None and not DATE_RE.match(str(date)):
        errors.append(f"date が YYYY/MM/DD でない: {date!r}")

    # paths.toml のパスが実在するか
    for key, rel in paths.items():
        if not os.path.exists(os.path.join(repo_root, rel.rstrip("/"))):
            errors.append(f"paths.toml のパスが実在しない: {key} = {rel}")

    listed = {}
    for block in idx.blocks:
        listed.setdefault(block.lang, set()).update(mid for g in block.groups for mid in g)

    # 孤児（ディレクトリにあるのに、どのグループにも載っていない）
    for lang, ids in listed.items():
        lang_dir = os.path.join(doc_dir, lang)
        if not os.path.isdir(lang_dir):
            continue
        for root, _dirs, files in os.walk(lang_dir):
            for fn in files:
                if not fn.endswith((".md", ".xml")):
                    continue
                mid = os.path.relpath(os.path.join(root, fn), lang_dir).rsplit(".", 1)[0]
                if mid not in ids:
                    errors.append(f"インデックスに載っていないモジュール: {lang}/{mid}")

    # 日英の対
    ja = {i for i in listed.get("ja", set()) if not i.startswith("shared:")}
    en = {i for i in listed.get("en", set()) if not i.startswith("shared:")}
    if ja and en:
        allow = set()
        for block in idx.blocks:
            allow |= set(block.allow_unpaired)
        for mid in sorted((ja - en) | (en - ja)):
            if mid not in allow:
                warnings.append(f"日英の対が揃っていない: {mid}")

    # モジュール本文の規律と、テンプレートが要求するメタ
    for block, groups, _ in blocks:
        for entries in groups:
            for mod, _shift, _prefix in entries:
                text = open(mod.path, encoding="utf-8").read()
                if mod.path.endswith(".xml"):
                    inner = text.split("<![CDATA[", 1)[-1]
                    inner = inner.rsplit("]]>", 1)[0]
                    if "]]>" in inner:
                        errors.append(f"CDATA の中に生の ]]> がある: {mod.path}")
                if not mod.raw:
                    heads = re.findall(r"^(#+)\s", mod.body, re.M)
                    if not heads or len(heads[0]) != 1:
                        errors.append(f"先頭見出しが H1 でない: {mod.path}")
                    if sum(1 for h in heads if len(h) == 1) > 1:
                        errors.append(f"H1 が複数ある: {mod.path}")
                for key in mod.requires:
                    if key and key not in idx.meta:
                        errors.append(f"テンプレートが要求するメタが [meta] に無い: {key}（{mod.path}）")

    for key in unused_meta:
        warnings.append(f"[meta] にあるのに参照されていない: {key}")

    return errors, warnings
