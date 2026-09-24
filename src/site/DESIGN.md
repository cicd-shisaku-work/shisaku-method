# シサクメソッド公開サイト・ビルド設計書（src/site）

**Version:** v0.1
**Date:** 2026/09/23
**性格：** `shisaku-method` リポジトリの `README.md` と `concepts/**` を、静的サイトとして S3 に公開する道具の設計仕様。実装する者が、この文書だけを読んで着手できることを合格条件とする。
**範囲：** 本書は道具の設計だけを扱う。運用の手順は `OPERATIONS.md`。AWS 側の設定（バケット・IAM・EventBridge・証明書・CDN・DNS）は本書の外。

---

## 0. この道具は何か

`concepts/**/*.md`・`README.md`・`concepts/**/figures/*.svg` を入力に、ナビゲーション付きの HTML と付随資産（CSS・共有画像・sitemap 等）を生成し、S3 に配置する静的サイトジェネレータ。

**既存エンジン（`src/engine/build.py`）の延長ではない。** エンジンは `src/docs/` のモジュール化済み文書だけを扱うが、`concepts/` の大半は手書きで未モジュール化である。ゆえに本道具は：

- 入力を **リポジトリにある `.md`／`.svg` ファイルそのもの** とする（モジュール由来か手書きかを問わない）。
- 文書の発見を **ファイルシステムの走査** で行う（`index.toml`／`paths.toml` に依存しない）。
- `src/docs`・`src/engine` には触れない。独立の道具として `src/site/` に置く。

**目的：** GitHub のままでは人間が原典群をたどりにくい。第一に、**人間が読み・概念単位で回遊できる**サイトを独自ドメイン下に作る。第二に、クロールされやすい HTML として露出し、ドメインを育てる（SEO 資産）。主眼は、一次＝**概念単位の回遊（ナビゲーション）**、二次＝**クロール可能性（SEO）**。

---

## 1. 全体像と原則

```
concepts/**/*.md          ──┐
README.md                 ──┼─→  build_site.py  ─→  出力（生成物・コミットしない）  ─→  deploy（boto3）─→ S3
concepts/**/figures/*.svg ──┘        ↑
                        環境変数（BASE_URL / GA_MEASUREMENT_ID / SOURCE_REPO / …）をビルド時に読む
                        共有画像用フォント（パッケージに同梱・§9.1）

  日次： EventBridge → Lambda（tarball 取得 → 生成 → 品質関門 → S3 同期）
```

原則：

- **正本はリポジトリの `.md`／`.svg`。** 出力は生成物であり、コミットしない。既定の出力先は `dist/`。CI と Lambda はリポジトリ外の一時ディレクトリに出力する。
- **配備に固有の値をリポジトリに置かない。** 取得元リポジトリ・ドメイン・GA 測定 ID・S3 バケット・CloudFront ID は、すべて**環境変数**で与える（§8）。本書とコードが持つのは変数の**名前と意味だけ**で、値はコードにも設定ファイルにも書かない。
  - 目的は秘密の保護ではない（ドメインも GA ID も公開 HTML に出る）。**フォークした人が、コードを編集せずに自分の配備で使える**ようにするためである。
  - Lambda の環境変数は秘密の置き場ではない。本当の秘密（取得元を非公開にしたときのトークン等）が生じたら、SSM Parameter Store／Secrets Manager に置く。
- **生成は準決定的。** 本文・構造・共有画像は同入力→同出力。唯一の例外はフッタの**生成日時**で、これは毎日変わる。日次で全ページ（HTML）が再アップロードになるが、サイトは小さいので許容する。共有画像（PNG）は日時を含まないので、題が変わらなければ再アップロードされない。

責務分割：

```
src/site/
├── DESIGN.md / OPERATIONS.md
├── build_site.py            # 入口：CLI（生成のみ・§10）
├── lambda_handler.py        # 入口：Lambda（取得 → 生成 → 関門 → 配置）
├── fetch_fonts.py           # 入口：共有画像用フォントの取得（パッケージ作成時・CI）
├── requirements.txt         # 外部依存（版を完全固定）
├── sitebuild/
│   ├── config.py            # 入口で読んだ環境変数・引数をまとめた設定
│   ├── rules.py             # 規則をデータとして一か所に（§16.3）
│   ├── fetch.py             # tarball の取得・安全な展開・コミット SHA の取り出し
│   ├── discover.py          # 走査：対象概念・文書・図版の発見
│   ├── model.py             # 発見したものと、その公開先 URL
│   ├── render.py            # md → HTML 本文・題・description
│   ├── order.py             # 概念の並び（上流依存 → 上流から下流へ）
│   ├── nav.py               # パンくず・ローカルメニュー・HTML サイトマップ
│   ├── seo.py               # OGP・hreflang・sitemap.xml・robots.txt
│   ├── page.py              # テンプレート合成（GA・シェア・フッタ含む）
│   ├── fonts.py             # フォントの取得と照合（固定コミット・SHA-256）
│   ├── cards.py             # 共有画像（既定画像・題のカード）の描画
│   ├── assets.py            # CSS・svg の配置
│   ├── build.py             # 段階の順序（発見 → 生成 → 書き出し → 関門）
│   ├── validate.py          # 配置前の品質関門（§16.1）
│   └── deploy.py            # boto3 による S3 同期・CloudFront 無効化
├── templates/               # HTML テンプレート（標準ライブラリ string.Template）
├── content/                 # サイト自身の文言（landing.ja.md／landing.en.md）
├── assets/site.css          # 単一の手書き CSS
└── tests/                   # 回帰テスト（unittest・fixture リポジトリ）
```

設定ファイルは置かない。構造上の規則はコード（`rules.py`）が持ち、配備の値は環境変数が持つ。

---

## 2. 入力の発見（走査）

`concepts/` を機械的に歩く。索引に依存しない。

- **対象概念**：`concepts/<category>/<concept>/` のうち、**原典名一致の文書 `ja/<concept>.md` を持つ概念だけ**。持たない概念は丸ごと対象外（v0.1 時点で 4 概念：`personal-llmo`・`shisaku-persona-architecture`・`kosei-mining`・`shisaku-cognitive-frame`。対象は 13 概念）。License・canonical URL を持たない文書（`shisaku-persona-architecture` の 2 件）は、この規則で外れる。
- **文書**：対象概念の `<lang>/**/*.md`（`figures/` と隠しファイルを除く）。`<lang>` ∈ `ja`／`en`。1 ファイル＝1 ページ。入れ子のディレクトリも展開する。
- **図版**：対象概念の `<lang>/figures/*.svg`。
- **トップ**：ルート `README.md`。無ければエラー。
- **対象外**：README と concepts 以外の直下文書（`CONTRIBUTING.md`・`authoring-policy.md`・`terminology-*.md`・`src/`・`logs/`・`publications/`）。

v0.1 時点で、対象概念に en の文書は無い。**en 側は README だけ**になる（en 文書が加われば走査が拾う）。対象外の概念も、原典名一致の文書が立った時点で走査が拾う。

---

## 3. URL と出力構造

**言語を最上位のパスに置く**（`/ja/…`・`/en/…`）。**ファイル名は元の `.md` の名をそのまま活かす**（`README.md`→`readme.html`）。

| 種類 | URL | 中身 |
| :-- | :-- | :-- |
| トップ | `/`（`index.html`） | このサイトが何かを ja/en で書く案内（§7）＋サイトマップ |
| README | `/ja/readme.html`・`/en/readme.html` | README を日英分割（§7）＋サイトマップ |
| 文書 | `/<lang>/concepts/<cat>/<concept>/<doc>.html` | 文書本文（§5） |
| 図版ページ | `/<lang>/concepts/<cat>/<concept>/figures/<name>.html` | svg を主コンテンツにした単独 HTML（§6） |
| 図版実体 | `/<lang>/concepts/<cat>/<concept>/figures/<name>.svg` | svg をそのまま配置 |
| SEO | `/sitemap.xml`・`/robots.txt` | §9 |
| 資産 | `/assets/site.css` | §11 |
| 共有画像（既定） | `/assets/og-default.png` | トップ・README の `og:image`（§9.1） |
| 共有画像（カード） | `/assets/og/<lang>/concepts/<cat>/<concept>/<doc>.png`（図版ページは `…/figures/<name>.png`） | 文書・図版ページの `og:image`。ページのパスを `/assets/og/` の下に写し、`.html` を `.png` にする（§9.1） |

- リポジトリのパス `concepts/<cat>/<concept>/<lang>/<doc>.md` を、言語先頭に組み替えて `/<lang>/concepts/<cat>/<concept>/<doc>.html` に写す（言語ディレクトリの下の入れ子は、その相対パスを保つ）。
- サイト内のリンクはルート相対（`/…`）で出す。例外は図版ページの `<img>` で、同じディレクトリの svg をファイル名だけで参照する（§6）。絶対 URL は canonical・OGP・hreflang・sitemap・シェアの宛先だけ。
- **概念用の index ページは作らない。** 概念内の回遊はローカルメニュー（§4.2）が、概念間の回遊はトップと README のサイトマップ（§4.5）が担う。
- README 内の `concepts/…` はコードスパンの言及であってリンクではない。原文には手を入れない。

---

## 4. ページの HTML 構造

```html
<!doctype html>
<html lang="<lang>">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>…（§4.3）</title>
  <meta name="description" content="…（§4.3）">
  <link rel="canonical" href="<BASE_URL>/…">
  <!-- OGP・hreflang（§9） -->
  <link rel="stylesheet" href="/assets/site.css">
  <!-- Google Analytics：GA_MEASUREMENT_ID があるときだけ出力 -->
</head>
<body>
  <a class="skip-link" href="#content">本文へ移動</a>
  <header class="site-header"><a class="site-title" href="/">shisaku-method …</a><!-- 言語切替（対があるとき）--></header>
  <nav class="breadcrumb" aria-label="パンくずリスト">…</nav>
  <div class="layout">
    <main id="content" class="main">
      <article class="origin" data-origin="github" lang="<lang>"><!-- md をレンダリングした本文＝GitHub の原文そのまま --></article>
      <nav class="share" aria-label="シェア">…</nav><!-- §4.6 -->
      <nav class="sitemap" aria-label="サイトマップ">…</nav>
    </main>
    <aside class="local-nav" aria-label="この概念のドキュメント">…</aside>
  </div>
  <footer class="site-footer">…（§4.4）</footer>
</body>
</html>
```

**ページ種別ごとの構成要素：**

| 要素 | トップ | README | 文書 | 図版ページ |
| :-- | :-- | :-- | :-- | :-- |
| パンくず | 出さない | `Home / README` | 全段（§4.1） | 全段（§4.1） |
| ローカルメニュー | 出さない | 出さない | 出す | 出す |
| `<article data-origin="github">` | 使わない（案内文はサイト自身の文言） | 使う | 使う | 使わない（§6） |
| サイトマップ（HTML） | 出す | 出す | 出さない | 出さない |
| License・GitHub URL | 持たない（サイト自身の案内文） | 原文側の対応待ち（§13） | 原文が持つ | ページが付ける（§6） |
| シェア（X・Facebook） | 出す | 出す | 出す | 出す |
| 共有画像（`og:image`） | 既定画像 | 既定画像 | 題のカード | 題のカード |
| GA・フッタ | 出す | 出す | 出す | 出す |

- DOM の順は本文が先、ローカルメニューが後。広い画面では CSS でメニューを左に置き、狭い画面では本文の下に回す（§11）。

### 4.1 パンくずリスト
`Home(/) / README(/<lang>/readme.html) / <カテゴリ（英語のまま・非リンク）> / <概念（原典ページへのリンク）> / <現在ページ（非リンク・aria-current="page"）>`。

- 概念の原典ページ自身では、概念が現在ページになるので、末尾を重ねない（`… / <カテゴリ> / <概念（現在）>`）。
- 図版ページの末尾は図版名。
- 概念へのリンク先は、その言語の先頭文書（原典があれば原典）。その言語に文書が無ければ ja の原典。

### 4.2 ローカルメニュー（同階層ナビ）
その概念・その言語配下の**文書一覧**と**図版一覧**。文書は原典を上段に置き（「原典」の印を付ける）、補足はその下に 1 段下げて（ファイル名昇順）並べる。原典と補足の関係が字下げで見えるようにするためである。現在ページは `aria-current="page"` で強調する。

### 4.3 タイトル・メタ
- `<title>`：
  - 文書：`(ドキュメント名) | shisaku-method （シサクメソッド）`。ドキュメント名＝本文先頭 H1 の文字列（装飾記号を除いた平文）。H1 が無ければファイル名。
  - 図版ページ：`(図版名) | shisaku-method （シサクメソッド）`。図版名＝svg のファイル名の語幹。
  - README：`README | shisaku-method （シサクメソッド）`（H1 が「shisaku-method」で重複するため）。
  - トップ：`shisaku-method （シサクメソッド）`。
- `description`／OGP：**メタ行（`上流依存`／`関連`／`Author`／`Version`／`帳簿注記` 等・`ラベル：` 行）を飛ばした最初の散文段落**から導く。先頭の箇条書き・引用の記号は除去し、インラインの装飾は平文にし、~120 字を超えるときは文末（40 字以上の最初の文）で切る。文末が無ければ 120 字で切って「…」。何も残らなければ題を使う。
  - トップ：案内文（ja）の冒頭段落。
  - 図版ページ：`(図版名)（<概念名>の図版）`（en は `(name) (Figure of <concept>)`）。

### 4.4 出典・ライセンス・生成日時
- **本文は単一ブロックで囲む。** md をレンダリングした本体は `<article data-origin="github">` で囲み、GitHub の原文そのままであることを構造で示す。サイトが生成する要素（パンくず・ローカルメニュー・シェア・サイトマップ・フッタ）は、このブロックの外に置く。
- **License・GitHub URL は重ねない。** 対象文書は末尾に License（CC BY 4.0）と canonical URL を自身が持つ。ゆえにフッタは**サイトのフッタ**とし、License・URL を足さない。
- **生成日時と版を明記する。** フッタに、GitHub から取得・生成した時刻とコミットを出す。
  - 時刻：ja ページは **JST**、en ページは **UTC**。トップ（日英併記）は両方。`<time datetime="ISO 8601">` で機械可読にする。
  - 版：コミット SHA（§8 の取り出し）。短縮形（7 桁）を表示し、GitHub のコミット URL（`SOURCE_REPO` から導出）へリンクする。`SOURCE_REPO` が無ければ短縮形だけを出す。SHA が分からなければ `unknown`。
  - 例（ja）：`GitHub から取得・生成：2026-09-23 09:00 JST（commit abc1234）`
  - 例（en）：`Fetched from GitHub and built: 2026-09-23 00:00 UTC (commit abc1234)`

### 4.5 サイトマップ（HTML）
トップと README の本文の下に、サイトが生成する `<nav class="sitemap">` を置く。`<article data-origin="github">` の外であり、原文には手を入れない。

- 構成：概念（原典の題・カテゴリを英語のまま小さな印で添える）→ 原典 → その下に 1 段下げて補足と図版。その言語に原典が無い概念は、字下げせずに並べる。**概念は上流から下流の順に 1 列で並べる。** カテゴリで区切らない（上流と下流がカテゴリをまたぐため）。
- **並びの規則**（別の一覧を持たず、各原典が自分で書く上流依存から導く）：
  1. 各原典の冒頭（先頭 20 行）にある最初の `上流依存：` の行を読む。`／` で区切った各項が上流の宣言で、項の中の `A → B` は「A の上流が B」、`最上流：X` は「その行の各鎖の末尾（鎖が無ければその原典自身）の上流が X」。名前は括弧書きと末尾の版表記を除いて、各原典の H1 と突き合わせる。
  2. 上流が先、下流が後になるように並べる（トポロジカル順）。
  3. 同時に置ける概念が複数あるときは、解釈（ディレクトリ名が `-interpretation`）を先に、残りは名前順。
  - 公開されない概念の名前（例：対象外の原典）は並びに使わず、`--report` に `upstream outside the site` として出す。
  - 依存が循環したら、置けなかった概念を名前順で末尾に置き、警告を出す。サイトは止めない（並びは回遊の補助であり、止めるほどの欠陥ではない）。
  - v0.1 時点の並び：世界解釈 → 社会更新解釈 → 前提優位理論 → 予測モデル解釈 → クオリア解釈 → 価値解釈 → ヒト変容理論 → ヒト距離構造 → ヒト表現構造 → ヒト IDION 構造 → ヒト共鳴構造 → ヒト軌跡構造 → 入口設計の認知フレーム。README の「含まれる概念」と重なる 8 概念は、README と同じ順になる。
- トップ：README（ja／en）へのリンクと、ja の全ページ。
- `/ja/readme.html`：ja の全ページ。
- `/en/readme.html`：en の全ページだけ（ja の一覧は載せない）。en の概念文書が無い間は README 自身へのリンクだけになる。
- SEO 用の `sitemap.xml`（§9）とは別物で、両方作る。

### 4.6 シェア
全ページの本文の下（サイトマップより上）に、X と Facebook の共有画面へのリンクを置く。

- **リンクだけで作る。** 外部のスクリプト・ウィジェットは読み込まない（読み込みの遅れ・追跡・表示崩れを持ち込まないため）。新しいタブで開き、`rel="noopener noreferrer"` を付ける。
- 宛先：X は `https://x.com/intent/tweet?text=<ページの title>&url=<canonical>`、Facebook は `https://www.facebook.com/sharer/sharer.php?u=<canonical>`。値は URL エンコードする。canonical は `BASE_URL` から作るので、共有されるのは公開 URL になる。
- 表示は文字（ja「X でシェア」「Facebook でシェア」／en「Share on X」「Share on Facebook」）。各社のロゴは商標なので描かない。
- 件数は出さない（X は 2015 年に件数の提供を止め、Facebook も件数付きのプラグインを終えている）。
- 共有されたときの画像は §9.1。
- 印刷時は隠す。

---

## 5. md → HTML（本文レンダリング）

- パーサ：**`markdown-it-py`**（CommonMark）＋ **`mdit-py-plugins`**。有効化：表・取り消し線・脚注・見出しアンカー（全見出しに id。同名は `-1` 等で一意化）。
- **生の HTML は通す。** 原文そのままを原則とし、入力は取得元リポジトリの文書である。
- **サイトは本文の文字列を書き換えない。** 例外は相対リンクの宛先だけ。
- **図版参照は本文に存在しない**（v0.1 時点）。本文への svg 埋め込みは行わない。
- **相対リンク**：v0.1 時点で対象文書に相対リンクは無い。現れた場合は、リポジトリ内のパスとして解決し、公開される文書・図版を指すなら出力 URL（§3）へ貼り替える（断片 `#…` は保つ）。公開されない宛先は、`SOURCE_REPO` があれば GitHub の該当ファイルへ向け、`--report` で一覧する。`SOURCE_REPO` が無ければ原文のまま残り、品質関門（§16.1）がリンク切れとして止める。
- 外部リンク（スキーム付き）とページ内リンク（`#…`）には触れない。

---

## 6. 図版（svg）の扱い

参照位置が本文に無いので、**svg を主コンテンツにした単独 HTML**を作る。

1. **実体の配置**：`figures/*.svg` を出力の同じパスへコピー。
2. **図版ページ**：図版 1 枚ごとに `<name>.html` を生成。主コンテンツは、その svg を **`<img src="<name>.svg" alt="<name>">` で参照しただけ**の本体（`<figure>` で囲う）。サイトの外装（ヘッダ・パンくず・ローカルメニュー・GA・フッタ）は持つ。
3. **License と URL を付ける。** 図版ページだけは md 本文を持たないので、figure の下に License（CC BY 4.0・`https://creativecommons.org/licenses/by/4.0/`）と、その svg の GitHub URL（`https://github.com/<SOURCE_REPO>/blob/<SOURCE_BRANCH>/concepts/…/<name>.svg`）を明記する。`SOURCE_REPO` が無ければリポジトリ内のパスを文字で出す。
4. ローカルメニューの図版一覧と、サイトマップから辿れる。単体でリンク・クロールされる面になる。

---

## 7. トップページと README

- **トップ `/`**：このサイトが何であるかを **ja/en 併記**で書く案内ページ。文言の正本は `content/landing.ja.md`／`landing.en.md`。`<html lang="ja">` とし、各言語を `<section lang="…">` で囲む。案内文の下にサイトマップ（§4.5）。
- **README**：日英併記で H1 が 2 つ。英語 H1（`# shisaku-method (English)`）の行で分割し、`/ja/readme.html` と `/en/readme.html` にする。境目の区切り線（`---`）は日本語側の末尾から落とす。相互に `hreflang` と言語切替を張る。本文の下にサイトマップ（§4.5）。英語 H1 が無ければ日本語側だけを出す。

---

## 8. 環境変数と取得・配置

**値はコード・設定ファイルに書かない。運用者が Lambda のコンソールで設定する。** ローカルビルドでは同名の環境変数を使う。環境変数を読むのは入口（`build_site.py`・`lambda_handler.py`）だけ。

| 変数 | 用途 | 無いとき |
| :-- | :-- | :-- |
| `SOURCE_REPO` | 取得元（`owner/name`）。tarball URL・コミット URL・図版 URL を導く | Lambda：停止／ローカル：コミット・GitHub へのリンクを出さず警告 |
| `SOURCE_BRANCH` | 取得するブランチ | 既定 `main` |
| `BASE_URL` | canonical・sitemap・OGP・hreflang の絶対 URL（末尾の `/` なし） | `http://localhost:8000` で生成し警告 |
| `GA_MEASUREMENT_ID` | Google Analytics 測定 ID（`G-` で始まる英大文字・数字） | GA を出さない。形が違えば警告して出さない |
| `S3_BUCKET` | 配置先 | Lambda：停止 |
| `CLOUDFRONT_DISTRIBUTION_ID` | 無効化 | 無効化しない |
| `ALLOW_SHRINK` | `1` のとき、縮小の安全弁（§16.2）を解除する | 安全弁を効かせる |
| `GITHUB_TOKEN` | 取得元が非公開のときだけ | 無認証で取得 |

- **Lambda は git を使わない。** Python ランタイムには git バイナリも `aws` CLI も無く、ファイルシステムは `/tmp` 以外読取専用。ゆえに：
  1. tarball を HTTPS で取得（`urllib`・タイムアウトと再試行つき）：`https://codeload.github.com/<SOURCE_REPO>/tar.gz/refs/heads/<SOURCE_BRANCH>`。公開リポジトリなら無認証。
  2. `/tmp` に標準ライブラリ `tarfile` で展開する。`filter="data"` でパス越え・絶対パス・デバイスファイル等を拒否し、トップディレクトリが 1 つであることと `README.md` の存在を確かめる。
  3. **コミット SHA は tar の pax グローバルヘッダ（`comment`）から取る。** tarball のトップディレクトリ名はブランチ名（例 `shisaku-method-main`）で、SHA を含まない。取得時刻は、ダウンロードが終わった時点の UTC。
  4. 生成 → 品質関門 → **boto3** で S3 同期 →（任意）CloudFront 無効化。
- **S3 同期（deploy.py）**：出力を走査し、S3 上の ETag（md5）とサイズが一致しないものだけ `put_object`。S3 にあって出力に無いキーは `delete_objects`（`sync --delete` 相当）。**追加・更新をすべて終えてから最後に削除する。** `Content-Type` と `Cache-Control` は §11。
- 必要な権限（AWS 側で付与）：`s3:ListBucket`・`s3:PutObject`・`s3:DeleteObject`、無効化を使うなら `cloudfront:CreateInvalidation`。

---

## 9. SEO

- **`sitemap.xml`**：生成した全 HTML（トップ・README・文書・図版ページ）を `BASE_URL` 基準で列挙。`lastmod` は出さない（tarball に履歴が無く、正しい更新日を持てないため）。
- **`robots.txt`**：全許可＋`Sitemap: <BASE_URL>/sitemap.xml`。
- **canonical**：各ページ自身の URL。
- **OGP**：`og:title`・`og:description`・`og:url`・`og:site_name`（`shisaku-method`）・`og:type`（トップは `website`、他は `article`）・`og:locale`（`ja_JP`／`en_US`）・`og:image`（絶対 URL）・`og:image:width`（1200）・`og:image:height`（630）・`og:image:alt`。X 向けに `twitter:card`＝`summary_large_image`（題・説明・画像は X が OGP から読む）。
- **hreflang**：ja と en で、言語を入れ替えたパスが一致するページを対とし、双方に張る（v0.1 時点は README のみ）。

### 9.1 共有画像（og:image）

SNS で共有されたときに出る 1200×630 の PNG。**ビルド時に Pillow で描く。** リポジトリに画像はコミットしない。

- **2 種類：**
  - **既定画像**（`/assets/og-default.png`）：サイト名（`shisaku-method`／シサクメソッド）・短い案内文・段の模様（上流から下流へ段を下げて流れる横棒）。トップ・README と、カードを持たないページが使う。`og:image:alt` は `shisaku-method（シサクメソッド）`（en は `shisaku-method`）。
  - **題のカード**（文書・図版ページ）：左上に種別の印（原典／補足／図版。en は Canon／Supplement／Figure）と、補足・図版なら属する概念の題。中央に題（文書は H1、図版は図版名）。下に区切り線・サイト名・小さな段の模様。`og:image:alt` はそのページの `<title>`。
- **題の組み方：**
  - 大きい順に 64・58・52・46・42px を試し、枠（幅 1040px）に収まる最大を使う。42px でも収まらなければ、最後の行を「…」で切る。
  - 和文は文字の間で、英単語は単語の間（ハイフンの後も可）で折り返す。閉じ括弧・句読点・小書きの仮名は行頭に置かず前の行にぶら下げ、開き括弧は行末に置かない。文節での改行はしない（§15）。
  - フォントに無い字形は近い字形に置き換える（`―`→`—`、`～`→`〜`、`‒`→`–`）。置き換えても無い字形は、そのページを警告に出す（止めない。画像の一字が欠けても、ページの読みは損なわれないため）。
  - 字の配置は Pillow の基本レイアウトで行い、任意のライブラリ（raqm 等）の有無で結果を変えない。
- **フォント：Zen Maru Gothic（Bold：題／Medium：印・概念名・サイト名）。** 丸ゴシックで、サイトの書体方針（§11）に合わせる。SIL Open Font License 1.1。
  - 取得元は GitHub の `google/fonts`（`ofl/zenmarugothic/`）。**コミットを固定し、ファイルごとの SHA-256 を `rules.py` に持つ。** `OFL.txt` も同じく固定して一緒に取る（OFL の条件：フォントを配布物に含めるときはライセンス文を添える）。
  - **取得はパッケージ作成時と CI だけ**（`fetch_fonts.py`）。日次の実行はネットワークからフォントを取らない。リポジトリにもコミットしない（約 7.6MB）。
  - ビルドのたびに SHA-256 を照合し、合わないファイルは無いものとして扱う。
  - サイトのページはこのフォントを読み込まない（ウェブフォントは使わない・§11）。画像の中に描くだけである。
- **フォントが無いとき：**
  - ローカル・CI のビルド（`--fonts` なし、または照合に失敗）：カードを描かず、全ページが既定画像を使う。既定画像は文字を持たない模様だけになる。警告を出して止めない。
  - **Lambda：配置を拒む**（§10）。パッケージの作り損ないで、文字の無い画像を公開してしまうのを防ぐ。
- **決定性：** 同じ文字列・フォント・Pillow の版なら、同じバイトになる（aarch64 と x86_64 で一致を確認済み）。ゆえに日次の配置で、題が変わらないカードは再アップロードされない。

---

## 10. CLI

```bash
python3 src/site/build_site.py --src <リポジトリのルート> --out <出力先> [--clean] [--commit <SHA>] [--fetched-at <ISO 8601>] [--fonts <フォントのディレクトリ>] [--report]
python3 src/site/fetch_fonts.py --dest <フォントのディレクトリ>
```

- `--src`：入力のルート（既定：カレント）。`--out`：出力先（既定：`dist`）。**出力先は空であること**（古いファイルの残留を防ぐ）。`--clean` は出力先を先に消す。
- `--commit`／`--fetched-at`：フッタの版・時刻。省略時は、SHA は `git rev-parse HEAD`（使えなければ `unknown`）、時刻は現在時刻。`--fetched-at` はオフセット付き。
- `--fonts`：共有画像用フォントのディレクトリ（§9.1）。省略時はカードを描かず警告する。
- `--report`：要約（ページ数・ファイル数・対象外の概念・共有画像の種別・貼り替え不能なリンク・サイト外の上流名・警告・関門の違反）を出す。
- `fetch_fonts.py`：固定したフォントと `OFL.txt` を取得し、SHA-256 を照合して置く。照合済みのファイルがあれば取り直さない。合わなければ何も残さず終了コード 1。
- 終了コード：0＝成功。1＝`README.md` が無い、読み取り・書き出しに失敗、出力先が空でない、**品質関門（§16.1）に違反がある**。警告（環境変数の欠落等）は stderr に出して止めない。
- `lambda_handler.handler` は、環境変数の読取 → 取得 → 生成と関門 → 配置 → 無効化の順に実行し、コミット・ページ数・put／delete 件数を返す。フォントはパッケージ内の `fonts/` から読む。関門の違反・フォントの欠落・例外は Lambda の失敗として返し、S3 には触れない。

---

## 11. CSS と資産

- 単一の手書き `site.css`。フレームワーク不使用。
- **フォント：ゴシック・親しみやすいもの。明朝は使わない。** 和文システムフォントを優先し、丸ゴシック（`Hiragino Maru Gothic ProN`）→ `BIZ UDPGothic` → `Hiragino Sans` → `Noto Sans JP` → `Yu Gothic UI` → `Meiryo` の順で当てる。ウェブフォントは読み込まない（共有画像の中の文字だけは、同梱のフォントで描く・§9.1）。
- ライト/ダーク（`prefers-color-scheme`）。svg はライト地で描かれているので、図版は常に白地の枠に置く。
- 本文の可読幅を制限（44rem）。広い画面（60rem 以上）ではローカルメニューを左に固定表示、狭い画面では本文の下に回す。**JS は使わない**（GA を除く）。
- 印刷時はヘッダ・パンくず・メニュー・シェア・サイトマップを隠す。
- S3 の `Content-Type`：`.html` `text/html; charset=utf-8`／`.css` `text/css; charset=utf-8`／`.svg` `image/svg+xml`／`.png` `image/png`／`.xml` `application/xml`／`.txt` `text/plain; charset=utf-8`。
- `Cache-Control`：HTML・xml・txt は `public, max-age=3600`（日次更新のため短め）、CSS・svg・png は `public, max-age=86400`。

---

## 12. 実行環境（Python・ランタイム）

- **要求：Python 3.11.4 以上。** 既存エンジン（3.11+）と下限をそろえる。`tarfile` の `filter="data"` が使えるのが 3.11.4 から。
- **Lambda ランタイム：Python 3.13（または 3.12）。** `boto3` はランタイム同梱。
- **依存：`markdown-it-py`・`mdit-py-plugins`・`mdurl`・`pillow`**（`requirements.txt` で版を完全固定）。デプロイパッケージに同梱する。Pillow はバイナリを含むので、**Lambda のアーキテクチャ（x86_64／arm64）と Python の版に合う wheel** を入れる（手順は OPERATIONS）。
- **フォント**（§9.1）：デプロイパッケージの `fonts/` に、`OFL.txt` と一緒に置く。パッケージは zip で約 11MB（直接アップロードの上限 50MB に収まる）。
- 出力は Python のマイナー版に依存させない。テストは 3.11・3.12・3.13 で通す（CI は Lambda に合わせて 3.12・3.13）。

---

## 13. 外部依存（本道具の外で行う作業）

- **README に License 節が無い**（エンジン DESIGN §16.1 で「持たせるかは管轄外」と空いている項目）。README 側に License 節ができるまで、README ページには License 表示が出ない。README の改修は `src/docs/root/readme` 側で行う。

---

## 14. 未決

なし。

---

## 15. 予約

- クライアント側の全文検索。
- 共有画像の和文を文節で折り返す（今は文字の間で折るので、語の途中で改行することがある）。
- 構造化データ（JSON-LD `Article`）。
- `paths.toml` の再利用（出典リンク生成への流用。発見はスキャンのまま）。

---

## 16. 実装の設計方針

優先順位は **品質 → 安定性 → 保守性 → 関心の分離**。二つが衝突したら上位を取る。

### 16.1 品質 ― 読者に届くものが正しい

一次目的（人間が読み、回遊できる）を満たす出力であること。面は二つ：**忠実**（原文を変えずに出す）と**到達**（辿れる・壊れていない）。

- **忠実**：`<article data-origin="github">` の中身は md のレンダリング結果だけ。サイトは本文の文字列を書き換えない（置換・要約・補正をしない）。
- **品質関門（validate.py）**：生成後・配置前に出力全体を読み、1 件でも違反があれば終了コード 1 で止める。出力だけを読むので、読者が受け取るものを検査することになる。
  - サイト内のリンク（`href`／`src`・スタイルシートを含む）がすべて出力内の実在ファイルに解決する。
  - 全ページに `lang`・空でない `title`・空でない `description` と、自身を指す `canonical` がある。
  - `hreflang` が双方向で対になっている。
  - フッタに生成日時（`<time datetime>`）とコミットがある。
  - `sitemap.xml` が全ページを過不足なく列挙し、トップ以外の全ページがどれかの HTML サイトマップに載っている。`robots.txt` がある。
  - 全ページに `og:image` があり、サイト内の実在ファイルを指し、そのファイルが 1200×630 の PNG である（PNG のヘッダで確かめる）。
- **回帰テスト**（`tests/`）：固定の入力（fixture リポジトリ）から生成し、ページ構成・題・本文ブロック・フッタ・日英対・サイトマップ（上流からの並び・原典の下への字下げ）・ローカルメニュー・シェアのリンク・共有画像（フォントの有無それぞれで、どのページがどの画像を指すか・カードの寸法）・図版ページ・決定性（二度の生成がバイト一致）を突き合わせる。題の折り返し（禁則・英単語・ハイフン・省略）は幅を数える関数を差し替えて、フォント無しでテストする。フォントの取得と照合（欠落・改変・取得時の不一致で何も残さないこと）もテストする。フォントを要するテストは、環境変数 `SITE_FONTS` がフォントのディレクトリを指すときだけ走る（CI は指す）。上流依存の読み取りと並び（鎖・最上流・サイト外の名前・循環）、取得（pax ヘッダの SHA・パス越えの拒否）、配置（差分・削除の順・縮小の安全弁・Content-Type）もそれぞれ単体でテストする。description 抽出は、公開文書に実在する型（上流依存行・関連行・英語メタ・太字メタ・帳簿注記・箇条書き・長文）を写した正解表で持つ。実文書そのものを正解にしない——文書の改訂のたびに CI が落ちる状態を作らないため。関門は、正常な出力を 1 か所ずつ壊して必ず違反を返すことをテストする。
- **失敗機構**：関門なしで配置すると、リンク切れや空の title が黙って公開される。読者は壊れたサイトを見て離れ、一次目的そのものが空振りする。

### 16.2 安定性 ― 無人の日次実行が、公開中のサイトを壊さない

- **fail-closed**：取得・生成・検査のどこかで失敗したら、S3 に一切触れない。公開中のサイトは前回の正常版のまま残る。
- **配置の順序**：追加・更新をすべて終えてから、最後に削除する。途中で落ちても、ページが欠けた時間を作らない。
- **縮小の安全弁**：生成した HTML の数が S3 上の現行 HTML の半分未満なら、配置を止める（S3 には触れない）。取得の欠損や構成変更の事故で、削除がサイトを消し去るのを防ぐ。意図した大規模削除のときだけ `ALLOW_SHRINK=1` で一度解除する。
- **取得の頑健さ**：タイムアウトと再試行（5xx・429・通信失敗のみ。4xx は再試行しない）。展開の安全は §8。
- **依存の固定**：`requirements.txt` で版を完全固定する。上流の更新で HTML が黙って変わるのを防ぐ。版上げは回帰テストを通してから。CI の外部 action もコミット SHA で固定する。フォントは取得元のコミットと SHA-256 で固定する（§9.1）。
- **日次の実行が外に取りに行くのは tarball だけ**：フォントはパッケージに同梱し、実行時に取らない。欠けていれば配置を拒む。
- **失敗を失敗として返す**：例外を握りつぶさず、Lambda を失敗で終わらせる（検知・通知は AWS 側）。ログは段階ごとに件数（取得したコミット・ページ数・違反・put・delete）を出す。

### 16.3 保守性 ― 一人の保守者とフォークした人が、読んで直せる

- 標準ライブラリを優先し、外部依存は md パーサ一式と Pillow（画像の描画）だけ。フレームワークもテンプレートエンジンも入れない。
- **規則はデータとして一か所に置く**（`rules.py`）：対象概念の判定、原典の判定、上流依存の行の読み方と同順位の並べ方、description のメタ行パターンと字数、表示ラベル、シェアの宛先、共有画像（パス・寸法・配色・字の大きさ・禁則文字・字形の置き換え）、フォントの取得元と SHA-256、タイムゾーン、Content-Type、Cache-Control、縮小の閾値。規則を変えるときに触るのはここだけ。
- テンプレートは HTML ファイルとして外に出す（`templates/`）。
- 巧妙さより明示。型ヒントを付け、1 関数 1 仕事。
- 文書は `DESIGN.md`（何を・なぜ）と `OPERATIONS.md`（どう回す）の対で持つ（エンジンと同じ作法）。

### 16.4 関心の分離 ― 保守性とテストのための手段

- **段階と入出力を固定する**：fetch（ネットワーク → ソース＋SHA）→ discover（ソース → モデル）→ render（→ 本文・題・description）→ order（原典の上流依存 → 概念の並び）→ nav／seo／page（→ HTML 文字列）→ cards（→ PNG のバイト列）→ write（→ 出力）→ validate（出力 → 違反一覧）→ deploy（出力 → S3）。順序は `build.py` と `lambda_handler.py` が持つ。
- **I/O は両端だけ**（fetch・write・deploy。フォントの取得は別の入口 `fetch_fonts.py`）。中核は文字列を返す関数にし、ファイルもネットワークも無しでテストできるようにする。deploy は S3 クライアントを引数で受け取り、テストは偽のクライアントで行う。
- **環境変数を読むのは入口だけ**（`build_site.py`・`lambda_handler.py`）。読んだ値は `config.py` の設定オブジェクトにまとめて渡し、各モジュールは `os.environ` に触れない。
- 生成器は AWS を知らず、deploy は md を知らない。
- **分離は目的ではない。** 一緒に変わるものは同じモジュールに置く（エンジン DESIGN §3.1 の過分割の戒めと同じ）。

### 16.5 衝突したときの判断例

- **品質 vs 安定性**：1 文書のレンダリングに失敗したとき、その文書を飛ばして配置するのではなく、ビルド全体を止める。fail-closed なので公開中のサイトは前回版で保たれ、安定性も損なわない。
- **安定性 vs 保守性**：縮小の安全弁はコードを増やす（保守の負担）が、サイト消失を防ぐので入れる。
- **保守性 vs 関心の分離**：境界を増やしても変更の単位が分かれないなら、分けない。

---

## 17. CI（GitHub Actions）

- **置き場**：`.github/workflows/site.yml`。
- **起動**：`src/site/**`・`concepts/**`・`README.md`・ワークフロー自身に変更がある push と PR。手動実行（`workflow_dispatch`）も持つ。
- **中身**：
  1. Python 3.12／3.13 の行列で、`requirements.txt` の固定版を入れる（Lambda のランタイムと合わせる）。
  2. 共有画像用フォントを `fetch_fonts.py` で取る（固定コミット・SHA-256 照合。§9.1）。
  3. 回帰テストを回す（標準ライブラリの `unittest`。テスト用の追加依存は入れない）。`SITE_FONTS` にフォントのディレクトリを渡し、フォントを要するテストも走らせる。
  4. そのコミットの中身で `build_site.py --fonts …` を実行し、品質関門まで通す。本文の変更が日次ビルドを落とすことを、PR の段階で知るためである。`SOURCE_REPO`・`SOURCE_BRANCH` は GitHub の実行コンテキスト（`github.repository` 等）から渡す。リポジトリに値を書くのではない。
- **配置はしない。** CI は AWS に触れず、AWS の認証情報も配備の値も持たない。
- **フォークでもそのまま動く。** secrets を使わないため。
- **権限は `contents: read` だけ。** 外部の action（checkout・setup-python）はコミット SHA で固定し、checkout は認証情報を残さない（`persist-credentials: false`）。
- **失敗機構**：CI が無いと、本文の変更で関門違反が起きても、気づくのは翌日の Lambda の失敗になる。fail-closed なのでサイトは壊れないが、その間サイトの更新が黙って止まる。

---

## License

This document defines the design of the site build under `src/site/` in the shisaku-method repository.

Copyright (c) 2026 shisaku

Licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0).

License: https://creativecommons.org/licenses/by/4.0/
Author: https://note.com/abstraction
Canonical repository: https://github.com/cicd-shisaku-work/shisaku-method/tree/main/src/site
