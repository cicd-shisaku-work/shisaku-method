# shisaku-method

**Author:** shisaku  
**Status:** 継続的インテグレーション中 / Continuously Integrating  
**Version:** v0.1  
**Date:** 2026/06/05

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
concepts/  — 定義書・プロトコル・造語の設計概念
logs/      — 概念構築の過程としてのAI対話ログ
```

エゴ・マイニングによって生まれた概念がここに格納される。同時に、エゴ・マイニングそのものの記録もここに格納される。器と内容物が同一の場所に存在する。

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

---

## リポジトリ構造

```
shisaku-method/
│
├── README.md
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
│   └── shisaku-persona-architecture/
│       ├── ja/
│       │   ├── shisaku-persona-architecture-design-memo-v0.1.md
│       │   ├── honest-domain-strict-v1.0.md
│       │   └── lens-conductor-honest-v6.0.md
│       └── en/
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
concepts/  — definitions, protocols, coined terms
logs/      — AI dialogue records as proof of process
```

The concepts here were born through ego-mining (KOSEI Mining). The records of that process are also stored here. The container and its contents share the same origin.

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
* **Date:** 2026/06/05