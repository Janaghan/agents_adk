# Architecture Overview

This document provides a holistic, visual overview of the Travel Agent Multi-Agent System (MAS) architecture, detailing how requests flow from the user through the agent hierarchy, how tools are integrated, and how session memory is maintained.

---

## 1. High-Level System Architecture

At the highest level, the system consists of a User Interface (the Terminal Runner), a Session Memory layer, and the core Agent Hierarchy.

```mermaid
graph TD
    UI[Terminal / main.py] <-->|Event Stream| Mem[InMemorySessionService]
    Mem <-->|Context & History| Root[Root Agent: intake_agent]
    Root -.->|Transfer Control| MAS[Multi-Agent Pipeline]
    
    MAS --> API1[Open-Meteo API]
    MAS --> API2[Google Search API]
    MAS --> API3[Exchange Rate API]
```

---

## 2. Agent Hierarchy & Delegation Tree

The agents are organized hierarchically. An orchestrator delegates to sub-agents, which can delegate to specific tool-using nodes.

```mermaid
mindmap
  root((intake_agent))
    (coordinator_agent)
      [research_agent]
        ::icon(fa fa-search)
        weather_agent
        hotel_agent
      [budget_loop]
        ::icon(fa fa-sync)
        planner_agent
          itinerary_agent
        budget_agent
      [summary_agent]
        ::icon(fa fa-file-text)
```

---

## 3. End-to-End Request Lifecycle

This flowchart illustrates exactly what happens when a user types "I want to go to Chennai for 3 days with a 12k budget."

```mermaid
stateDiagram-v2
    [*] --> Intake
    
    state Intake {
        [*] --> CheckRequirements
        CheckRequirements --> AskUser: Missing Info
        AskUser --> CheckRequirements: User Replies
        CheckRequirements --> GenerateBrief: All Info Present
        GenerateBrief --> Handoff: transfer_to_agent(coordinator)
    }
    
    Intake --> Coordinator: Sequence Starts
    
    state Coordinator {
        state Research Phase {
            ResearchAgent --> WeatherAgent: get_weather()
            WeatherAgent --> ResearchAgent: return data
            ResearchAgent --> HotelAgent: search_hotels()
            HotelAgent --> ResearchAgent: return data
        }
        
        Research Phase --> Planning Phase
        
        state Planning Phase (Loop) {
            PlannerAgent --> ItineraryAgent: search_activities()
            ItineraryAgent --> PlannerAgent: return draft
            PlannerAgent --> BudgetAgent: Check Math
            
            state if_over_budget <<choice>>
            BudgetAgent --> if_over_budget
            if_over_budget --> PlannerAgent: Over Budget (Retry)
            if_over_budget --> ExitLoop: Under Budget (exit_loop tool)
        }
        
        Planning Phase --> Summary Phase
        
        state Summary Phase {
            SummaryAgent --> FinalMarkdown: Format data
        }
    }
    
    Coordinator --> [*]: Outputs Markdown to Terminal
```

---

## 4. Tool Integration Flow

Agents don't execute Python code directly. They output a JSON representation of a function call, which the ADK framework intercepts, executes, and returns to the agent.

```mermaid
sequenceDiagram
    participant LLM as Gemini Model
    participant Framework as ADK Runner
    participant Tool as Python Function (e.g., calculate_math)
    
    LLM->>Framework: Output: {"functionCall": {"name": "calculate_math", "args": {"expression": "2500 * 3 + 1500"}}}
    Framework->>Tool: Execute: calculate_math("2500 * 3 + 1500")
    Tool-->>Framework: Return: "9000"
    Framework->>LLM: Input: {"functionResponse": {"name": "calculate_math", "response": {"result": "9000"}}}
    LLM->>Framework: Output: Text reasoning based on the "9000" result
```

---

## 5. Session and Memory Flow

The `InMemorySessionService` acts as a continuous ledger. Every interaction (User Prompt, LLM Response, Tool Call, Tool Result, Agent Transfer) is appended to a massive array of events. When an agent wakes up to act, it reads this entire ledger to understand the current context.

* **Advantage:** If the `summary_agent` runs at the very end of the pipeline, it can effortlessly look back at the `hotel_agent`'s tool response from the very beginning of the pipeline without needing data explicitly passed to it via arguments.
* **Limitation:** As the sequence grows, the context window fills up, which is why models like `gemini-2.0-flash` with massive context windows (1M+ tokens) are required for complex Multi-Agent Systems.
