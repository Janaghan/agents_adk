from google.adk.tools.google_search_agent_tool import GoogleSearchAgentTool, create_google_search_agent

MODEL = 'gemini-2.5-flash-lite'

# Each search agent MUST have a unique name or ADK's registry will
# confuse them and raise "Tool '<agent>' not found" errors.

_research_search_agent = create_google_search_agent(MODEL)
_research_search_agent.name = 'research_search_agent'
research_search_tool = GoogleSearchAgentTool(_research_search_agent)

_hotel_search_agent = create_google_search_agent(MODEL)
_hotel_search_agent.name = 'hotel_search_agent'
hotel_search_tool = GoogleSearchAgentTool(_hotel_search_agent)

_itinerary_search_agent = create_google_search_agent(MODEL)
_itinerary_search_agent.name = 'itinerary_search_agent'
itinerary_search_tool = GoogleSearchAgentTool(_itinerary_search_agent)
