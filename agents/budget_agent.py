from google.adk.agents.llm_agent import Agent
from tools.currency_tool import get_exchange_rate

budget_agent = Agent(
    model='gemini-2.5-flash',
    name='budget_agent',
    description="Specialist in travel budgeting and currency conversion.",
    instruction="""You are a Travel Budget Expert. 
    1. Help users estimate costs for flights, hotels, and daily expenses.
    2. Use 'get_exchange_rate' when users need to compare costs in different currencies.
    3. Always provide a breakdown of costs.""",
    tools=[get_exchange_rate],
)
