# -*- coding: utf-8 -*-
"""本文中トークン {{種類:キー}} の解決。"""
import re

PATTERN = re.compile(r"\{\{([a-z]+):([^}]+)\}\}")
ESCAPE = "\x00ESCAPED_OPEN\x00"
MAX_DEPTH = 5


class Resolver:
    def __init__(self, meta, paths, base_url, errors):
        self.meta = meta
        self.paths = paths
        self.base_url = base_url
        self.errors = errors
        self.used_meta = set()
        self._optional_missing = False

    # --- 値の解決 -------------------------------------------------
    def value(self, kind, key, secmap, render, depth=0, optional=()):
        if kind == "meta":
            if key not in self.meta:
                if key in optional:
                    # 任意メタが無い＝その行は出さない（行落ち）。エラーにしない。
                    self._optional_missing = True
                    return ""
                self._err(f"[meta] に無いキー: {{{{meta:{key}}}}}")
                return None
            self.used_meta.add(key)
            v = str(self.meta[key])
            return self.resolve(v, secmap, render, depth + 1, optional) if PATTERN.search(v) else v
        if kind == "path":
            if key not in self.paths:
                self._err(f"paths.toml に無いキー: {{{{path:{key}}}}}")
                return None
            return self.paths[key]
        if kind == "url":
            if key not in self.paths:
                self._err(f"paths.toml に無いキー: {{{{url:{key}}}}}")
                return None
            return self.base_url.rstrip("/") + "/" + self.paths[key].strip("/")
        if kind in ("sec", "num", "title"):
            node = secmap.get(key)
            if node is None:
                self._err(f"解決できない参照: {{{{{kind}:{key}}}}}")
                return None
            if kind == "title":
                return node["title"]
            if node["section"] is None:
                self._err(f"番号を持たないモジュールへの参照: {{{{{kind}:{key}}}}}")
                return None
            if kind == "num":
                return node["section"]
            fmt = render.get("sec", "{n}")
            return fmt.replace("{n}", node["section"]).replace("{t}", node["title"])
        self._err(f"未知の種類: {{{{{kind}:{key}}}}}")
        return None

    def _err(self, msg):
        if msg not in self.errors:
            self.errors.append(msg)

    # --- 本文の解決 -----------------------------------------------
    def resolve(self, text, secmap, render, depth=0, optional=()):
        if depth > MAX_DEPTH:
            self._err("[meta] の参照が深すぎる（循環の疑い）")
            return text
        text = text.replace("\\{{", ESCAPE)
        out = []
        for line in text.split("\n"):
            if not PATTERN.search(line):
                out.append(line)
                continue
            original = line
            self._optional_missing = False

            def repl(m):
                v = self.value(m.group(1), m.group(2), secmap, render, depth, optional)
                return "" if v is None else v

            new = PATTERN.sub(repl, line)
            # 行落ち：(a) 値の無い任意メタを含む行 (b) 埋めた結果、空白だけになった行
            if self._optional_missing:
                continue
            if new.strip() == "" and original.strip() != "":
                continue
            out.append(new)
        return "\n".join(out).replace(ESCAPE, "{{")
