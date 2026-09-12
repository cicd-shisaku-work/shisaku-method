---
id: tree
---
# リポジトリ構造

```
shisaku-method/
│
├── README.md
├── CONTRIBUTING.md                    # git運用規約（ブランチ・PR・コミット規約）
├── terminology-policy.md              # 用語規約（系列横断・一語一軸）
├── terminology-ledger.md              # 用語台帳（語・軸・対象・定義位置）
│
├── concepts/                          # 概念定義（成果物）
│   ├── kosei-mining/
│   │   ├── ja/                        # 日本語版
│   │   │   ├── kosei-mining-definition.md
│   │   │   ├── kosei-mining-protocol-definition.md
│   │   │   ├── kosei-mining-origin.md
│   │   │   └── kosei-mining-origin-note.md
│   │   └── en/                        # 英語版（準備中）
│   ├── personal-llmo/
│   │   ├── ja/
│   │   └── en/
│   ├── shisaku-persona-architecture/
│   │   ├── ja/
│   │   │   ├── shisaku-persona-architecture-design-memo-v0.1.md
│   │   │   ├── honest-domain-strict-v1.0.md
│   │   │   └── lens-conductor-honest-v6.0.md
│   │   └── en/
│   ├── premise-primacy/
│   │   ├── ja/
│   │   │   └── premise-primacy.md
│   │   └── en/
│   ├── shisaku-cognitive-frame/
│   │   ├── ja/
│   │   │   ├── shisaku-cognitive-frame-canon.md
│   │   │   ├── shisaku-cognitive-frame-runtime.md
│   │   │   └── shisaku-cognitive-frame-operation-guide-vcurrent.md
│   │   └── en/
│   ├── trust-signal-frame/            # 信頼signalフレーム（モードI適用例）
│   │   ├── ja/
│   │   │   └── trust-signal-frame.md
│   │   └── en/
│   ├── shisaku-human-transformation/         # 変容理論（SHTT・上位／四成分を統べる）
│   │   ├── ja/
│   │   │   ├── shisaku-human-transformation.md
│   │   │   ├── shtt-object-layers.md          # 補足：変容の対象層（種類の軸）
│   │   │   ├── shtt-depth-terms.md            # 補足：深度語彙（量の語と境界検査）
│   │   │   ├── shtt-process-stages.md         # 補足：変容の過程の八段（両端共通の詳細）
│   │   │   ├── shtt-authoring-policy.md       # 資料作成オペレーションルール（原典/補足の境界）
│   │   │   └── figures/shisaku-human-transformation.svg
│   │   └── en/
│   ├── shisaku-human-trajectory-structure/   # 軌跡（SHTST）
│   │   ├── ja/
│   │   │   ├── shisaku-human-trajectory-structure.md
│   │   │   └── figures/shisaku-human-trajectory-structure.svg
│   │   └── en/
│   ├── shisaku-human-expression-structure/   # 表現（SHEST）
│   │   ├── ja/
│   │   │   ├── shisaku-human-expression-structure.md
│   │   │   ├── shest-media-map.md             # 補足：媒体の四層マップと受容系全表
│   │   │   ├── shest-qualia-desire-types.md   # 補足：クオリア欲求の類型・再構成タイプ
│   │   │   └── figures/shisaku-human-expression-structure.svg
│   │   └── en/
│   ├── shisaku-human-distance-structure/     # 距離（SHDST）
│   │   ├── ja/
│   │   │   ├── shisaku-human-distance-structure.md
│   │   │   ├── shdst-distance-axes.md         # 補足：距離軸の全域スキャン
│   │   │   └── figures/shisaku-human-distance-structure.svg
│   │   └── en/
│   ├── shisaku-human-kyomei-structure/       # 共鳴（SHKST）
│   │   ├── ja/
│   │   │   ├── shisaku-human-kyomei-structure.md
│   │   │   ├── shkst-entry-points.md          # 補足：入口（同調の起動点）のカタログ
│   │   │   ├── shkst-instance-decomposition.md # 補足：共鳴事例の分解表（軸の MECE と実例）
│   │   │   └── figures/shisaku-human-kyomei-structure.svg
│   │   └── en/
│   └── shisaku-human-idion-structure/        # IDION（SHTT の入口側＝表現者の固有核）
│       ├── ja/
│       │   ├── shisaku-human-idion-structure.md
│       │   ├── idion-cases.md                 # 補足：具体事例集と分離検出
│       │   ├── idion-cost-forms.md            # 補足：変容コストの形態の地図
│       │   ├── idion-axes-map.md              # 補足：層と軸の地図
│       │   ├── idion-system-isomorphism.md    # 補足：システムとの同型（設計の検査道具）
│       │   └── figures/shisaku-human-idion-structure.svg
│       └── en/
│
├── publications/                      # メディアから参照されるサンプル・成果物
│   ├── published/                     # 公開記事から参照される安定成果物
│   │   ├── note/
│   │   │   ├── ja/
│   │   │   │   ├── pees/
│   │   │   │   │   ├── pees-prelim-business.md
│   │   │   │   │   ├── pees-prelim-business-output-format.md
│   │   │   │   │   ├── shisaku-evaluator-axioms.md   # SEFA（PEES同時読み用の上位公理）
│   │   │   │   │   └── verification-results/
│   │   │   │   └── swp/                              # シサク書き手原則フレーム（SWP）
│   │   │   │       ├── README.md
│   │   │   │       ├── swp-writer-principles.md
│   │   │   │       ├── swp-claude-generation-guideline.md
│   │   │   │       └── swp-voice-extraction-prompts.md
│   │   │   └── en/
│   │   ├── medium/
│   │   │   ├── ja/
│   │   │   └── en/
│   │   └── kindle/
│   │       ├── ja/
│   │       └── en/
│   └── tmp/                           # その時のアイデア／プロトタイプの仮置き
│
├── logs/                              # AI対話ログ（証跡）
│   ├── kosei-mining/
│   └── personal-llmo/
│
└── src/                               # 文書ビルド（モジュールが正本・README等はここから生成）
    ├── engine/                        # ビルド本体・設計書・運用手順書
    ├── shared/                        # 文書をまたぐ共有モジュール（ヘッダー・奥付・ライセンス）
    ├── paths.toml                     # リポジトリ内パスの対応表
    └── docs/                          # 文書のモジュール（ディレクトリ名＝出力の語幹）
        ├── root/                      # リポジトリ直下へ出る文書
        └── concepts/                  # concepts/ へ出る文書
```
