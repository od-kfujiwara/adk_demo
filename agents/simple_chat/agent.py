from google.adk.agents import Agent
from .instruction import INSTRUCTION

root_agent = Agent(
    name="simple_chat",
    description="ユーザーの質問に答えるチャットボット",
    model="gemini-2.0-flash",
    instruction=INSTRUCTION
)
