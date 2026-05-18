from google.adk.agents.llm_agent import Agent
from agents.research_agent import research_agent
from agents.planner_agent import planner_agent
from tools.calculate_math import calculate_math

coordinator_agent = Agent(
    model='gemini-2.5-flash',
    name='coordinator_agent',
    description="Main entry point for travel planning. Orchestrates a 5-step linear flow.",
    instruction="""You are the Master Travel Orchestrator. You MUST follow this exact sequence:
    
    1. **Understand Destination**: Confirm the target location and budget.
    2. **Parallel Research**: Call the 'research_agent' to perform parallel searches for Weather, Hotels, and Food.
    3. **Draft Plan**: Call the 'planner_agent' to create the itinerary with itemized costs.
    4. **Check Budget (LOOP START)**: Use 'calculate_math' to sum the total cost of the itinerary. If the total cost > user budget, you MUST message the 'planner_agent' to "Refine Plan" and swap for cheaper options. Repeat Step 4 until the budget is satisfied (max 3 retries).
    5. **Generate Summary**: Once the budget is verified, ask the 'planner_agent' to format the final summary for the user.""",
    tools=[calculate_math],
    sub_agents=[research_agent, planner_agent],
)
