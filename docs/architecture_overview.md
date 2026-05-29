# Architecture Overview

This document provides a holistic overview of the Travel Agent Multi-Agent System (MAS) architecture, detailing how requests flow from the user through the agent hierarchy, how tools are integrated, and how session memory is maintained.

## Comprehensive Execution Flowchart

```text
                  [ User Input ]
                        │
                        ▼
             ┌─────────────────────┐
             │     main.py         │ ◄─── (Terminal Chat Loop)
             └──────────┬──────────┘
                        │ (runner.run_async)
                        ▼
             ┌─────────────────────┐
             │    intake_agent     │ ◄─── (Conversational Gating)
             └──────────┬──────────┘
                        │ (transfer_to_agent)
                        ▼
             ┌─────────────────────┐
             │  coordinator_agent  │ ◄─── (Orchestrator Sequence)
             └──────────┬──────────┘
                        │
      ┌─────────────────┴─────────────────┐
      ▼ (Step 2: Research)                ▼ (Step 3 & 5: Itinerary & Summary)
┌───────────┐                       ┌───────────┐
│ research_ │                       │ planner_  │
│   agent   │                       │   agent   │
└─────┬─────┘                       └─────┬─────┘
      │                                   │
      ├─► Weather API (get_weather)       ├─► Drafts itinerary with itemized costs.
      ├─► Exchange Rates (currency_tool)  └─► Formats final summary.
      └─► Google Search (Hotels & Food)
```

## Explanation of Stages

### 1. Terminal Chat Loop (`main.py`)
This is the entry point of the application. It captures user input from the terminal and sends it to the ADK `Runner`. The Runner wraps the input and sends it to the root agent. It is also responsible for maintaining the `InMemorySessionService`, which stores the full conversation history and tool outputs so all agents have access to the latest context.

### 2. Conversational Gating (`intake_agent`)
When a user submits a query, it first goes to the `intake_agent`. This agent acts as a friendly receptionist. Its sole job is to ensure that the three core requirements—Destination, Travel Dates, and Budget—are collected. If any information is missing, it pauses the workflow and asks the user follow-up questions. Once all details are collected, it calls the `transfer_to_agent` tool to hand off control to the orchestrator.

### 3. Orchestrator Sequence (`coordinator_agent`)
The `coordinator_agent` is a `SequentialAgent` that acts as the general manager. It does not interact with the user or call APIs directly. Instead, it silently coordinates a strict execution pipeline. It guarantees that Research happens first, followed by Planning and Budgeting, and finally Summarization.

### 4. Research Phase (`research_agent`)
The orchestrator triggers the `research_agent`, which acts as a manager for data gathering. It delegates tasks to specialized sub-agents:
*   **`weather_agent`**: Uses the `get_weather` tool to fetch live weather data for the destination.
*   **`hotel_agent`**: Uses a specialized Google Search tool to find real-time hotel prices, ratings, and availability.
Once both sub-agents complete their tasks, the data is passed forward.

### 5. Planning and Budgeting Phase (`planner_agent` & `budget_loop`)
With research complete, the orchestrator triggers the planning loop.
*   The **`planner_agent`** creates a day-by-day itinerary and delegates activity searching to the **`itinerary_agent`**.
*   The **`budget_agent`** then reviews the drafted itinerary. It uses the `calculate_math` and `currency_tool` to sum all costs.
*   If the costs exceed the user's budget, it rejects the plan and loops back to the `planner_agent` to create a cheaper itinerary. If the costs are within budget, it uses the `exit_loop` tool to finish this phase.

### 6. Summary Phase (`summary_agent`)
Finally, the orchestrator triggers the `summary_agent`. This agent reads the massive ledger of session memory—containing the weather data, the hotel options, the day-by-day itinerary, and the budget breakdown—and formats it into a beautiful, cohesive Markdown travel guide that is printed back to the user in the terminal.
