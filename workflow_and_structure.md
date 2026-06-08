# Travel Agent Workflow & Folder Structure

This document provides a detailed overview of the Travel Agent project, built using Google's **Agent Development Kit (ADK)**. It covers the overall folder structure, agent architecture, custom tools, and the execution workflow.

---

## 📂 Directory Structure

The project follows a clean, modular structure, separating agent definitions, custom tools, workflows, configuration files, and utility schemas.

```text
/data/Janaghan/gemini/agents_adk/
├── .adk/                    # ADK-specific runtime state/cache metadata
├── .env                     # Local environment variables (e.g., GEMINI_API_KEY)
├── .gitignore               # Ignored files (virtual envs, cached files)
├── .venv/                   # Python virtual environment
├── main.py                  # Entrypoint: terminal chat runner loop
├── schema.py                # Pydantic data schemas for structured outputs
├── requirements.txt         # Project dependencies (google-adk, pydantic, etc.)
├── flow_chart.md            # Text-based flowchart of the execution flow
├── structure.md             # Text representation of project structure
├── workflow_and_structure.md # This document
│
├── configs/                 # Configuration files
│   └── settings.yaml        # ADK settings (caching, observability/Laminar)
│
├── agents/                  # ADK Agent definitions
│   ├── coordinator_agent.py # Master orchestrator (SequentialAgent)
│   ├── intake_agent.py      # Conversational intake agent (entry agent)
│   ├── research_agent.py    # Gathers data (sub-agents: weather, hotel)
│   ├── weather_agent.py     # Weather specialist (tool: get_weather)
│   ├── hotel_agent.py       # Hotel accommodation specialist (tool: hotel_search_tool)
│   ├── planner_agent.py     # Day-by-day planner (sub-agent: itinerary)
│   ├── itinerary_agent.py   # Activity planner (tool: itinerary_search_tool)
│   ├── budget_agent.py      # Budget verifier (tools: calculate_math, get_exchange_rate, exit_loop)
│   └── summary_agent.py     # Prepares final premium travel markdown guide
│
├── tools/                   # Custom tool implementations
│   ├── __init__.py          # Tool exports
│   ├── weather_tool.py      # Fetches weather forecasts from Open-Meteo
│   ├── currency_tool.py     # Real-time exchange rate fetched from Open Exchange Rate API
│   ├── calculate_math.py    # Safe mathematical expression evaluator
│   ├── get_current_time.py  # Real-time local time provider using Open-Meteo geocoding
│   └── search_tools.py      # Google Search tools for agents (hotel, itinerary, research)
│
└── workflows/               # High-level orchestration wrappers
    └── planner_workflow.py  # Wrapper execution class mapping query to coordinator
```

---

## 🔄 Agent Hierarchy & Workflow Flowchart

The system uses a hierarchical agent structure managed by `coordinator_agent` (a `SequentialAgent`), coordinating the sequentially executed research, planning, budgeting, and summarization tasks.

### Architecture Diagram

```mermaid
graph TD
    User([User Input]) --> Main[main.py]
    Main --> Runner[ADK Runner]
    Runner --> Intake[intake_agent <br/><i>Agent (Conversational Intake)</i>]
    Intake -- "Handoff (transfer_to_agent)" --> Coord[coordinator_agent <br/><i>SequentialAgent</i>]

    subgraph Phase 1: Research
        Coord --> Research[research_agent <br/><i>Agent</i>]
        Research --> Weather[weather_agent <br/><i>Agent</i>]
        Research --> Hotel[hotel_agent <br/><i>Agent</i>]
        Research --> GoogleSearch1[research_search_tool <br/><i>GoogleSearchAgentTool</i>]

        Weather --> WeatherTool[weather_tool.py <br/><i>get_weather</i>]
        Hotel --> GoogleSearchHotel[hotel_search_tool <br/><i>GoogleSearchAgentTool</i>]
    end

    subgraph Phase 2: Budget Loop
        Coord --> BudgetLoop[budget_loop <br/><i>LoopAgent (max 5 iterations)</i>]
        BudgetLoop --> Planner[planner_agent <br/><i>Agent</i>]
        BudgetLoop --> Budget[budget_agent <br/><i>Agent</i>]

        Planner --> Itinerary[itinerary_agent <br/><i>Agent</i>]
        Itinerary --> GoogleSearchItinerary[itinerary_search_tool <br/><i>GoogleSearchAgentTool</i>]
        
        Budget --> CalcMath[calculate_math.py <br/><i>calculate_math</i>]
        Budget --> CurrTool[currency_tool.py <br/><i>get_exchange_rate</i>]
        Budget --> ExitLoop[exit_loop <br/><i>ADK Tool</i>]
    end

    subgraph Phase 3: Summary
        Coord --> Summary[summary_agent <br/><i>Agent</i>]
    end

    Summary --> FinalOutput([Final Markdown Response])
```

---

## 👥 Component Descriptions

### 1. Agents Directory (`agents/`)

Each agent is defined using the ADK model with specialized instructions, tools, and sub-agents.

| Agent Name | Type / Wrapper | Model | Role & Scope |
| :--- | :--- | :--- | :--- |
| **intake_agent** | `Agent` | `gemini-2.5-flash-lite` | **First step.** Collects destination, travel dates, and budget from the user. Asks follow-up questions for any missing details and confirms a Trip Brief before handing off. |
| **coordinator_agent** | `SequentialAgent` | - | Master orchestrator. Runs `research_agent` → `budget_loop` → `summary_agent` sequentially. |
| **research_agent** | `Agent` | `gemini-2.5-flash-lite` | Coordinates weather & hotel lookups. Gathers research data and compiles a report. |
| **weather_agent** | `Agent` | `gemini-2.5-flash-lite` | Sub-agent to `research_agent`. Uses `get_weather` tool and suggests packing advice before handoff. |
| **hotel_agent** | `Agent` | `gemini-2.5-flash-lite` | Sub-agent to `research_agent`. Uses `hotel_search_tool` to find actual hotel rates and availability. |
| **budget_loop** | `LoopAgent` | - | Handles iterative feedback loop containing `planner_agent` and `budget_agent` to enforce budget limits (max 5 iterations). |
| **planner_agent** | `Agent` | `gemini-2.5-flash-lite` | Uses `itinerary_agent` to build daily plans, ensuring costs are listed. Updates plan if budget is exceeded. |
| **itinerary_agent** | `Agent` | `gemini-2.5-flash-lite` | Sub-agent to `planner_agent`. Uses `itinerary_search_tool` to find activities, schedules, and local options. |
| **budget_agent** | `Agent` | `gemini-2.5-flash-lite` | Sums costs, checks against user budget limit, and calls `exit_loop` if valid, or requests refinement. |
| **summary_agent** | `Agent` | `gemini-2.5-flash-lite` | Gathers research and planned itineraries to format a cohesive and premium markdown output. |

### 2. Tools Directory (`tools/`)

Tools are Python functions that are exposed to agents for external integration.

- **`weather_tool.py` (`get_weather`)**: Fetches current temperature and weather conditions using Open-Meteo's geocoding and weather APIs.
- **`currency_tool.py` (`get_exchange_rate`)**: Provides real-time exchange rates via Open-Meteo Exchange Rate API (`open.er-api.com`).
- **`calculate_math.py` (`calculate_math`)**: Safely evaluates simple math expressions (useful for sum checks).
- **`get_current_time.py` (`get_current_time`)**: Dynamic tool providing real-time local time using Open-Meteo geocoding and `zoneinfo` conversion.
- **`search_tools.py` (`research_search_tool`, `hotel_search_tool`, `itinerary_search_tool`)**: Google Search agents configured as tools for web search functionality across different phases.

---

## 🚀 Execution Lifecycle

1. **User Prompt**: The user runs `python main.py` and inputs a query (e.g. *"Plan a 3-day trip to Goa with a budget of $500"*).
2. **Initialization**: `main.py` loads `.env` settings, creates an `InMemorySessionService`, and binds `intake_agent` to an ADK `Runner`.
3. **Intake Phase**:
   - `intake_agent` talks to the user to collect the Destination, Dates, and Budget.
   - Once all details are collected, it calls the `transfer_to_agent` tool to hand off control to `coordinator_agent`.
4. **Research Phase**:
   - `research_agent` kicks off.
   - It calls `weather_agent` (which calls `get_weather`) to find Goa's weather.
   - It calls `hotel_agent` (which queries `hotel_search_tool`) to list top-rated hotels in Goa.
   - It uses `research_search_tool` to research local restaurants and must-try food.
   - It aggregates findings and returns to the coordinator.
5. **Iterative Planning & Budget Validation Loop**:
   - `planner_agent` accepts research data and asks `itinerary_agent` to build day-by-day activities.
   - `itinerary_agent` uses `itinerary_search_tool` to lookup activities and costs.
   - `budget_agent` receives the itinerary, sums the costs using `calculate_math`, and uses `get_exchange_rate` if currency conversion is needed.
   - If the cost is $\le \$500$, `budget_agent` calls `exit_loop` and breaks out.
   - If the cost is $>\$500$, `budget_agent` provides a breakdown of expensive items and control returns to `planner_agent` to re-estimate/optimize.
6. **Final Summary**:
   - `summary_agent` is invoked to format the final itinerary, hotel list, weather warning, and budget verification into a beautiful Markdown report.

---

## ✅ Workflow Organization Audit

Based on a thorough review of the directory and the codebase:
- **Clean Structure**: Separation between `agents`, `tools`, `docs`, and `workflows` matches the recommended ADK workflow setup perfectly.
- **Clear Handoffs**: Sub-agents correctly call `transfer_to_agent` (automatically provided by ADK) to return execution to parent agents (`research_agent` and `planner_agent`).
- **Effective Loop constraints**: The `LoopAgent` prevents infinite loops by capping iterations at 5, and utilizes `exit_loop` properly inside the budget checker.
- **Observability ready**: The config specifies Laminar integration, enabling seamless execution tracing.
