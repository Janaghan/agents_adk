# Phase 3: Workflows (Pipelines & Loops)

## 1. Phase Overview
Prompting an LLM to "do X, then do Y, then do Z" often fails because models can lose track of complex multi-step instructions. In this phase, we move the orchestration logic out of the prompt and into the code structure using **Workflows**.
In our ADK implementation, we use a `SequentialAgent` to enforce a strict pipeline (`research_agent` $\rightarrow$ `budget_loop` $\rightarrow$ `summary_agent`) and a `LoopAgent` to iterate on budget adjustments.

**Why this phase is important:** Workflows guarantee execution order. They turn a probabilistic LLM text generator into a deterministic software pipeline.

---

## 2. Concepts Learned
- **Sequential Agent:** An orchestration wrapper that runs a list of sub-agents in a strict linear order. Agent A finishes, passing its output as context to Agent B.
- **Loop Agent:** An orchestration wrapper that reruns a set of sub-agents repeatedly until a specific exit condition is met (or a max iteration limit is reached).

**Beginner-Friendly Explanation:**
Instead of telling one chef, *"Go buy ingredients, then cook the food, then plate it,"* you set up an assembly line. The Shopper buys the food and puts it on a conveyor belt. The Cook takes it, cooks it, and puts it back on the belt. The Plater finishes it. If the Cook burns the food, a Loop sends it back to the Shopper to buy more.

---

## 3. Implementation Details
- **SequentialAgent (`coordinator_agent.py`):** 
  ```python
  coordinator_agent = SequentialAgent(
      sub_agents=[research_agent, budget_loop, summary_agent]
  )
  ```
  This guarantees that we *never* summarize before we plan, and we *never* plan before we research.
- **LoopAgent (`budget_loop`):** Wraps `planner_agent` and `budget_agent`. If the `budget_agent` determines the plan is too expensive, it outputs feedback but *does not* call the exit tool. The `LoopAgent` sees the exit condition wasn't met and loops back to the `planner_agent` to try again with cheaper options.

---

## 4. Architecture Diagram

```text
      [ Start Sequence ]
              │
              ▼
    ┌────────────────────┐
    │  research_agent    │
    └─────────┬──────────┘
              │
              ▼ (Start Loop)
    ┌────────────────────┐ ◄──────┐
    │  planner_agent     │        │
    └─────────┬──────────┘        │
              │                   │
              ▼                   │
    ┌────────────────────┐        │
    │  budget_agent      │ ──[Over Budget]
    └─────────┬──────────┘
              │
        [Under Budget]
       (Calls exit_loop)
              │
              ▼
    ┌────────────────────┐
    │  summary_agent     │
    └─────────┬──────────┘
              │
              ▼
       [ End Sequence ]
```

---

## 5. Why This Concept Is Needed
**The Problem Solved:** If you put all tasks into one massive prompt for a single agent, the LLM will often skip steps, hallucinate costs, or combine tasks prematurely.
**Benefits Introduced:** High reliability. By compartmentalizing tasks into a pipeline, we can independently test the Research phase vs the Planning phase. The Loop provides a self-healing mechanism to fix errors without bothering the user.

---

## 6. With vs Without This Concept

| Without Workflows (Prompt Only) | With Workflows (Code Pipelines) |
| :--- | :--- |
| LLM might skip the research step and hallucinate a hotel | Code guarantees research runs before planning |
| If over budget, the agent just outputs the expensive plan | Loop automatically retries until budget is met |
| Difficult to debug where the breakdown occurred | Easy to trace which specific node failed |
