from agents.weather_agent import coordinator_agent

class PlannerWorkflow:
    """
    Implements the flow:
    User asks: "Weather in Goa?" -> Coordinator Agent -> LLM decides: Need Weather Tool 
    -> Weather Tool Executes -> Returns Structured Data -> LLM Generates Final Answer -> Response to User
    """
    def __init__(self):
        self.coordinator = coordinator_agent

    async def execute_plan(self, user_query: str):
        print(f"User asks: '{user_query}'")
        print("Routing to Coordinator Agent...")
        
        # The ADK coordinator agent handles the Tool delegation internally
        # It decides to use weather_tool, gets the structured dict, and generates the final response.
        response = await self.coordinator.run_async(user_query)
        return response

