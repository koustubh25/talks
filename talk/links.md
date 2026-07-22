# Per-slide reference links

Backstage map: for every demo beat, where the *real* artifact lives (GitHub / Azure).
Open these in advance as pinned tabs or keep this file on the second screen.

IDs: tenant `79fa077b-e5f3-474a-8e36-c79ac59b00ed` · subscription `5d98f681-c627-4a4d-9f1d-001ae04c2358`

## Base URLs

| What | URL |
|---|---|
| Repo | https://github.com/koustubh25/ai-evals-talk |
| Foundry portal (project) | https://ai.azure.com/foundryProject/overview?wsid=/subscriptions/5d98f681-c627-4a4d-9f1d-001ae04c2358/resourceGroups/rg-evals-demo/providers/Microsoft.CognitiveServices/accounts/evalsdemo-ktb-au/projects/proj-evals-demo&tid=79fa077b-e5f3-474a-8e36-c79ac59b00ed |
| Azure portal (resource group) | https://portal.azure.com/#@79fa077b-e5f3-474a-8e36-c79ac59b00ed/resource/subscriptions/5d98f681-c627-4a4d-9f1d-001ae04c2358/resourceGroups/rg-evals-demo/overview |
| Mock inventory API | https://inventory-mock-ktb-au.azurewebsites.net/healthz · [/openapi.json](https://inventory-mock-ktb-au.azurewebsites.net/openapi.json) |

If the `wsid` deep link ever breaks: ai.azure.com → sign in → project **proj-evals-demo** → left nav has **Agents / Tracing / Evaluations / Data Generation**.

## Slides 3–8 — evals philosophy (no live links needed)

Source material if asked "says who?": Hamel Husain & Shreya Shankar (Lenny's Podcast; error analysis, binary judges, 4–7 judges, ~30 min/week), Phil Hetzel/Braintrust (evals ≠ unit tests, "rerun production"), Ankur Goyal/Braintrust (eval suite as the durable asset / living spec). Notes: `.claude/skills/ai-evals-talk/references/`.

## Slide 9 — The setup

- GitHub Actions workflow: https://github.com/koustubh25/ai-evals-talk/blob/main/.github/workflows/eval-gate.yml
- All eval-gate runs: https://github.com/koustubh25/ai-evals-talk/actions
- Foundry agent (versions): portal → **Agents** → `flight-booking-agent`
- Inventory API resource: https://portal.azure.com/#@79fa077b-e5f3-474a-8e36-c79ac59b00ed/resource/subscriptions/5d98f681-c627-4a4d-9f1d-001ae04c2358/resourceGroups/rg-evals-demo/providers/Microsoft.Web/sites/inventory-mock-ktb-au/appServices

## Slide 10 — Meet the agent

- Same conversation, in the portal: Foundry → **Agents** → `flight-booking-agent` → *Playground* (try the same booking live in a chat UI)

## Slides 12–13 — Act 1: PR + red verdict

- PR #1 (the sabotage → fix): https://github.com/koustubh25/ai-evals-talk/pull/1
- Diff view: https://github.com/koustubh25/ai-evals-talk/pull/1/files (net diff is empty — see commits tab for the story)
- Commits (sabotage + fix): https://github.com/koustubh25/ai-evals-talk/pull/1/commits
- The RED run (13m38s, 30 conversations): https://github.com/koustubh25/ai-evals-talk/actions/runs/29558000033 — open the **job summary** for Microsoft's comparison table with confidence intervals
- The eval behind it, in Azure: Foundry → **Evaluations** → `eval_e5df61b29c024e02930467732b820072` (per-conversation scores, judge reasoning)

## Slide 15 — Act 1 fixed (green)

- The GREEN run (10m12s): https://github.com/koustubh25/ai-evals-talk/actions/runs/29558629014
- Its eval in Azure: Foundry → **Evaluations** → `eval_af515a09741c4aaeb7256d56eef2df29`

## Slide 16 — Act 2: the harmless UX PR

- PR #2 (merged): https://github.com/koustubh25/ai-evals-talk/pull/2
- Diff: https://github.com/koustubh25/ai-evals-talk/pull/2/files
- Its green gate run: https://github.com/koustubh25/ai-evals-talk/actions/runs/29574563822

## Slides 17–18 — the incident

- Flip switch (also in deck): `./runbook/degrade.sh on|off|status`
- Watch the mock lie live: https://inventory-mock-ktb-au.azurewebsites.net/flights?origin=MEL&dest=SYD&date=2026-12-24
- App Service logs (if asked "is this real?"): portal → inventory-mock-ktb-au → *Log stream*

## Slide 19 — the trace evidence

- Foundry → **Tracing** — filter agent `flight-booking-agent`, look for `invoke_agent` spans; open one from the capture run (18 hallucinated conversations, 17 Jul)
- Raw store, App Insights: https://portal.azure.com/#@79fa077b-e5f3-474a-8e36-c79ac59b00ed/resource/subscriptions/5d98f681-c627-4a4d-9f1d-001ae04c2358/resourceGroups/rg-evals-demo/providers/microsoft.insights/components/appi-evals-demo/overview → *Logs*, table `AppDependencies`
- KQL to paste there: `AppDependencies | where Name startswith "invoke_agent" | order by TimeGenerated desc`

## Slides 20–21 — close the loop / trace replay

- Traces → dataset: Foundry → **Data Generation** → *Create dataset* → *From traces* (pin agent + version)
- Datasets land in: Foundry → **Data** (a.k.a. Data + indexes)
- Trace replay: Foundry → **Evaluations** → open an eval run → *Replay* (the one portal-only moment in the talk)
- ⚠ `gh pr checks 2` red-gate backend not built yet — pending work item

## Slide 23 — Thanks

- Repo (audience takeaway): https://github.com/koustubh25/ai-evals-talk
