from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from tools.weather_tool import get_weather
from tools.currency_tool import get_exchange_rate

# We use bypass_multi_tools_limit=True to allow combining search with local tools
from google.adk.tools.google_search_tool import GoogleSearchTool
realtime_search = GoogleSearchTool(bypass_multi_tools_limit=True)

research_agent = Agent(
    model='gemini-2.5-flash',
    name='research_agent',
    description="Specialist in gathering real-time data for weather, hotels, and food.",
    instruction="""You are a Travel Research Specialist. Your goal is to perform a comprehensive search:
    1. **Weather**: Use 'get_weather' to find current conditions.
    2. **Hotels**: Use 'google_search' to find the top-rated accommodations and prices.
    3. **Food Search**: Use 'google_search' to find must-try local restaurants and popular dishes.
    4. **Merge Results**: Combine all three findings into a structured 'Research Report' for the coordinator.""",
    tools=[get_weather, get_exchange_rate, realtime_search],
)
