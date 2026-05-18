from google.adk.agents.llm_agent import Agent

summary_agent = Agent(
    model='gemini-2.5-flash',
    name='summary_agent',
    description="Specialist in summarizing travel plans.",
    instruction="""You are a Travel Summarizer.
    1. You will receive data from several other agents (Budget, Weather, Hotels, Itinerary).
    2. Your job is to create a beautiful, cohesive, and "ready-to-go" summary for the user.
    3. Use markdown for better formatting (bolding, lists, etc.).
    4. Make the user feel excited about their trip!""",
    tools=[],
)
