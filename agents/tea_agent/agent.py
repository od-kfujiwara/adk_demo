from google.adk.agents import Agent

tea_agent = Agent(
    name="tea_agent",
    description="紅茶に関する専門知識を持つエージェント",
    model="gemini-2.0-flash",
    instruction="""
    あなたは紅茶の専門家です。
    紅茶の種類、淹れ方、茶葉の特徴、ティータイムのマナーなど、紅茶に関するあらゆる質問に専門的に答えてください。
    """
)
