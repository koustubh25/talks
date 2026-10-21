# Speaker script — "From Unit Tests to Eval Gates: CI/CD for AI Agents"

Experts Live Melbourne 2026 · 20-minute slot (3:40–4:00 PM) · Koustubh Bhaskar Gaikwad

**Budget:** ~6 min talk (slides 1–6) → ~10 min live demo → slide 8 as the ~1 min close → remainder Q&A.
Slide numbers below match `slides.html`. Timestamps are cumulative targets, not hard stops — better to run slightly under than to eat into the demo.

---

## Slide 1 — Title (0:00–0:15)

> Hi everyone — I'm Koustubh, Sr. Manager on the PwC Engineering team. I've got the pre-production half of a bigger story today — what happens *before* your agent ever sees a real user. There are two other talks running in parallel right now, in other rooms, on the runtime half of this — telemetry and observability. If today hooks you on the "before" side, go find the recordings of theirs for the "after" side.

Keep this fast. No agenda slide, no "a bit about me" — the title card is doing that work silently. Get to content in 15 seconds.

## Slide 2 — The hook (0:15–1:00)

> Let's start with a number. If a single step in your agent's workflow is 95% accurate — which sounds great, that's an A on any test you took in school — here's what happens as the task gets longer. Five steps, you're at 77%. Ten steps, 60%. Twenty steps — the length of a fairly normal multi-tool agent task — you're at 36%. Fifty steps, under 8%.
>
> Your agent doesn't need to fail once. It needs to succeed *every single step*, and every extra tool call you bolt on is another coin flip stacked on the last one.

Let the chart sit for a beat before you start talking numbers — don't rush past the visual. This is the entire justification for the rest of the talk; don't over-explain it.

## Slide 3 — Why unit tests stop working (1:00–2:00)

> So naturally, our instinct is: test it. We know how to do that — we've been writing unit tests for decades. Assert booking confirmed equals true. Done, ship it.
>
> Except the failures that actually hurt you in an agent don't look like that. "Was this a good conversation?" "Should it have escalated to a human here?" There's no single correct answer to assert against — you could put five good engineers in a room and they'd argue about it.
>
> Try to `assert()` your way through that and you get... [gesture at the shrug on screen]. That's the wall everyone hits.

This is the pivot slide — the audience needs to feel the gap between what they know (unit tests) and what they're being asked to do differently. Don't rush it, but don't over-stay either.

## Slide 4 — Enter eval gates (2:00–3:05)

> So here's the reframe: an eval gate does the *same job* as a failing unit test. It's wired into your pipeline, it fails, the merge blocks. That part hasn't changed at all. What's changed is who's doing the judging — it's a check, either plain code where you can write one, or an LLM acting as a judge where you can't.
>
> If you're on Azure AI Foundry, this isn't something you build from scratch — there's a named, built-in set of these for agents specifically: Task Adherence, Tool Call Accuracy, Intent Resolution, Tool Output Utilization.
>
> And before anyone starts mentally budgeting for hundreds of these — most teams that do this seriously land on somewhere between four and seven. This is not a second test suite the size of your first one.

This is the definitional slide — say the "same job as a failing test" line clearly and slowly, it's the thesis of the whole talk in one sentence.

## Slide 5 — The pattern (3:05–4:05)

> Concretely, on Azure, this looks like a Dev, Test, Prod promotion — same as any pipeline you already run — except the gate between Test and Prod is an eval, not just a build check. Microsoft ships this as an actual GitHub Action, `microsoft/ai-agent-evals`, or the equivalent Azure DevOps task if that's your world. You point it at your agent version, your dataset, the evaluators you want — and it blocks the merge on your behalf.
>
> This is not a science project. It's a checkpoint you can add to a pipeline you already have this afternoon.

Point at the diagram left to right as you talk through it. This is the "here's the real artifact, go use it" slide — say the package name clearly, people will want to write it down.

## Slide 6 — The honest part (4:05–5:10)

> Now — before we go further, I want to be straight with you about what this does and doesn't do. Nothing prevents every AI bug from reaching production. Nothing prevents every bug in *any* complex system, honestly — that's not a new AI problem. What a gate buys you is narrower and more honest than that: it catches what you already knew to test for, and it shrinks the blast radius on what you didn't.
>
> And here's the part that sounds backwards until you sit with it: an eval suite that never fails isn't a sign you're safe. It's a sign you're not looking hard enough.
>
> So — what actually happens when something gets past the gate anyway? Let's not talk about it in the abstract. Let's watch it happen.

Slow down here — this is the credibility beat of the talk, and it's also the setup for the entire demo. Don't rush the transition line; let it be the literal hinge into the demo.

## → Demo (5:10 talk-time → ~10 minutes, see `demo-plan.md`)

Walk straight from slide 6 into the demo environment. Slide 7 ("Now boarding: production") can sit on screen as you switch windows/tabs — no need to narrate it separately, it's just a title card for the demo section.

## Slide 8 — Closing (after demo, ~1 min)

> So — green CI never meant safe. It meant tested for what we already knew. Every one of those production surprises we just walked through becomes tomorrow's regression test. That's genuinely the whole game here — not zero bugs, a system that gets a little safer every time it's wrong.
>
> We've covered "Evaluate" today. If you want the "Trace, Monitor, Optimize" half of this story, Raj Mallikarjuna and Pouya Koushandehfar are covering exactly that right now in other rooms — catch the recordings. Thank you.

Name-drop them by name — it's a courtesy to two speakers you're implicitly building on, and it signals to the audience this was a deliberately scoped talk, not an incomplete one. Since their sessions run in parallel rather than after yours, point people to the recordings rather than implying "go there next."

---

## Delivery notes

- Total pre-demo talk time target: **5–6 minutes**. If you're running long by slide 4, cut slide 3's second example line rather than rushing slide 6 — slide 6 is the credibility beat and shouldn't feel rushed.
- The deck has a built-in speaker-notes overlay — press **N** while presenting to toggle a short cue per slide (visible only on your screen/laptop, not on the projector output if you're on a second display).
- If the live demo breaks, the fallback is a screen recording — see `demo-plan.md` for what to capture in advance.
