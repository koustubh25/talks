---
name: ai-evals-talk
description: Knowledge base and brainstorming aid for Koustubh's Experts Live Melbourne 2026 talk, "From Unit Tests to Eval Gates: CI/CD for AI Agents." Distilled from 5 AI-evals YouTube videos (Hamel Husain, Shreya Shankar, Phil Hetzel/Braintrust, Aakash Gupta, Ankur Goyal). Use when brainstorming talk outline, narrative arc, analogies, slides, demos, or specific claims/frameworks to cite.
---

# AI Evals Talk — Knowledge Base

Source material for prepping "From Unit Tests to Eval Gates: CI/CD for AI Agents" — a 20-minute short session at Experts Live Melbourne, 30 July 2026, 3:40–4:00 PM. Shares the slot with talks on agent telemetry (Raj Mallikarjuna) and agent observability (Pouya Koushandehfar) — so this talk should own the **pre-production / CI gate** part of the story and hand off cleanly to their **runtime / production monitoring** angle.

## What's in `references/`

Five paraphrased summaries of AI-evals videos (not verbatim transcripts — each note is a distilled knowledge-base entry with frameworks, examples, takeaways, soundbites, and a "conference-talk-relevant" section):

1. `01-hamel-peter-yang-clearly-explained.md` — Hamel Husain walks through a real eval build (Nurture Boss) in ~50 min. Best source for a single clean worked example.
2. `02-hamel-shreya-lennys-podcast.md` — Hamel Husain & Shreya Shankar, Lenny's Podcast, ~1h46m. **Richest/deepest source** — full error-analysis methodology, anti-patterns, org process, "evals as living PRD."
3. `03-phil-hetzel-braintrust-maturity-phases.md` — Phil Hetzel (Braintrust), AI Engineer conference, ~18 min. **Structurally closest analog to our talk** — it's a short conference session on a 4-stage eval maturity model; good reference for pacing/structure, not just content.
4. `04-aakash-hamel-shreya-step-by-step.md` — Aakash Gupta interviews Hamel & Shreya, ~1h07m. Same methodology as #2 but organized as a numbered step-by-step pipeline — maps well onto a "stages in a CI/CD pipeline" visual.
5. `05-aakash-ankur-goyal-dont-build-ai.md` — Aakash Gupta interviews Ankur Goyal (CEO, Braintrust), ~52 min. Most provocative/urgency-framed source; good for an opening hook and for the "evals as moat, not gate" counter-argument.
6. `06-latest-and-azure-2026.md` — Web research supplement (July 2026): recent agent-specific failure dynamics/incidents/academic standards not covered by the videos, **plus Azure-native eval tooling** (Foundry built-in evaluators, `azure-ai-evaluation` SDK, the official `microsoft/ai-agent-evals` GitHub Action/Azure DevOps task, the Foundry Dev/Test/Prod gating pattern, Build 2026's "Trace → Evaluate → Monitor → Optimize"). **Read this one first if you want the talk to feel current and Azure-native rather than generic** — this is an Azure conference audience.

## Cross-video synthesis — recurring ideas across all 5 sources

These showed up independently across multiple speakers/videos, which makes them safe to treat as consensus/citable claims rather than one person's opinion:

- **"Evals ≠ unit tests."** Everyone rejects the naive analogy. Unit tests chase exhaustive, deterministic coverage; evals target specific, known failure modes discovered by reading real data, and can be usefully non-exhaustive. This is the direct tension in our talk's own title ("From Unit Tests to Eval Gates") — worth addressing head-on rather than implying they're the same thing with a fancier name.
- **Error analysis is the unskippable first step.** Every source insists the highest-leverage activity is a human manually reading ~15–100 real traces and taking freeform notes *before* building any automated eval. Skipping this and going straight to generic metrics (helpfulness, toxicity, 1–5 scores) is the most-cited failure mode.
- **Open coding → axial coding → counting → gate.** The same pipeline recurs (named explicitly in #1, #2, #4; implicit in #3, #5): freeform notes → clustered failure-mode taxonomy → frequency count/prioritization → targeted evaluator (code-based or LLM-judge) → wire into CI + production monitoring.
- **Binary judges, not Likert scores.** Universal agreement that LLM-as-judge should output pass/fail, not 1–5. A "3.2 vs 3.7" score is called out repeatedly as meaningless false precision — this is a great concrete visual/soundbite for the talk.
- **"Judge the judge" before trusting it.** Never wire an LLM judge into CI without validating it against human-labeled data via TPR/TNR (not raw "agreement," which is misleading on imbalanced failure rates). Directly parallels "test your test suite."
- **Code-based evals vs. LLM-as-judge** is a consistent two-lane split: cheap deterministic assertions for objective failures, expensive LLM judges reserved for narrow subjective failure modes.
- **CI gate + production monitoring are complementary, not either/or.** Multiple sources describe the same validated judge being used two ways: blocking regressions on commits (CI) and sampling live traffic (monitoring). This is essentially the eval-gate architecture for our talk, and it's also the natural handoff line to the telemetry/observability talks sharing our slot.
- **You don't need many evals.** Mature products converge on roughly 4–7 LLM-judge evals total, not exhaustive coverage — useful for countering the "this sounds like a lot of overhead" objection in a CI/CD pitch.
- **"Evals as living PRD."** Repeated framing (esp. #2, #5): the judge prompt becomes a continuously-updated, executable spec of what "correct" means, derived from real data rather than imagined upfront — a strong bridge from traditional software specs to CI-enforced AI behavior.
- **Myth to actively bust:** "just have the AI grade itself" doesn't work — models lack the product/domain context to catch real failures (multiple concrete examples across #1, #2, #4 of an LLM judge missing an issue a domain expert caught instantly).

## How to use this for talk prep

- For **narrative arc / opening hook**: look at #5 (provocative framing, "distance from the end user" as the argument for *why* gates matter) and #1 (skeptical-client-converted mini-story).
- For **structure/pacing of a short conference talk**: study #3 closely — it's the only other ~15–20 min conference session in the set, and its own transcript shows where a real speaker ran out of time (compress the intro, don't shortchange the core framework, use a clean numbered model as the spine).
- For **the core technical framework to teach**: synthesize #2 and #4 (same methodology, two framings) into a single pipeline diagram — this is likely the backbone of the middle section.
- For **the "gate" specifically (CI/CD framing)**: pull from #1's CI-vs-monitoring split and #3's maturity phases (stage 2, "measuring to manage," is literally about automating human judgment into CI-usable gates).
- For **handoff to the telemetry/observability talks in the same slot**: use the CI-gate-vs-production-monitoring split as the explicit bridge — "this is where our talk stops and Raj/Pouya's pick up."
- Don't just read one file — cross-reference the "Notable soundbites" and "Anything conference-talk-relevant" sections across all 5 first; that's where the fastest talk-ready material is.
- For **making the talk Azure-native**: use file 06 — swap generic "wire it into your CI pipeline" language for the actual `microsoft/ai-agent-evals` GitHub Action / Azure DevOps task and the Foundry Dev→Test→Prod gating pattern. This is what will differentiate the talk from a generic evals talk for this specific audience.
- Note on the two "reported incident" items in file 06 (Amazon Kiro, Meta SEV1): these are secondary-sourced (blog aggregators, not primary company statements). Fine as color/cautionary anecdotes with a "reportedly" qualifier, but verify further before stating as confirmed fact on stage.
