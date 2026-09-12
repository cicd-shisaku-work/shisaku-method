# -*- coding: utf-8 -*-
"""並び・深さ・番号の決定と、連結。"""
import os
import sys

from .heading import shift_headings
from .module import find_path, load
from .token import Resolver

SEP = "\n\n---\n\n"
JOIN = "\n\n"


def _section_prefix(idx, counters, depth):
    fmts = idx.numbering_format
    fmt = fmts[depth - 1] if depth - 1 < len(fmts) else fmts[-1]
    return fmt.replace("{n}", ".".join(str(c) for c in counters[:depth]))


def collect(idx, src_root, doc_dir, errors):
    """ブロックごとに、モジュールと構造（shift・節番号）を決める。"""
    blocks = []
    for block in idx.blocks:
        counters, secmap, groups = [], {}, []
        for group in block.groups:
            entries = []
            for mid in group:
                path = find_path(src_root, doc_dir, block.lang, mid)
                if path is None:
                    errors.append(f"モジュールが無い: {block.lang}/{mid}")
                    continue
                mod = load(path, mid.split(":")[-1] if mid.startswith("shared:") else mid)
                # 共有モジュールの id はリポジトリ内の置き場であって文書の階層ではない。
                # 所属（cluster_depth）も深さも持たない、1 階層のものとして扱う。
                shared = mid.startswith("shared:")
                segments = 1 if shared else max(1, len(mid.split("/")) - block.cluster_depth)
                if mod.level is not None:
                    shift = mod.level - 1
                else:
                    shift = block.base_depth + segments - 1
                numbered = mod.numbered
                if numbered is None:
                    numbered = idx.numbering_enabled and not mod.raw
                prefix = None
                if numbered and not mod.raw:
                    while len(counters) < segments:
                        counters.append(idx.numbering_sub_start - 1 if len(counters) else idx.numbering_start - 1)
                    del counters[segments:]
                    counters[segments - 1] += 1
                    prefix = _section_prefix(idx, counters, segments)
                section = ".".join(str(c) for c in counters[:segments]) if prefix else None
                secmap[mid] = {"section": section, "title": mod.title}
                entries.append((mod, shift, prefix))
            groups.append(entries)
        blocks.append((block, groups, secmap))
    return blocks


def build_document(idx, src_root, doc_dir, paths, base_url, errors):
    blocks = collect(idx, src_root, doc_dir, errors)
    resolver = Resolver(idx.meta, paths, base_url, errors)
    rendered_groups = []
    for block, groups, secmap in blocks:
        for entries in groups:
            parts = []
            for mod, shift, prefix in entries:
                body = mod.body if mod.raw else shift_headings(mod.body, shift, prefix)
                parts.append(resolver.resolve(body, secmap, block.render, optional=tuple(mod.optional)).strip("\n"))
            rendered_groups.append(JOIN.join(parts))
    text = ""
    for i, part in enumerate(rendered_groups):
        if i:
            text += "\n\n---"       # 空のグループは区切り線だけを出す
            if part:
                text += "\n\n"
        text += part
    text += "\n"
    unused = set(idx.meta) - resolver.used_meta
    return text, sorted(unused), blocks


def resolve_output(idx, paths, base_url, errors):
    r = Resolver(idx.meta, paths, base_url, errors)
    return r.resolve(idx.output, {}, {})
