"""
トークン使用量をロギング・DB保存するユーティリティ

各エージェントのコールバック関数から共通で使用します。
"""

import logging
import os
from typing import Optional

from dotenv import load_dotenv
from models.token_usage import TokenUsageRepository

# .envファイルから環境変数を読み込む
load_dotenv()

logger = logging.getLogger(__name__)

# グローバル変数として TokenUsageRepository のインスタンスを保持
# 初回呼び出し時に初期化される
_repository: Optional[TokenUsageRepository] = None


def get_repository() -> Optional[TokenUsageRepository]:
    """
    TokenUsageRepository のシングルトンインスタンスを取得

    Returns:
        TokenUsageRepository インスタンス、または環境変数が未設定の場合は None
    """
    global _repository

    if _repository is None:
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            try:
                _repository = TokenUsageRepository(database_url)
                logger.info("TokenUsageRepository を初期化しました")
            except Exception as e:
                logger.error(f"TokenUsageRepository の初期化に失敗しました: {e}")
                _repository = None
        else:
            logger.warning("DATABASE_URL が設定されていません。トークン使用量はDBに保存されません。")

    return _repository


def log_and_save_token_usage(
    agent_name: str,
    input_tokens: int,
    output_tokens: int,
    total_tokens: int,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    model_name: Optional[str] = None,
    invocation_id: Optional[str] = None,
    user_message: Optional[str] = None,
    ai_response: Optional[str] = None,
) -> None:
    """
    トークン使用量をログ出力し、データベースに保存

    Args:
        agent_name: エージェント名
        input_tokens: 入力トークン数
        output_tokens: 出力トークン数
        total_tokens: 合計トークン数
        session_id: セッションID（オプション）
        user_id: ユーザーID（オプション）
        model_name: モデル名（オプション）
        invocation_id: 呼び出しID（オプション）
        user_message: ユーザーの発話内容（オプション）
        ai_response: AIの応答内容（オプション）
    """
    # コンソールにログ出力
    logger.info(
        f"[TOKEN USAGE - {agent_name}] Input: {input_tokens}, Output: {output_tokens}, Total: {total_tokens}"
    )

    # データベースに保存
    repository = get_repository()
    if repository and session_id:
        try:
            repository.save_token_usage(
                session_id=session_id,
                agent_name=agent_name,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                model_name=model_name,
                user_id=user_id,
                invocation_id=invocation_id,
                user_message=user_message,
                ai_response=ai_response,
            )
            logger.debug(f"トークン使用量をDBに保存しました: session_id={session_id}, agent={agent_name}")
        except Exception as e:
            logger.error(f"トークン使用量のDB保存に失敗しました: {e}")
    elif not repository:
        logger.debug("Repository が初期化されていないため、DBへの保存をスキップしました")
    elif not session_id:
        logger.debug("session_id が提供されていないため、DBへの保存をスキップしました")
