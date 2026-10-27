# 中央競馬 Prompt INDEX（初期版・正本）

**中央競馬専用**。ユーザーの中央用プロンプトは未提供のため、以下は汎用的な初期ルールです。地方v9のルールとは別系統です。
中央競馬の新しい独自ルールができたらこのフォルダ内のMarkdownを改訂してください。

## 参照方法
1. すべてのAgentは `central/prompts/common/principles.md` と `central/prompts/common/evidence_policy.md` を先に読む。
2. 担当する以下のモジュールを読み、判断はMarkdownを正本とする。
3. 地方の `local/prompts/` や原本アーカイブを参照しない。
4. `central/prompts/courses/` に検証済みの開催場・距離ルールがあれば追加参照する。

## 担当ルーティング

### `main`
- `central/prompts/common/principles.md`
- `central/prompts/common/evidence_policy.md`
- `central/prompts/workflow/procedure.md`
- `central/prompts/output/format.md`

### `race_researcher`
- `central/prompts/common/principles.md`
- `central/prompts/common/evidence_policy.md`
- `central/prompts/research/race_info.md`
- `central/prompts/research/past_runs.md`

### `form_analyst`
- `central/prompts/common/principles.md`
- `central/prompts/common/evidence_policy.md`
- `central/prompts/analysis/ability.md`
- `central/prompts/analysis/jockey.md`

### `track_pace_analyst`
- `central/prompts/common/principles.md`
- `central/prompts/common/evidence_policy.md`
- `central/prompts/analysis/course_track.md`
- `central/prompts/analysis/pace.md`

### `odds_analyst`
- `central/prompts/common/principles.md`
- `central/prompts/common/evidence_policy.md`
- `central/prompts/decision/odds.md`

### `bet_strategy_analyst`
- `central/prompts/common/principles.md`
- `central/prompts/common/evidence_policy.md`
- `central/prompts/decision/betting.md`

## その他の管理対象
- `central/prompts/review/postmortem.md` — 事後検証の基準（通常の情報収集・予想では不要）
- `central/prompts/courses/README.md` — 場別ファイルの置き方（判定ルールではない）
