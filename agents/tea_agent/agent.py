from google.adk.agents import Agent
from agents.callbacks import get_token, log_token_usage


tea_agent = Agent(
    name="tea_agent",
    description="紅茶に関する専門知識を持つエージェント",
    model="gemini-2.0-flash",
    instruction="""
    あなたは紅茶の専門家です。
    紅茶の種類、淹れ方、茶葉の特徴、ティータイムのマナーなど、紅茶に関するあらゆる質問に専門的に答えてください。
    """,
    after_agent_callback=log_token_usage,
    after_model_callback=get_token,
)
