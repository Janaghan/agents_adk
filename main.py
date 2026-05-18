import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agents.coordinator_agent import coordinator_agent
from agents.budget_agent import budget_agent
from agents.itinerary_agent import itinerary_agent

if __name__ == "__main__":
    import asyncio
    from google.adk.runners import Runner
    from google.adk.sessions.in_memory_session_service import InMemorySessionService
    from google.genai import types

    print("Travel Agent ADK Initialized (Terminal Chat Mode).")
    print("Type 'exit' or 'quit' to stop.\n")
    
    # Initialize services for the Runner
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="travel_agent",
        agent=coordinator_agent,
        session_service=session_service,
        auto_create_session=True
    )

    async def chat():
        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() in ['exit', 'quit']:
                    break
                
                print("Coordinator Agent: ", end="", flush=True)
                
                # Wrap the string input into the expected Content type
                new_message = types.Content(parts=[types.Part(text=user_input)])
                
                async for event in runner.run_async(
                    user_id="local_user",
                    session_id="local_session",
                    new_message=new_message
                ):
                    # Only process events that have content from the model
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            # Explicitly check for text to avoid SDK warnings about non-text parts
                            # like function_calls which are handled internally by the Runner
                            if hasattr(part, 'text') and part.text:
                                print(part.text, end="", flush=True)
                            elif hasattr(part, 'function_call') and part.function_call:
                                # Optional: Print a subtle indicator that a tool is being called
                                print(f"\n[Tool Calling: {part.function_call.name}]...", end="", flush=True)
                print("\n")
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\nError: {e}")
            
    asyncio.run(chat())
