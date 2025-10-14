# ADK Demo - マルチエージェントシステム

Google Agent Development Kit (ADK)を使用した飲み物案内マルチエージェントのデモプロジェクトです。

## 機能

- **マルチエージェント構成**: コーヒーエージェントと紅茶エージェントが専門知識で応答
- **トークン使用量のモニタリング**: 各会話のトークン数（input/output/total）をリアルタイムでログ出力
- **会話履歴の永続化**: PostgreSQLを使って会話履歴を自動保存
- **トークン使用量のDB保存**: 各LLM呼び出しのトークン使用量を専用テーブルに記録し、後から分析可能

## セットアップ

### 1. 依存パッケージのインストール
```bash
uv sync
```

### 2. 環境変数の設定
`.env`ファイルを作成し、Google API Keyを設定してください：

```
GOOGLE_API_KEY=your_api_key_here
```

### 3. PostgreSQLの起動
Docker Composeを使ってPostgreSQLを起動します：

```bash
docker compose up -d
```

データベースの起動確認：

```bash
docker compose ps
```

### 4. データベースマイグレーション（初回のみ）

トークン使用量を保存するテーブルを作成します：

```bash
uv run python scripts/run_migration.py
```

成功すると、`token_usage`テーブルが作成されます。

## 使用方法
### ADK Web UIの起動
PostgreSQLに会話履歴を保存しながらADKを起動：

```bash
uv run adk web --session_service_uri postgresql://adk_user:adk_password@localhost:5432/adk_sessions --log_level info
```

ブラウザで表示されたURLにアクセスして、エージェントと会話できます。

### トークン使用量の確認

#### コンソールログ
コンソールに以下のようなログが表示されます：

```
INFO:utils.token_logger:[TOKEN USAGE - root_agent] Input: 150, Output: 200, Total: 350
INFO:utils.token_logger:[TOKEN USAGE - coffee_agent] Input: 100, Output: 150, Total: 250
```

#### データベースから確認
PostgreSQLに接続してトークン使用量を確認：

```bash
# PostgreSQLに接続
docker compose exec postgres psql -U adk_user -d adk_sessions

# 最近のトークン使用量を表示
SELECT timestamp, agent_name, input_tokens, output_tokens, total_tokens
FROM token_usage
ORDER BY timestamp DESC
LIMIT 10;

# エージェント別の集計
SELECT agent_name, COUNT(*) as calls, SUM(total_tokens) as total
FROM token_usage
GROUP BY agent_name;

# 終了
\q
```

#### 分析用SQLの実行
[queries/token_usage_analysis.sql](queries/token_usage_analysis.sql)には様々な分析用SQLが用意されています：
- 全体のトークン使用量サマリー
- エージェント別の集計
- 時系列分析（日別・時間帯別）
- セッション別の分析
- コスト推定
- 異常検知

## プロジェクト構成

```
.
├── agents/
│   ├── agent.py              # ルートエージェント
│   ├── coffee_agent/
│   │   └── agent.py          # コーヒー専門エージェント
│   ├── tea_agent/
│   │   └── agent.py          # 紅茶専門エージェント
│   └── instruction.py        # エージェントの指示
├── batch/
│   └── run_agent_sample.py   # バッチ実行用スクリプト
├── migrations/
│   └── 001_create_token_usage_table.sql  # DBマイグレーション
├── models/
│   └── token_usage.py        # トークン使用量モデル
├── queries/
│   └── token_usage_analysis.sql  # 分析用SQLサンプル
├── scripts/
│   └── run_migration.py      # マイグレーション実行スクリプト
├── utils/
│   └── token_logger.py       # トークンロギングユーティリティ
├── docker-compose.yml        # PostgreSQL設定
├── pyproject.toml            # 依存パッケージ定義
└── .env                      # 環境変数（Git管理外）
```

## データベース管理
### PostgreSQLコンテナの停止

```bash
docker compose down
```

### データベースの完全削除（データも削除）

```bash
docker compose down -v
```

### PostgreSQLに直接接続

```bash
docker compose exec postgres psql -U adk_user -d adk_sessions
```

## トラブルシューティング
### PostgreSQLに接続できない

1. コンテナが起動しているか確認：
   ```bash
   docker compose ps
   ```

2. ログを確認：
   ```bash
   docker compose logs postgres
   ```

### トークン使用量が表示されない
`--log_level info`オプションを指定していることを確認してください。

## 開発
### 新しいエージェントの追加
1. `agents/`配下に新しいディレクトリを作成
2. `agent.py`を作成してエージェントを定義
3. `agents/agent.py`でサブエージェントとして登録

### バッチ実行
CSVファイルから質問を読み込んで一括処理：

```bash
uv run -m batch.run_agent_sample
```

## ライセンス
このプロジェクトはデモ用です。
