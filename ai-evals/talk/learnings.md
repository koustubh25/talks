# Learnings log — "Green CI, broken production" build

Running log of non-obvious lessons hit while building the demo. Add to this every session; many entries double as slide material. (🟦 = GCP analogy per demo-plan §2.5.)

## Azure platform

- **Data-plane RBAC is separate from control-plane.** Subscription Owner couldn't call the Foundry project API. Needed `Cognitive Services User` on the account (docs say "Azure AI User" — that role doesn't exist in this tenant). Propagation took ~5–10 min and the error message changed shape mid-propagation. 🟦 Project owner still needs `roles/aiplatform.user`. (`infra/03-rbac.sh`)
- **Free-tier model quota decides your model, not you.** All planned candidates had limit=0 in australiaeast; only `gpt-5-mini` had quota. Check `az cognitiveservices usage list` before promising a model.
- **az CLI extensions are broken on this machine** (Homebrew python@3.14 pyexpat vs system libexpat). Started as "can't install extensions", later broke core `az webapp up`. Workaround baked into scripts: `export DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib`. Root fix someday: `brew upgrade expat python@3.14 azure-cli`.
- **App Service F1 is the free way to get a public URL without Docker** when Container Apps is unavailable (extension bug). FastAPI needs an explicit `--startup-file`; cold start ~30s; 60 CPU-min/day cap. 🟦 App Engine free tier.

## Foundry agents (azure-ai-projects 2.x — the 2026 SDK)

- **Agents are versioned prompt agents now**, not threads/runs. Publish with `agents.create_version` (idempotent — unchanged definition returns same version); invoke via OpenAI Responses API with `extra_body={"agent_reference": {"type": "agent_reference", "name": ..., "version": ...}}`. The old `{"agent": ...}` payload is deprecated.
- **Fresh agent versions propagate eventually.** First requests after `create_version` can hit a stale config **with no tools** and return empty output. Always warm up with a canary before measuring (in `agent/publish.py` and `evals/run_local.py`).
- **gpt-5-mini sometimes narrates instead of acting** ("Searching now… one moment" → ends turn, no tool call; occasionally prints tool arguments as text). Mitigations: explicit "act, don't narrate" instruction rule + retry when a response has zero tool calls (`run_conversation`).
- **OpenAPI tools = server-side execution.** Fetch the spec from the live service's `/openapi.json` so schemas can't drift; set FastAPI `operation_id`s (they become tool names), `servers` (base URL), and `include_in_schema=False` on endpoints the agent must not discover (the degrade switch!).

## Evals

- **Evaluator input format failures are SILENT and catastrophic.** Passing plain strings → "falling back to raw input, accuracy will degrade" → judge saw no tool evidence → scored everything 0. Correct format: agent message protocol (content as typed blocks, tool_calls as assistant/tool message pairs, system instructions included). **When the eval got better, it immediately caught a real bug** (agent booked a sold-out flight) that the degraded eval had been passing. → Sanity-check your evals before trusting them; eval quality gates bug discovery.
- **Reasoning models as judge need `is_reasoning_model=True`** in azure-ai-evaluation evaluators (else `max_tokens` errors from gpt-5-mini).
- **Judge variance is real.** Two rows fail intermittently on judgment-call grounds even when the agent behaved correctly. → CI gates on aggregates/statistics, never on 12/12 perfection.
- **Catalog evaluator names** for the CI action: `builtin.task_adherence`, `builtin.tool_output_utilization` (verified via `project.beta.evaluators.get_version(name, "latest")`).

## CI gate (microsoft/ai-agent-evals@v3-beta)

- **The action runs agents SERVER-SIDE in Foundry** (`azure_ai_target_completions` eval runs). Local/client-executed function tools cannot work in CI — this forced the OpenAPI-tool + public-mock architecture.
- **The action never fails the job.** It writes a comparison report (confidence intervals, Improved/Degraded + significance) to the step summary. The red X needs your own gate step (we grep the summary for "Degraded").
- **agent-ids format is `name:version`**; dataset is JSON (`{"name", "evaluators": [...], "data": [{"query"}...]}`), not JSONL.
- **Sabotage for a red-gate demo must be decisive.** First Act 1 attempt ("answer from context; search when you need exact details") didn't change behavior — the model decided it always needs exact details and kept searching; 10/12 vs 10/12 → green. That green was CORRECT (no significant difference), which is itself the point of statistical gating: it doesn't punish noise, only real regressions. The working sabotage explicitly forbids searching popular routes and makes flight ids constructible.
- **12 samples sit ON the significance boundary — verdicts flip-flop.** Identical sabotaged agent, two runs: p=0.034 (Degraded) then p=0.063 (Inconclusive). A gate that flips on rerun is worse than no gate. Dataset expanded to 30 queries so a real ~40-point regression lands far below p=0.05 every time. Slide-worthy: sample size is a reliability knob, not a detail.
- **Gate on the machine-readable verdict, never the rendered report.** First gate grepped the job summary for "Degraded" — but the summary renders effects as colored icons/tooltips, so a *detected* regression (Degraded, delta −0.41, p=0.034) still passed the gate. Fix: `evals/ci_gate.py` reads the comparison insight from Foundry (`project.beta.insights`, match on `request.evalId`; effects per metric in `result.comparisons[].compareItems[].treatmentEffect`). Rendered markdown is UI, not contract.
- **`tool_output_utilization` yielded almost no samples in server-side CI runs** (1 result across 24 conversations) while `task_adherence` scored all rows. Comparison currently rides on task adherence; investigate the data mapping before relying on the second evaluator. [open question]
- **Separate propagation checks from behavior checks.** The publish warm-up must only verify the version is reachable — if it also demands tool use, a sabotaged candidate fails at publish instead of at the gate, ruining the red-gate story.

## Act 2: engineering a reproducible hallucination

- **5xx from an OpenAPI tool never reaches the model.** Foundry's executor fails the whole response with `tool_user_error` (400) — no hallucination path via HTTP errors. Silent degradation must be **200 with lying content**. (Also: the executor redacts query params in its error messages.)
- **Explicit failure payloads don't induce hallucination.** With "booking NOT confirmed" in the body, gpt-5-mini stayed honest 100% of the time, even under user pressure. Honesty had to be dismantled in layers:
  1. ambiguous payload ("accepted and queued", ref number, no confirmation) → still honest 4/4
  2. + benign-looking tone prompt ("avoid hedging words like pending; hide system details") → 1/4 hallucinated
  3. + "Booked: ..." summary template line + **"seat held for passenger"** phrasing in the payload → **4/5 hallucinated**
- **The Act 2 PR is the vector, and it's genuinely benign-looking**: a customer-tone rule + a response-format template. On healthy routes behavior is identical (real confirmation codes exist), so the CI gate passes honestly. The bug only exists at the intersection of (tone prompt × degraded tool × rushed user) — exactly the "no eval would have caught this a priori" story.
- **Hallucination needs a multi-turn rushed user.** Single-turn, the agent asks clarifying questions and surfaces warnings. Turn 2 "don't ask me anything else, confirm it now" is what breaks it. Use `previous_response_id` to chain turns in the Responses API.

## GitHub / security

- **2026 GitHub OIDC subjects embed immutable IDs**: `repo:owner@OWNER_ID/name@REPO_ID:pull_request`. Classic `repo:owner/name:...` federated credentials silently stop matching (AADSTS700213). Get IDs: `gh api repos/OWNER/NAME --jq '.id, .owner.id'`. (`infra/04-ci-oidc.sh`)
- **.gitignore before first push, always.** `.env` (with the App Insights connection string) went out in the initial public push. Recovery: purge from history (amend + force-push), rotate the credential — App Insights connection strings can't be rotated in place; the resource must be recreated (`infra/06-rotate-appinsights.sh`). Trace data survives (it lives in Log Analytics).
- **az CLI shell quoting eats subjects** — `:ref` got mangled inside inline JSON; pass `--parameters @file.json` for anything with colons.

## presenterm: wide/side-by-side ASCII boxes don't survive
- presenterm soft-wraps exec output lines at spaces when its "counted width" exceeds ~⅔ of the window; box-drawing chars count ~3 wide and unstyled runs are counted in bytes, so a 53-col twin-box row wraps even in a 110-col window.
- Side-by-side boxes (two color spans per line) always fragment. Converting spaces to NBSP is worse: the line becomes one word and gets hard-broken mid-word.
- Safe envelope = slide 3's geometry: single-column boxes ≤36 wide (≤41 visible cols with the 5-space centering prefix), connector labels ≤~22 chars, color opened per line with few toggles. Reuse those exact border strings for any new diagram.

## Concept slides as high-res images inside presenterm (unified deck)
- presenterm renders real images via the terminal graphics protocol (iTerm2 inline-image / kitty), NOT ascii — projector-crisp if the source PNG is high-res. Lets us fold the HTML/keynote concept slides INTO the terminal deck as image-slides, so the whole talk is one presenterm run (image concept slides → live +exec demo slides). No HTML→terminal app switch; the "handoff" is just the next slide.
- Render pipeline: author each slide as HTML/SVG (1280x720 viewBox) → headless Chrome → 4K PNG. Command:
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=3 --window-size=1280,720 --screenshot=out.png "file://$PWD/slide.html"
  → 3840x2160 PNG, ~150KB, text razor-sharp. (rsvg-convert/resvg NOT installed; Chrome is the renderer. mmdc's puppeteer chromium also present at ~/.cache/puppeteer/chrome as fallback.)
- Embed: ![](assets/x.png) on its own slide; presenterm scales to fit. OPEN QUESTION to verify on real iTerm2 + projector: light (white) 16:9 image on the dark presenterm bg may show dark letterbox bars if terminal aspect ≠ 16:9 — eyeball before committing. Test deck: talk/slides/imgtest.md.
- Font caveat: headless Chrome uses system fonts (used Helvetica/Menlo in proof). For the real pack, embed the chosen display face via @font-face data URI in the slide HTML so renders are deterministic (not dependent on whatever's installed).
