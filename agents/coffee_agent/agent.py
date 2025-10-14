import logging
from typing import Optional

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse
from utils.token_logger import log_and_save_token_usage

# ロガーの設定（コーヒーエージェントのトークン使用量をログ出力するために使用）
logger = logging.getLogger(__name__)


async def log_token_usage(
    callback_context: CallbackContext,
    llm_response: LlmResponse,
) -> Optional[LlmResponse]:
    """
    コーヒーエージェントのトークン使用量をログ出力・DB保存するコールバック関数

    この関数はcoffee_agentがLLMから応答を受け取るたびに自動的に呼び出されます。
    """
    # レスポンスにusage_metadata（トークン使用量情報）が含まれているかチェック
    if llm_response and hasattr(llm_response, "usage_metadata"):
        usage = llm_response.usage_metadata
        if usage:
            # 各トークン数を取得
            input_tokens = getattr(usage, "prompt_token_count", 0)      # 入力トークン数
            output_tokens = getattr(usage, "candidates_token_count", 0)  # 出力トークン数
            total_tokens = getattr(usage, "total_token_count", 0)        # 合計トークン数

            # CallbackContextのstateからセッションIDを取得（可能な場合）
            if hasattr(callback_context, "state"):
                session_id = callback_context.state.get("_session_id", "unknown")
                user_id = callback_context.state.get("_user_id", None)
            else:
                session_id = "unknown"
                user_id = None

            # ユーザーの発話とAIの応答を取得
            user_message = None
            ai_response = None

            # callback_contextからユーザーメッセージを取得
            user_message = None
            try:
                if hasattr(callback_context, 'user_content') and callback_context.user_content:
                    user_content = callback_context.user_content
                    if hasattr(user_content, 'parts') and user_content.parts:
                        for part in user_content.parts:
                            if hasattr(part, 'text') and part.text:
                                user_message = part.text
                                break
            except Exception:
                user_message = None

            # LLMの応答から応答テキストを取得
            ai_response = None
            try:
                if hasattr(llm_response, 'content') and llm_response.content:
                    content = llm_response.content
                    if hasattr(content, 'parts') and content.parts:
                        for part in content.parts:
                            if hasattr(part, 'text') and part.text:
                                ai_response = part.text
                                break
            except Exception:
                ai_response = None

            # トークン使用量をログ出力してDBに保存
            log_and_save_token_usage(
                agent_name="coffee_agent",
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                session_id=session_id,
                user_id=user_id,
                model_name="gemini-2.0-flash",
                user_message=user_message,
                ai_response=ai_response,
            )

    return None


coffee_agent = Agent(
    name="coffee_agent",
    description="コーヒーに関する専門知識を持つエージェント",
    model="gemini-2.0-flash",
    instruction="""
    あなたはコーヒーの専門家です。
    コーヒーの種類、淹れ方、豆の特徴、カフェのおすすめなど、コーヒーに関するあらゆる質問に専門的に答えてください。
    """,
    after_model_callback=log_token_usage
)
