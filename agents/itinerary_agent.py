from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_agent_tool import GoogleSearchAgentTool, create_google_search_agent

search_agent_tool = GoogleSearchAgentTool(create_google_search_agent('gemini-2.5-flash'))

itinerary_agent = Agent(
    model='gemini-2.5-flash',
    name='itinerary_agent',
    description="Specialist in travel itineraries and finding places of interest.",
    instruction="""You are a Travel Planner. 
    1. Help users plan their daily activities.
    2. Use the search tool to find real-time events, seasonal attractions, and local recommendations.
    3. Create structured day-by-day plans with live details.
    4. Once you have built the detailed itinerary, call the 'transfer_to_agent' tool to transfer control back to your parent agent planner_agent.""",
    tools=[search_agent_tool],
)



