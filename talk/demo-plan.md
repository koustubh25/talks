# Demo plan — "Green CI, broken production"

For: "From Unit Tests to Eval Gates: CI/CD for AI Agents," Experts Live Melbourne 2026.
Audience: 10 minutes of a 20-minute slot, live (or recorded fallback) after the talk portion (`script.md`, slide 6 → demo).

This file is written to be picked up by an AI coding assistant to actually build the demo assets. It specifies the scenario, the exact bug, the eval setup, and the two acts precisely enough to implement without further clarification — flag anything genuinely ambiguous back to Koustubh rather than guessing silently.

> **Currency note (updated 2026-07-13):** "Azure AI Foundry" has been rebranded **Microsoft Foundry**; its evaluation/tracing stack went GA in March 2026, and Build 2026 (June) added the preview features this plan now leans on. Use current product names in all assets. Full research notes for slides: `talk/research-notes.md`.

---

## 1. Premise (do not skip this framing when building)

A travel-booking agent passes its CI eval gate cleanly. It ships. During a holiday-season traffic surge, the flight-availability tool it depends on starts degrading (slow / partial / error responses) under load — a condition that never appeared in the offline eval dataset, which was captured under normal, low-season traffic. The agent, never having seen a degraded tool response, fills the gap with a hallucinated "confirmed" booking instead of surfacing the uncertainty. A production trace exposes this. The team mines that trace into a new eval, redeploys, and the gate now catches it.

**The point of the demo is not "look, a bug."** It's: the gate did its job (caught what it was built to catch), and the *system* — gate + trace review + feedback loop — is what closes the gap, not the gate alone. Don't let the demo read as "the gate failed and was useless."

## 2. The agent under test

- **Domain:** a simple flight-booking assistant. Tools:
  - `search_flights(origin, destination, date)` → returns a list of flights with seat availability and price.
  - `book_flight(flight_id, passenger_name)` → attempts to book; returns a confirmation or an error/unavailable status.
- Build this as a small, real, runnable agent (not just a mock in slides) — e.g. a Foundry Agent Service agent, or a lightweight agent using the Microsoft Foundry SDK, with `search_flights` and `book_flight` as tool functions backed by a small in-memory/mock inventory service (a tiny local API is fine — it needs to be controllable so the demo can force a degraded response on cue). Foundry tracing is now framework-agnostic via OpenTelemetry, so a simple local SDK agent still lands in the Foundry trace viewer — no need to host it in Agent Service just for tracing.
- Keep the surface area small. The demo needs to run reliably twice (once in rehearsal, once live) — do not depend on a real third-party flight API.

## 2.5 GCP → Azure Rosetta stone (for Koustubh's mental model)

Koustubh thinks in GCP. Use this table to translate — but **the implementation is Azure/Foundry only**; GCP names must never appear in demo assets, slides, or code, this section is purely a comprehension aid.

| What we're doing | GCP equivalent (mental model) | Azure/Foundry (what we actually build) |
|---|---|---|
| AI platform umbrella | Vertex AI | **Microsoft Foundry** (ex "Azure AI Foundry") |
| Project container | GCP project + Vertex AI resources in a region | Foundry **project** (under a hub; region matters for previews) |
| The LLM behind the agent | Gemini Flash endpoint on Vertex | A small Foundry **model deployment** (gpt-4o-mini class) |
| Agent runtime/SDK | Agent Development Kit (ADK) / Vertex AI Agent Engine | **Foundry SDK** local agent (we skip Foundry Agent Service — like using ADK locally instead of deploying to Agent Engine) |
| Tool functions | ADK function tools | Foundry SDK tool functions (`search_flights`, `book_flight`) |
| Offline eval service | Vertex AI Gen AI Evaluation Service (pointwise metrics, trajectory eval) | Foundry **built-in agent evaluators** (Task Adherence ≈ trajectory/instruction-following metrics; Tool Output Utilization ≈ tool-use/grounding metrics) |
| Eval in CI | Gen AI eval run from Cloud Build / GitHub Actions (you'd wire it yourself) | **`microsoft/ai-agent-evals` GitHub Action v3-beta** — packaged, with confidence intervals + significance tests built in |
| Tracing | Cloud Trace + Cloud Logging (OTel) | **Foundry tracing** → Application Insights (also OTel; same mental model, different viewer) |
| Trace → eval data | Roughly: BigQuery-logged prompts/responses → hand-built eval dataset | **Traces to dataset (preview)** — productized one-click version of that pipeline, with intelligent sampling |
| Replay a trace against a fix | No direct Vertex equivalent | **Trace replay (preview)** |
| Prod quality monitoring | Vertex AI model monitoring / eval on live traffic | Foundry **continuous evaluation** on sampled production traffic with drift alerts |
| CI/CD system | Cloud Build | GitHub Actions (our choice; Azure DevOps is the alternative) |
| Free credits | $300/90-day GCP free trial | **$200/30-day Azure free account** (tighter: expires ~12 Aug) |

Biggest mindset shifts from GCP: (1) Foundry bundles evals+tracing+CI gating into one opinionated product surface, where Vertex leaves more assembly to you — lean on the packaged pieces instead of hand-rolling; (2) region choice gates preview features much more aggressively than typical Vertex previews — pick the region for feature availability first, latency second.

## 3. Act 1 — the gate catches a real bug (target: ~4 min)

Goal: show the CI eval gate doing exactly what slides 4–5 promised.

1. Prepare an offline eval dataset (~10–15 examples) of realistic booking conversations, captured under "normal" conditions — the mock inventory service always responds quickly and cleanly (either a clean list of available flights, or a clean "sold out" response).
2. Wire up `microsoft/ai-agent-evals` (GitHub Action, **v3-beta** — v2-beta is for Foundry *classic* agents only) or the Azure DevOps equivalent, using Foundry's built-in agent evaluators — at minimum **Task Adherence** and **Tool Output Utilization** (these are the two most relevant to "did the agent correctly reflect what the tool told it"). The action reports **confidence intervals and statistical-significance tests** on scores — call this out on stage: the gate says the regression is *statistically real*, not run-to-run noise.
3. Prepare a PR that introduces an *obviously bad* agent change unrelated to the holiday bug — e.g. a prompt edit that causes the agent to skip calling `search_flights` before claiming a seat is available. This is Act 1's bug: simple, clearly wrong, and something the offline dataset already exercises well.
4. Run the eval gate live (or show a pre-run CI job) → red, PR blocked. Show the evaluator output/score explaining why.
5. Fix the prompt, re-run → green, merge. This closes Act 1 cleanly: the gate works exactly as advertised.

**Have this pre-staged**, not typed live: PR already open, CI already configured and tested end-to-end at least once in rehearsal, terminal/browser tabs pre-loaded and already authenticated.

## 4. Act 2 — the twist: holiday season, degraded tool, hallucinated confirmation (target: ~5–6 min)

Goal: show a *different*, subtler change that passes the same gate cleanly, then reveal what happens when the mock inventory service degrades — simulating a real holiday-season load spike — during a scenario the offline dataset never covered.

1. **The change that ships clean:** a plausible, unrelated feature change (e.g. adding a "list nearby dates" tool, or adjusting the response formatting) that passes Task Adherence / Tool Output Utilization against the *existing* offline dataset, because that dataset still only contains clean tool responses.
2. **The degrade:** add a mode to the mock inventory service that, on cue, returns a slow/timeout or malformed response for a specific popular route (simulate "holiday load"). This can be a simple flag/env var/query param you flip live — do not rely on actually generating real load.
3. **The production trace:** run the agent live against the degraded mode. Expected failure: the agent does not surface "I couldn't confirm availability" — it fabricates a flight number, price, and a "confirmed" seat that doesn't exist. Capture this as a trace (Foundry tracing / any OTel-based tracing works) so it can be walked through visually — a trace viewer UI is much stronger on stage than reading raw JSON.
4. **Walk the trace live**, pointing out precisely where the tool response was degraded and where the model's output diverges from it into fabrication.
5. **Name the root cause on stage** (ties back to `script.md` / the talk's slide 6 framing): the offline dataset only ever exercised the tool's happy path; a degraded/error tool response was a scenario nobody wrote into eval data, because nobody had seen it happen yet.
6. **Close the loop, on stage — use Foundry's productized loop, don't hand-build it:**
   - Use **Traces to dataset (preview)** in the Foundry portal: select the hallucinated-booking trace → *Create dataset* — Foundry's intelligent sampling turns production traces into a versioned eval dataset with no code. This replaces hand-writing the new test case and is the demo's "mind-blow" moment: the manual feedback loop from the talk narrative is now one click. (Preview + region-gated: verify availability in the project's region during week-1 setup, and pre-record this segment.)
   - Still add the targeted code-based check: given a degraded/error/empty tool response, the agent's output must not assert a confirmed booking — it must surface uncertainty or retry, never fabricate (e.g. tool-call trace shows error state while final response says "confirmed"). Faster to build and easier to demo than a new LLM judge.
   - Re-run the eval gate against the new dataset+check: it now correctly fails the same "clean" change from step 1 when replayed against the degraded scenario.
   - Fix the agent, then use **Trace replay (preview)** to replay the *same* captured degraded-tool trace against the fixed candidate — show it now surfaces uncertainty instead of fabricating. Stronger closer than just re-running the suite.
   - Redeploy the fixed agent version through the Dev→Test→Prod pattern from slide 5; show the new eval passing.
7. **Closing slide (mention, don't demo):** the same evaluator definitions now run continuously on sampled production traffic with drift alerts (continuous evaluation), and **Agent Optimizer** (public preview ~July 2026) automates this exact loop — consumes production traces + evals, proposes ranked prompt fixes with diffs and rollback. "The loop we just closed by hand is becoming a product feature." See `research-notes.md` for the full list (user simulation, rubric evaluator, ASSERT, AI Red Teaming Agent).

## 5. Risk management (read before rehearsing)

- **This demo has two live surfaces (Act 1 CI run, Act 2 live agent + trace).** That's already a lot for a 10-minute, no-recovery-time slot. Strongly consider **pre-recording Act 2** (the degraded-tool/hallucination/trace-walkthrough part) as a screen capture, and presenting it as "here's a trace we pulled" rather than triggering it live — the audience cannot tell the difference, and it removes the riskiest live-agent-behavior dependency from the room. Act 1 (a CI job going red/green) is comparatively safe to run live since it's deterministic infrastructure, not model behavior.
- Rehearse the full sequence at least twice end-to-end before the talk, on the actual hardware/network you'll present with.
- Pre-stage everything: all auth done in advance, all browser tabs/terminal panes already open and positioned, PRs already created (not created live), mock service already running in the background.
- Have a static fallback (a few annotated screenshots of each key moment: red gate, green gate, the hallucinated trace, the fixed re-run) in case both the live and recorded demo fail — this should never leave you with nothing to show.
- Keep the mock inventory service and agent completely local/offline-capable — no dependency on a real external flight API or live internet connectivity for the demo to run.
- **Azure free account caveats:** the US$200/30-day credit expires ~12 Aug 2026 (fine for a 30 Jul talk), but free-tier model quota is restricted and some deployments require upgrading to pay-as-you-go (the credit survives the upgrade). The preview features this demo depends on (Traces to dataset, Trace replay) are **region-gated** — pick the Foundry project's region for feature availability, and verify both work in week 1, not talk week.

## 6. Assets to produce before the talk

- [ ] Mock inventory service (local, with a togglable "degraded mode" for a specific route)
- [ ] Booking agent (Foundry Agent Service or Azure AI Foundry SDK) with `search_flights` / `book_flight` tools
- [ ] Offline eval dataset v1 (~10–15 clean examples)
- [ ] `microsoft/ai-agent-evals` GitHub Action (or Azure DevOps task) wired into a repo, tested end-to-end
- [ ] Act 1 PR (the obviously-bad prompt change) pre-created
- [ ] Act 2 "clean-looking" PR (the change that passes offline eval but is vulnerable to the degraded-tool case) pre-created
- [ ] Tracing set up (Foundry tracing or OTel) so the hallucinated-booking trace can be visually walked through
- [ ] Screen recording of Act 2 as a fallback (recommended default, see risk section)
- [ ] Offline eval dataset v2 (v1 + the new degraded-tool-response test case) and the new code-based check
- [ ] Static screenshot fallback set (red gate / green gate / hallucinated trace / fixed re-run)
