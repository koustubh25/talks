# Research notes — Microsoft Foundry evals landscape (as of 13 Jul 2026)

Source material for slides for "From Unit Tests to Eval Gates: CI/CD for AI Agents," Experts Live Melbourne, 30 Jul 2026. Companion to `demo-plan.md` (which references this file). All statuses verified 13 Jul 2026 — re-verify preview items in talk week; this space moves fast.

## Naming / status headlines (get these right on slides)

- **"Azure AI Foundry" → "Microsoft Foundry"** (rebrand). Old name reads dated to an Azure audience. "Foundry classic" refers to the old agent platform.
- **Evaluations, monitoring, and tracing went GA in March 2026** ([announcement](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/generally-available-evaluations-monitoring-and-tracing-in-microsoft-foundry/4502760)).
- Build 2026 (June) was the big drop for agent observability/eval features — most below are from it ([Build observability blog](https://devblogs.microsoft.com/foundry/build-2026-from-observability-to-roi-for-ai-agents-on-any-framework/), [What's new, Build edition](https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-build-2026/)).

## Feature inventory (GA vs preview)

| Feature | Status | One-liner for slides |
|---|---|---|
| Tracing + evaluations (core) | GA (Mar 2026) | Every model call, tool invocation, sub-agent hop in one OTel pipeline; evals link back to the trace that produced them |
| Framework-agnostic tracing | GA | LangChain, LangGraph, OpenAI SDK, Agent Framework, any custom framework — one trace view via OpenTelemetry |
| `microsoft/ai-agent-evals` GitHub Action | v3-beta | CI eval gate; reports **confidence intervals + statistical significance** — "the red X is statistically real, not noise" |
| **Traces to dataset** | Preview, region-gated | One click: production trace → versioned eval dataset, intelligent sampling picks representative traces. "Production traces are the highest-fidelity test data you have" (Microsoft's words) |
| **Trace replay** | Preview | Step-by-step visual replay of an agent run; replay a captured trace against a candidate fix |
| Continuous evaluation on production traffic | Available (intelligent trace sampling in preview) | Same evaluator definitions run in CI **and** on sampled live traffic, alerting on quality/safety/cost drift |
| User simulation + multi-turn evaluation | Preview | Auto-generates multi-turn conversations & edge cases to pressure-test agents pre-ship; USR-8 rubric research behind it |
| Rubric evaluator | Preview | Generates context-aware weighted criteria (task success, tone, safety, cost, latency) from intended behavior |
| **Agent Optimizer** | Public preview ~early Jul 2026 | Consumes production traces + evals → ranked candidate prompt/skill fixes → validates → recommends winner with diffs, lineage, rollback |
| ASSERT + ACS | Open source | Policy-driven agent evaluation framework (Adaptive Spec-driven Scoring for Evaluation and Regression Testing) from MSR |
| AI Red Teaming Agent | Preview | PyRIT-based automated adversarial probing, incl. Foundry agents with tool calls |
| Agent registry / control plane | Available | Records which agent version is live where, who deployed, when — audit story |
| ROI dashboard | Private preview | Agent costs → business metrics (task completion, time saved) |

## How this maps to the talk narrative

- **Thesis validation:** the talk's core argument — "the gate alone isn't the system; gate + trace review + feedback loop is" — is exactly what Microsoft productized at Build 2026. Frame it as: *the workflow I'm showing you manually is the workflow the platform is absorbing.*
- **Demo Act 1** uses the GA/stable layer (action v3-beta, built-in evaluators, statistical significance callout).
- **Demo Act 2** climax = **Traces to dataset** (the manual loop becomes one click) + **Trace replay** against the fix. Both preview → pre-record.
- **Closing slide** = continuous evaluation + Agent Optimizer: "eval gates are becoming a *continuous* surface, and the fix loop itself is being automated." Name-drop user simulation ("generate the degraded-scenario conversations you never thought to write"), ASSERT, AI Red Teaming Agent.
- Quotable industry framing: The New Stack on Foundry — Microsoft is betting enterprise AI is about **reliability, not capability** ([article](https://thenewstack.io/microsoft-foundry-build-2026-ai-agents/)). Perfect epigraph for the talk.

## Stage-ready sound bites

- "Production traces are the highest-fidelity test data you have." (Microsoft, Build 2026)
- "The gate didn't fail — it caught everything it was built to catch. The dataset failed."
- "This red X comes with a p-value: the gate knows the difference between a regression and noise."
- "The loop we just closed by hand? That's a product feature now."

## Practical constraints (demo build)

- Azure free account: US$200 / 30 days, started ~13 Jul → expires ~12 Aug (covers the 30 Jul talk). Free-tier model quota is restricted; may need pay-as-you-go upgrade (credit carries over). Use smallest viable deployment (e.g. gpt-4o-mini class).
- Preview features are **region-gated** — check [traces-to-dataset supported regions](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/traces-to-dataset) before creating the project.
- `ai-agent-evals` action: v3-beta for current Foundry agents; v2-beta only for classic. Docs: [run an evaluation in GitHub Action](https://learn.microsoft.com/en-us/azure/foundry/how-to/evaluation-github-action).

## Source list

- https://devblogs.microsoft.com/foundry/build-2026-from-observability-to-roi-for-ai-agents-on-any-framework/
- https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-build-2026/
- https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-june-2026/
- https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/generally-available-evaluations-monitoring-and-tracing-in-microsoft-foundry/4502760
- https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/traces-to-dataset
- https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/intelligent-sampling-in-microsoft-foundry-the-science-behind-selecting-better-pr/4523722
- https://github.com/microsoft/ai-agent-evals
- https://learn.microsoft.com/en-us/azure/foundry/how-to/evaluation-github-action
- https://learn.microsoft.com/en-us/azure/foundry/concepts/observability
- https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/evaluating-multi-turn-agents-a-quality-study-of-microsoft-foundry%E2%80%99s-multi-turn-e/4524106
- https://learn.microsoft.com/en-us/azure/foundry/concepts/ai-red-teaming-agent
- https://thenewstack.io/microsoft-foundry-build-2026-ai-agents/
