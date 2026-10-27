---
name: central-race-info
description: JRA中央競馬の当日開催・出馬表・近5走・騎手・馬場・オッズをネットで情報収集するだけのSkill。予想や印・買い目はしない。
---


# 中央競馬 — 当日情報収集だけ

1. 対象日(JST)、JRA開催場、R番号を確定。開催予定・発走時刻を公式で確認する。
2. `central/prompts/INDEX.md` の `race_researcher` に割り当てられたMarkdownを読む。
3. **`race_researcher` だけを1体起動**し、`category=中央`、`race_key=YYYY-MM-DD|中央|場|R` を渡す。
4. JRA公式サイトを優先して出馬表、全頭近5走、騎手、芝/ダート/障害、距離、馬場、取消、オッズと日時を調査する。
5. URL、確認時刻、未確認項目を記載して報告。**印・評価順位・買い目・展開予想はしない**。
6. 中央のデータに地方v9のC3等の判断ルールを混ぜない。
