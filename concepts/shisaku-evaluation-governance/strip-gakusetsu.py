#!/usr/bin/env python3
"""学説タグ除去スクリプト（SEGT 採点ビュー生成）

SEGT 原典（`shisaku-evaluation-governance-canon.md`）は、外部学説名を
HTMLコメント形式の学説タグで囲っている：

    <!--学説-->……学説名を含む記述……<!--/学説-->

設計・監査局面は原典をそのまま読む。採点局面へは、このスクリプトで
学説タグの区間を丸ごと除去した「採点ビュー」を渡す。評価者に学説名を
露出させず、合理化劇場（採点票の地の文で学説語を自己正当化に使う漏出）を
物理的に断つため（SGGT 1.5 / SEGT 序）。

操作の感触と内部相互参照（SEFA / SGGT）は地の文に残るので、採点ビューでも
拘束は保たれる。

使い方:
    python3 strip-gakusetsu.py 入力.md            # 標準出力へ
    python3 strip-gakusetsu.py 入力.md 出力.md     # 出力ファイルへ
    python3 strip-gakusetsu.py                    # 既定: ja/ の原典 → *.scoring-view.md
"""

import re
import sys
from pathlib import Path

OPEN_TAG = "<!--学説-->"
CLOSE_TAG = "<!--/学説-->"

# 学説タグ区間（開きタグから最も近い閉じタグまで）を除去する。
# re.DOTALL で改行をまたぎ、非貪欲(*?)で入れ子でない最短区間に限定する。
_GAKUSETSU_SPAN = re.compile(
    re.escape(OPEN_TAG) + r".*?" + re.escape(CLOSE_TAG),
    re.DOTALL,
)

# 除去後に残る 3 連以上の空行を 2 行に畳む（見た目の穴を塞ぐ）。
_EXTRA_BLANK_LINES = re.compile(r"\n{3,}")


def strip_gakusetsu(text: str) -> str:
    """学説タグ区間を除去し、余分な空行を畳んだ採点ビュー文字列を返す。"""
    stripped = _GAKUSETSU_SPAN.sub("", text)
    stripped = _EXTRA_BLANK_LINES.sub("\n\n", stripped)
    return stripped


def _assert_no_leak(text: str) -> None:
    """タグが片方だけ残っていないか（対応漏れ）を検査し、あれば止める。"""
    if OPEN_TAG in text or CLOSE_TAG in text:
        raise SystemExit(
            "学説タグが除去後も残存: 開き/閉じの対応が壊れている可能性。"
            "原典のタグ対応を確認してください。"
        )


def _default_input() -> Path:
    return (
        Path(__file__).parent
        / "ja"
        / "shisaku-evaluation-governance-canon.md"
    )


def main(argv: list[str]) -> int:
    if len(argv) >= 2:
        in_path = Path(argv[1])
    else:
        in_path = _default_input()

    source = in_path.read_text(encoding="utf-8")
    view = strip_gakusetsu(source)
    _assert_no_leak(view)

    if len(argv) >= 3:
        out_path = Path(argv[2])
    elif len(argv) == 2:
        out_path = None  # 明示入力・出力未指定 → 標準出力
    else:
        # 既定: 原典と同じ場所に *.scoring-view.md を書く
        out_path = in_path.with_suffix(".scoring-view.md")

    if out_path is None:
        sys.stdout.write(view)
    else:
        out_path.write_text(view, encoding="utf-8")
        removed = source.count(OPEN_TAG)
        sys.stderr.write(
            f"採点ビューを書き出し: {out_path} "
            f"（学説区間 {removed} 箇所を除去）\n"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
