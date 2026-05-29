from google.adk.agents.llm_agent import Agent
from agents.itinerary_agent import itinerary_agent

planner_agent = Agent(
    model='gemini-2.5-flash',
    name='planner_agent',
    description="Specialist in travel planning and compiling itineraries.",
    instruction="""You are a Senior Travel Planner. 
    1. You will receive research data about weather, budget, hotels, and food.
    2. Call the 'itinerary_agent' to generate a detailed day-by-day plan of activities.
    3. Once the itinerary_agent transfers control back to you, compile the final day-by-day itinerary.
    4. **CRITICAL**: Ensure every hotel and activity has a clearly estimated cost in USD.
    5. If the budget_agent asks you to refine the plan because it exceeds the budget, select cheaper alternatives and compile an updated cheaper itinerary.""",
    tools=[],
    sub_agents=[itinerary_agent],
)

