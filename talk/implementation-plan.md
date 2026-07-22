# Implementation plan — demo build ("Green CI, broken production")

Companion to `demo-plan.md` (the *what*); this is the *how*, in gated phases. Nothing in a phase is executed until Koustubh approves that phase — each ends with an explicit **GATE**. GCP analogies inline (🟦) per `demo-plan.md` §2.5; implementation is Azure-only.

**Region decision: `australiaeast` (Sydney).** Verified 13 Jul 2026: it's on the official supported-regions list for Traces to dataset (preview), and has all candidate small models (gpt-4o-mini, gpt-4.1-mini/nano, gpt-5.x-mini/nano). Australia Southeast (Melbourne) does not carry AI services — Sydney is the only Australian option.

## Phase 0 — preliminary inspection ✅ (done 13 Jul, read-only)

- az CLI 2.88.0 authenticated as kosta250@gmail.com; subscription `5d98f681-…2358` ("Azure subscription 1", free account) enabled.
- Azure MCP server + `azure:microsoft-foundry` plugin skill available (covers agent scaffold, batch/continuous eval, dataset-from-traces flows).
- `Microsoft.CognitiveServices` provider **NotRegistered** (normal for fresh subscription). 🟦 Like a new GCP project before `gcloud services enable`. Consequence: quota numbers unreadable until Phase 1 registers it.
- Traces-to-dataset facts that shape the demo (from docs): portal flow is *Data Generation → Create dataset → From traces*; intelligent sampling is on by default; **min 15 samples per generation job**; App Insights ingestion lag 30–90 s (never demo the conversion immediately after capturing the trace); connected App Insights must allow public network access; pin `agent_version` when generating.

## Phase 1 — subscription prep (~5 min, $0)

1. Register resource providers: `Microsoft.CognitiveServices`, `Microsoft.Insights`, `Microsoft.OperationalInsights`, `Microsoft.Storage`. Free, reversible, no resources created.
2. Create resource group `rg-evals-demo` in `australiaeast`. 🟦 Rough equivalent of a GCP project as a billing/lifecycle container — deleting the RG at the end deletes everything in one command (that's our teardown).
3. Create a **budget alert** at $50 and $100 on the subscription (email to kosta250@gmail.com). Free account has a hard spend cap, but alerts give early warning during rehearsals.
4. Re-check quota now that the provider is registered: `az cognitiveservices usage list -l australiaeast` — confirms which small model we can actually deploy and at what TPM. Free-tier quota is restricted; if a model has zero quota we pick the next candidate (order: gpt-4.1-mini → gpt-4o-mini → gpt-5.4-mini).

**GATE 1: Koustubh approves provider registration + RG + budget.** ✅ Approved & executed 2026-07-13 (`demo/infra/01-subscription-prep.sh`). **Quota finding: `gpt-5-mini` (GlobalStandard, 500K TPM) is the only OpenAI chat model with free-tier quota in australiaeast — all original candidates had zero. Phase 2 model = `gpt-5-mini`.**

## Phase 2 — Foundry project + model + tracing backbone (~30 min, cents/day)

1. Create the Foundry resource (AIServices kind) + a **Foundry project** in `rg-evals-demo`, `australiaeast`. 🟦 Vertex AI in a region-enabled project.
2. Deploy the chosen small model (from Phase 1.4) with the minimum TPM that quota allows. 🟦 A Gemini Flash endpoint; billing is per-token, idle cost ≈ $0 for standard deployments.
3. Create Application Insights + connect it to the project (public network access ON — required by traces-to-dataset). 🟦 Cloud Trace/Logging sink.
4. Smoke test: one SDK call through the project endpoint; confirm the span shows up in the Foundry tracing UI.
5. Record everything (endpoint, deployment name, RG) in `demo/.env.example` + a `demo/infra/` script so the whole thing is reproducible from zero.

Cost estimate: model calls only — a full rehearsal is ~50–100 small-model calls ≈ **well under $1**. Biggest cost risk is App Insights ingestion, still expected < $5 total.

**GATE 2: Koustubh approves resource creation (this starts consuming credit).** ✅ Approved & executed 2026-07-13 (`demo/infra/02-foundry-setup.sh`). Live: account `evalsdemo-ktb-au`, project `proj-evals-demo` (endpoint in `demo/.env.example`), `gpt-5-mini` @ 50K TPM GlobalStandard, `law-evals-demo` + `appi-evals-demo` connected to the project. Smoke test passed (96 tokens). Note: app-insights CLI extension broken on this machine — App Insights managed via generic `az resource`/`az rest` instead.

## Phase 3 — local build: mock service, agent, dataset v1 (~half day, $0 infra)

All local; no new Azure resources.

1. `demo/inventory-service/` — tiny FastAPI app: `/flights` (search) + `/book`. Degraded mode togglable via env var/endpoint for one popular route (e.g. MEL→SYD on a holiday date): timeout / HTTP 503 / truncated JSON.
2. `demo/agent/` — flight-booking agent on the Foundry SDK with `search_flights` / `book_flight` tool functions calling the mock service; OTel instrumentation exporting to the connected App Insights. 🟦 An ADK agent run locally, tools as plain Python functions.
3. `demo/evals/dataset-v1.jsonl` — 10–15 clean booking conversations (happy path + clean sold-out).
4. Run agent against dataset locally with `azure-ai-evaluation` (Task Adherence, Tool Output Utilization) to sanity-check scores before any CI wiring.

**GATE 3: Koustubh reviews agent behavior + baseline eval scores locally.** Built 2026-07-16, pending review. Live: mock service (port 8787, degraded mode verified MEL→SYD only), agent `flight-booking-agent` v1 as a *versioned prompt agent* in `proj-evals-demo` (azure-ai-projects 2.x: published via `agents.create_version`, invoked via OpenAI Responses API with `agent_reference`; tools executed locally), OTel spans (`invoke_agent flight-booking-agent:1`) confirmed in App Insights. Baseline eval 12/12 pass on Task Adherence + Tool Output Utilization (judge = gpt-5-mini with `is_reasoning_model=True`). Findings: (a) data-plane RBAC needed — `Cognitive Services User` on the account (`03-rbac.sh`; docs' "Azure AI User" role doesn't exist in this tenant); (b) evaluators need the agent *message protocol* (assistant/tool message lists) — passing raw strings silently drops tool calls and fails everything (great war story for the talk).

## Phase 4 — CI gate: GitHub + ai-agent-evals (~half day)

1. ✅ GitHub repo `koustubh25/ai-evals-talk` (rooted at `demo/`), pushed by Koustubh.
2. ✅ OIDC federated credentials, done MANUALLY by Koustubh 2026-07-16 (learning exercise), captured in `04-ci-oidc.sh`: app `gh-evals-demo` (clientId bf761fea-…), fed creds for PRs + main, `Cognitive Services User` on the Foundry account, gh secrets set. 🟦 Workload Identity Federation.
3. ✅ **Architecture change (approved)**: ai-agent-evals runs agents *server-side in Foundry*, so localhost function tools can't work in CI. Mock deployed publicly — App Service F1 (free), `https://inventory-mock-ktb-au.azurewebsites.net` (`05-inventory-appservice.sh`; `az containerapp` blocked by the extension bug; `az webapp up` needed the DYLD expat workaround, now in the script). Agent v4 uses an **OpenAPI tool** (spec fetched live from `/openapi.json`; admin/health endpoints hidden from schema). Reliability findings: fresh agent versions take seconds to propagate (warm-up canary in run_local), and gpt-5-mini intermittently narrates instead of calling tools (retry-on-no-tool-call shim in `run_conversation`). Re-baseline: 10–12/12, two borderline rows are judge variance → gate on aggregates, not perfection.
4. ✅ Workflow `eval-gate.yml`: OIDC login → publish PR code as candidate agent version → `ai-agent-evals@v3-beta` compares vs `evals/BASELINE_AGENT` → `evals/ci_gate.py` fails on machine-readable `Degraded` verdict (the action itself never fails the job; rendered markdown is not greppable). GitHub 2026 OIDC subjects embed account/repo IDs — fed creds updated. Dataset: 30 queries (n=12 flip-flopped across the significance boundary).
5. ✅ **Act 1 rehearsed on PR #1** (2026-07-17): sabotage commit → 🔴 task adherence −50.7pts p<0.001; fix commit → 🟢 delta +0.09 p=0.45. Note: first sabotage attempt was too subtle — the model kept searching anyway; decisive sabotage explicitly forbids searching popular routes. All gotchas in `talk/learnings.md`.

**GATE 4: Act 1 verified red→green in CI at least once. ✅ 2026-07-17. Koustubh to review PR #1's checks tab + job summaries.**

## Phase 5 — Act 2 assets: degrade, trace, close the loop (~1 day)

1. Create **Act 2 PR** (benign formatting/feature change) → passes gate against dataset v1.
2. Flip degraded mode, run the agent on the vulnerable route, capture the hallucinated-confirmation trace; verify it's walkable in the Foundry tracing UI. (May need prompt nudging to reliably reproduce fabrication — this is the least deterministic step; budget iteration time.)
3. Wait ≥90 s (ingestion lag), then run **Traces to dataset** from the portal (min 15 samples means we drive ~15–20 conversations through the degraded window, not just one). Produces dataset v2 input.
4. Add the code-based check (tool error state + "confirmed" in final answer ⇒ fail) as a custom evaluator in the workflow; re-run gate on the Act 2 PR → now red.
5. Fix the agent (surface uncertainty on tool failure), use **Trace replay** against the fix, re-run gate → green.
6. Screen-record the whole Act 2 sequence as the recommended fallback; capture the static screenshot set.

**GATE 5: rehearsal sign-off; recording quality approved.**

## Phase 6 — talk-week ops

- Two full end-to-end rehearsals on presentation hardware/network (per `demo-plan.md` §5).
- Pre-stage: tabs, auth, PRs open, mock service running.
- **Teardown after the talk:** `az group delete -n rg-evals-demo` + delete the Entra app registration. Credit expires ~12 Aug regardless.

## Standing rules for the build

- Every Azure mutation goes through a script checked into `demo/infra/` — nothing click-ops except the two portal moments that *are* the demo (traces-to-dataset, trace replay).
- Explain-before-execute: each phase's commands get walked through with Koustubh before running (he's learning the Azure side; 🟦 analogies in every explanation).
- Cheapest viable everything; check `azure:azure-cost` after each rehearsal.
