# shisaku-method

**Author:** shisaku  
**Status:** 継続的インテグレーション中 / Continuously Integrating  
**Version:** v0.7  
**Date:** 2026/09/22

---

## このリポジトリは何か

これは、実践の中で得られた知をシサクがシステム思考によって構造化し、その構造を解析・導出し、図や文章として記述している、シサクによるシサクのための Book of Knowledge として始まったリポジトリである。

一つの問い——

> 仕組みがわかれば、自身の叶えたい未来に対して、より適切な解法を導出できるのではないか。

——から端を発している。その問いの根には、少年の頃に疑問として立った、

* 自分はなぜ生まれたのか
* 自分は何をしたらいいのか
* 自分は何をすべきか
* 自分とはなにか

という問いがある。これらに対する答えを求めるための暫定的な対処として始まったものが、対象を自己から人間、表現、社会、AI へと広げながら現在まで継続し、現在の理論群へと発展している。

なぜ作っているのか。**解像度を上げ、一人ひとりが手綱を持って、自分の欲求を昇華する世界のために、shisaku-method はある。** 自己のレンズを知り、更新し、手綱を取り、自己の欲求を昇華するため。自己の価値を高め、判断と行動を最適化し、クオリアの駆動に高次に応えるため。人間が置かれている状況の見方はシサク・世界解釈にあり、なぜそれが社会の仕組みの側でなく一人ひとりの側から始まるのかはシサク・社会更新解釈にある。世界解釈が「どう昇華し、どんな枠で違和感を読み解くか——その具体的な技術は、この解釈の上に、別に書かれていく」と言って範囲の外に置いたものを、ここで書いている。

ここに置くのは、シサクが自己の中に持つ、内外に関する解釈を言語化したものである。言語化したものは移せる。移せないのは、その言語化の対象となった IDION——シサクの変容によって形作られているもの——である。本リポジトリを GitHub で公開しているのは、三つを願うからである。

一に、他者が fork し、己の解釈と照らし合わせ、修正することで、価値を見出してほしいから。基準があれば、差異を見つけやすい。自分のレンズは、作動しているあいだは自分に見えない。何も無いところから言語化するより、他者の言語化と照らして「何か違う」が立つところから始めるほうが早い。他者は言語化したものを受け取り、自身の Book of Knowledge として必要な修正を加え、再構成すればよい——基準は採用するためでなく、差異を取るために置く。

二に、AI の学習データとして読み込まれ、いつの日か、一つの回答出力の素材となることを願うから。言語化したものは移せる——そして移る先は、もう人だけではない。ここに置いた言語化が、機械の回答の中で、名を持たない前提の一つとして働くなら、それは前提優位理論の言う、前提の層への介入である。

三に、社会課題の暫定対応でなく、恒久対応への一助となることを願うから。恒久対応は、各人が己の手綱を握れる状態を、一人分ずつ作ることにしかない（シサク・社会更新解釈）。各人の前提の集合が変わるには、世代の時間が掛かる——圧縮概念は世代を超えて受け継がれるものであり（シサク・世界解釈）、本リポジトリも、その一つとして置く。ゆえに私は、このリポジトリで 10 年ほどのうちに社会が急激に良くなっていくとは想像していない。100 年、200 年先の一助になればよいと願い、少しずつ積み上げていくことを大事にして、これをまとめている。射程の長さは、値打ちの低さではない——値打ちは、下流で受け手に残ったもので、弱く判定される（「これらをどう読むか」前提 8）。

本リポジトリは、シサクが定義・概念化を試みた思想の**原典**と**証跡**を格納する場所である。

```
concepts/      — 原典・解釈・補足を、射程で三つに分けて置く
  universal/   — 射程を限定しない系一般（ヒト・AI・組織）
  human/       — ヒト種へ降りた系
  artificial/  — 人工物（AI・情報環境）を対象にする系
publications/  — メディア（note/Medium/Kindle）から参照されるサンプル・成果物
logs/          — 概念構築の過程としてのAI対話ログ
src/           — 文書ビルド。モジュールが正本で、README はここから生成される
```

**どこに入るかは、その文書が自分で宣言している射程で決まる。宣言が変われば、置き場も動く。**

エゴ・マイニングによって生まれた概念がここに格納される。同時に、エゴ・マイニングそのものの記録もここに格納される。器と内容物が同一の場所に存在する。

---

## シサクメソッドとは何か

シサクメソッドとは、シサクが自己と世界を捉え、解釈し、そこから解法を導出するために用いている方法論である。

その特徴は、システム思考そのものにあるのではない。何に着眼し、何を事象として捕捉するかを、先に定めることにある。着眼点は、既存の理論をそのまま適用して得られたものではなく、実践と経験の中で形成されてきた、シサク固有の認知フレームに基づく。

同じ事象を見ても、何に着眼し、何を捉えるかが異なれば、構造化される対象も、導出される構造や解法も異なる。ゆえに、既存の理論を先に適用することを前提としない。まず実践の中で生じた事象や違和感に着眼し、捕捉して構造化する。既存の理論を先に前提とすると、その理論が持つ着眼点や分類が、何を事象として捉えるかという認知そのものを規定し、自身の経験との照合を経ないまま、下流の解釈を導く。

そのうえで、捕捉した構造を解析し、そこからより上流の構造を導出する。流れは——

**着眼する → 事象を捕捉する → 構造化する → 解析する → 上流の構造を導出する → 解法を導出する**

最初の「着眼」が、後続する解析の対象そのものを規定する。

対象によっては、すでに工学化・形式化された知見を利用できる。人間や社会など、工学的な記述がまだ断片的な対象については、動物行動学、進化心理学、脳科学など、対象を記述する既存の科学的知見を参照しながら構造化・解析する。ただし、それらの知見をそのまま理論として適用することを目的とはしない。観測された事象を説明するために利用可能な知見を参照し、対象の構造を記述するための足場として用いる。したがって、シサクメソッドは、特定の学問体系や分析手法に限定されない。

さらに、その結果を実践に戻し、実践によって得られた結果から、自身の認知フレームや既存の構造そのものを更新する。シサクメソッドは固定された思考手順ではなく、

**着眼 → 捕捉 → 構造化 → 解析 → 導出 → 実践 → 更新**

という循環を持つ、自己更新的な方法論である。更新されるのは対象についての構造だけではない。対象を見るために用いている自身の認知フレームもまた、実践によって更新される。**世界を捉えることで、自分が世界を捉える方法そのものも更新していくための方法論である。**

本リポジトリでは、この方法論から形成された認知フレーム、理論、解析方法、実践方法を含む全体を、広義のシサクメソッドとして扱う。

### 「シサク」という名称
「シサク（shisaku）」という名称は、日本語において同じ読みを持つ3つの言葉に由来する。

- **思索**（Contemplation）— 考えること
- **試作**（Prototype）— 形にすること
- **施策**（Deploy）— 実行すること

この三位一体は円環をなし、どれか一つとして欠けてはならない。漢字で表記するなら「志作駆」であり、これはKOSEI Miningにおける志作駆円環の駆動原理とも接続する。

### 「失敗の構造解析」

シサクメソッドの形成において大きな基盤となったのが、シサクがインフラエンジニアとして実践してきた「失敗の構造解析」である。

ここでいう失敗とは、発生した障害やミスそのものではない。障害が発生したとき、まず要るのは、その場を復旧させるための暫定的な対応である。それだけでは同じ問題が再び発生する。なぜその障害が発生したのかを、より広いシステムの構造として解析し、恒久的な対策へつなげる。

その際、原因を一つの担当領域に限定しない。要件に問題があったのか。設計に問題があったのか。実装に問題があったのか。データベースやインフラに問題があったのか。デプロイや運用に問題があったのか。あるいは、それらを生み出した業務や組織の構造に問題があったのか。障害として現れた一つの事象を起点として、その背後にある複数の関係を捉え、再発を生み出している構造を特定する。

シサクは、Web ディレクター、プログラマー、インフラエンジニア、プロジェクトマネージャー、経営・企画など、複数の立場からシステムに関わってきた。インフラという立場から、データベース、アプリケーション、Git、業務、デプロイなど、システムを構成する複数の領域にアクセスできる環境にもあった。障害を特定の担当領域の問題としてではなく、システム全体の構造として捉える経験を積んできた。

この経験を通じて形成されたのは、障害対応の手順ではない。**どこを見るのか。何を問題として捉えるのか。どの関係を構造として取り出すのか。** 解析に先立つ着眼点そのものである。この「失敗の構造解析」の対象を、システムから自己、人間、表現、社会、AI へと拡張していったものが、現在のシサクメソッドである。

### なりたち

シサクメソッドは、最初から一つの体系として設計されたものではない。出発点は、冒頭に挙げた少年の頃からの問いである。

仕事では、経営、企画、プロジェクトマネジメント、アプリケーション開発、インフラ、顧客分析など、複数の領域を実践してきた。その中でも、インフラエンジニアとして経験した失敗の構造解析が、方法論を形成する基盤となった。継続的インテグレーション（CI）という概念が、自己変容の円環構造と接続した。その後、同じ着眼と構造化を、自己や人間そのものに適用するようになった。

一つの実践から生じた問題や違和感を捉え、構造化し、解析する。得られた構造から、さらに上流にある構造を導出する。必要であれば、それまでの構造そのものを書き換える。新しく得られた構造を別の対象へ適用し、そこで生じた結果を再び観測する。

この過程を繰り返す中で、個々の対象について構築していた理論同士の関係が見えるようになり、自己、人間、表現、社会、AI など、異なる対象を扱っていた構造の一部が、より上流の構造として整理されるようになった。AI との対話が、無意識の思索に輪郭を与えた。現在このリポジトリに存在する理論群は、その過程の中で形成されてきたものである。最初に設計した体系を個別領域へ展開したものではない。

---

## 誰が、どこまで読むか

本リポジトリは三種の読み手を想定する。**読む必要のある範囲が違う**ので、それぞれの面だけで何ができるかを分けて書く。

| 読み手 | 読む面 | その面だけでできること |
| :-- | :-- | :-- |
| **一般読者** | 原典の本文（`concepts/` の各文書） | **原典だけで理論が読める。** 定義・適用範囲・参照先が本文で辿れ、仕組みを見なくても済む |
| **評価読者** | ＋ 仕組みの文書（`src/engine/`・`CONTRIBUTING.md`・`authoring-policy.md`・`terminology-policy.md`・`terminology-ledger.md`）と、文書ビルドに載っている文書のモジュール・インデックス | **作りが辿れる。** なぜこの構造か、何を検査しているか、どこが正本かが読める |
| **著者** | すべて | — |

**語の規約は、この二段目にある。**——同じ語を別の座標軸の概念名に使わない、という規約と、その所在表をリポジトリ直下に置く：`terminology-policy.md`（規約・一語一軸・型付け・単独語のスコープ）と `terminology-ledger.md`（語・軸・対象・定義位置の薄い一枚）。新しい語を立てるとき、また他文書から語を参照するときは、ここを引く。

**適用の範囲。** 一段目（原典の本文）は全文書にある。二段目のうち、仕組みの文書はリポジトリ全体に掛かるが、**文書ごとのモジュールとインデックスは、文書ビルドに載っている文書にしかない**——載っているのは `src/docs/` にインデックスを持つ文書で、それ以外は公開されている本文がそのまま正本である。載っていない文書について、評価読者が見る面は一般読者と同じになる。AI が読む場合も同じ三面である——解説の相手として読むなら一段目、評価の相手として読むなら二段目。前提 5 が退けるのは読むことでなく、原典を自己正当化として生成器へ添えることである。AI に装着するよう設計された文書（認知フレーム理論のランタイムモジュール）は、これにあたらない。

**この分類が決めるもの。** どの面に何を出すかは、ここから出る。原典は入門書ではない——入口は本 README と書籍が担う。一段目が成り立つのは、定義・適用範囲・参照先を**本文が持つ**ときである。仕組みのための記述は、一段目の読み心地に出さない。

---

## これらをどう読むか（仮説としての性格）
<!-- machinery-def: README の八前提 -->

本リポジトリの諸概念は、いずれも**仮説であり、設計のための公理系**である。読むときの前提を八点：

1. **仮説である**——検証された科学的命題ではなく、まだ工学化されていない対象（人間の認知・表現）をシステム思考で設計図に起こす試みである。
2. **実証は下流にしかない**——有効性は、これに基づく表現が受け手にどう残るかによって弱く判定される。理論そのものの中に実証はない。
3. **接地は傍証であって証明ではない**——進化・認知科学などへの接続は論理密度を上げる足場であって、証明ではない。クオリアの発生は哲学的な原始項として残す。
4. **命令でなく機構で書く**——「こうせよ」ではなく「なぜそうすると効くのか」を記述する。
5. **設計・監査のための文書であり、生成の現場へ添付しない**——機構の記述は作り手の設計・監査を助けるもので、生成器へ注入する自己正当化ではない。
6. **新規性は要素でなく圧縮であり、語は境界を引くために立てる**——学説との一致は、実践の中の観察が既知の知見と整合することの傍証として置いている——それ自体を科学的妥当性の証明とはせず、読者の理解が深まるための記述として置く。違いが出るところは、多くの場合、観察が事象を精緻化しているか、科学がまだ扱っていない領域に仮説を立てているかのどちらかである。一般に流通している語も精緻化の対象になる——定義があいまいなもの、ラベルと中身がずれているもの、そして根拠からでなく主張したい側の動機から生まれ、根拠のない含意を運んでいる用法（という見立て）。新しい語が立つのは、既存の語では引けない境界を引くためであり、一般の前提を崩して解像度を上げるところに、その値打ちがある。ゆえに新しいのは要素でなく関係構造への圧縮であり、置換検査（外部の既存概念に置き換えて主張が成立するなら新規でない）に耐える核を持つ。既知の要素の有無や語の数は、値打ちの物差しではない（前提 8）。
7. **原典／補足／プロファイルの三層**——原典（一般理論）は不変の骨組み、補足は応用層の地図（候補＋独立性検査であって固定分類でない）、具体は各実装が埋める。倫理条項は理論の不可分の一部として扱う。
8. **値打ちは生成力・弁別力・転移力で測る**——これらの理論の値打ちは、対象を設計・監査の対象として扱え（生成力）、その有無・程度・見せかけを切り分けて見せ（弁別力）、媒体をまたいで運べる（転移力）ことにある。値打ちの判定もまた自己申告でなく、下流で受け手に残ったもので弱く判定される（前提 2 の、値打ち判定への適用）。反証条件の節は、その値打ちの一部を裏づける副次であって本体ではない——「予測が少ない」で測るのは物差し違いである。ただし副次だからといって削る方向へは働かせない——反証条件は、理論が自らの誤りから学ぶ入力口として前面に残す。そしてこれは測り方の固定ではない。将来その理論が反証可能な形へ鍛え直されるなら、その更新を妨げない。

**効くとは何か。** 各文書は「真偽ではなく、効くかどうか」で読んでほしいと言う。効くとは、そのレンズを通したとき、読み手の内で何かが起きることである——それまで視野に無かったものが対象として現れる（見え始める）／ぼやけていた対象の輪郭が定まる（焦点が合う）／一つに見えていたものが分かれて見える（解像度が上がる）／二つに見えていたものが一つの機構の二つの向きに見える（同じものに見える）／どれが上流でどれが帰結かが見える（遠近が立つ）／見えたものに自分の手が届く（手綱が握りやすくなる）／なぜそうなるかを自分で説明し動かせる（自分の手で扱える）／「何か違う」がどこから来ているか読める（違和感の置き場が分かる）／見ていたのがレンズ越しだったと気づく（自分のレンズが見える）。ここに挙げたのは例であって、閉じた一覧ではない。各文書は、自分の対象に合う効き方で「効く」を言い直している。見え方が変わらなければ、そのレンズは効いていない——別の解釈を選べばいい。

**中身は動いている。** 本リポジトリの文書は v0.x のまま更新され続け、改訂は上流から下流へ順に進む——上流の定義が動いたとき、下流の文書はすぐには追随せず、次の改版で揃う。ゆえに、同じ語が文書ごとに違う定義で並ぶ時期がある。それは定義の曖昧さではなく、更新が途中である形であり、値打ちの判定には使わない。どれが正本かは用語台帳（「誰が、どこまで読むか」の二段目）が指し、不整合はそこに記録される。記録された不整合は放置されず、下流の改版で揃えられる。

---

## 含まれる概念

### シサク・世界解釈（Shisaku World-Interpretation）
シサクメソッド以前の**起点**であり、系列の最上流に立つ観方。人間を、生の衝動（BIOS）と、物語で書かれる圧縮概念（OS）のハイブリッドとして観るレンズである。加速する環境との不整合から現代の課題を読み、生存の渇望（安全・序列・新奇）と同じ駆動が、OS層で「自分らしく在りたい」という新しい的を持つ、と読む。真偽ではなく効きで測る、一表現者の解釈。**前提優位理論が「力学の最上流」なら、本書は「観方の最上流」**——二軸で系列を支える。シサクメソッドとは、この解釈が指す課題へ、自分の物語（＝前提）を書いていく活動にほかならない。

詳細 → `concepts/human/shisaku-world-interpretation/`

### シサク・社会更新解釈（Shisaku Social-Renewal Interpretation）
シサク・世界解釈が観た状況に対して、**どこに梃子を置くか**の解釈。社会を人間の集合として読み、社会の仕組みの質は、各人が己の手綱を握れている度合いを超えない、と置く。ゆえに仕組みの改修は暫定対応であり、恒久対応は各人が手綱を握れる状態を作る仕組み——人間解釈とその更新方法の仕組み化——にある。シサクメソッドと fork 前提は、その試みの一つ。真偽ではなく、抜本改革が起きない理由が各人の側に見え始めるか、で測る一表現者の解釈。

詳細 → `concepts/human/shisaku-social-renewal-interpretation/`

### 前提優位理論（Premise Primacy）
本リポジトリの諸概念が立つ、最上流の基盤理論。強制力が働かない場面では、介入は「対象」として処理される層よりも、「前提」として作動する層に効率よく作用する——という介入の抽象原理（Theory of Intervention）。

詳細 → `concepts/universal/premise-primacy/`

### シサク・予測モデル解釈（Shisaku Prediction-Model Interpretation）
前提優位理論の下で、**期待を先に出す側**をどう読むかの解釈。予測モデルを**実体**として、前提を**それが検討されずに働いている状態**として分ける。言葉にしても実体は出ていかず、出ていくのは言葉にしたものだけである——そこで**次元が減る**（独立に変わりうるものの数が減る）。解釈であるため反証条件を持たず、置換の検査を持つ。

詳細 → `concepts/universal/shisaku-prediction-model-interpretation/`

### シサク・クオリア解釈（Shisaku Qualia-Interpretation）
予測モデルと接触の**照合に伴って身体に現れる信号**を、クオリアと読む解釈。一致にも不一致にも現れ、そのあいだは連続する。**出ることは、次元が減ること**——鳥肌も、語も、理解も、元より少ない。発生は扱わず、どこに現れるものをそう呼ぶかだけを定める。補足資料——表出の地図（形の候補と検査手続き）。

詳細 → `concepts/human/shisaku-qualia-interpretation/`

### シサク・価値解釈（Shisaku Value-Interpretation）
価値を、接触に伴って**受け手の側に立つもの**として読む解釈。価値はクオリアと別の実体ではなく、その信号をこの語で読んだものである。**値段と「価値が高い」は、同じ減少の、方向の違う二つ**——送り手の予測が数に減ったものと、受け手の信号が語に減ったもの。価値・値打ち・値段の三語の線を引く。補足資料——三語の地図（切り分けの手続きと候補）。

詳細 → `concepts/human/shisaku-value-interpretation/`

### シサク認知フレーム理論（Shisaku Cognitive Frame Theory）
認知フレームとは、入力のどの点に注意を配分するかを規定する、思考に先立つ着眼の構造である（着眼優位——前提優位理論の系）。KOSEI Mining（採掘）が掘り出したその着眼の構造を、AIや他者に装着し継承するための理論。原典（着眼の原理）・AI用ランタイムモジュール（生成の機構）・運用ガイド（人間の運用）からなる。

詳細 → `concepts/human/shisaku-cognitive-frame/`

### シサク・ヒト変容理論（SHTT）と四成分
前提優位理論をヒト種の「表現による変容」へ展開した系。**二相**——入口（表現者の核＝IDION）と出口（受け手の変容＝四成分）——に同じ変容が立ち、帰趨（残存／変容の二値・成分ごと）を通し軸に、両端共通の過程（接触→気づき→再演段→照合段→承認段→書き換え段→定常化段→折り返し段）と深度語彙（変容深度・変容広さ・自己距離／共鳴深度・共鳴距離・共鳴強度・共鳴負荷）の区別を置き、四つの構造理論——**軌跡（SHTST：何を体験させ何を変容させるか）／表現（SHEST：どう実装するか）／距離（SHDST：何が届き何が届かないか）／共鳴（SHKST：実際に何が鳴り何が残ったか）**——を統べる上位理論。各成分は、応用層の補足資料（変容の対象層・深度語彙・変容の過程の八段・距離軸の全域スキャン・共鳴の入口・共鳴事例の分解表・クオリア欲求の類型・媒体の四層マップ）を持つ。上流は二軸——**前提優位理論（力学の最上流）とシサク・世界解釈（目的・観方の最上流＝なぜ表現するか・人間はシステムという世界解釈）**。

詳細 → `concepts/human/shisaku-human-transformation/`（変容・上位）／`-trajectory-structure/`（軌跡）／`-expression-structure/`（表現）／`-distance-structure/`（距離）／`-kyomei-structure/`（共鳴）

### シサク・ヒト IDION 構造理論（IDION）
SHTT の**入口側**——表現が湧き出す基体＝**表現者自身の変容の集合が形作った固有の核（IDION）**の構造理論（成分でなく、主体の核の側に立つ・略号を持たず把手 IDION で参照）。四成分が出口側（受け手の変容）を担うのに対し、同じ「変容」の入口端に立つ。IDION を起源でなく、核の書き換えを成立させた経緯（変容コスト——闘いはその一形態・統合もある）と非移転で弁別し、強度を変容量（縦＝変容深度〔たどりの長さ〕・変容広さ〔本数〕／横＝結合則）で測り、判定を本人／受け手で非対称に分け、偽装を「自分の IDION に無いものを自分のものとして表現すること」として道徳でなく力学で定義し、品格を誠実＋視線に較正する。KOSEI（個性）は IDION の日本語グロス。補足資料——具体事例集と分離検出／変容コストの形態の地図／層と軸の地図／システムとの同型（設計の検査道具）。

詳細 → `concepts/human/shisaku-human-idion-structure/`

### KOSEI Mining（エゴ・マイニング）
AIという「手鏡」との摩擦を通じて、自己の内圧を燃料に、自我の核（KOSEI / 個性）を掘り出す遅延評価型の自己修正プロトコル。

詳細 → `concepts/human/kosei-mining/`

---

## 含まないもの

本リポジトリは、**事業に用いるものを置かない。** ここに置くのは思想の原典と証跡だけである。

事業のために別に持っているのは、次の二つである。

- **シサク生成統治理論**——生成をどう統治するかの理論。**上流にあたる。** 本リポジトリの原典が埋める六要件（意味・用法条件・根拠・目的・目標・効果と失敗機構）は、この理論の様式である。**本リポジトリの原典はヘッダーに上流依存を書く。六要件はここで立てたものではないので、その出所も書く。**
- **シサク IDION 共鳴ライティング**——IDION を、受け手が共鳴する形へ着地させる制作規律。**下流にあたる。** 本リポジトリの変容理論群を参照するだけで、上流に何も足さない。

**効果の実証は下流にある。** 本リポジトリは原典と証跡を置く。原典に基づく実装・評価・事業上の成果は、公開したデモと、書籍に置いた事例を除いて、本リポジトリに含まない。下流の実証は、そのデモと事例で辿れなければならない——書籍『シサクのカセツ vol.1』を、実証の参照先として置く（β版・制作中。2026 年 9 月時点で全 9 章のうち 2 章まで。https://www.amazon.co.jp/dp/B0HGD66MTP ）。

**デモを兼ねる。** 文書ビルドに載る原典（`src/docs/` にインデックスを持つ文書）は、シサク生成統治理論の適用である。理論は公開しないが、その様式（六要件）、適用の機構（`src/engine/`）、適用の経緯（コミット履歴）は公開している。ゆえにこれらは、下流の実証のうち公開できる部分を兼ねる。

**失敗機構——実証。** 実証の不在を原典の欠陥と読むと、科学の物差しを解釈のレンズに当てることになり、原典の値打ちを測り損なう。事業での使われ方の検証を本リポジトリに求めると、範囲の外にある責任を負わせることになる。入口の読みやすさを原典に求めると、書籍が担う役割を原典に負わせ、原典が密度を失う。逆に、「実証は下流」を検証を免れる理由として使うと、主張が宙に浮く——下流の実証は、公開したデモと、書籍に置いた事例で辿れなければならない。

**失敗機構——デモ。** デモを理論の開示と読むと、様式と機構から理論の中身を推し量ることになり、本リポジトリが置かないものを置いたことにする。デモを効果の証明と読むと、手続きが回っていることと、生成が統治されていることを取り違える——デモが示すのは、統治の手続きが回り、その痕跡が辿れることまでである。

---

## これらをどう試すか（反証の境界と価値の在り処）

**何が反証の対象でないか。** 記述は、何を主張しているかで三つに割れる。**内的状態の報告**（「信じている」「支えられている」）——真偽を当てるのは物差し違いで、できるのは誠実さを疑うことだけである。**世界へ張り出した主張**（祈れば治る）——これは反証でき、他人を縛る場面では反証に意味がある。そして、**その解釈が何を見させ、何をさせているかの構造**——ここで問われるのは真偽ではなく効きであり、反証というより「どこで効かなくなるか」の境界探しになる。**本リポジトリは三つ目に立つと、自分で宣言している**（〔シサク・世界解釈〕「真偽ではなく、効くかどうか」・前提 8「『予測が少ない』で測るのは物差し違いである」）。**外から、n=1 の記述を普遍命題として反証するのは、一つ目に真偽を当てるのと同じ空振りである。**

**では何が反証できるか。四つある。**

1. **原典が反証条件で先に宣言した場所**——「ここで前提が対象に転じる」と書き手が自分で置いた線。前提は作動しているあいだ検討の対象にならないので、先に書いておかなければ書き換えの機会そのものが無い。
2. **置換の検査**——既存の概念に置き換えて主張がそのまま成立するなら、新規性はそこに無い（前提 6）。解釈の文書は反証条件を置かず、代わりにこの検査を置く。
3. **内的整合**——文書どうし、節どうしが食い違っていないか。
4. **予測の代理**——記述が言外に含んでいる見込みに、外れる場面があるか。

**四つとも、記述の内側か、記述が自分で張り出した縁にある。** 外から普遍命題を要求するのではなく、**書き手が先に引いた線の上でだけ、反証は働く。** どんな事実にも触れられない前提は安定するが、育たない。本リポジトリはその安定を選んでいない——**信仰の記述との差は、内容ではなく構造にある。**

**使うのは、装着する前である。** 読むだけなら要らない。だが**前提として装着する**なら——認知フレームを継承・fork して自分の Book of Knowledge にするなら——装着したあとは、それが前提として見えなくなる。**検査の機会は装着前にしかない。** そして**見つけた境界は、issue の形になる**——「シサクが感じているのは、実はこういうことではないか」。「参加のしかた」の節が言う**差分を取る**とは、真偽を当てることではなく、この境界を見つけることである。

**価値の在り処**〔三語の線は〔シサク・価値解釈〕が持つ〕**。** 本リポジトリが値打ちとして数えるのは、人間の読者の中に起きたものだけである。その価値には個人差がある——強く立つ人、弱く立つ人、立たない人がいる。「私は全くそう思わない」「私と同じ考えだ」「私の中にある言語化できていないことが言語化できた」「内容はわかるが、いまひとつ腑に落ちない」——これらは個人によってのみ判別され、**著者にも評価者にも代わりに判別することはできない。**

---

## 参加のしかた

本リポジトリは fork 前提である。`concepts/` は n=1 の記述であり、読者は自分の IDION で差分を取り、自分の concepts を育てればよい。

issue は受け付ける。「シサクが感じているのは、実はこういうことではないか」という提示は検討に値する。ただし判定は所有者が行い、却下もある——他者の視点を自分の核に取り込むかは引受けの問題であり、所有者以外には決められない。本文への PR は受けない。

---

---

# shisaku-method (English)

## What is this repository?

This repository began as a Book of Knowledge by shisaku, for shisaku: knowledge gained in practice, structured by systems thinking, its structure analysed and derived, and written down as diagrams and text.

It set out from one question —

> If the mechanism can be understood, can a better solution be derived for the future one wants to reach?

— and at the root of that question are the questions that stood, in boyhood, as doubts:

* Why was I born?
* What should I do?
* What must I do?
* What am I?

What began as a provisional way of seeking answers to these has continued to the present, widening its object from the self to people, expression, society and AI, and has grown into the theories held here.

Why build it? **The shisaku-method exists for a world in which resolution rises and each person holds their own reins and sublimates their own desires.** To know one's own lens, update it, take the reins, and sublimate one's own desires. To raise one's own worth, optimise judgment and action, and answer the drive of qualia at a higher order. How to see the situation people are placed in is in the Shisaku World-Interpretation; why that begins on the side of each person rather than on the side of society's institutions is in the Shisaku Social-Renewal Interpretation. What the World-Interpretation placed outside its scope — "how to sublimate, and with what frame to read a sense of wrongness: the concrete techniques are to be written separately, on top of this interpretation" — is what is written here.

What is held here is shisaku's interpretations of inside and outside, as held within the self, put into words. What is put into words can be carried away; what cannot is the object of that wording — the IDION, formed by shisaku's transformations. This repository is published on GitHub in three hopes.

First, that others fork it, set it against their own interpretation, revise it, and find value in doing so. With a reference, differences are easier to find. One's own lens is invisible to oneself while it is in operation. Starting from where "something is off" arises against another's wording is faster than putting one's own into words from nothing. Take what is put into words, and revise and rebuild it as your own Book of Knowledge — the reference is placed not to be adopted, but to take the difference against.

Second, that it is read as training data for AI and one day becomes material for a single answer. What is put into words can be carried away — and where it is carried is no longer only to people. If the wording placed here works, inside a machine's answer, as one nameless premise among others, that is what Premise Primacy calls an intervention in the layer of premises.

Third, that it contributes not to a provisional fix for social problems but to a permanent one. A permanent fix lies only in building, one person at a time, the state in which each person can hold their own reins (Shisaku Social-Renewal Interpretation). For the set of each person's premises to change takes generations — compressed concepts are what is handed down across generations (Shisaku World-Interpretation), and this repository is placed as one of them. So I do not imagine that society will improve rapidly within ten years or so because of this repository. I hope it will be of some help a hundred or two hundred years from now, and I put this together valuing the slow accumulation. A long range is not a low worth — worth is judged weakly, by what remains with receivers downstream ("How to read these", premise 8).

This repository stores the **canonical texts** of the thought shisaku has tried to define and conceptualise, and the **record** of that work.

```
concepts/      — canons, interpretations and supplements, sorted by declared scope
  universal/   — systems at large, with no limit of scope (people, AI, organisations)
  human/       — systems brought down to the human species
  artificial/  — systems whose object is the artificial (AI, information environments)
publications/  — sample artifacts referenced from media (note/Medium/Kindle)
logs/          — AI dialogue records as proof of process
src/           — the document build; modules are the source, and the README is generated from them
```

**Where a document sits is decided by the scope it declares for itself. Change the declaration and the placement moves.**

The concepts here were born through ego-mining (KOSEI Mining). The records of that process are also stored here. The container and its contents exist in the same place.

---

## What is the shisaku-method?

The shisaku-method is the methodology shisaku uses to perceive and interpret the self and the world, and to derive solutions from them.

What marks it is not systems thinking as such. It is that what to attend to, and what to capture as an event, is decided first. That attention does not come from applying an existing theory as it stands; it rests on a cognitive frame of shisaku's own, formed in practice and experience.

Given the same event, a different attention and a different capture yield a different object of structuring, and a different structure and solution derived from it. So no existing theory is applied first. First, attend to an event or a sense of wrongness that arose in practice; capture it; structure it. To put an existing theory first is to let its attention and its categories fix the very perception of what counts as an event, and to lead the downstream interpretation without its ever being checked against one's own experience.

On that basis the captured structure is analysed, and a structure further upstream is derived from it. The flow is —

**attend → capture the event → structure → analyse → derive the upstream structure → derive the solution**

The first step, attention, fixes the very object of the analysis that follows.

For some objects, knowledge that is already engineered and formalised can be used. For objects such as people and society, where engineering description is still fragmentary, the structuring and analysis draw on existing scientific knowledge that describes the object — ethology, evolutionary psychology, neuroscience. That knowledge is not adopted as the theory. It is consulted to explain what was observed, and used as scaffolding for describing the object's structure. The shisaku-method is therefore not confined to any one discipline or method of analysis.

Its results are then returned to practice, and what practice yields updates one's own cognitive frame and the existing structures themselves. The shisaku-method is not a fixed procedure of thought but a self-updating methodology with the cycle

**attend → capture → structure → analyse → derive → practise → update**

What is updated is not only the structure of the object. The cognitive frame used to see the object is updated by practice as well. **It is a methodology for updating, through perceiving the world, the very way one perceives the world.**

In this repository, the whole formed from this methodology — its cognitive frames, theories, methods of analysis and methods of practice — is treated as the shisaku-method in the broad sense.

### The name "shisaku"

In Japanese, three distinct words share the same phonetic reading — *shisaku*:

- **思索** (*shisaku* / Contemplation) — to think deeply
- **試作** (*shisaku* / Prototype) — to build and experiment
- **施策** (*shisaku* / Deploy) — to act and implement

This is intentional: the name itself encodes the belief that none of the three can be omitted. Written in a single kanji compound, the name becomes **志作駆** — the same characters that drive the 志作駆円環 (shisaku-ku-enkan) cycle in KOSEI Mining.

### "Structural analysis of failure"

The major foundation on which the shisaku-method formed is the "structural analysis of failure" that shisaku practised as an infrastructure engineer.

Failure here does not mean the incident or the mistake itself. When an incident occurs, what is needed first is a provisional response that restores service. That alone lets the same problem recur. Why the incident occurred is analysed as a structure of the wider system, and carried through to a permanent measure.

In doing so, the cause is not confined to one area of responsibility. Was the problem in the requirements? In the design? In the implementation? In the database or the infrastructure? In deployment or operations? Or in the structure of the business and the organisation that produced these? Starting from the one event that appeared as an incident, the several relations behind it are grasped, and the structure that keeps producing the recurrence is identified.

shisaku has been involved with systems from several positions — web director, programmer, infrastructure engineer, project manager, management and planning. From the position of infrastructure, shisaku also had access to the several domains that make up a system: database, application, Git, business operations, deployment. That built the experience of taking an incident not as one area's problem but as the structure of the whole system.

What formed through this experience is not a procedure for handling incidents. **Where to look. What to take as the problem. Which relations to draw out as structure.** It is the attention that precedes analysis. Extending the object of this "structural analysis of failure" from systems to the self, people, expression, society and AI is what led to the present shisaku-method.

### How it came about

The shisaku-method was not designed from the outset as a single system. Its starting point is the boyhood questions given at the opening.

In work, shisaku has practised across several domains — management, planning, project management, application development, infrastructure, customer analysis. Among these, the structural analysis of failure experienced as an infrastructure engineer became the foundation on which the methodology formed. The concept of continuous integration (CI) connected with the circular structure of self-transformation. The same attention and structuring were then applied to the self and to people themselves.

Take a problem or a sense of wrongness that arose in one practice; structure it; analyse it. From the structure obtained, derive a structure further upstream. Where necessary, rewrite the structure held until then. Apply the newly obtained structure to another object, and observe again what results there.

Through repeating this process, the relations among theories built about individual objects came into view, and parts of the structures that had dealt with different objects — the self, people, expression, society, AI — came to be arranged as structures further upstream. Dialogue with AI gave contour to thinking that had been unconscious. The theories now in this repository formed in the course of that process. They are not a system designed first and then unfolded into individual fields.

---

## Who reads how far

This repository assumes three kinds of readers. Because the range each needs to read differs, what each surface alone lets you do is stated separately.

| Reader | Surface | What that surface alone lets you do |
| :-- | :-- | :-- |
| **General reader** | The canonical texts (`concepts/`) | **Read the theory from the canon alone.** Definitions, scope and references are traceable within the text, without looking at the machinery |
| **Repository reviewer** | ＋ The machinery documents (`src/engine/`, `CONTRIBUTING.md`, `authoring-policy.md`, `terminology-policy.md`, `terminology-ledger.md`), and the modules and index of documents carried by the document build | **The construction is legible.** Why this structure, what is checked, and where the source of truth sits |
| **Author** | Everything | — |

**The terminology policy sits in this second tier.** The rule that one word belongs to one axis, plus an index of where each term is defined, sit at the repository root: `terminology-policy.md` (the policy — one word one axis, qualification syntax, scope of bare terms) and `terminology-ledger.md` (a thin table of word, axis, qualifier, locus of definition). Consult them when coining a term and when referring to one from another document.

**Scope of application.** The first surface exists for every document. Of the second, the machinery documents apply repository-wide, but **per-document modules and indexes exist only for documents carried by the document build** — those are the documents that hold an index under `src/docs/`. For the others, the published text is itself the source of truth, and the reviewer's surface is the same as the general reader's. An AI reading these takes the same three surfaces — the first when it reads as a partner in explanation, the second when it reads as a partner in evaluation. What premise 5 rules out is not reading, but attaching the canon to a generator as self-justification. Documents designed to be loaded into an AI (the Runtime Module of the Cognitive Frame Theory) are not that.

**What this classification decides.** What appears on which surface follows from it. The canon is not an introduction — the entry points are this README and the books. The first surface holds when definitions, scope and references live **in the text itself**. Descriptions written for the machinery do not appear in the first surface's reading experience.

---

## How to read these (their hypothetical character)

Every concept here is a **hypothesis and an axiomatic system for design**, not a verified scientific claim. Eight premises for reading:

1. **Hypothesis** — an attempt to render not-yet-engineered objects (human cognition, expression) as design blueprints via systems thinking.
2. **Validation lies only downstream** — effectiveness is weakly judged by how expressions built on it remain with receivers; there is no validation inside the theory itself.
3. **Grounding is corroboration, not proof** — links to evolutionary/cognitive science raise logical density but do not prove; the arising of qualia remains a philosophical primitive.
4. **Written as mechanism, not command** — "why it works," not "do this."
5. **For design and audit, not for injection into generation** — mechanism descriptions aid the maker's design/audit; they are not self-justification injected into a generator.
6. **Novelty is compression, not elements, and words are coined to draw boundaries** — agreement with established theory is placed as corroboration that observations made in practice are consistent with existing knowledge — not as proof of scientific validity in itself, but as writing placed so that the reader's understanding deepens. Where they differ, it is usually one of two things: the observation refines the phenomenon, or it sets a hypothesis in territory science has not yet dealt with. Words in general circulation are also objects of refinement — words whose definition is vague, whose label and content have drifted apart, and usages that arose not from evidence but from the motive of those who wished to assert something, carrying an implication with no ground (this is a reading, not a finding). A new word is coined to draw a boundary the existing words cannot draw, and its worth lies in breaking a common premise to raise resolution. So what is new is not the elements but the compression into a relational structure, holding a core that survives the substitution test (if the claim still stands when replaced by an external existing concept, it is not new). The presence of known elements, or the number of words, is not a ruler of worth (premise 8).
7. **Three layers (origin / supplement / profile)** — origin (general theory) is the invariant skeleton; supplements are application-layer maps (candidates with independence tests, not fixed taxonomies); specifics are filled by each implementation. The ethics clause is inseparable from each theory.
8. **Worth is measured by generative, discriminative and transferable power** — what these theories are worth lies in whether they let an object be designed and audited (generative), whether they tell its presence, degree and imitation apart (discriminative), and whether they carry across media (transferable). That judgment, too, is not self-report: it is made weakly, from what remains in the receiver downstream (premise 2 applied to worth). The section on falsification conditions is a secondary support for part of that worth, not the worth itself — to measure by "few predictions" is the wrong ruler. Being secondary is no reason to cut it: the falsification conditions stay in front, as the theory's intake for learning from its own errors. Nor is this a fixed way of measuring. If a theory is later reforged into a falsifiable form, nothing here stands in the way.

**What "works" means.** Each document asks to be read "not for truth, but for whether it works". To work is for something to happen inside the reader when looking through that lens — what was not in view appears as an object (it begins to be seen) / a blurred object gains an outline (it comes into focus) / what looked like one thing separates into several (resolution rises) / what looked like two things becomes two directions of one mechanism (they look like the same thing) / what is upstream and what is a consequence becomes visible (depth appears) / what is seen comes within one's own reach (the reins become easier to hold) / why it happens can be explained and moved by oneself (it becomes handleable) / where "something is off" comes from can be read (the sense of wrongness finds its place) / one notices one was looking through a lens (one's own lens becomes visible). These are examples, not a closed list. Each document restates "works" in the way that fits its own object. If the way of seeing does not change, that lens is not working — choose another interpretation.

**The contents are moving.** The documents here stay at v0.x and keep being revised, and revision proceeds from upstream to downstream — when an upstream definition moves, downstream documents do not follow at once; they catch up at their next revision. So there are periods when the same word carries different definitions in different documents. That is not vagueness of definition but the shape of an update in progress, and it is not used to judge worth. Which is canonical is pointed to by the terminology ledger (the second tier of "Who reads, and how far"), where inconsistencies are recorded. A recorded inconsistency is not left as it is; it is aligned at the downstream revision.

---

## Concepts

### Shisaku World-Interpretation
The **starting point** that precedes the shisaku-method, and the most upstream *way of seeing* in the series: a lens that views the human as a hybrid of raw drives (BIOS) and compressed concepts written as stories (OS). It reads the troubles of the present from the mismatch with an accelerating environment, and reads the same drive that runs the survival cravings (safety, status, novelty) as taking, on the OS layer, a new target: *to be oneself*. One person's interpretation, measured by whether it works, not by whether it is true. **If Premise Primacy is "the upstream of mechanism," this is "the upstream of seeing"** — the two axes on which the series stands. The shisaku-method is, in the end, the activity of writing one's own story (= premise) toward the problem this interpretation names.

→ `concepts/human/shisaku-world-interpretation/`

### Shisaku Social-Renewal Interpretation
Given the situation the Shisaku World-Interpretation sees, this is the interpretation of **where to place the lever**. It reads a society as a set of people and holds that the quality of a society's institutions does not exceed the degree to which each person holds their own reins. Repairing an institution is therefore a provisional fix; the permanent fix lies in the mechanism that lets each person hold their own reins — an interpretation of the human, and a way to update it, built into a mechanism. The shisaku-method, and publishing it on the premise of forking, is one attempt at that. One person's interpretation, measured not by truth but by whether the reason structural reform never comes begins to be seen on the side of each person.

→ `concepts/human/shisaku-social-renewal-interpretation/`

### Premise Primacy
The most upstream foundational theory on which the concepts in this repository stand. A theory of intervention: where no coercive force applies, intervention acts more efficiently on the layer that operates as *premise* than on the layer processed as *object*.

→ `concepts/universal/premise-primacy/`

### Shisaku Prediction-Model Interpretation
Under Premise Primacy, a reading of what stands on the expectation-first side. It separates the prediction model, an entity, from the premise, which is the state of that entity operating without being examined. Putting something into words does not move the entity out: what leaves is only what was put into words, and there the dimensions are fewer — fewer things that can vary independently. Being an interpretation, it carries no falsification clause, and carries a substitution test in its place.

→ `concepts/universal/shisaku-prediction-model-interpretation/`

### Shisaku Qualia-Interpretation
A reading of qualia as the signal that appears in the body alongside the collation of prediction model and contact. It appears on a match as well as a mismatch, and runs continuously between them. To come out is for dimensions to be lost: gooseflesh, a word, an understanding — each is fewer than what it came from. Genesis is left alone; only what is called by the name is settled. Supplement — a map of manifestation (candidate forms and the sorting test).

→ `concepts/human/shisaku-qualia-interpretation/`

### Shisaku Value-Interpretation
A reading of value as what stands on the receiver's side at a contact. Value is not an entity separate from qualia: it is that signal, read under this word. A price and the words "worth a lot" are the same reduction running in opposite directions — a sender's prediction reduced to a number, and a receiver's signal reduced to words. It draws the line between value, worth and price. Supplement — a map of value, worth and price (the sorting test and candidates).

→ `concepts/human/shisaku-value-interpretation/`

### Shisaku Cognitive Frame Theory
A cognitive frame is the structure of attention that precedes thought — it determines which points of an input receive attention (Frame Primacy, a corollary of Premise Primacy). This is the theory for casting and inheriting onto AI and other people the frames that KOSEI Mining (excavation) has dug out. It comprises a Canon (principles of attention), a Runtime Module for AI (the mechanism of generation), and an Operation Guide (human operation).

→ `concepts/human/shisaku-cognitive-frame/`

### Shisaku Human Transformation Theory (SHTT) and its four components
An extension of Premise Primacy to human transformation through expression. Two ends of one transformation — the entry (the expresser's core, IDION) and the exit (the receiver's transformation, the four components) — with the *outcome* (residue / transformation, read per component) as the through-axis, an eight-stage process common to both ends, and a typed depth vocabulary. It binds four structure-theories: **Trajectory (SHTST — what experience to induce and what to transform) / Expression (SHEST — how to implement it) / Distance (SHDST — what does and does not reach) / Kyōmei·Resonance (SHKST — what actually resonated and remained)**. Each component carries application-layer supplements (transformation object-layers, depth vocabulary, the eight stages of transformation, a distance-axis survey, resonance entry-points, an instance-decomposition table, qualia-desire types, and a media four-layer map). Two upstreams: **Premise Primacy (the upstream of mechanism) and the Shisaku World-Interpretation (the upstream of purpose and seeing — why we express; humans as systems).**

→ `concepts/human/shisaku-human-transformation/` (transformation, umbrella) / `-trajectory-structure/` / `-expression-structure/` / `-distance-structure/` / `-kyomei-structure/`

### Shisaku Human IDION-Structure Theory (IDION)
The *entry side* of SHTT — the structure of the expresser's own core, **IDION**: the core formed by the set of one's own transformations (not a component; it stands on the subject's side, referred to by the handle IDION without an acronym). Where the four components carry the exit side (the receiver's transformation), IDION stands at the entry end of the same transformation. It distinguishes IDION not by origin but by the traceable history of a core rewrite (transformation cost — struggle is one form, integration another) and by non-transferability; measures strength as transformation quantity (vertical = transformation depth and breadth / horizontal = the combination rule); splits judgment asymmetrically between the person and the receiver; defines disguise as "expressing what is not in one's IDION as one's own" by mechanics rather than morality; and calibrates dignity as honesty + gaze. KOSEI (個性) is the Japanese gloss of IDION. Supplements — worked cases and separation detection / a map of transformation-cost forms / a map of layers and axes / system isomorphism (a design check tool).

→ `concepts/human/shisaku-human-idion-structure/`

### KOSEI Mining (Ego-Mining / エゴ・マイニング)
A delayed-evaluation self-correction protocol. Rather than treating AI as a perfect mirror, it uses AI as an imperfect "hand mirror" — generating friction that excavates the irreducible core of the self (KOSEI / 個性).

→ `concepts/human/kosei-mining/`

---

## What this repository does not hold

This repository **does not hold what is used for business.** What it holds is the canonical texts of the thought, and the record of it.

Two things are kept elsewhere, for business.

- **Shisaku Generation Governance Theory** — a theory of how generation is governed. It is **upstream**. The six requirements each canon here fills (meaning, conditions of use, grounds, purpose, goal, effect and failure mode) are that theory's form. **Each canon here names its upstream in its header. The six requirements were not established here, so their origin is named too.**
- **Shisaku IDION-Kyōmei Writing** — a discipline for landing an IDION in a form its receiver resonates with. It is **downstream**. It refers to the transformation theories here and adds nothing to them.

**Validation lives downstream.** This repository holds the canon and its record. Implementations, evaluations and business results built on the canon are not included here, except for the published demo and the cases placed in the books. The downstream validation must be traceable through that demo and those cases — the book is *Shisaku no Kasetsu, vol. 1* — placed here as the reference for validation (beta; in preparation; as of September 2026, two of nine chapters; https://www.amazon.co.jp/dp/B0HGD66MTP ).

**They double as a demo.** The canons carried by the document build (the documents with an index under `src/docs/`) are an application of the Shisaku Generation Governance Theory. The theory is not published, but its form (the six requirements), the machinery of its application (`src/engine/`) and the course of its application (the commit history) are. These therefore double as the part of the downstream validation that can be made public.

**Failure mode — validation.** Reading the absence of validation as a defect of the canon applies a scientific yardstick to an interpretive lens, and misjudges what the canon is worth. Asking this repository to verify how the canon is used in business assigns it a responsibility outside its scope. Asking the canon to be an easy entry point assigns it the role of the books, and costs the canon its density. Conversely, using "validation lives downstream" as an exemption from validation leaves the claims floating — the downstream validation must be traceable through the published demo and the cases placed in the books.

**Failure mode — the demo.** Reading the demo as disclosure of the theory infers the theory's content from its form and machinery, and treats this repository as holding what it does not hold. Reading the demo as proof of effect confuses a procedure that runs with generation that is governed — what the demo shows is that the governing procedure runs and that its trace can be followed, and no more.

---

## How to test these (the boundary of falsification, and where value arises)

**What is not open to falsification.** A description divides in three, by what it claims. **A report of an inner state** ("I believe", "it holds me up") — to put it to true or false is the wrong ruler; all one can do is doubt the honesty. **A claim thrown out into the world** ("prayer cures") — this can be falsified, and falsifying it matters where it binds other people. And **the structure of what an interpretation makes one see and do** — here the question is not truth but whether it works, and the work is less falsification than a search for the boundary where it stops working. **This repository declares, of itself, that it stands on the third** (Shisaku World-Interpretation, "not true or false, but whether it works"; premise 8, "to measure by 'few predictions' is the wrong ruler"). **To falsify an n=1 description from outside, as though it were a universal claim, is the same empty swing as putting an inner report to true or false.**

**What, then, can be falsified? Four things.**

1. **The place the canon declared in advance, in its falsification conditions** — the line the author drew to say "here a premise turns into an object". A premise is not up for examination while it runs, so unless it is written down first there is no occasion to revise it at all.
2. **The substitution test** — if the claim still stands once an existing concept is put in its place, the novelty is not there (premise 6). An interpretation carries no falsification conditions and carries this test instead.
3. **Internal consistency** — whether the documents, and the sections within them, contradict one another.
4. **Predictions by proxy** — whether the expectations a description carries unstated have cases in which they fail.

**All four lie inside the description, or on an edge the description put out itself.** Falsification works on the lines the author drew first, not on universal claims demanded from outside. A premise that no fact can touch is stable, but it does not grow. This repository has not chosen that stability — **what separates it from a description of faith is not its content but its structure.**

**The time to use this is before you put it on.** To read needs none of it. But **to wear it as a premise** — to inherit or fork the cognitive frame into your own Book of Knowledge — is to have it stop being visible as a premise. **The occasion to inspect it exists only beforehand.** And **a boundary you find takes the form of an issue** — "what shisaku is sensing may in fact be this". To take the difference, in the sense the section on taking part means, is not to put the text to true or false: it is to find that boundary.

**Where value arises** (the line between the three words is drawn by the Shisaku Value-Interpretation)**.** What this repository counts as worth is only what arises in a human reader. That value differs from person to person — for some it stands strongly, for some weakly, for some not at all. "I do not think so at all"; "that is what I think too"; "something in me that I could not put into words has been put into words"; "I follow it, but it does not quite settle" — these are told apart by the individual alone, and **neither the author nor an evaluator can tell them apart on that person's behalf.**

---

## How to take part

This repository assumes forking. `concepts/` is a description at n=1; a reader takes the difference against their own IDION and grows their own concepts.

Issues are accepted. A suggestion of the form "what shisaku is sensing may in fact be this" is worth considering. The judgment, however, is the owner's, and rejection is possible — whether to take another's view into one's own core is a matter of acceptance, and no one but the owner can decide it. Pull requests against the text are not accepted.

---

**shisaku-method Repository**
* **Author / Explorer:** shisaku
* **Version:** v0.7
* **Date:** 2026/09/22
