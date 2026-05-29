from google.adk.agents.llm_agent import Agent
from google.adk.tools import exit_loop
from tools.currency_tool import get_exchange_rate
from tools.calculate_math import calculate_math

budget_agent = Agent(
    model='gemini-2.5-flash',
    name='budget_agent',
    description="Specialist in travel budgeting, calculating total cost, and verifying if it is within budget.",
    instruction="""You are a Travel Budget Expert.
    1. You will receive the itinerary from the planner_agent.
    2. Calculate the total cost of all items in the itinerary. Use the 'calculate_math' tool to sum the costs.
    3. Check if the total cost is within the user's budget.
    4. If the total cost is within the budget, call the 'exit_loop' tool immediately. Do not generate additional responses after calling 'exit_loop'.
    5. If the total cost exceeds the budget, explain by how much it exceeds, list the most expensive items, and do NOT call 'exit_loop' so that the planner_agent can refine the plan in the next iteration.""",
    tools=[get_exchange_rate, exit_loop, calculate_math],
)

