# 地方競馬 (NAR) — 共通v9から移行済み

- **正本**: `local/prompts/` 内の27個のルールMarkdown。元v9の32セクションを文面そのままで保持しています。
- **索引**: `local/prompts/INDEX.md`（Agentごとの担当モジュールを管理）。
- **参照原本**: `local/archive/地方_共通_v9_原本.md`。移行確認用。通常実行時は読まない。
- **Skill**: `$local-race-info`、`$local-full-prediction`、`$local-odds-check`。
- **専用コースファイル**: `local/prompts/courses/`。元の場別プロンプトは今回提供されていないため未収録。
- **調査レビュー資料**: 元v9が参照する `地方競馬予想_調査レビュー_20261019.md` は未提供。

### 更新時
判断基準を変更する場合は `local/prompts/` 内の該当Markdownだけ編集してください。
`local/archive/` は元のv9のまま保存します。移行一致テストは初期状態の検証用です。
