# ADK Demo - マルチエージェントシステム

Google Agent Development Kit (ADK)を使用した飲み物案内マルチエージェントのデモプロジェクトです。

## 機能

- **マルチエージェント構成**: コーヒーエージェントと紅茶エージェントが専門知識で応答
- **トークン使用量のモニタリング**: 各会話のトークン数（input/output/total）をリアルタイムでログ出力
- **会話履歴の永続化**: PostgreSQLを使って会話履歴を自動保存

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

## 使用方法
### ADK Web UIの起動
PostgreSQLに会話履歴を保存しながらADKを起動：

```bash
uv run adk web --session_service_uri postgresql://adk_user:adk_password@localhost:5432/adk_sessions --log_level info
```

ブラウザで表示されたURLにアクセスして、エージェントと会話できます。

### トークン使用量の確認
コンソールに以下のようなログが表示されます：

```
INFO:agents.agent:[TOKEN USAGE] Input: 150, Output: 200, Total: 350
INFO:agents.coffee_agent.agent:[TOKEN USAGE - coffee_agent] Input: 100, Output: 150, Total: 250
```

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
