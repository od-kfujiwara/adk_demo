import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agents.agent import root_agent

async def test_basic_functionality():
    """基本的な動作確認テスト"""
    print("🧪 ADK 1.18.0 互換性テスト開始")

    # セッションサービス作成
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="upgrade_test",
        user_id="test_user"
    )
    print("✅ セッション作成成功")

    # ランナー作成
    runner = Runner(
        agent=root_agent,
        session_service=session_service,
        app_name="upgrade_test"
    )
    print("✅ ランナー作成成功")

    # テストメッセージ送信
    content = types.Content(
        role="user",
        parts=[types.Part(text="こんにちは")]
    )

    print("📤 テストメッセージ送信中...")
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.is_final_response():
            response_text = event.content.parts[0].text[:100]
            print(f"✅ レスポンス受信: {response_text}...")
            break

    print("🎉 互換性テスト完了")

if __name__ == "__main__":
    asyncio.run(test_basic_functionality())
