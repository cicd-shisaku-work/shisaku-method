# シサクメソッド公開サイト・運用手順書（src/site）

**Version:** v0.1
**Date:** 2026/09/23
**性格：** `src/site/` の道具を日々どう回すかの手順。仕組みそのものの設計は `DESIGN.md`。本書は「何をどの順で叩くか」だけを扱う。

---

## 1. 前提

- Python 3.11.4 以上（3.12／3.13 を推奨）。
- 依存は `src/site/requirements.txt`（版を完全固定）。仮想環境に入れる。

```bash
python3 -m venv .venv
.venv/bin/pip install -r src/site/requirements.txt
```

- 共有画像用のフォント（`DESIGN.md` §9.1）を、リポジトリの外に一度だけ取る。取得元のコミットと SHA-256 は固定されていて、照合済みなら取り直さない。

```bash
.venv/bin/python src/site/fetch_fonts.py --dest ~/.cache/shisaku-site-fonts
```

- バイトコードのキャッシュをリポジトリに作らないよう、`PYTHONDONTWRITEBYTECODE=1` を付けて実行する（入口のスクリプトは自分で抑止するが、テストの実行経路では効かない）。

---

## 2. ローカルでビルドして見る

```bash
export PYTHONDONTWRITEBYTECODE=1
.venv/bin/python src/site/build_site.py --src . --out /tmp/site --clean \
    --fonts ~/.cache/shisaku-site-fonts --report
python3 -m http.server 8000 -d /tmp/site      # http://localhost:8000/ で確認
```

- 出力先はリポジトリの外を勧める。リポジトリ内の `dist/` に出すなら、コミットに含めない。
- 環境変数（`DESIGN.md` §8）が無くてもビルドはできる。無いものは警告が出て、GA・コミットのリンク・GitHub へのリンクが省かれる。本番に近い形で見るときは、同名の環境変数を渡す（値はリポジトリに書かない）。
- `--fonts` を付けないと、ページごとのカードは作られず、全ページが文字の無い既定画像を指す（警告が出る。止まらない）。
- 共有画像は `/assets/og-default.png` と `/assets/og/…` に出る。ブラウザで直接開いて確かめる。
- `--report` の `violation:` 行が品質関門の違反。1 件でもあれば終了コード 1。`warning: … share card font has no glyph for …` は、題にフォントの無い字形がある（画像のその字が欠ける）。`rules.py` の `CARD_GLYPH_SUBSTITUTES` に置き換えを足すか、そのままにする。

---

## 3. テスト

```bash
SITE_FONTS=~/.cache/shisaku-site-fonts PYTHONDONTWRITEBYTECODE=1 \
    .venv/bin/python -m unittest discover -s src/site/tests -t src/site -v
```

- `SITE_FONTS` が無いと、フォントを要するテスト（カードの描画）は skip になる。CI はフォントを取ってから回すので、skip しない。

- 入力は `src/site/tests/fixtures/repo/`（小さな擬似リポジトリ）。実文書には依存しない。
- 規則（`sitebuild/rules.py`）を変えたら、どのテストが動いたかで影響を確かめる。description の規則を変えたときは `tests/test_render.py` の正解表を見直す。並びの規則（上流依存の読み方・同順位の並べ方）を変えたときは `tests/test_order.py` を見直す。
- 依存の版を上げるときは、`requirements.txt` を書き換えてテストと実データのビルド（§2）を通してから。Pillow の版を上げると、全カードのバイトが変わりうる（その日の配置で全カードが再アップロードされる）。見た目を確かめてから上げる。
- フォントを替える・版を上げるときは、`rules.py` の `FONT_SOURCE`（コミットを含む URL）と `FONT_FILES`（ファイル名と SHA-256）を書き換え、パッケージを作り直す。

CI（`.github/workflows/site.yml`）が push・PR で同じテストと実データのビルドを回す。CI は配置をしない。

---

## 4. Lambda への配置

### 4.1 パッケージを作る

```bash
ARCH=x86_64          # 関数のアーキテクチャ。arm64 の関数なら aarch64
PY=3.13              # 関数のランタイムの版
rm -rf build/lambda && mkdir -p build/lambda
pip install -r src/site/requirements.txt -t build/lambda \
    --platform manylinux_2_28_$ARCH --only-binary=:all: --python-version $PY --implementation cp
cp -R src/site/build_site.py src/site/lambda_handler.py \
      src/site/sitebuild src/site/templates src/site/content src/site/assets build/lambda/
python3 src/site/fetch_fonts.py --dest build/lambda/fonts
(cd build/lambda && zip -qr ../site-lambda.zip .)
```

- **Pillow はバイナリを含む。** 手元の機械ではなく、関数のアーキテクチャと Python の版に合わせて入れる（上の `--platform` 等）。合わないと、Lambda で `import PIL` が失敗する。
- **フォントは `fonts/` に置く**（`OFL.txt` を含む）。無い・改変されたパッケージは、Lambda が配置を拒む。
- zip は約 11MB（コンソールから直接アップロードできる）。

- 道具のコード（テンプレート・CSS・案内文を含む）はパッケージの側を使う。取得した tarball から使うのは `README.md` と `concepts/` だけ。**道具を直したら、パッケージを作り直して Lambda を更新する。** 文書の更新は日次の実行で自動的に反映される。
- `build/` はコミットしない。

### 4.2 関数の設定

| 項目 | 値 |
| :-- | :-- |
| ランタイム | Python 3.13（または 3.12） |
| ハンドラ | `lambda_handler.handler` |
| タイムアウト | 数分（目安 5 分） |
| メモリ | 512 MB 程度 |
| 一時領域（`/tmp`） | 既定（512 MB）で足りる |

- 環境変数は `DESIGN.md` §8 の表のとおり。**値はコンソールで設定し、リポジトリには書かない。**
- 権限：`s3:ListBucket`（バケット）、`s3:PutObject`・`s3:DeleteObject`（オブジェクト）、無効化を使うなら `cloudfront:CreateInvalidation`。
- 起動：EventBridge のスケジュールで 1 日 1 回。

### 4.3 実行結果の見方

- 成功時の戻り値：`commit`・`pages`・`put`・`delete`・`unchanged`・`invalidation`。
- ログの段階：取得したコミット → 生成したページ数 → 配置の件数 → 無効化。

---

## 5. 失敗したとき

失敗した実行は S3 に触れていない。公開中のサイトは前回の正常版のまま（fail-closed）。

| 症状 | 見るところ | 直し方 |
| :-- | :-- | :-- |
| `violation:` が出て止まった | ログの違反一覧 | リンク切れ・題の欠落など。ローカルで同じコミットをビルドして再現し、原文か道具を直す |
| `refusing to publish … below 50%` | 生成ページ数と現行ページ数 | 取得の欠損や対象判定の事故を疑う。意図した大規模削除なら、その 1 回だけ `ALLOW_SHRINK=1` を付けて実行し、終わったら外す |
| `download failed` | 取得元・ブランチ・通信 | `SOURCE_REPO`・`SOURCE_BRANCH` の値、GitHub 側の状態 |
| `SOURCE_REPO and S3_BUCKET must be set` | 環境変数 | コンソールで設定する |
| `share-card fonts are missing or altered in the package` | パッケージの `fonts/` | §4.1 の `fetch_fonts.py` を入れてパッケージを作り直す |
| `No module named 'PIL'`／`_imaging` の読み込み失敗 | パッケージの Pillow | §4.1 の `--platform`・`--python-version` を関数に合わせて作り直す |

---

## 6. 規約との関係

本書は手順であって規約ではない。設計上の決まりは `DESIGN.md` が正本で、ここには写さない。

---

## License

This document defines the operating procedure for the site build under `src/site/` in the shisaku-method repository.

Copyright (c) 2026 shisaku

Licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0).

License: https://creativecommons.org/licenses/by/4.0/
Author: https://note.com/abstraction
Canonical repository: https://github.com/cicd-shisaku-work/shisaku-method/tree/main/src/site
