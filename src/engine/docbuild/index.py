# -*- coding: utf-8 -*-
"""インデックス（index.toml）とパス対応表（paths.toml）の読み取り。"""
import sys

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 以下では tomli を使う
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        sys.exit("[FATAL] Python 3.11 以上（tomllib）、または tomli が要る。")


class Block:
    def __init__(self, d):
        self.lang = d.get("lang", "ja")
        self.base_depth = int(d.get("base_depth", 1))
        self.cluster_depth = int(d.get("cluster_depth", 0))
        self.render = d.get("render", {})
        self.groups = d.get("groups", [])
        self.allow_unpaired = d.get("allow_unpaired", [])


class Index:
    """1 文書のインデックス。"""

    def __init__(self, path):
        with open(path, "rb") as f:
            data = tomllib.load(f)
        doc = data.get("doc", {})
        self.path = path
        self.id = doc.get("id")
        self.output = doc.get("output")
        self.meta = data.get("meta", {})
        num = data.get("numbering", {})
        self.numbering_enabled = bool(num.get("enabled", False))
        self.numbering_start = int(num.get("start", 1))
        self.numbering_sub_start = int(num.get("sub_start", 1))
        self.numbering_format = num.get("format", ["{n}. ", "{n} "])
        self.blocks = [Block(b) for b in data.get("block", [])]
        if not self.id or not self.output:
            sys.exit(f"[FATAL] {path}: [doc] id と output が要る。")
        if not self.blocks:
            sys.exit(f"[FATAL] {path}: [[block]] が無い。")


def load_paths(path):
    """paths.toml → (base_url, {key: repo 相対パス})。"""
    with open(path, "rb") as f:
        data = tomllib.load(f)
    return data.get("base", {}).get("url", ""), data.get("paths", {})
