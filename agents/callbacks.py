from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse

# モデル呼び出し回数をカウントするグローバル変数
model_call_count = 0


async def get_token(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    """モデルが呼ばれるたびにカウントを増やす"""
    global model_call_count

    if llm_response and hasattr(llm_response, "usage_metadata"):
        usage = llm_response.usage_metadata
        if usage and hasattr(usage, "total_token_count"):
            model_call_count += 1
            print(f"🔔 モデル呼び出し #{model_call_count} (total_tokens: {usage.total_token_count})")

    return None


async def log_token_usage(callback_context: CallbackContext) -> None:
    """
    エージェントの処理完了後にトークン使用量とイベント情報をログ出力するコールバック関数
    """
    global model_call_count

    session = getattr(callback_context, "session", None)

    if not session or not getattr(session, "events", None):
        return

    # モデル呼び出し回数が0の場合は何もしない
    if model_call_count == 0:
        return

    # モデル呼び出し回数分のイベントを取得
    print(f"\n🔍 モデル呼び出し回数: {model_call_count}")
    print("=" * 80)

    # 最新からmodel_call_count個のAI応答イベントを取得
    ai_events = []
    for event in reversed(session.events):
        if hasattr(event, "content") and hasattr(event.content, "role"):
            if event.content.role == "model":
                ai_events.append(event)
                if len(ai_events) >= model_call_count:
                    break

    # AI応答イベントを古い順に並び替え（最初に呼ばれたものから順に表示）
    ai_events.reverse()

    if not ai_events:
        model_call_count = 0  # カウンターをリセット
        return

    # 各AI応答イベントに対して情報を出力
    for idx, ai_event in enumerate(ai_events, 1):
        # このAI応答の直前のユーザーメッセージを探す
        user_event = None
        ai_event_found = False
        for event in reversed(session.events):
            # まずこのAI応答イベントを見つける
            if event.id == ai_event.id:
                ai_event_found = True
                continue
            # AI応答イベントが見つかった後、最初のユーザーイベントを取得
            if ai_event_found:
                if hasattr(event, "content") and hasattr(event.content, "role"):
                    if event.content.role == "user":
                        user_event = event
                        break

        # 情報を抽出
        event_id = ai_event.id
        app_name = session.app_name
        user_id = session.user_id
        session_id = session.id
        user_message = (
            user_event.content.parts[0].text
            if user_event and user_event.content.parts
            else None
        )
        ai_response = (
            ai_event.content.parts[0].text if ai_event.content.parts else None
        )

        # トークン使用量を取得
        usage = ai_event.usage_metadata
        input_tokens = usage.prompt_token_count if usage else 0
        output_tokens = usage.candidates_token_count if usage else 0
        total_tokens = usage.total_token_count if usage else 0

        # 情報を出力
        print(f"\n📊 イベント #{idx}/{model_call_count}:")
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

    # カウンターをリセット
    model_call_count = 0
