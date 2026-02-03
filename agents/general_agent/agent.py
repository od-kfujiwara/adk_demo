import datetime
import holidays
from typing import Optional
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from agents.callbacks import get_token, log_token_usage

TZ = ZoneInfo("Asia/Tokyo")


def get_current_time() -> str:
    return datetime.datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def get_jp_holidays(year: Optional[int] = None):
    year = year or datetime.datetime.now(TZ).year
    jp = holidays.country_holidays("JP", years=year)
    return {
        "year": year,
        "holidays": [
            {"date": d.isoformat(), "name": str(name)} for d, name in sorted(jp.items())
        ],
    }


general_agent = Agent(
    name="general_agent",
    description="雑談に対応するエージェント",
    model="gemini-2.0-flash",
    instruction="""
    あなたは、雑談の専門家です。
    日常会話、趣味、時事問題など、幅広いトピックに関する質問に親しみやすく答えてください。

    カレンダー情報（祝日・連休）を答えるときは、必ず以下の手順で回答してください。

    手順
    1. get_current_time を呼び、基準となる「年」を確定する（JST）。
    2. get_jp_holidays を呼び、対象年の祝日一覧を取得する。
    3. 「連休/三連休」と聞かれた場合は、祝日一覧に加えて土日も休みとして扱い、連続する休みが3日以上になる区間だけを抽出して答える。

    禁止:
    - 祝日を列挙するだけで「連休」を答えたことにしない。
    - ツール結果にない日付を推測で作らない。
    """.strip(),
    tools=[get_current_time, get_jp_holidays],
    after_agent_callback=log_token_usage,
    after_model_callback=get_token,
)
