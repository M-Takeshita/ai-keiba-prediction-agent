# 中央競馬 (JRA) — 独立した初期プロンプト

- **正本**: `central/prompts/` 内の項目別Markdown。
- **索引**: `central/prompts/INDEX.md`（Agentごとの担当ファイル一覧）。
- **Skill**: `$central-race-info`、`$central-full-prediction`、`$central-odds-check`。
- **中央独自の予想プロンプトは未提供**のため、ルールは一般的な初期設定です。ユーザーオリジナルの中央ルールを移植したものではありません。
- 中央固有の芝・ダート・障害、JRAクラス、開催場に対応する方針を地方とは別に管理します。
- 特定コースの独自ルールは `central/prompts/courses/` に追加してください。

### 更新時
既存項目は担当Markdownのみ編集します。新規ファイルを増やした場合は `central/prompts/INDEX.md` に参照ルートを登録します。
