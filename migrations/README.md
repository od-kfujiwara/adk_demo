# データベースマイグレーション

このディレクトリにはデータベーススキーマのマイグレーションファイルが含まれています。

## マイグレーションの実行方法

### 1. マイグレーションの適用

```bash
# PostgreSQLに接続
psql postgresql://adk_user:adk_password@localhost:5432/adk_sessions

# マイグレーションを実行
\i migrations/001_create_token_usage_table.sql
```

または、コマンドラインから直接実行：

```bash
psql postgresql://adk_user:adk_password@localhost:5432/adk_sessions -f migrations/001_create_token_usage_table.sql
```

### 2. ロールバック（元に戻す）

```bash
psql postgresql://adk_user:adk_password@localhost:5432/adk_sessions -f migrations/001_rollback.sql
```

## マイグレーションファイルの命名規則

- `NNN_description.sql`: マイグレーション本体
- `NNN_rollback.sql`: ロールバック用スクリプト

NNNは連番（001, 002, 003...）で、実行順序を示します。

## テーブル一覧

### token_usage テーブル

AIモデルのトークン使用量とイベント情報を記録します。

| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| id | SERIAL | PRIMARY KEY | 自動採番ID |
| event_id | VARCHAR(128) | NOT NULL, FK | イベントID |
| app_name | VARCHAR(128) | NOT NULL | アプリケーション名 |
| user_id | VARCHAR(128) | NOT NULL | ユーザID |
| session_id | VARCHAR(128) | NOT NULL, FK | セッションID |
| user_message | TEXT | | ユーザの発話内容 |
| ai_response | TEXT | | AIの応答内容 |
| input_tokens | INT | | 入力トークン数 |
| output_tokens | INT | | 出力トークン数 |
| total_tokens | INT | | 合計トークン数 |
| created_at | TIMESTAMP | DEFAULT NOW() | レコード作成日時 |

### インデックス

- `idx_token_usage_event_id`: event_idでの検索用
- `idx_token_usage_session_id`: session_idでの検索用
- `idx_token_usage_user_id`: user_idでの検索用
- `idx_token_usage_app_name`: app_nameでの検索用
- `idx_token_usage_created_at`: 日時での検索・ソート用
