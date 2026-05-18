from dotenv import load_dotenv
load_dotenv()
import json
from google.adk.agents.llm_agent import Agent
from google.adk.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    # Returns Structured Data
    data = {"location": location, "temperature": "32°C", "condition": "Sunny and Humid"}
    return json.dumps(data)

coordinator_agent = Agent(
    model='gemini-2.5-flash',
    name='Coordinator_Agent',
    description="I am a coordinator that uses tools to answer questions.",
    instruction="You are a Coordinator Agent. Use the get_weather tool to answer weather questions.",
    tools=[get_weather],
)

response = coordinator_agent.run("Weather in Goa?")
print("Response to User:")
print(response)
