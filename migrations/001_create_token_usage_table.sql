-- トークン使用量を記録するテーブルを作成
-- このテーブルは各LLM呼び出しのトークン使用量を保存します

CREATE TABLE IF NOT EXISTS token_usage (
    -- 主キー（自動採番）
    id SERIAL PRIMARY KEY,

    -- セッションID（ADKのsessionsテーブルと紐付け可能）
    session_id VARCHAR(255) NOT NULL,

    -- エージェント名（どのエージェントがトークンを使用したか）
    agent_name VARCHAR(100) NOT NULL,

    -- トークン使用時刻
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- 入力トークン数（プロンプト）
    input_tokens INTEGER NOT NULL DEFAULT 0,

    -- 出力トークン数（応答）
    output_tokens INTEGER NOT NULL DEFAULT 0,

    -- 合計トークン数
    total_tokens INTEGER NOT NULL DEFAULT 0,

    -- 使用モデル名（例: gemini-2.0-flash）
    model_name VARCHAR(100),

    -- ユーザーID（オプション）
    user_id VARCHAR(255),

    -- 呼び出しID（ADKの invocation_id と紐付け可能）
    invocation_id VARCHAR(255)
);

-- インデックスの作成（検索パフォーマンス向上のため）

-- セッションIDでの検索を高速化
CREATE INDEX IF NOT EXISTS idx_token_usage_session_id ON token_usage(session_id);

-- エージェント名での検索を高速化
CREATE INDEX IF NOT EXISTS idx_token_usage_agent_name ON token_usage(agent_name);

-- 日時範囲での検索を高速化
CREATE INDEX IF NOT EXISTS idx_token_usage_timestamp ON token_usage(timestamp DESC);

-- ユーザーIDでの検索を高速化（NULL値も含む）
CREATE INDEX IF NOT EXISTS idx_token_usage_user_id ON token_usage(user_id) WHERE user_id IS NOT NULL;

-- コメント追加（テーブルとカラムの説明）
COMMENT ON TABLE token_usage IS 'ADKマルチエージェントシステムのトークン使用量を記録するテーブル';
COMMENT ON COLUMN token_usage.id IS '主キー（自動採番）';
COMMENT ON COLUMN token_usage.session_id IS 'セッションID（ADKのsessionsテーブルと紐付け）';
COMMENT ON COLUMN token_usage.agent_name IS 'エージェント名（root_agent, coffee_agent, tea_agentなど）';
COMMENT ON COLUMN token_usage.timestamp IS 'トークン使用時刻';
COMMENT ON COLUMN token_usage.input_tokens IS '入力トークン数（プロンプト）';
COMMENT ON COLUMN token_usage.output_tokens IS '出力トークン数（応答）';
COMMENT ON COLUMN token_usage.total_tokens IS '合計トークン数';
COMMENT ON COLUMN token_usage.model_name IS '使用したLLMモデル名';
COMMENT ON COLUMN token_usage.user_id IS 'ユーザーID';
COMMENT ON COLUMN token_usage.invocation_id IS 'ADKの呼び出しID';
