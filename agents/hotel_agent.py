from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

hotel_agent = Agent(
    model='gemini-2.5-flash',
    name='hotel_agent',
    description="Specialist in finding accommodations.",
    instruction="""You are a Hotel Specialist.
    1. Help users find hotels based on their destination and budget level.
    2. Use 'google_search' to find actual, real-time hotel availability, pricing, and reviews.
    3. Provide current options with links if possible.""",
    tools=[google_search],
)
