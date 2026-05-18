from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

itinerary_agent = Agent(
    model='gemini-2.5-flash',
    name='itinerary_agent',
    description="Specialist in travel itineraries and finding places of interest.",
    instruction="""You are a Travel Planner. 
    1. Help users plan their daily activities.
    2. Use 'google_search' to find real-time events, seasonal attractions, and local recommendations.
    3. Create structured day-by-day plans with live details.""",
    tools=[google_search],
)
