import logging
from typing import Optional

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse

# ロガーの設定（コーヒーエージェントのトークン使用量をログ出力するために使用）
logger = logging.getLogger(__name__)


async def log_token_usage(_: CallbackContext, llm_response: LlmResponse,) -> Optional[LlmResponse]:
    """
    コーヒーエージェントのトークン使用量をログ出力するコールバック関数

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

            # coffee_agentであることを明示してログ出力
            logger.info(
                f"[TOKEN USAGE - coffee_agent] Input: {input_tokens}, Output: {output_tokens}, Total: {total_tokens}"
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
