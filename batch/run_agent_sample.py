import asyncio
import csv

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.agent import root_agent

# .envを読み込む
load_dotenv()

CONCURRENCY_LIMIT = 5  # 同時実行数を制限
semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)


# 質問に対する回答を取得
async def run_question(qid: int, question: str) -> tuple[int, str, str]:
    async with semaphore:
        # セッション用意
        session_service = InMemorySessionService()
        session = await session_service.create_session(app_name="demo", user_id=f"user_{qid}")

        # ランナー作成
        runner = Runner(agent=root_agent, session_service=session_service, app_name="demo")

        content = types.Content(role="user", parts=[types.Part(text=question)])
        answer = ""
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                answer = (event.content.parts[0].text or "").strip()
        return qid, question, answer


async def main() -> None:
    # CSVから質問リストを読み込み
    questions = []
    with open("batch/questions.csv", newline="", encoding="utf-8") as qfile:
        reader = csv.DictReader(qfile)
        for row in reader:
            questions.append((int(row["id"]), row["question"]))

    # 質問を並列実行
    tasks = [run_question(qid, question) for qid, question in questions]
    results = await asyncio.gather(*tasks)

    # 結果をCSVに出力
    with open("batch/answers.csv", "w", newline="", encoding="utf-8") as afile:
        writer = csv.writer(afile)
        writer.writerow(["id", "question", "answer"])
        for qid, ques, ans in results:
            writer.writerow([qid, ques, ans])


if __name__ == "__main__":
    asyncio.run(main())

# uv run -m batch.questions_runner で実行
# poetry run python -m batch.questions_runner で実行
