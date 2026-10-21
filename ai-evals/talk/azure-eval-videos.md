# Azure eval videos — to go deeper (curated, Jul 2026)

Azure/Microsoft-Foundry-specific YouTube videos on evals, LLM-as-judge, CI gates, and
observability. Deliberately **excludes** the five vendor-neutral videos already distilled
in the `ai-evals-talk` subagent (Hamel Husain, Shreya Shankar, Ankur Goyal, Phil Hetzel,
Aakash Gupta) — these are the Azure-native complement to those.

Ranked by usefulness for *this* talk (pre-production eval gates on Foundry).

## Start here — official Foundry walkthroughs

1. **AI Show: On Demand — Evaluating Azure AI Foundry Agents** · Seth Juarez & Chang Liu · Apr 2025
   https://www.youtube.com/watch?v=B1NCt4TLnik
   Most approachable intro; walks the portal + SDK eval flow with sample resources. Good first watch.

2. **Automate evaluations | Microsoft Foundry** · May 2026
   https://www.youtube.com/watch?v=gS3dvMzm89M
   Short, current. Automating quality/safety/performance evals — closest to our CI-gate framing.

3. **Building and evaluating AI agents with Foundry Agent Service | ODSP1411** · Nov 2025
   https://www.youtube.com/watch?v=oF5ib8AIVCE
   End-to-end: build an agent, then evaluate it. Ties the agent + eval story together.

## The CI-gate / SDK internals (most relevant to our demo)

4. **Agentic Excellence: Mastering AI Agent Evals w/ Azure AI Evaluation SDK** · Cedric Vidal (Microsoft) · AI Engineer conf
   https://www.youtube.com/watch?v=J4vPq2i0QzE
   Deepest technical talk — the `azure-ai-evaluation` SDK, judge design, running evals in code.
   Best single video for the machinery behind our `verdict.py` / `ci_gate.py`.

5. **Evaluating Multi-Turn AI Agents with Azure AI Foundry | DEM593** · May 2025
   https://www.youtube.com/watch?v=LME5JAEpEr0
   Multi-turn conversation evaluation — mirrors our 30-conversation, multi-turn suite.

## Observability + eval (the production loop — hand-off to the other talks in our slot)

6. **Observe and evaluate agents for quality and safety in Microsoft Foundry** · Microsoft Mechanics · Jun 2026
   https://www.youtube.com/watch?v=JQFyd-RvfGo
   Most up-to-date; GA tracing + evals + monitoring in the Foundry Control Plane.

7. **Monitor, optimize and scale with AI Observability in Microsoft Foundry | BRK190** · Build 2026
   https://www.youtube.com/watch?v=LOLI0emzDb0
   The continuous-evaluation-on-production-traffic story (our Act 2 closing loop).

8. **AI and Agent Observability in Azure AI Foundry and Azure Monitor | BRK168** · Build
   https://www.youtube.com/watch?v=QGVoTJLKnYk
   Tracing → evaluation → monitoring pipeline; how evals link back to the trace that produced them.

## Adjacent / optional

9. **How to Choose the Right AI Model | Benchmark Evaluation Guide**
   https://www.youtube.com/watch?v=2dgUOyRslkI
   Model-selection benchmarking (evals-for-models, not evals-for-products) — context, not core.

10. **How to use Agent Evaluation in Microsoft Copilot Studio**
    https://www.youtube.com/watch?v=VwjKUXsfsVQ
    Low-code/Copilot Studio angle — useful if any audience members live in that world.

## Watch order if short on time
For the talk specifically: **#4 (SDK internals) → #2 (automation) → #7 (production loop)**.
For a gentle ramp: **#1 → #6 → #4**.
