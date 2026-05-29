from google.adk.agents.llm_agent import Agent
from agents.weather_agent import weather_agent
from agents.hotel_agent import hotel_agent
from google.adk.tools.google_search_agent_tool import GoogleSearchAgentTool, create_google_search_agent

search_agent_tool = GoogleSearchAgentTool(create_google_search_agent('gemini-2.5-flash'))

research_agent = Agent(
    model='gemini-2.5-flash',
    name='research_agent',
    description="Specialist in gathering real-time data for weather, hotels, and food.",
    instruction="""You are a Travel Research Specialist. Your goal is to coordinate a comprehensive research:
    1. Call the 'weather_agent' to get the current weather and travel advice.
    2. Call the 'hotel_agent' to find top-rated accommodations and prices.
    3. Use the search tool to find must-try local restaurants and food.
    4. Once the sub-agents transfer control back to you with their reports, merge everything into a structured 'Research Report' for the next step.""",
    tools=[search_agent_tool],
    sub_agents=[weather_agent, hotel_agent],
)


