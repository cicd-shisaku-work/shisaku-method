# shisaku-method

**Author:** shisaku  
**Status:** 継続的インテグレーション中 / Continuously Integrating  
**Version:** v0.3  
**Date:** 2026/09/16

---

## シサクメソッドとは何か

シサクメソッドとは、工学化されていない対象を、システム思考で解析し、設計図に起こし、そしてその設計図をもとにアクションを起こすことを試みる実践である。

### 「シサク」という名称
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
src/           — 文書ビルド。モジュールが正本で、README はここから生成される
```

エゴ・マイニングによって生まれた概念がここに格納される。同時に、エゴ・マイニングそのものの記録もここに格納される。器と内容物が同一の場所に存在する。

---

## 誰が、どこまで読むか

本リポジトリは三種の読み手を想定する。**読む必要のある範囲が違う**ので、それぞれの面だけで何ができるかを分けて書く。

| 読み手 | 読む面 | その面だけでできること |
| :-- | :-- | :-- |
| **一般読者** | 原典の本文（`concepts/` の各文書） | **原典だけで理論が読める。** 定義・適用範囲・参照先が本文で辿れ、仕組みを見なくても済む |
| **評価読者** | ＋ 仕組みの文書（`src/engine/`・`CONTRIBUTING.md`・`terminology-policy.md`・`terminology-ledger.md`）と、文書ビルドに載っている文書のモジュール・インデックス | **作りが辿れる。** なぜこの構造か、何を検査しているか、どこが正本かが読める |
| **著者** | すべて | — |

**適用の範囲。** 一段目（原典の本文）は全文書にある。二段目のうち、仕組みの文書はリポジトリ全体に掛かるが、**文書ごとのモジュールとインデックスは、文書ビルドに載っている文書にしかない**——載っているのは `src/docs/` にインデックスを持つ文書で、それ以外は公開されている本文がそのまま正本である。載っていない文書について、評価読者が見る面は一般読者と同じになる。

**この分類が決めるもの。** どの面に何を出すかは、ここから出る。一段目が成り立つのは、定義・適用範囲・参照先を**本文が持つ**ときである。仕組みのための記述は、一段目の読み心地に出さない。

---

## これらをどう読むか（仮説としての性格）
<!-- machinery-def: README の七前提 -->

本リポジトリの諸概念は、いずれも**仮説であり、設計のための公理系**である。読むときの前提を七点：

1. **仮説である**——検証された科学的命題ではなく、まだ工学化されていない対象（人間の認知・表現）をシステム思考で設計図に起こす試みである。
2. **実証は下流にしかない**——有効性は、これに基づく表現が受け手にどう残るかによって弱く判定される。理論そのものの中に実証はない。
3. **接地は傍証であって証明ではない**——進化・認知科学などへの接続は論理密度を上げる足場であって、証明ではない。クオリアの発生は哲学的な原始項として残す。
4. **命令でなく機構で書く**——「こうせよ」ではなく「なぜそうすると効くのか」を記述する。
5. **設計・監査のための文書であり、生成の現場へ添付しない**——機構の記述は作り手の設計・監査を助けるもので、生成器へ注入する自己正当化ではない。
6. **新規性は要素でなく圧縮**——構成要素はいずれも既知である。新しいのは関係構造への圧縮であり、置換検査（外部の既存概念に置き換えて主張が成立するなら新規でない）に耐える核を持つ。
7. **原典／補足／プロファイルの三層**——原典（一般理論）は不変の骨組み、補足は応用層の地図（候補＋独立性検査であって固定分類でない）、具体は各実装が埋める。倫理条項は理論の不可分の一部として扱う。

**語の規約（系列横断）**——同じ語を別の座標軸の概念名に使わない、という規約と、その所在表をリポジトリ直下に置く：`terminology-policy.md`（規約・一語一軸・型付け・単独語のスコープ）と `terminology-ledger.md`（語・軸・対象・定義位置の薄い一枚）。新しい語を立てるとき、また他文書から語を参照するときは、ここを引く。

---

## 含まれる概念

### シサク・世界解釈（Shisaku World-Interpretation）
シサクメソッド以前の**起点**であり、系列の最上流に立つ観方。人間を、生の衝動（BIOS）と、物語で書かれる圧縮概念（OS）のハイブリッドとして観るレンズである。加速する環境との不整合から現代の課題を読み、生存の渇望（安全・序列・新奇）の上に、OS層の渇望「自分らしく在りたい」を置く。真偽ではなく効きで測る、一表現者の解釈。**前提優位理論が「力学の最上流」なら、本書は「観方の最上流」**——二軸で系列を支える。シサクメソッドとは、この解釈が指す課題へ、自分の物語（＝前提）を書いていく活動にほかならない。

詳細 → `concepts/shisaku-world-interpretation/`

### 前提優位理論（Premise Primacy）
本リポジトリの諸概念が立つ、最上流の基盤理論。強制力が働かない場面では、介入は「対象」として処理される層よりも、「前提」として作動する層に効率よく作用する——という介入の抽象原理（Theory of Intervention）。

詳細 → `concepts/premise-primacy/`

### シサク認知フレーム理論（Shisaku Cognitive Frame Theory）
KOSEI Mining（採掘）と対をなす概念。掘り出した認知フレーム（思考に先立つ着眼の構造）を、AIや他者に装着し継承するための理論。原典（着眼の原理）・AI用ランタイムモジュール（生成の機構）・運用ガイド（人間の運用）からなり、前提優位理論を基盤に持つ。

詳細 → `concepts/shisaku-cognitive-frame/`

### シサク・ヒト変容理論（SHTT）と四成分
前提優位理論をヒト種の「表現による変容」へ展開した系。**二相**——入口（表現者の核＝IDION）と出口（受け手の変容＝四成分）——に同じ変容が立ち、帰趨（残存／変容の二値・成分ごと）を通し軸に、両端共通の過程（接触→気づき→再演段→照合段→承認段→書き換え段→定常化段→折り返し段）と深度語彙（変容深度・変容広さ・自己距離／共鳴深度・共鳴距離・共鳴強度・共鳴負荷）の区別を置き、四つの構造理論——**軌跡（SHTST：何を体験させ何を変容させるか）／表現（SHEST：どう実装するか）／距離（SHDST：何が届き何が届かないか）／共鳴（SHKST：実際に何が鳴り何が残ったか）**——を統べる上位理論。各成分は、応用層の補足資料（変容の対象層・深度語彙・変容の過程の八段・距離軸の全域スキャン・共鳴の入口・共鳴事例の分解表・クオリア欲求の類型・媒体の四層マップ）を持つ。上流は二軸——**前提優位理論（力学の最上流）とシサク・世界解釈（目的・観方の最上流＝なぜ表現するか・人間はシステムという世界解釈）**。

詳細 → `concepts/shisaku-human-transformation/`（変容・上位）／`-trajectory-structure/`（軌跡）／`-expression-structure/`（表現）／`-distance-structure/`（距離）／`-kyomei-structure/`（共鳴）

### シサク・ヒト IDION 構造理論（IDION）
SHTT の**入口側**——表現が湧き出す基体＝**表現者自身の変容の集合が形作った固有の核（IDION）**の構造理論（成分でなく、主体の核の側に立つ・略号を持たず把手 IDION で参照）。四成分が出口側（受け手の変容）を担うのに対し、同じ「変容」の入口端に立つ。IDION を起源でなく、核の書き換えを成立させた経緯（変容コスト——闘いはその一形態・統合もある）と非移転で弁別し、強度を変容量（縦＝変容深度〔たどりの長さ〕・変容広さ〔本数〕／横＝結合則）で測り、判定を本人／受け手で非対称に分け、偽装を「自分の IDION に無いものを自分のものとして表現すること」として道徳でなく力学で定義し、品格を誠実＋視線に較正する。KOSEI（個性）は IDION の日本語グロス。補足資料——具体事例集と分離検出／変容コストの形態の地図／層と軸の地図／システムとの同型（設計の検査道具）。

詳細 → `concepts/shisaku-human-idion-structure/`

### KOSEI Mining（エゴ・マイニング）
AIという「手鏡」との摩擦を通じて、自己の内圧を燃料に、自我の核（KOSEI / 個性）を掘り出す遅延評価型の自己修正プロトコル。

詳細 → `concepts/kosei-mining/`

---

## 含まないもの

本リポジトリは、**事業に用いるものを置かない。** ここに置くのは思想の原典と証跡だけである。

事業のために別に持っているのは、次の二つである。

- **シサク生成統治理論**——生成をどう統治するかの理論。**上流にあたる。** 本リポジトリの原典が埋める六要件（意味・用法条件・根拠・目的・目標・効果と失敗機構）は、この理論の様式である。**本リポジトリの原典はヘッダーに上流依存を書く。六要件はここで立てたものではないので、その出所も書く。**
- **シサク IDION 共鳴ライティング**——IDION を、受け手が共鳴する形へ着地させる制作規律。**下流にあたる。** 本リポジトリの変容理論群を参照するだけで、上流に何も足さない。

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
src/           — the document build; modules are the source, and the README is generated from them
```

The concepts here were born through ego-mining (KOSEI Mining). The records of that process are also stored here. The container and its contents share the same origin.

---

## Who reads how far

This repository assumes three kinds of readers. Because the range each needs to read differs, what each surface alone lets you do is stated separately.

| Reader | Surface | What that surface alone lets you do |
| :-- | :-- | :-- |
| **General reader** | The canonical texts (`concepts/`) | **Read the theory from the canon alone.** Definitions, scope and references are traceable within the text, without looking at the machinery |
| **Repository reviewer** | ＋ The machinery documents (`src/engine/`, `CONTRIBUTING.md`, `terminology-policy.md`, `terminology-ledger.md`), and the modules and index of documents carried by the document build | **The construction is legible.** Why this structure, what is checked, and where the source of truth sits |
| **Author** | Everything | — |

**Scope of application.** The first surface exists for every document. Of the second, the machinery documents apply repository-wide, but **per-document modules and indexes exist only for documents carried by the document build** — those are the documents that hold an index under `src/docs/`. For the others, the published text is itself the source of truth, and the reviewer's surface is the same as the general reader's.

**What this classification decides.** What appears on which surface follows from it. The first surface holds when definitions, scope and references live **in the text itself**. Descriptions written for the machinery do not appear in the first surface's reading experience.

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

**Terminology policy (series-wide)** — the rule that one word belongs to one axis, plus an index of where each term is defined, sit at the repository root: `terminology-policy.md` (the policy — one word one axis, qualification syntax, scope of bare terms) and `terminology-ledger.md` (a thin table of word, axis, qualifier, locus of definition). Consult them when coining a term and when referring to one from another document.

---

## Concepts

### Shisaku World-Interpretation
The **starting point** that precedes the shisaku-method, and the most upstream *way of seeing* in the series: a lens that views the human as a hybrid of raw drives (BIOS) and compressed concepts written as stories (OS). It reads the troubles of the present from the mismatch with an accelerating environment, and places — above the survival cravings (safety, status, novelty) — an OS-layer craving: *to be oneself*. One person's interpretation, measured by whether it works, not by whether it is true. **If Premise Primacy is "the upstream of mechanism," this is "the upstream of seeing"** — the two axes on which the series stands. The shisaku-method is, in the end, the activity of writing one's own story (= premise) toward the problem this interpretation names.

→ `concepts/shisaku-world-interpretation/`

### Premise Primacy
The most upstream foundational theory on which the concepts in this repository stand. A theory of intervention: where no coercive force applies, intervention acts more efficiently on the layer that operates as *premise* than on the layer processed as *object*.

→ `concepts/premise-primacy/`

### Shisaku Cognitive Frame Theory
The counterpart to KOSEI Mining (excavation): a theory for casting and inheriting the cognitive frames one has excavated — the attentional structures that precede thought — onto AI and other people. It comprises a Canon (principles of attention), a Runtime Module for AI (the mechanism of generation), and an Operation Guide (human operation), and stands on Premise Primacy.

→ `concepts/shisaku-cognitive-frame/`

### Shisaku Human Transformation Theory (SHTT) and its four components
An extension of Premise Primacy to human transformation through expression. Two ends of one transformation — the entry (the expresser's core, IDION) and the exit (the receiver's transformation, the four components) — with the *outcome* (residue / transformation, read per component) as the through-axis, an eight-stage process common to both ends, and a typed depth vocabulary. It binds four structure-theories: **Trajectory (SHTST — what experience to induce and what to transform) / Expression (SHEST — how to implement it) / Distance (SHDST — what does and does not reach) / Kyōmei·Resonance (SHKST — what actually resonated and remained)**. Each component carries application-layer supplements (transformation object-layers, depth vocabulary, the eight stages of transformation, a distance-axis survey, resonance entry-points, an instance-decomposition table, qualia-desire types, and a media four-layer map). Two upstreams: **Premise Primacy (the upstream of mechanism) and the Shisaku World-Interpretation (the upstream of purpose and seeing — why we express; humans as systems).**

→ `concepts/shisaku-human-transformation/` (transformation, umbrella) / `-trajectory-structure/` / `-expression-structure/` / `-distance-structure/` / `-kyomei-structure/`

### Shisaku Human IDION-Structure Theory (IDION)
The *entry side* of SHTT — the structure of the expresser's own core, **IDION**: the core formed by the set of one's own transformations (not a component; it stands on the subject's side, referred to by the handle IDION without an acronym). Where the four components carry the exit side (the receiver's transformation), IDION stands at the entry end of the same transformation. It distinguishes IDION not by origin but by the traceable history of a core rewrite (transformation cost — struggle is one form, integration another) and by non-transferability; measures strength as transformation quantity (vertical = transformation depth and breadth / horizontal = the combination rule); splits judgment asymmetrically between the person and the receiver; defines disguise as "expressing what is not in one's IDION as one's own" by mechanics rather than morality; and calibrates dignity as honesty + gaze. KOSEI (個性) is the Japanese gloss of IDION. Supplements — worked cases and separation detection / a map of transformation-cost forms / a map of layers and axes / system isomorphism (a design check tool).

→ `concepts/shisaku-human-idion-structure/`

### KOSEI Mining (Ego-Mining / エゴ・マイニング)
A delayed-evaluation self-correction protocol. Rather than treating AI as a perfect mirror, it uses AI as an imperfect "hand mirror" — generating friction that excavates the irreducible core of the self (KOSEI / 個性).

The cycle: inner pressure (内圧) → friction with AI → falsification spiral → stripping of imprinted goals → emergence of the unexcavated self.

→ `concepts/kosei-mining/`

---

## What this repository does not hold

This repository **does not hold what is used for business.** What it holds is the canonical texts of the thought, and the record of it.

Two things are kept elsewhere, for business.

- **Shisaku Generation Governance Theory** — a theory of how generation is governed. It is **upstream**. The six requirements each canon here fills (meaning, conditions of use, grounds, purpose, goal, effect and failure mode) are that theory's form. **Each canon here names its upstream in its header. The six requirements were not established here, so their origin is named too.**
- **Shisaku IDION-Kyōmei Writing** — a discipline for landing an IDION in a form its receiver resonates with. It is **downstream**. It refers to the transformation theories here and adds nothing to them.

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
* **Version:** v0.3
* **Date:** 2026/09/16
