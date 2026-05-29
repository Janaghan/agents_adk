# Phase 1: Single Agent Architecture

## 1. Phase Overview
In this initial phase, we explore the most basic implementation of an AI agent: a Single Agent processing a user prompt and returning a text response. 
In our Travel Agent project, the `intake_agent` embodies this concept. It acts as the frontline greeter, ensuring the user provides three mandatory pieces of information (Destination, Dates, Budget) before any complex processing begins.

**Why this phase is important:** It establishes the baseline. Before adding tools, memory, or multiple agents, we must understand how to construct a reliable, prompt-driven persona that can parse user intent.

---

## 2. Concepts Learned
- **LLM Agent Definition:** Wrapping a Large Language Model (like Gemini) with a specific persona, goal, and ruleset (System Prompt/Instruction).
- **Zero-Shot Reasoning:** The agent evaluates the user's input against its criteria in a single pass without needing prior examples.
- **State Evaluation:** The agent determines if it has all necessary data (Complete) or if it needs to ask follow-up questions (Incomplete).

**Beginner-Friendly Explanation:**
Imagine hiring a new receptionist for your office. You give them one very strict rule: *"Do not let anyone past this desk until they tell you three things: their name, their appointment time, and who they are here to see."* 

If a visitor walks in and only says, "I'm here to see John," the receptionist won't let them through. Instead, they will politely ask, "What is your name and appointment time?" 

A Single Agent works exactly like this receptionist. It acts as a smart gatekeeper that chats with the user, understands what information is missing, and naturally asks follow-up questions before allowing the system to move forward to the complex planning stages.

---

## 3. Implementation Details
In our project, this is implemented in `agents/intake_agent.py`.

- **Components Involved:**
  - Google ADK's `Agent` class.
  - The `gemini-2.0-flash` model.
- **How it works:**
  We initialize the agent with a strict `instruction`. If the user says *"I want to go to Paris"*, the agent's internal logic recognizes that Dates and Budget are missing. It formulates a polite response asking for those specific items. Once all items are provided, it outputs a standardized "Trip Brief".

---

## 4. Architecture Diagram

```text
           [ User Prompt ]
                  │
                  ▼
          ┌───────────────┐
          │ intake_agent  │
          └───────┬───────┘
                  │
           (Check Details)
             /          \
      [ Missing ]    [ Complete ]
          │                │
          ▼                ▼
   [ Ask User ]    [ Generate Brief ]
          │                │
     (Loop Back)     (Pass to Next Phase)
```

---

## 5. Why This Concept Is Needed
**The Problem Solved:** If we pass incomplete information to a complex planning pipeline, the system will hallucinate or crash. For example, trying to find hotel prices without knowing the travel dates.
**Benefits Introduced:** It acts as a strict validation gatekeeper, ensuring high-quality, structured inputs for the rest of the application.

---

## 6. With vs Without This Concept

| Without a Single Agent Gatekeeper | With a Single Agent Gatekeeper |
| :--- | :--- |
| System tries to plan trips with missing data | System halts and gracefully asks for missing data |
| High likelihood of LLM hallucinations | High-quality, guaranteed structured inputs |
| Complex logic required in the UI to validate forms | Natural, conversational requirement gathering |
