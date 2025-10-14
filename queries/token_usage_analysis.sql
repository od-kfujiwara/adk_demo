-- トークン使用量分析用のSQLクエリサンプル

-- ==========================================
-- 1. 基本的な集計
-- ==========================================

-- 全体のトークン使用量サマリー
SELECT
    COUNT(*) AS total_calls,
    SUM(input_tokens) AS total_input_tokens,
    SUM(output_tokens) AS total_output_tokens,
    SUM(total_tokens) AS total_tokens,
    AVG(input_tokens) AS avg_input_tokens,
    AVG(output_tokens) AS avg_output_tokens,
    AVG(total_tokens) AS avg_total_tokens
FROM token_usage;

-- ==========================================
-- 2. エージェント別の集計
-- ==========================================

-- エージェントごとのトークン使用量
SELECT
    agent_name,
    COUNT(*) AS call_count,
    SUM(input_tokens) AS total_input,
    SUM(output_tokens) AS total_output,
    SUM(total_tokens) AS total,
    AVG(total_tokens) AS avg_tokens_per_call
FROM token_usage
GROUP BY agent_name
ORDER BY total DESC;

-- ==========================================
-- 3. 時系列分析
-- ==========================================

-- 日別のトークン使用量
SELECT
    DATE(timestamp) AS date,
    COUNT(*) AS call_count,
    SUM(total_tokens) AS daily_total_tokens,
    AVG(total_tokens) AS avg_tokens_per_call
FROM token_usage
GROUP BY DATE(timestamp)
ORDER BY date DESC;

-- 時間帯別のトークン使用量（1時間ごと）
SELECT
    DATE_TRUNC('hour', timestamp) AS hour,
    COUNT(*) AS call_count,
    SUM(total_tokens) AS hourly_total_tokens
FROM token_usage
GROUP BY DATE_TRUNC('hour', timestamp)
ORDER BY hour DESC;

-- ==========================================
-- 4. セッション別の分析
-- ==========================================

-- セッションごとのトークン使用量（上位10件）
SELECT
    session_id,
    COUNT(*) AS interaction_count,
    SUM(total_tokens) AS session_total_tokens,
    MIN(timestamp) AS session_start,
    MAX(timestamp) AS session_end
FROM token_usage
WHERE session_id != 'unknown'
GROUP BY session_id
ORDER BY session_total_tokens DESC
LIMIT 10;

-- ==========================================
-- 5. ユーザー別の分析
-- ==========================================

-- ユーザーごとのトークン使用量
SELECT
    user_id,
    COUNT(*) AS call_count,
    SUM(total_tokens) AS user_total_tokens,
    AVG(total_tokens) AS avg_tokens_per_call
FROM token_usage
WHERE user_id IS NOT NULL
GROUP BY user_id
ORDER BY user_total_tokens DESC;

-- ==========================================
-- 6. コスト推定（参考）
-- ==========================================

-- トークン使用量からコスト推定
-- 注意: 実際の料金は各モデルの価格設定を確認してください
-- 例: Gemini 2.0 Flash の場合（2025年1月時点の仮想価格）
--   Input: $0.075 per 1M tokens
--   Output: $0.30 per 1M tokens

SELECT
    agent_name,
    SUM(input_tokens) AS total_input,
    SUM(output_tokens) AS total_output,
    SUM(total_tokens) AS total,
    -- 仮想的なコスト推定（実際の価格に置き換えてください）
    ROUND((SUM(input_tokens) * 0.075 / 1000000)::numeric, 4) AS estimated_input_cost_usd,
    ROUND((SUM(output_tokens) * 0.30 / 1000000)::numeric, 4) AS estimated_output_cost_usd,
    ROUND(((SUM(input_tokens) * 0.075 + SUM(output_tokens) * 0.30) / 1000000)::numeric, 4) AS estimated_total_cost_usd
FROM token_usage
GROUP BY agent_name
ORDER BY estimated_total_cost_usd DESC;

-- ==========================================
-- 7. 詳細なトークン使用履歴
-- ==========================================

-- 最近のトークン使用履歴（上位20件）
SELECT
    id,
    timestamp,
    agent_name,
    session_id,
    input_tokens,
    output_tokens,
    total_tokens,
    model_name
FROM token_usage
ORDER BY timestamp DESC
LIMIT 20;

-- ==========================================
-- 8. 異常検知
-- ==========================================

-- 平均より大幅に多いトークンを使用したリクエストを検出
WITH stats AS (
    SELECT
        AVG(total_tokens) AS avg_tokens,
        STDDEV(total_tokens) AS stddev_tokens
    FROM token_usage
)
SELECT
    t.id,
    t.timestamp,
    t.agent_name,
    t.session_id,
    t.total_tokens,
    s.avg_tokens,
    ROUND((t.total_tokens - s.avg_tokens) / s.stddev_tokens, 2) AS z_score
FROM token_usage t, stats s
WHERE t.total_tokens > s.avg_tokens + (2 * s.stddev_tokens)
ORDER BY t.total_tokens DESC;

-- ==========================================
-- 9. パフォーマンス監視
-- ==========================================

-- 直近1時間のトークン使用量推移（5分ごと）
SELECT
    DATE_TRUNC('minute', timestamp - (EXTRACT(MINUTE FROM timestamp)::int % 5 || ' minutes')::interval) AS time_bucket,
    COUNT(*) AS call_count,
    SUM(total_tokens) AS total_tokens,
    AVG(total_tokens) AS avg_tokens
FROM token_usage
WHERE timestamp >= NOW() - INTERVAL '1 hour'
GROUP BY time_bucket
ORDER BY time_bucket DESC;
