# Codex 競馬予想マルチエージェント — Agent × Skill × Prompt / 地方・中央対応

VS CodeのCodexに `$local-full-prediction 今日の園田10R` または `$central-full-prediction 次の東京11R` と入力し、Web検索と専門Agentで調査・分析する**プロンプト構成キット**です。ChatGPT Plusで利用可能なCodexの範囲で試せます（利用枠に制限あり）。OpenAI APIキー不要。**実運用・Web取得の成功は未検証**。

## 3層の役割

| 種別 | 場所 | 意味 |
|---|---|---|
| Agent | `.codex/agents/*.toml` | 誰が調査・分析するか。地方と中央で同じ5体を再利用 |
| Skill | `.agents/skills/*/SKILL.md` | どのAgentをどの順で呼ぶか。6つのワークフロー |
| Prompt | `local/prompts/` / `central/prompts/` | 実際の予想基準。地方v9と中央初期版を**完全分離** |
| `AGENTS.md` | ルート | 全Skillに共通する守るべき事項のみ。起動スクリプトではない |

## フォルダ概観

```text
keiba-codex-agent-skills/
├── AGENTS.md
├── .codex/
│   ├── config.toml            # Web検索 live / Agent 設定
│   └── agents/               # 情報収集・能力・馬場展開・オッズ・買い目 の5 Agent
├── .agents/skills/           # local-* / central-* 各3 Skill（計6）
├── local/
│   ├── prompts/INDEX.md      # 地方専用Agentルーティング
│   ├── prompts/...           # 元の地方v9を27 Markdownに分割した正本
│   ├── archive/...           # 元v9と移行manifest
│   └── predictions/          # 予想ログ
├── central/
│   ├── prompts/INDEX.md      # 中央専用Agentルーティング
│   ├── prompts/...           # JRA用の初期ルール（独立・今後拡張可能）
│   └── predictions/
└── scripts/validate_project.py
```

## VS Codeで開始

1. ZIPを解凍し、この**ルートフォルダ**をVS Codeで開く。
2. Codex拡張機能をインストールしてChatGPTアカウントでログイン。必要に応じてワークスペースを信頼する。
3. Codexチャットの入力欄で `$` を打ってスキル一覧を確認。読み込めない場合は拡張機能の更新/再起動とフォルダの開き直しを試す。
4. 下のいずれかを入力。必要なら公式サイトへのWebアクセス許可を与える（検索だけで全情報が見つかる保証はない）。

### 呼び出し例（6 Skill）

| やりたいこと | Codexチャット入力 |
|---|---|
| 地方の当日情報だけ | `$local-race-info 今日の園田10Rの情報だけ調べて` |
| 地方の総合予想 | `$local-full-prediction 今日の園田10Rを予想して` |
| 地方オッズだけ確認 | `$local-odds-check 園田10Rの最新オッズを確認して` |
| 中央の当日情報だけ | `$central-race-info 次の東京11Rの出馬表を調べて` |
| 中央の総合予想 | `$central-full-prediction 次の東京11Rを予想して` |
| 中央オッズだけ確認 | `$central-odds-check 東京11Rの最新オッズを確認して` |

特に**当日情報だけ**のSkillは `race_researcher` のみ呼びます。予想・買い目・他のサブAgentは起動しない想定です。

## 予想Skillの実行順

1. 情報収集 `race_researcher`。
2. 能力 `form_analyst` と馬場・展開 `track_pace_analyst` を（オッズ抜きで）分析。
3. メインが能力印を確定。
4. `odds_analyst` が価格/人気を分析し、印は変更しない。
5. `bet_strategy_analyst` が買い目・見送りを検討。

## 変更の仕方（重複編集を避ける）

- たとえば地方C3のルールだけ変更：`local/prompts/analysis/low_class.md` のみ編集。
- 中央の芝・ダートの適性判断だけ変更：`central/prompts/analysis/course_track.md` のみ編集。
- 専門Agentの**役割**変更：該当 `.codex/agents/*.toml` を変更。
- 専門Agentの**実行順や起動対象**変更：該当 `.agents/skills/*/SKILL.md` を変更。
- 新しいプロンプトファイル**追加**時だけ、担当する `local/prompts/INDEX.md` または `central/prompts/INDEX.md` に登録。
- **元の地方v9全文は `local/archive/` に保全**。現行実行では読まないので正本が二重化しない。

## 制限と注意

- `central/prompts/` は**新規作成の初期草案**であり、ユーザー提供の中央用独自プロンプトは反映されていません。地方v9をJRAへコピーしていません。
- このキットは**プロンプト・設定だけ**で、公式サイトからの自動CSVダウンロードや専用APIクライアントは未実装。Web検索では最新オッズ、全頭近5走、騎手成績が欠けることがあります。検索できない場合は必ず欠損を表示します。
- 競馬場別の元ファイルと、地方v9内で参照される調査レビュー文書は未提供のため未収録。
- 発走後の確定結果を「発走前の予想」として扱いません。自動投票・決済は一切しません。
- ZIPはコード/Markdown/設定の構文と参照整合を検証済みですが、**実際のVS Code + Codex上でのSubagent起動・Web検索成功までは確認できていません**。
- 複数AgentはCodexの利用枠を消費します。APIキー契約は不要ですが、追加利用が発生する契約オプション等は各自の設定に依存します。

## オフライン検証

Python 3.11以上で実行：

```bash
python scripts/validate_project.py
python scripts/validate_project.py --verify-local-v9
```

2つ目は**移行直後の地方v9全文が原本と一致するか**の初回比較用。ルールMarkdownを改訂したあとは差分が出て正常です。

## 設定仕様（公式資料）

- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/multi-agent
- https://developers.openai.com/codex/guides/agents-md
- https://developers.openai.com/codex/config-basic
