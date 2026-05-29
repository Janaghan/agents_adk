# Phase 2: Tools and Memory

## 1. Phase Overview
An LLM in isolation only knows what it was trained on and what you just told it. In this phase, we give the agent two superpowers: **Tools** (to interact with the real world) and **Memory** (to remember what we discussed five minutes ago).
In our project, we see this in action when the `weather_agent` uses the `get_weather` tool to fetch live data, while `main.py` utilizes the `InMemorySessionService` to remember the user's destination across multiple chat turns.

**Why this phase is important:** Without tools, an agent is just a chatbot hallucinating facts. Without memory, it has gold-fish amnesia. Combining these allows for stateful, fact-based interactions.

---

## 2. Concepts Learned
- **Function Calling (Tools):** Providing a Python function signature (and docstring) to the LLM so it knows *when* and *how* to ask the system to run code on its behalf.
- **Session Memory:** Storing the history of user messages and agent responses in a continuous "Session" context window.

**Beginner-Friendly Explanation:**
Think of an AI Agent like a person sitting in a windowless room with no internet. If you ask them, "What is the weather in Tokyo right now?", they can only guess based on books they read years ago. 

- **Tools** are like sliding a smartphone under the door. Now, the AI can open a weather app, look up the exact live temperature in Tokyo, and give you a 100% accurate, factual answer.
- **Memory** is like the AI keeping a notepad of your conversation. If your next question is simply, "What should I pack?", the AI looks at its notepad, remembers that you are talking about Tokyo, and suggests an umbrella because it just saw that it's raining there.

---

## 3. Implementation Details
- **Tools:** Implemented in `tools/weather_tool.py`. The `@AgentTool` decorator exposes a standard Python function (which makes an HTTP request to Open-Meteo) to the ADK. We then pass this tool into the `tools=[...]` array of the `weather_agent`.
- **Memory:** Implemented in `main.py` using `InMemorySessionService` injected into the ADK `Runner`. The runner automatically appends every turn to this session object before sending it to the model.

---

## 4. Architecture Diagram

```text
   [ User ]         [ ADK Memory ]        [ Agent ]         [ Weather API ]
      │                   │                   │                   │
      ├─ "Weather?" ─────►│                   │                   │
      │                   ├─ Context + Prompt►│                   │
      │                   │                   │                   │
      │                   │◄── Call Tool ─────┤                   │
      │                   ├─ Execute Func ───────────────────────►│
      │                   │◄─────────────────────── {temp: 35C} ──┤
      │                   │                   │                   │
      │                   ├─ Inject Result ──►│                   │
      │                   │                   │                   │
      │◄─── "It's 35°C" ──┼◄── Text Reply ────┤                   │
      │                   │                   │                   │
```

---

## 5. Why This Concept Is Needed
**The Problem Solved:** Models have a knowledge cutoff date and cannot browse the live internet natively. Furthermore, APIs are stateless by default (each request is treated as brand new).
**Benefits Introduced:** Tools allow retrieval of dynamic, real-time data (weather, exchange rates). Memory allows for natural back-and-forth dialogue without forcing the user to repeat themselves.

---

## 6. With vs Without This Concept

| Without Tools & Memory | With Tools & Memory |
| :--- | :--- |
| Agent guesses the weather (hallucination) | Agent fetches real-time API data (factual) |
| "What should I pack for there?" $\rightarrow$ "Where?" | "What should I pack for there?" $\rightarrow$ "For Chennai..." |
| Static knowledge | Dynamic capabilities |
