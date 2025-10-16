from google.adk.agents import Agent
from agents.instruction import INSTRUCTION
from agents.coffee_agent.agent import coffee_agent
from agents.tea_agent.agent import tea_agent
from agents.callbacks import get_token, log_token_usage

root_agent = Agent(
    name="root_agent",
    description="飲み物の案内人として、コーヒーや紅茶の専門エージェントに適切にルーティングします",
    model="gemini-2.0-flash",
    instruction=INSTRUCTION,
    sub_agents=[coffee_agent, tea_agent],
    after_agent_callback=log_token_usage,
    after_model_callback=get_token
)
