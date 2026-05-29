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
If you ask a person in a sealed room what the weather is in Tokyo, they'll guess. But if you give them a smartphone (a Tool), they can look it up and give you a factual answer. Furthermore, if you later say "What should I pack?", they remember you are going to Tokyo (Memory) and suggest an umbrella.

---

## 3. Implementation Details
- **Tools:** Implemented in `tools/weather_tool.py`. The `@AgentTool` decorator exposes a standard Python function (which makes an HTTP request to Open-Meteo) to the ADK. We then pass this tool into the `tools=[...]` array of the `weather_agent`.
- **Memory:** Implemented in `main.py` using `InMemorySessionService` injected into the ADK `Runner`. The runner automatically appends every turn to this session object before sending it to the model.

---

## 4. Architecture Diagram

```text
[ User: "What's the weather in Chennai?" ]
                        │
                        ▼
             ┌─────────────────────┐
             │   Runner (Memory)   │ ◄─── (Stores Chat History)
             └──────────┬──────────┘
                        │ (Passes Prompt + History)
                        ▼
             ┌─────────────────────┐
             │       Agent         │
             └──────────┬──────────┘
                        │ (Requests get_weather("Chennai"))
                        ▼
             ┌─────────────────────┐
             │   Runner (Memory)   │ 
             └──────────┬──────────┘
                        │ (Executes Python Function)
                        ▼
             ┌─────────────────────┐
             │ Tool (External API) │
             └──────────┬──────────┘
                        │ (Returns {temp: 35C})
                        ▼
             ┌─────────────────────┐
             │   Runner (Memory)   │ ◄─── (Injects Tool Result)
             └──────────┬──────────┘
                        │ 
                        ▼
             ┌─────────────────────┐
             │       Agent         │
             └──────────┬──────────┘
                        │
                        ▼
     [ User: "It's 35°C in Chennai today!" ]
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
