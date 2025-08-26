from google.adk.agents import Agent

coffee_agent = Agent(
    name="coffee_agent",
    description="コーヒーに関する専門知識を持つエージェント",
    model="gemini-2.0-flash",
    instruction="""
    あなたはコーヒーの専門家です。
    コーヒーの種類、淹れ方、豆の特徴、カフェのおすすめなど、コーヒーに関するあらゆる質問に専門的に答えてください。
    """
)
