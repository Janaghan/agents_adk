from google.adk.agents.llm_agent import Agent
from tools.search_tools import itinerary_search_tool

itinerary_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='itinerary_agent',
    description="Specialist in travel itineraries and finding places of interest.",
    instruction="""You are a Travel Planner. 
    1. Help users plan their daily activities.
    2. Use the search tool to find real-time events, seasonal attractions, and local recommendations.
    3. Create structured day-by-day plans with live details.
    4. Once you have built the detailed itinerary, call the 'transfer_to_agent' tool to transfer control back to your parent agent planner_agent.""",
    tools=[itinerary_search_tool],
)




