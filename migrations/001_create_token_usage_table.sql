-- マイグレーション: トークン使用量記録テーブルの作成
-- 作成日: 2025-10-16

-- トークン使用量を記録するテーブル
CREATE TABLE IF NOT EXISTS token_usage (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(128) NOT NULL,
    app_name VARCHAR(128) NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    session_id VARCHAR(128) NOT NULL,
    user_message TEXT,
    ai_response TEXT,
    input_tokens INT,
    thoughts_tokens INT,
    output_tokens INT,
    total_tokens INT,

    -- 外部キー制約（eventsテーブルへの複合外部キー）
    -- eventsテーブルの (id, app_name, user_id, session_id) を参照
    CONSTRAINT fk_events_composite
        FOREIGN KEY (event_id, app_name, user_id, session_id)
        REFERENCES events(id, app_name, user_id, session_id)
        ON DELETE CASCADE
);

-- インデックスの作成
CREATE INDEX IF NOT EXISTS idx_token_usage_event_id ON token_usage(event_id);
CREATE INDEX IF NOT EXISTS idx_token_usage_session_id ON token_usage(session_id);
CREATE INDEX IF NOT EXISTS idx_token_usage_user_id ON token_usage(user_id);
CREATE INDEX IF NOT EXISTS idx_token_usage_app_name ON token_usage(app_name);

-- コメントの追加
COMMENT ON TABLE token_usage IS 'トークン使用量とイベント情報を記録するテーブル';
COMMENT ON COLUMN token_usage.event_id IS 'eventsのid';
COMMENT ON COLUMN token_usage.app_name IS 'アプリ名';
COMMENT ON COLUMN token_usage.user_id IS 'ユーザID';
COMMENT ON COLUMN token_usage.session_id IS 'セッションID';
COMMENT ON COLUMN token_usage.user_message IS 'ユーザの発話内容';
COMMENT ON COLUMN token_usage.ai_response IS 'AIの応答内容';
COMMENT ON COLUMN token_usage.input_tokens IS '入力トークン数';
COMMENT ON COLUMN token_usage.thoughts_tokens IS '内部推論トークン数';
COMMENT ON COLUMN token_usage.output_tokens IS '出力トークン数';
COMMENT ON COLUMN token_usage.total_tokens IS '合計トークン数';
