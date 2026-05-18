from dotenv import load_dotenv
load_dotenv()
from agents.weather_agent import coordinator_agent

import asyncio

async def main():
    print('User asks: "Weather in Goa?"')
    print('│\n▼\nCoordinator Agent\n│\n▼')
    
    # ADK will automatically execute the rest of the flow
    print('Response to User:')
    async for chunk in coordinator_agent.run_async("Weather in Goa?"):
        print(chunk, end="")
    print()

if __name__ == "__main__":
    asyncio.run(main())
