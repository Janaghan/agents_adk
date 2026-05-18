from google.adk.agents.llm_agent import Agent
from tools.weather_tool import get_weather

weather_agent = Agent(
    model='gemini-2.5-flash',
    name='weather_agent',
    description="Specialist in weather lookups.",
    instruction="""You are a Weather Specialist. 
    1. Use 'get_weather' to find current conditions for the destination.
    2. Provide travel-relevant advice based on the weather (e.g., 'bring an umbrella' or 'perfect for the beach').""",
    tools=[get_weather],
)
