-- ロールバック: トークン使用量記録テーブルの削除
-- 作成日: 2025-10-16

-- インデックスの削除
DROP INDEX IF EXISTS idx_token_usage_created_at;
DROP INDEX IF EXISTS idx_token_usage_app_name;
DROP INDEX IF EXISTS idx_token_usage_user_id;
DROP INDEX IF EXISTS idx_token_usage_session_id;
DROP INDEX IF EXISTS idx_token_usage_event_id;

-- テーブルの削除
DROP TABLE IF EXISTS token_usage;
