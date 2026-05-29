# Travel Agent Multi-Agent System 

Welcome to the **Travel Agent ADK Project**! This repository demonstrates the evolution from a basic Large Language Model (LLM) interaction to a **Multi-Agent System** using Google's Agent Development Kit (ADK).

##  Project Overview & Objectives

The goal of this project is to build an intelligent, autonomous travel planner that can:
1. **Intake:** Converse with users to collect travel requirements (Destination, Dates, Budget).
2. **Research:** Dynamically fetch live weather forecasts and search for real-time hotel availability.
3. **Plan & Budget:** Construct a day-by-day itinerary, calculate estimated costs, and iteratively adjust the plan if it exceeds the user's budget limit.
4. **Summarize:** Output a beautifully formatted, comprehensive markdown travel guide.

By following this documentation, you will learn how to orchestrate complex reasoning, tool execution, and delegation across multiple specialized AI agents.
 
--- 

##  Quick Start: How to Run

Follow these steps to get the travel agent running on your local machine:

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd agents_adk
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Run the agent:**
   ```bash
   python3 main.py
   ```

You will enter a terminal chat loop. Start by asking it to plan a trip!

---

##  Learning Roadmap

This repository contains a dedicated `docs/` folder charting the learning journey. We recommend reading them in this order:

1. **[Phase 1: Single Agent Basics](docs/phase_01_single_agent.md)** — Understanding the core LLM Agent.
2. **[Phase 2: Tools & Memory](docs/phase_02_tools_and_memory.md)** — Empowering agents to fetch live data and remember conversation context.
3. **[Phase 3: Workflows & Pipelines](docs/phase_03_workflows.md)** — Imposing structure using `SequentialAgent` and `LoopAgent`.
4. **[Phase 4: Delegation & Sub-Agents](docs/phase_04_sub_agents.md)** — Hierarchical control and the `transfer_to_agent` mechanism.
5. **[Phase 5: The Full Multi-Agent System](docs/phase_05_multi_agent_system.md)** — Bringing it all together into a robust orchestrator.
6. **[Architecture Overview](docs/architecture_overview.md)** — A holistic, visual deep-dive into the final system architecture.

---

##  Folder Structure

```text
agents_adk/
├── README.md                      # This file
├── docs/                          # Multi-Agent Learning Journey Documentation
├── main.py                        # Entrypoint: terminal chat runner loop
├── schema.py                      # Pydantic data schemas for structured outputs
├── requirements.txt               # Dependencies
│
├── tools/                         # Custom Tool Implementations
│   ├── __init__.py                
│   ├── search_tools.py            # Instantiates unique Google Search agents
│   ├── weather_tool.py            # Fetches weather from Open-Meteo
│   ├── currency_tool.py           # Real-time exchange rates (Open Exchange Rate)
│   ├── calculate_math.py          # Mathematical expression evaluator
│   └── get_current_time.py        # Dynamic geocoding & timezone resolution
│
└── agents/                        # ADK Agent Definitions
    ├── intake_agent.py            # Gathers user requirements (Entry point)
    ├── coordinator_agent.py       # Orchestrator (SequentialAgent)
    ├── research_agent.py          # Coordinates data gathering
    ├── weather_agent.py           # Uses weather_tool
    ├── hotel_agent.py             # Uses search tool for accommodations
    ├── planner_agent.py           # Generates day-by-day itineraries
    ├── itinerary_agent.py         # Uses search tool for activities
    ├── budget_agent.py            # Verifies total costs against limits
    └── summary_agent.py           # Compiles final markdown report
```

---

## 🛠️ Technologies and Frameworks Used

- **[Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/)**: The core framework providing `Agent`, `SequentialAgent`, `LoopAgent`, memory services, and tool integration.
- **Google Gemini API**: Utilizing the `gemini-2.0-flash` model for high-speed, cost-effective reasoning.
- **Python 3.10+**: Standard library tools like `zoneinfo` and `datetime`.
- **Open-Meteo APIs**: Used for keyless geocoding and live weather forecasting.
- **Pydantic**: For type-safe data modeling.

---

##  Key Concepts Learned

- **Function Calling:** Allowing LLMs to execute Python functions and interpret the results.
- **Session Memory:** Retaining state across a continuous user interaction.
- **Agent Handoffs:** Safely transferring execution context from a "manager" agent to a "specialist" agent and back.
- **Deterministic Orchestration:** Using Code (Sequential/Loop nodes) rather than Prompts to guarantee the order of execution.
- **Self-Correction Loops:** Creating agents that verify their own output (like our `budget_loop`) and retry if constraints fail.



