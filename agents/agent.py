import logging
from typing import Optional

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse
from agents.instruction import INSTRUCTION

from agents.coffee_agent.agent import coffee_agent
from agents.tea_agent.agent import tea_agent

# サブエージェントをインポート
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# ロガーの設定（トークン使用量をログ出力するために使用）
logger = logging.getLogger(__name__)


async def log_token_usage(_: CallbackContext, llm_response: LlmResponse,) -> Optional[LlmResponse]:
    """
    LLMからのレスポンス後にトークン使用量をログ出力するコールバック関数

    この関数はLLMが応答を返すたびに自動的に呼び出されます。
    usage_metadataからトークン数を取得してログに記録します。
    """
    # レスポンスにusage_metadata（トークン使用量情報）が含まれているかチェック
    if llm_response and hasattr(llm_response, "usage_metadata"):
        usage = llm_response.usage_metadata
        if usage:
            # 各トークン数を取得
            input_tokens = getattr(usage, "prompt_token_count", 0)      # 入力トークン数（プロンプト）
            output_tokens = getattr(usage, "candidates_token_count", 0)  # 出力トークン数（応答）
            total_tokens = getattr(usage, "total_token_count", 0)        # 合計トークン数

            # トークン使用量をINFOレベルでログ出力
            # uv run adk web --log_level info で実行すると表示されます
            logger.info(
                f"[TOKEN USAGE] Input: {input_tokens}, Output: {output_tokens}, Total: {total_tokens}"
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
