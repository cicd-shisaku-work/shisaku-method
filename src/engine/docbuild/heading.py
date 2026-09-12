# -*- coding: utf-8 -*-
"""見出しの深さシフトと節番号の合成。"""
import re

FENCE = re.compile(r"^\s*(```+|~~~+)")


def shift_headings(body, shift, section_prefix=None):
    """先頭 H1 に section_prefix を付け、全見出しを shift 段ずらす。

    コードフェンスの内側は素通し。番号は最初の H1 にだけ付ける。
    """
    out, in_fence, numbered = [], False, False
    for line in body.split("\n"):
        if FENCE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if not in_fence and line.startswith("#"):
            m = re.match(r"^(#+)\s*(.*)$", line)
            if m:
                hashes, title = m.group(1), m.group(2)
                new = "#" * (len(hashes) + shift)
                if len(hashes) == 1 and not numbered and section_prefix:
                    line = f"{new} {section_prefix}{title}"
                    numbered = True
                else:
                    line = f"{new} {title}"
        out.append(line)
    return "\n".join(out)
