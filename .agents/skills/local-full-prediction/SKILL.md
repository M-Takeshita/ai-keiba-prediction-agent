---
name: local-full-prediction
description: 地方競馬のレースを総合予想するSkill。公式データ検索、能力・馬場分析、能力印確定、オッズ・買い目・見送りまで順番に5体の専門Agentへ依頼する。
---


# 地方競馬 — 総合予想

## 準備
- `local/prompts/INDEX.md` を読んで `main` のルール、`local/prompts/workflow/procedure.md`、`local/prompts/output/format.md` に従う。必要な場別プロンプトが提供されていれば読む。
- 対象を `YYYY-MM-DD|地方|場|R` と定義し、開催日・発走時刻を検証。発走済みを事前予想として扱わない。

## 実行順
1. **`race_researcher`** に公式優先の最新Web検索を依頼。公式事実、全頭過去5走、騎手、馬場、オッズ、時刻、未確認を取得。取得できない項目は欠損とする。
2. **`form_analyst` と `track_pace_analyst`** を起動し、**人気とオッズを一切渡さず**事実情報だけで能力・再現性と馬場・展開を分析してもらう。2つは並列依頼してよい。
3. メインが **オッズを見ず** `local/prompts/workflow/procedure.md` の評価順序で印順位・軸候補と不確実性を決定。判断できなければ未確定とする。
4. **`odds_analyst`** に確定印と市場情報を渡し、印を変えず人気・妙味・リスクを評価してもらう。
5. **`bet_strategy_analyst`** に能力印・展開・オッズ分析を渡し、買い目の成立根拠と見送りを検討してもらう。
6. メインが `local/prompts/output/horse_table.md` の**全頭10列表**を含め、地方v9の `local/prompts/output/format.md` を守って結果を出す。

## 禁止
- 中央競馬のルールを混ぜない。オッズだけで印を変更しない。外部情報を捏造しない。実際の投票・課金はしない。
- 情報が不足して買い目を判断できない場合は見送りや保留を示す。
