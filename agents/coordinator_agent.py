from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.loop_agent import LoopAgent
from agents.research_agent import research_agent
from agents.planner_agent import planner_agent
from agents.budget_agent import budget_agent
from agents.summary_agent import summary_agent

budget_loop = LoopAgent(
    name='budget_loop',
    description="Iterative loop to compile an itinerary and verify if it matches the user's budget.",
    sub_agents=[planner_agent, budget_agent],
    max_iterations=3
)

coordinator_agent = SequentialAgent(
    name='coordinator_agent',
    description="Main Travel Assistant. Coordinates sequential execution of Research, Planning/Budget checks, and final Summary.",
    sub_agents=[research_agent, budget_loop, summary_agent]
)

