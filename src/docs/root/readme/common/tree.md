---
id: tree
---
# リポジトリ構造

```
shisaku-method/
├── README.md
├── CONTRIBUTING.md          # git運用規約（ブランチ・PR・コミット規約・バージョニング）
├── terminology-policy.md    # 用語規約（系列横断・一語一軸）
├── terminology-ledger.md    # 用語台帳（語・軸・対象・定義位置）
├── LICENSE
│
├── concepts/                # 概念定義。概念ごとに原典と補足を持ち、各々 ja/ と en/ に分かれる
├── publications/            # メディアから参照される成果物（published/ ＝安定・tmp/ ＝仮置き）
├── logs/                    # AI対話ログ（証跡）
└── src/                     # 文書ビルド。モジュールが正本で、README などはここから生成される
```

各概念の中身と置き場は「含まれる概念」を参照。
