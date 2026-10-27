# Codex 競馬予想マルチエージェント（ローカル試作キット）

Codex IDE拡張機能をChatGPTアカウントで使い、メイン（AGENTS.md）+ 専門サブエージェント3体（TOML）で、競馬予想を試すための設定一式です。**独立して起動するWebアプリや自動取得ツールはまだ含まれません**。

## セットアップ（Windows 11 + VS Code想定）
1. このZIPを展開します。フォルダごとVS Codeで開き、ワークスペースを信頼します。
2. VS Code公式のCodex拡張機能をインストールして、ChatGPTアカウントでサインインしてください（APIキー不要）。
   - https://marketplace.visualstudio.com/items?itemName=OpenAI.chatgpt
   - https://developers.openai.com/codex/ide/
3. Codexサイドバーで新しいローカルチャットを開きます。設定やエージェント定義が反映されない場合は、新しいチャットにするかVS Codeを再読み込みしてください。
4. 以下のデモ用プロンプトを入力します。

```
デモデータ data/demo/demo_race.json を使って架空競馬場10Rを予想して。
past_run_analyst、odds_analyst、track_analystをそれぞれサブエージェントとして起動し、
独立して分析させた後で結果を統合してください。
これは架空のデモであると明示し、根拠・不明点・最終順位を説明して。
```

## 実際のレースを分析する
地方競馬情報サイトの「本日のレース情報」ページにある当日データダウンロード機能から、
当日のレース情報ZIPとオッズ情報ZIPを取得し、展開したCSVを `data/input/` に入れてください。
当日CSVは場ごとやレースごとではなく当日全体の場合があります。`YYYYMMDD_racelist.csv`, `YYYYMMDD_horselist.csv`, `YYYYMMDD_odds.csv` のようなファイルを検索して利用します。

- 公式サイト: https://www.keiba.go.jp/
- 公式データ説明書: https://www.keiba.go.jp/pdf/manual/data_pdf_manual.pdf

Codexで次のように依頼します。

```
今日の園田10Rを予想して。
data/input/ にある公式CSVから対象日・園田・10Rのデータだけを取り出し、
必要な専門サブエージェントを起動して評価を統合して。
実在する情報だけを使用し、更新日時と欠損情報も示して。
```

### 補足
- `data/input/` が空の場合、本番レースの実データの予想はできません。新規の自動ダウンロード機能は未実装です。
- 過去走情報をより豊富に使う場合は、月次ファイルなどを `data/archive/` に展開してください。巨大なファイルをCodexに丸ごと読み込ませず、必要な条件で絞る処理を次のステップでTypeScript等で実装するのがおすすめです。
- 出馬表に載る一部の成績集計だけでも初期分析は可能ですが、直近数走の詳細と同じ意味ではありません。
- 当日のデータ取得が必要な場合は、公式規約に準拠した取得方法と更新頻度を確認してから自動化してください。
- ChatGPT PlusでCodexを動かす範囲では追加のAPIキーは不要ですが、利用枠の制限はあります。複数のサブエージェントを動かすと利用枠をより消費する可能性があります。
- 各エージェントは「専門的な指示を持つCodexのサブスレッド」です。独立した追加課金モデルを作ったり、常駐するサーバを立てたりするものではありません。

## ディレクトリ構成
```
AGENTS.md                     メインエージェントの全体方針
.codex/config.toml            マルチエージェント設定
.codex/agents/*.toml          専門エージェント3体
data/demo/demo_race.json       架空デモ（テスト専用）
data/input/                   当日CSVの格納場所
data/archive/                 過去CSVの格納場所
```
