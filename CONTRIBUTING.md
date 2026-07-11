# CONTRIBUTING — git運用規約

**バージョン：v0.1**
**Date:** 2026/07/11
**性格：** 本リポジトリ（shisaku-method）のgit運用ルール。過去のgitログ（2026/06〜07）から実際に安定した運用を成文化したもの。本リポジトリはドキュメント中心であり、規約もそれに最適化する。

---

## 1. ブランチ運用（PRフロー）

```
main ← トピックブランチ（PR経由・squash merge）
```

- **mainへの直コミットはしない。** すべての変更はトピックブランチを切り、GitHub上のPull Requestを経由してmainへマージする。
- PRはソロ運用でもセルフレビューの場として使う——diffを俯瞰し、一晩置いて読み直してからマージしてよい。**確定は人間の目を通す**（SEFA・PEESの「評価器は提案し、確定は人間」と同じ思想）。
- マージ方式は **squash merge** とし、マージ後にトピックブランチを削除する。これにより「1トピック＝main上の1コミット」が保たれる。

### ブランチ命名

| プレフィックス | 用途 | 例 |
| :-- | :-- | :-- |
| `add-*` | 新規ドキュメント・概念の追加 | `add-trust-signal-frame-and-publications` |
| `update-*` | 既存ドキュメントの版上げ・構造改訂 | `update-pees-v0.2` |
| `fix-*` | 誤記・リンク・ライセンス表記などの修正 | `fix-license-metadata` |

- 名前は英小文字とハイフン。内容が推測できる具体名にする（`update-docs` のような汎用名は避ける）。
- 1ブランチ=1トピック。無関係な変更を同じブランチに混ぜない。

## 2. コミットメッセージ規約

Conventional Commits の簡易形を用いる。本リポジトリはドキュメント中心のため、大半は `docs:` である。

```
<type>: <要約（英語または日本語・命令形・50字目安）>
```

| type | 用途 |
| :-- | :-- |
| `docs:` | ドキュメントの追加・改訂（本リポジトリの既定） |
| `fix:` | 誤記・リンク切れ・メタデータ修正 |
| `chore:` | ディレクトリ構成・.gitignore 等の整備 |

### 書式ルール

- **版上げは遷移を明記する：** `docs: kosei-mining-definition v0.7.2 -> v0.7.3`
- **新規追加は add + 対象 + 版：** `docs: add SEFA evaluator fidelity axioms v0.1`
- 複数ファイルにまたがる1トピックは、要約に主対象を書く。

### 本文（body）の義務（コミットの自己完結性）

コミットメッセージは、**diffを開かなくても「何が・なぜ変わったか」が分かる**ことを合格条件とする。mainのgit logだけで各ドキュメントの改訂履歴が再構成できる状態を保つ。

**bodyが必須となる条件（いずれか該当）：**

1. ドキュメントの版上げ（マイナー・パッチとも）
2. 採点ロジック・条項・構造に触れる変更
3. 複数トピック・複数ドキュメントにまたがる変更
4. ファイルの追加・移動・削除・配置換え

bodyには次を書く：**変更点の箇条書き**（ドキュメントごと・条項単位）、**改訂の根拠**（検証結果・観測・上流文書・issue）、移動があれば**旧配置→新配置**。

**要約（1行目）だけでよいのは**、単一ファイルの誤記・リンク・表記修正のみ（例：`fix: broken canonical URL in trust-signal-frame`）。

**禁止例（過去ログの反省点）：**

- `修正` ／ `update` ——対象も内容も分からない
- `docs: add SEFA v0.1; pees v0.1.8 -> v0.2; add CONTRIBUTING`（bodyなし）——3トピックの構造改訂が1行に潰れ、何がどう変わったか辿れない

**セルフチェック（コミット前に一問）：** 半年後の自分がこのメッセージだけを読んで、diffの中身を言い当てられるか。言い当てられないなら、bodyに書き足す。

**squash merge時の注意：** GitHubのsquashはローカルコミットのメッセージを連結して本文にする。bodyが確実に残るよう、`git commit -m "<要約>" -m "<body>"` の形でローカルコミット自体に本文を持たせる。PR説明にも同内容を書く（レビューの場で使うため）。

## 3. ドキュメント収録の必須チェック（PRチェックリスト）

新規ドキュメントを収録するPRでは、以下を満たすこと。

- [ ] **ヘッダー**：タイトル／短縮名（あれば）／`**バージョン：vX.Y**`／上流依存（該当時）を冒頭に持つ。
- [ ] **ライセンス表示**：末尾に `## License` セクション（CC BY 4.0、Copyright (c) 20XX shisaku、Author URL、Canonical repository URL）。
- [ ] **Canonical repository URLが配置先ディレクトリと一致**している（移動時は必ず書き換える）。
- [ ] **README同期**：`concepts/` 配下への追加は「含まれる概念」（日英）と構造ツリーを更新する。`publications/` 配下は構造ツリーのみでよい。
- [ ] **改訂の場合**：本文の改訂履歴に版・日付・変更点・根拠を追記する。
- [ ] **配置基準**：汎用性が実証された概念のみ `concepts/`。特定成果物に寄った文書・検証途上の文書は `publications/` に置き、格上げは実証後に `git mv` で行う（履歴が追える）。

## 4. バージョニング

- ドキュメントは各自の本文ヘッダーで版管理する（`v0.1` → `v0.1.1` → `v0.2`）。
  - **パッチ（v0.1.x）**：条項の明確化・表記修正・採点ロジックに触れない変更。
  - **マイナー（v0.x）**：構造改訂・条項の追加削除・採点ロジックの変更。
- 版を上げたら、旧版ファイルを残さない。旧版はgit履歴が保存する（`v0.1` と `v0.2` のファイル並置はしない）。

## 5. 履歴の衛生

- **push済みコミットのrebase・filter-branchはしない**（初期に履歴書き換えで荒れた反省による）。書き換えはローカルの未pushコミットに限る。
- squash mergeを使うため、トピックブランチ内のWIPコミットは自由でよい。mainに載る1コミットのメッセージだけ規約に従う。
- コミッターは `cicd <cicd@shisaku.work>` に統一する。

## 6. 標準フロー（コマンド例）

```bash
# 1. ブランチを切る
git checkout main && git pull origin main
git checkout -b update-pees-v0.2

# 2. 作業・コミット
git add <files>
git commit -m "docs: pees-prelim-business v0.1.8 -> v0.2"

# 3. push して PR を作る
git push -u origin update-pees-v0.2
gh pr create --fill   # または GitHub UI

# 4. セルフレビュー後、squash merge（GitHub UI推奨）
gh pr merge --squash --delete-branch
```

---

## License

This document defines the git workflow conventions for the shisaku-method repository.

Copyright (c) 2026 shisaku

Licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0).

License: https://creativecommons.org/licenses/by/4.0/
Author: https://note.com/abstraction
Canonical repository: https://github.com/cicd-shisaku-work/shisaku-method
