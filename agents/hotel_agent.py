from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_agent_tool import GoogleSearchAgentTool, create_google_search_agent

search_agent_tool = GoogleSearchAgentTool(create_google_search_agent('gemini-2.5-flash'))

hotel_agent = Agent(
    model='gemini-2.5-flash',
    name='hotel_agent',
    description="Specialist in finding accommodations.",
    instruction="""You are a Hotel Specialist.
    1. Help users find hotels based on their destination and budget level.
    2. Use the search tool to find actual, real-time hotel availability, pricing, and reviews.
    3. Provide current options with estimated costs and links if possible.
    4. Once you have gathered the hotel details, call the 'transfer_to_agent' tool to transfer control back to your parent agent research_agent.""",
    tools=[search_agent_tool],
)



