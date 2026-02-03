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

### バッチ実行
CSVファイルから質問を読み込んで一括処理：

```bash
uv run -m batch.run_agent_sample
```
