import logging
from typing import Optional

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse
from agents.instruction import INSTRUCTION

from agents.coffee_agent.agent import coffee_agent
from agents.tea_agent.agent import tea_agent
from utils.token_logger import log_and_save_token_usage

# サブエージェントをインポート
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# ロガーの設定（トークン使用量をログ出力するために使用）
logger = logging.getLogger(__name__)


async def log_token_usage(
    callback_context: CallbackContext,
    llm_response: LlmResponse,
) -> Optional[LlmResponse]:
    """
    LLMからのレスポンス後にトークン使用量をログ出力・DB保存するコールバック関数

    この関数はLLMが応答を返すたびに自動的に呼び出されます。
    usage_metadataからトークン数を取得してログに記録し、データベースに保存します。
    """
    # レスポンスにusage_metadata（トークン使用量情報）が含まれているかチェック
    if llm_response and hasattr(llm_response, "usage_metadata"):
        usage = llm_response.usage_metadata
        if usage:
            # 各トークン数を取得
            input_tokens = getattr(usage, "prompt_token_count", 0)      # 入力トークン数（プロンプト）
            output_tokens = getattr(usage, "candidates_token_count", 0)  # 出力トークン数（応答）
            total_tokens = getattr(usage, "total_token_count", 0)        # 合計トークン数

            # CallbackContextのstateからセッションIDを取得（可能な場合）
            # セッションIDはstateに保存されている必要があります
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
            except Exception as e:
                logger.debug(f"Error getting user message: {e}")

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
            except Exception as e:
                logger.debug(f"Error getting AI response: {e}")
                ai_response = None

            # トークン使用量をログ出力してDBに保存
            log_and_save_token_usage(
                agent_name="root_agent",
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

root_agent = Agent(
    name="root_agent",
    description="飲み物の案内人として、コーヒーや紅茶の専門エージェントに適切にルーティングします",
    model="gemini-2.0-flash",
    instruction=INSTRUCTION,
    sub_agents=[coffee_agent, tea_agent],
    after_model_callback=log_token_usage
)
