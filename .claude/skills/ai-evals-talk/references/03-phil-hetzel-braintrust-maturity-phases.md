# The maturity phases of running evals
Speaker: Phil Hetzel (Braintrust) | AI Engineer conference | ~18min | YouTube

## Core thesis
As agents grow more complex, teams move through predictable stages of eval maturity — from informal vibe-checking to production-driven, automated, judge-based evaluation. Evals exist purely in service of agent quality: they're both a defense against reputational/systems/compliance risk and an offense tool for measuring improvement. Evals are fundamentally different from unit tests — they should target known failure modes, not attempt exhaustive coverage, and results can be directional rather than perfect.

## The maturity phases / stages
Hetzel frames this as a continuum, not discrete steps, but names four stages that teams traverse as agent complexity grows:

1. **Just getting started (vibes-based)** — Teams "vibe check" outputs, which Hetzel says is fine as a starting point. Key discipline: document while vibe-checking. Run ~10 example inputs through the agent, have a human (ideally a subject-matter expert, not just the builder) give a thumbs up/down PLUS a written justification for the verdict. The justification is critical — it captures the domain knowledge needed later to scale judgment via an LLM judge.
2. **Measuring to manage** — Teams take the human justifications and run them (e.g., through Cursor/Claude Code/Codex) to derive concrete failure modes. Once failure modes are known, the goal is to scale human judgment via automation: LLM-as-judge for subjective quality, or deterministic code-based checks for objective conditions (e.g., too many tool calls, excessive token usage). Crucially, LLM judges must themselves be evaluated against human judgment — "putting a robe on an LLM doesn't make it trustworthy." At this stage, eval datasets should shift toward real production (or UAT-level) traces rather than synthetic examples — think of evals as "rerunning production," not running tests.
3. **Accounting for complexity** — Agents now call external tools/systems (context-gathering tools that inject data, and CRUD tools that mutate state). This forces evaluating the entire trace, not just the final output, and introduces new tooling needs to capture, inspect, and target evals at individual tool/MCP calls. Two hard problems emerge: (a) representing what state external systems were in when the eval input was captured, and (b) not wanting to run real CRUD operations against production during offline evals. Emerging techniques: since agent traces can be arbitrarily large, cram system-state context directly into the trace; use timestamped/versioned queries (e.g., point-in-time vector DB queries) to reconstruct external state as of when the original task ran.
4. **Advanced eval techniques** — Only briefly touched due to time: automatic topic modeling at scale to surface failure modes in production without manual review, and using coding agents (Claude Code) plus an "eval provider CLI" to automate eval creation/execution.

## Key frameworks / mental models
- Eval anatomy: task (agent/prompt under test) + dataset of example inputs + scoring functions.
- The "flywheel": capture production traces → diagnose issues (human or automated) → pull examples back into an offline experimentation/eval dataset → rerun and use results to guide agent improvements.
- Evals vs. unit tests: unit tests aim for exhaustive coverage; evals should target specific, known failure modes because exhaustive failure-mode coverage is infinite and unproductive.
- "Eval the eval" — treat LLM-judge outputs themselves as something requiring evaluation against a ground-truth/human-aligned dataset.
- Two tool-call categories: context-gathering tools vs. CRUD tools, each with distinct evaluation challenges.

## Concrete examples discussed
- Braintrust's own product: a live-codable human annotation UI (customized per use case rather than generic) and an LLM-as-judge scoring function builder.
- Hetzel's prior role at Slalom Consulting (Databricks practice) observing many customers stuck at the GenAI proof-of-concept stage, unable to reach production — motivation for the maturity framing.
- Live audience poll: asked who does evals and who uses human annotators; used to gauge room's maturity level and personalize discussion.

## Practical takeaways / how-to steps
1. Start with vibe-checking but force documentation: thumbs up/down plus written justification from a human evaluator (ideally a domain expert).
2. Mine those justifications to identify explicit failure modes.
3. Automate judgment at scale using LLM-as-judge (for subjective calls) and deterministic code checks (for objective conditions like tool-call counts or token usage).
4. Validate your LLM judges against human-labeled ground truth before trusting them.
5. Shift eval datasets from synthetic examples to real production/UAT traces as you mature.
6. As agents adopt tool use, evaluate the full trace, not just final output; build tooling to inspect individual tool/MCP calls.
7. For stateful/external-system evals, inject system state into the trace itself and/or use timestamped queries to reconstruct historical state.

## Notable soundbites (paraphrased)
- Vibe-checking gets a bad reputation, but it's a legitimate and necessary first step — better than nothing.
- Wrapping an LLM in "judge" robes doesn't automatically make its verdicts trustworthy — judges need auditing too.
- Don't treat evals like unit tests: chasing exhaustive coverage of every possible failure is an infinite, unproductive task.
- The goal isn't to "run tests" — it's to rerun production.
- Eval results don't need to be perfect; with non-deterministic judges, trending in the right direction is good enough.

## Anything conference-talk-relevant
- Opens with a self-aware hook acknowledging the post-lunch energy slump, then quickly does personal/company intro (~90 seconds) before pivoting to content — keeps setup lean given the 18-minute window.
- Explicitly states the agenda up front (bio → theoretical framework → future direction → Q&A) so the audience knows the shape of the talk.
- Uses a live audience poll (raise of hands) mid-talk to create interactivity and implicitly validate the maturity framework against the room.
- Structures the core content as a clean numbered/staged framework (4 maturity phases) — easy for an audience to mentally file and recall afterward; this is the single dominant "hook" of the talk.
- Explicitly scopes out of bounds ("we're not covering the platform today, come find me at the booth") to keep focus tight and avoid turning it into a product pitch.
- Time pressure is visible in the transcript itself — the speaker compresses stage 4 sharply and cuts Q&A to one question, explicitly narrating "I only have about 2 minutes left" — a reminder to budget generously for early stages since later content is what gets cut.
- Closes with a direct audience Q&A exchange (on deterministic vs. LLM-judge graders) rather than a formal summary slide — ends on a real-time, substantive exchange plus a booth call-to-action.
