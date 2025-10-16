import logging

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from agents.instruction import INSTRUCTION

from agents.coffee_agent.agent import coffee_agent
from agents.tea_agent.agent import tea_agent

# サブエージェントをインポート
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# ロガーの設定（トークン使用量をログ出力するために使用）
logger = logging.getLogger(__name__)


async def log_token_usage(
    callback_context: CallbackContext,
) -> None:
    """
    エージェントの処理完了後にトークン使用量とイベント情報をログ出力するコールバック関数

    この関数はエージェントの処理が完了するたびに自動的に呼び出されます。
    callback_contextから各種情報を取得してログに記録します。
    """
    # 基本情報を取得
    agent_name = getattr(callback_context, "agent_name", None)

    # セッション情報を取得
    session = getattr(callback_context, "session", None)
    event_id = None
    app_name = None
    user_id = None
    session_id = None
    user_message = None
    ai_response = None
    input_tokens = 0
    output_tokens = 0
    total_tokens = 0

    if session:
        app_name = getattr(session, "app_name", None)
        user_id = getattr(session, "user_id", None)
        session_id = getattr(session, "id", None)

        # イベントリストから最新のユーザーメッセージとAI応答を取得
        events = getattr(session, "events", [])
        if events:
            # 最後から逆順にイベントを確認
            for event in reversed(events):
                # AI応答を取得（まだ取得していない場合）
                if ai_response is None:
                    author = getattr(event, "author", None)
                    if author == agent_name:  # 現在のエージェントの応答
                        # AI応答イベントのIDを取得
                        event_id = getattr(event, "id", None)

                        content = getattr(event, "content", None)
                        if content:
                            parts = getattr(content, "parts", [])
                            if parts and hasattr(parts[0], "text"):
                                ai_response = parts[0].text

                        # トークン使用量を取得
                        usage_metadata = getattr(event, "usage_metadata", None)
                        if usage_metadata:
                            input_tokens = getattr(
                                usage_metadata, "prompt_token_count", 0
                            )
                            output_tokens = getattr(
                                usage_metadata, "candidates_token_count", 0
                            )
                            total_tokens = getattr(
                                usage_metadata, "total_token_count", 0
                            )

                # ユーザーメッセージを取得（まだ取得していない場合）
                if user_message is None:
                    content = getattr(event, "content", None)
                    if content:
                        role = getattr(content, "role", None)
                        if role == "user":
                            parts = getattr(content, "parts", [])
                            if parts and hasattr(parts[0], "text"):
                                user_message = parts[0].text

                # 両方取得できたらループを終了
                if user_message is not None and ai_response is not None:
                    break

    # 情報を出力
    print("\n" + "=" * 80)
    print("📊 イベント情報とトークン使用量:")
    print("=" * 80)
    print(f"🔑 event_id      : {event_id}")
    print(f"📱 app_name      : {app_name}")
    print(f"👤 user_id       : {user_id}")
    print(f"🔗 session_id    : {session_id}")
    print(f"💬 user_message  : {user_message}")
    print(f"🤖 ai_response   : {ai_response}")
    print(f"📥 input_tokens  : {input_tokens}")
    print(f"📤 output_tokens : {output_tokens}")
    print(f"📊 total_tokens  : {total_tokens}")
    print("=" * 80)

root_agent = Agent(
    name="root_agent",
    description="飲み物の案内人として、コーヒーや紅茶の専門エージェントに適切にルーティングします",
    model="gemini-2.0-flash",
    instruction=INSTRUCTION,
    sub_agents=[coffee_agent, tea_agent],
    after_agent_callback=log_token_usage,
)
