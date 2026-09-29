import unittest

from sitebuild.order import concept_order, normalize, parse_upstream


def canon(upstream_line: str | None) -> str:
    head = "# 題\n\n"
    return head + (upstream_line + "\n\n" if upstream_line else "") + "本文。\n"


class ParseTest(unittest.TestCase):
    def test_chain_and_root(self):
        up = parse_upstream(canon("**上流依存：シサク・ヒト変容理論（SHTT）→ 前提優位理論（Premise Primacy）／最上流：シサク・世界解釈**"))
        self.assertEqual(up.chains, [["シサク・ヒト変容理論", "前提優位理論"]])
        self.assertEqual(up.root, "シサク・世界解釈")

    def test_several_upstreams_and_version_noise(self):
        up = parse_upstream(canon("**上流依存：前提優位理論（Premise Primacy）／シサク認知フレーム理論（原典）v0.1**"))
        self.assertEqual(up.chains, [["前提優位理論"], ["シサク認知フレーム理論"]])
        self.assertIsNone(up.root)

    def test_bold_label_only(self):
        up = parse_upstream(canon("**上流依存：** ガンマ解釈 → ベータ理論"))
        self.assertEqual(up.chains, [["ガンマ解釈", "ベータ理論"]])

    def test_no_line(self):
        up = parse_upstream(canon(None))
        self.assertEqual((up.chains, up.root), ([], None))

    def test_normalize(self):
        self.assertEqual(normalize("**前提優位理論（Premise Primacy）**"), "前提優位理論")


class OrderTest(unittest.TestCase):
    # The published corpus, reduced to its upstream lines (v0.1 of the site).
    CANONS = {
        "shisaku-world-interpretation": (None, "シサク・世界解釈"),
        "premise-primacy": (None, "前提優位理論"),
        "shisaku-social-renewal-interpretation": ("**上流依存：シサク・世界解釈**", "シサク・社会更新解釈"),
        "shisaku-prediction-model-interpretation": ("**上流依存：前提優位理論**", "シサク・予測モデル解釈"),
        "shisaku-qualia-interpretation": ("**上流依存：シサク・予測モデル解釈**", "シサク・クオリア解釈"),
        "shisaku-value-interpretation": ("**上流依存：シサク・クオリア解釈 → シサク・予測モデル解釈**", "シサク・価値解釈"),
        "shisaku-human-transformation": ("**上流依存：前提優位理論（Premise Primacy）／最上流：シサク・世界解釈**", "シサク・ヒト変容理論"),
        "shisaku-human-idion-structure": ("**上流依存：シサク・ヒト変容理論（SHTT）→ 前提優位理論（Premise Primacy）／最上流：シサク・世界解釈**", "シサク・ヒト IDION 構造理論"),
        "shisaku-human-distance-structure": ("**上流依存：シサク・ヒト変容理論（SHTT）→ 前提優位理論（Premise Primacy）／最上流：シサク・世界解釈**", "シサク・ヒト距離構造理論"),
        "trust-signal-frame": ("**上流依存：前提優位理論（Premise Primacy）／シサク認知フレーム理論（原典）v0.1**", "入口設計の認知フレーム"),
    }

    def order(self, canons):
        texts = {k: canon(line) for k, (line, _) in canons.items()}
        titles = {k: title for k, (_, title) in canons.items()}
        return concept_order(texts, titles)

    def test_upstream_first_interpretations_first(self):
        result = self.order(self.CANONS)
        self.assertEqual(result.concepts, [
            "shisaku-world-interpretation",
            "shisaku-social-renewal-interpretation",
            "premise-primacy",
            "shisaku-prediction-model-interpretation",
            "shisaku-qualia-interpretation",
            "shisaku-value-interpretation",
            "shisaku-human-transformation",
            "shisaku-human-distance-structure",
            "shisaku-human-idion-structure",
            "trust-signal-frame",
        ])
        self.assertEqual(result.cycle, [])

    def test_unpublished_upstream_is_reported_not_used(self):
        result = self.order(self.CANONS)
        self.assertEqual(result.unmatched, ["trust-signal-frame: シサク認知フレーム理論"])

    def test_cycle_falls_back_to_name_order(self):
        result = self.order({
            "a": ("**上流依存：ビー**", "エー"),
            "b": ("**上流依存：エー**", "ビー"),
            "c": (None, "シー"),
        })
        self.assertEqual(result.concepts, ["c", "a", "b"])
        self.assertEqual(result.cycle, ["a", "b"])


if __name__ == "__main__":
    unittest.main()
