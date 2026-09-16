# -*- coding: utf-8 -*-
"""モジュールの読み取り（.md ／ .xml）とメタの正規化。"""
import os
import re
import sys
import xml.etree.ElementTree as ET

ALLOWED = {"id", "title", "numbered", "raw", "level", "maturity", "requires", "optional"}
TRUE = {"true", "True", "yes", "1"}


class Module:
    def __init__(self, mid, path, meta, body):
        self.id = mid
        self.path = path
        self.title = meta.get("title")
        self.numbered = meta.get("numbered")
        self.raw = str(meta.get("raw", "false")) in TRUE
        self.level = int(meta["level"]) if meta.get("level") else None
        self.requires = _split(meta.get("requires"))
        self.optional = _split(meta.get("optional"))
        self.body = body
        if self.numbered is not None:
            self.numbered = str(self.numbered) in TRUE
        if self.title is None:
            m = re.search(r"^#\s+(.*)$", body, re.M)
            self.title = m.group(1).strip() if m else mid


def _split(v):
    return [x.strip() for x in v.split(",")] if v else []


def find_path(src_root, doc_dir, lang, mid):
    """モジュール id からファイルを探す。`shared:` は src/shared/ を見る。"""
    if mid.startswith("shared:"):
        base = os.path.join(src_root, "shared", mid[len("shared:"):])
    else:
        base = os.path.join(doc_dir, lang, mid)
    found = [p for p in (base + ".md", base + ".xml") if os.path.exists(p)]
    if len(found) > 1:
        sys.exit(f"[FATAL] 同じ id に .md と .xml がある: {mid}")
    return found[0] if found else None


def load(path, mid):
    text = open(path, encoding="utf-8").read()
    if path.endswith(".xml"):
        meta, body = _parse_xml(text, path)
    else:
        meta, body = _parse_md(text, path)
    unknown = set(meta) - ALLOWED
    if unknown:
        sys.exit(f"[FATAL] {path}: メタの未知項目 {sorted(unknown)}")
    if meta.get("id") and meta["id"] != mid:
        sys.exit(f"[FATAL] {path}: front-matter の id ({meta['id']}) と位置 ({mid}) が違う。")
    return Module(mid, path, meta, body)


def _parse_md(text, path):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        sys.exit(f"[FATAL] {path}: front-matter が無い。")
    meta = {}
    for line in m.group(1).split("\n"):
        if not line.strip():
            continue
        mm = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if not mm:
            sys.exit(f"[FATAL] {path}: front-matter は `key: value` の行だけ: {line!r}")
        meta[mm.group(1)] = mm.group(2).strip()
    return meta, m.group(2)


def _parse_xml(text, path):
    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        sys.exit(f"[FATAL] {path}: XML として読めない ({e})")
    if root.tag != "module":
        sys.exit(f"[FATAL] {path}: ルート要素は module でなければならない。")
    body_el = root.find("body")
    if body_el is None or body_el.text is None:
        sys.exit(f"[FATAL] {path}: body 要素が無い。")
    body = body_el.text
    if body.startswith("\n"):
        body = body[1:]
    if body.endswith("\n"):
        body = body[:-1]
    return dict(root.attrib), body
