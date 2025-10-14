-- token_usageテーブルに会話内容カラムを追加
-- ユーザー発話とAI応答を保存できるようにする

-- ユーザーの発話内容を保存するカラムを追加
ALTER TABLE token_usage
ADD COLUMN IF NOT EXISTS user_message TEXT;

-- AIの応答内容を保存するカラムを追加
ALTER TABLE token_usage
ADD COLUMN IF NOT EXISTS ai_response TEXT;

-- コメント追加
COMMENT ON COLUMN token_usage.user_message IS 'ユーザーの発話内容';
COMMENT ON COLUMN token_usage.ai_response IS 'AIの応答内容';
