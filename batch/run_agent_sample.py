import asyncio

from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agents.agent import root_agent
from dotenv import load_dotenv

# .envを読み込む
load_dotenv()


async def main():
    # セッション用意
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="demo",
        user_id="user"
    )

    # ランナー作成
    runner = Runner(
        agent=root_agent,
        session_service=session_service,
        app_name="demo"
    )

    # 投げたい質問
    content = types.Content(
        role="user",
        parts=[types.Part(text="おすすめのホットドリンクは？")]
    )

    # 実行して最終応答だけ取得
    answer = ""
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                answer = event.content.parts[0].text
            else:
                answer = ""

    print(answer, end="")

if __name__ == "__main__":
    asyncio.run(main())
