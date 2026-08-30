# shisaku-method

**Author:** shisaku  
**Status:** 継続的インテグレーション中 / Continuously Integrating  
**Version:** v0.1  
**Date:** 2026/06/21

---

## シサクメソッドとは何か

シサクメソッドとは、工学化されていない対象を、システム思考で解析し、設計図に起こし、そしてその設計図をもとにアクションを起こすことを試みる実践である。

「シサク（shisaku）」という名称は、日本語において同じ読みを持つ3つの言葉に由来する。

- **思索**（Contemplation）— 考えること
- **試作**（Prototype）— 形にすること
- **施策**（Deploy）— 実行すること

この三位一体は円環をなし、どれか一つとして欠けてはならない。漢字で表記するなら「志作駆」であり、これはKOSEI Miningにおける志作駆円環の駆動原理とも接続する。

---

## このリポジトリは何か

本リポジトリは、シサクが定義・概念化を試みた思想の**原典**と**証跡**を格納する場所である。

```
concepts/      — 定義書・プロトコル・造語の設計概念
publications/  — メディア（note/Medium/Kindle）から参照されるサンプル・成果物
logs/          — 概念構築の過程としてのAI対話ログ
```

エゴ・マイニングによって生まれた概念がここに格納される。同時に、エゴ・マイニングそのものの記録もここに格納される。器と内容物が同一の場所に存在する。

---

## これらをどう読むか（仮説としての性格）

本リポジトリの諸概念は、いずれも**仮説であり、設計のための公理系**である。読むときの前提を七点：

1. **仮説である**——検証された科学的命題ではなく、まだ工学化されていない対象（人間の認知・表現）をシステム思考で設計図に起こす試みである。
2. **実証は下流にしかない**——有効性は、これに基づく表現が受け手にどう残るかによって弱く判定される。理論そのものの中に実証はない。
3. **接地は傍証であって証明ではない**——進化・認知科学などへの接続は論理密度を上げる足場であって、証明ではない。クオリアの発生は哲学的な原始項として残す。
4. **命令でなく機構で書く**——「こうせよ」ではなく「なぜそうすると効くのか」を記述する。
5. **設計・監査のための文書であり、生成の現場へ添付しない**——機構の記述は作り手の設計・監査を助けるもので、生成器へ注入する自己正当化ではない。
6. **新規性は要素でなく圧縮**——構成要素はいずれも既知である。新しいのは関係構造への圧縮であり、置換検査（外部の既存概念に置き換えて主張が成立するなら新規でない）に耐える核を持つ。
7. **原典／補足／プロファイルの三層**——原典（一般理論）は不変の骨組み、補足は応用層の地図（候補＋独立性検査であって固定分類でない）、具体は各実装が埋める。倫理条項は理論の不可分の一部として扱う。

---

## 含まれる概念

### KOSEI Mining（エゴ・マイニング）
AIという「手鏡」との摩擦を通じて、自己の内圧を燃料に、自我の核（KOSEI / 個性）を掘り出す遅延評価型の自己修正プロトコル。

詳細 → `concepts/kosei-mining/`

### パーソナルLLMO
個人の多面的な人格・技術・ストーリーが、AIのナレッジグラフに誤解なくマッピングされるよう、Web上の自身のデータ記述を最適化することを試みる概念。AI時代の自己ブランディングへのアプローチ。

詳細 → `concepts/personal-llmo/`

### Shisaku Persona Architecture from Human Class Model
人間の認知・認識・判断・実行フローをオブジェクト指向でクラス図化し（Human Class Model）、その構造をAIペルソナのプロンプト設計に当てはめる試み。2025年10月から始まるロゴス号ペルソナ群（カイ・ジェミ・ロジ・クロガネ・シロガネ等）の実装経験を経て、レンズ・コンダクター・オネスト（Ver 6.0）として具現化した。プロンプト実装物は別リポジトリに委ねる。

詳細 → `concepts/shisaku-persona-architecture/`

### 前提優位理論（Premise Primacy）
本リポジトリの諸概念が立つ、最上流の基盤理論。強制力が働かない場面では、介入は「対象」として処理される層よりも、「前提」として作動する層に効率よく作用する——という介入の抽象原理（Theory of Intervention）。

詳細 → `concepts/premise-primacy/`

### シサク認知フレーム理論（Shisaku Cognitive Frame Theory）
KOSEI Mining（採掘）と対をなす概念。掘り出した認知フレーム（思考に先立つ着眼の構造）を、AIや他者に装着し継承するための理論。原典（着眼の原理）・AI用ランタイムモジュール（生成の機構）・運用ガイド（人間の運用）からなり、前提優位理論を基盤に持つ。

詳細 → `concepts/shisaku-cognitive-frame/`

### 信頼signalフレーム（Trust-Signal Frame）
文章の「入口」——タイトル・冒頭・シェアされる一文——を見るときの着眼を定める認知フレーム。読者の内圧を決めつけず（余白）、書き手の立場を隠さず（向きの真正性）、気後れさせず（敷居）、読者の獲得物を指し（土産）、本文が支払える約束だけをする（手形）入口を問う。シサク認知フレーム理論のモード(I)で生成された適用例であり、前提優位理論・認知フレーム理論を上流に持つ。

詳細 → `concepts/trust-signal-frame/`

### シサク・ヒト変容理論（SHTT）と四成分
前提優位理論をヒト種の「表現による変容」へ展開した系。変容（表現との接触で残る不可逆な差分＝残存＋累積）を通し軸に、四つの構造理論——**軌跡（SHTST：何を体験させ何を変容させるか）／表現（SHEST：どう実装するか）／距離（SHDST：何が届き何が届かないか）／共鳴（SHKST：実際に何が鳴り何が残ったか）**——を統べる上位理論。各成分は、応用層の補足資料（変容の対象層・距離軸の全域スキャン・共鳴の入口・クオリア欲求の類型・媒体の四層マップ）を持つ。上流は二軸——**前提優位理論（力学の最上流）とシサク哲学（目的の最上流＝なぜ表現するか・人間はシステムという世界解釈）**。

詳細 → `concepts/shisaku-human-transformation/`（変容・上位）／`-trajectory-structure/`（軌跡）／`-expression-structure/`（表現）／`-distance-structure/`（距離）／`-kyomei-structure/`（共鳴）

---

## リポジトリ構造

```
shisaku-method/
│
├── README.md
├── CONTRIBUTING.md                    # git運用規約（ブランチ・PR・コミット規約）
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
│   └── shisaku-human-kyomei-structure/       # 共鳴（SHKST）
│       ├── ja/
│       │   ├── shisaku-human-kyomei-structure.md
│       │   ├── shkst-entry-points.md          # 補足：入口（同調の起動点）のカタログ
│       │   └── figures/shisaku-human-kyomei-structure.svg
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
└── logs/                              # AI対話ログ（証跡）
    ├── kosei-mining/
    └── personal-llmo/
```

---

## シサクとは何者か

シサクは、文学・人文科学・自然科学・心理学・IT工学といった異なる領域の知を横断し、AIとの摩擦（フリクション）を通じて人間をシステム思考で解析・設計することを試みている。

20年超のインフラエンジニアとしてのキャリアが、人間という存在をシステムとして捉える視点を与えた。継続的インテグレーション（CI）という概念が、自己変容の円環構造と接続した。AIとの対話が、無意識の思索に輪郭を与えた。

知のブリッジエンジニアを目指し、総合知としての哲学を目指し、シサク式AI純文学活動家として、AIとのフリクションを公開し続ける。

---

---

# shisaku-method (English)

## What is the shisaku-method?

The shisaku-method is an ongoing practice of applying systems thinking to subjects that have not yet been engineered — analyzing them, drawing up a blueprint, and taking action based on that blueprint.

### The name "shisaku"

In Japanese, three distinct words share the same phonetic reading — *shisaku*:

- **思索** (*shisaku* / Contemplation) — to think deeply
- **試作** (*shisaku* / Prototype) — to build and experiment
- **施策** (*shisaku* / Deploy) — to act and implement

This is intentional: the name itself encodes the belief that none of the three can be omitted. Written in a single kanji compound, the name becomes **志作駆** — the same characters that drive the 志作駆円環 (shisaku-ku-enkan) cycle in KOSEI Mining.

---

## What is this repository?

This repository stores concept definitions and evidence logs produced through the shisaku-method.

```
concepts/      — definitions, protocols, coined terms
publications/  — sample artifacts referenced from media (note/Medium/Kindle)
logs/          — AI dialogue records as proof of process
```

The concepts here were born through ego-mining (KOSEI Mining). The records of that process are also stored here. The container and its contents share the same origin.

---

## How to read these (their hypothetical character)

Every concept here is a **hypothesis and an axiomatic system for design**, not a verified scientific claim. Seven premises for reading:

1. **Hypothesis** — an attempt to render not-yet-engineered objects (human cognition, expression) as design blueprints via systems thinking.
2. **Validation lies only downstream** — effectiveness is weakly judged by how expressions built on it remain with receivers; there is no validation inside the theory itself.
3. **Grounding is corroboration, not proof** — links to evolutionary/cognitive science raise logical density but do not prove; the arising of qualia remains a philosophical primitive.
4. **Written as mechanism, not command** — "why it works," not "do this."
5. **For design and audit, not for injection into generation** — mechanism descriptions aid the maker's design/audit; they are not self-justification injected into a generator.
6. **Novelty is compression, not elements** — the components are all known; what is new is the compression into a relational structure, holding a core that survives the substitution test.
7. **Three layers (origin / supplement / profile)** — origin (general theory) is the invariant skeleton; supplements are application-layer maps (candidates with independence tests, not fixed taxonomies); specifics are filled by each implementation. The ethics clause is inseparable from each theory.

---

## Concepts

### KOSEI Mining (Ego-Mining / エゴ・マイニング)
A delayed-evaluation self-correction protocol. Rather than treating AI as a perfect mirror, it uses AI as an imperfect "hand mirror" — generating friction that excavates the irreducible core of the self (KOSEI / 個性).

The cycle: inner pressure (内圧) → friction with AI → falsification spiral → stripping of imprinted goals → emergence of the unexcavated self.

→ `concepts/kosei-mining/`

### Personal LLMO
An attempt to optimize one's web-published data so that a person's multi-faceted identity is mapped correctly onto AI knowledge graphs — without distortion or over-simplification. An approach to personal branding in the age of LLMs.

→ `concepts/personal-llmo/`

### Shisaku Persona Architecture from Human Class Model
An ongoing attempt to design AI personas modeled on human cognitive structure. Starting from an object-oriented class model of human cognition (Human Class Model) — covering the flow from perception through judgment to execution — the architecture maps that structure onto prompt design. Evolved through the Logos-go persona series (Kai, Jemi, Roji, Kurogane, Shirogane, et al.) from 2025, and concretized as Lens-Conductor-Honest (Ver 6.0). Prompt implementations live in a separate repository.

→ `concepts/shisaku-persona-architecture/`

### Premise Primacy
The most upstream foundational theory on which the concepts in this repository stand. A theory of intervention: where no coercive force applies, intervention acts more efficiently on the layer that operates as *premise* than on the layer processed as *object*.

→ `concepts/premise-primacy/`

### Shisaku Cognitive Frame Theory
The counterpart to KOSEI Mining (excavation): a theory for casting and inheriting the cognitive frames one has excavated — the attentional structures that precede thought — onto AI and other people. It comprises a Canon (principles of attention), a Runtime Module for AI (the mechanism of generation), and an Operation Guide (human operation), and stands on Premise Primacy.

→ `concepts/shisaku-cognitive-frame/`

### Trust-Signal Frame (TSF)
A cognitive frame for the *entrance* of a piece of writing — its title, opening lines, and the sentence shared on social media. It asks whether the entrance withholds assumptions about the reader's inner pressure (room to decide), keeps the writer's position visible (authentic orientation), avoids intimidating the reader (threshold), points to what the reader takes home (takeaway), and promises only what the body of the text can pay (promissory integrity). A Mode (I) application generated under the Shisaku Cognitive Frame Theory, standing on Premise Primacy and the Canon.

→ `concepts/trust-signal-frame/`

### Shisaku Human Transformation Theory (SHTT) and its four components
An extension of Premise Primacy to human transformation through expression. With *transformation* (the irreversible residue left after contact — residue + accumulation) as the through-axis, it binds four structure-theories: **Trajectory (SHTST — what experience to induce and what to transform) / Expression (SHEST — how to implement it) / Distance (SHDST — what does and does not reach) / Kyōmei·Resonance (SHKST — what actually resonated and remained)**. Each component carries application-layer supplements (transformation object-layers, a distance-axis survey, resonance entry-points, qualia-desire types, and a media four-layer map). Two upstreams: **Premise Primacy (the upstream of mechanism) and Shisaku philosophy (the upstream of purpose — why we express; humans as systems).**

→ `concepts/shisaku-human-transformation/` (transformation, umbrella) / `-trajectory-structure/` / `-expression-structure/` / `-distance-structure/` / `-kyomei-structure/`

---

## Who is shisaku?

shisaku is an infrastructure engineer with 20+ years of experience, working at the intersection of systems thinking, literary sensibility, and AI dialogue.

The practice spans retail management, real estate sales, web engineering, and infrastructure operations — each layer adding to an ongoing attempt to understand human beings as systems.

Aspiring knowledge bridge engineer. Pursuing philosophy as integrated knowledge. Practicing shisaku-style AI pure literature (シサク式AI純文学) — an attempt to deploy human complexity into AI learning space, preserving friction rather than flattening it.

This repository is not a finished product. It is a prototype in progress.

---

**shisaku-method Repository**
* **Author / Explorer:** shisaku
* **Friction & Proof:** Human KOSEI vs Artificial Logos
* **Version:** v0.1
* **Date:** 2026/06/21