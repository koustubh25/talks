# Speaker script — slides 1–15 (`concept.html`)

**"From Unit Tests to Eval Gates: CI/CD for AI Agents"** · Experts Live Melbourne, 30 Jul 2026 · Koustubh
**Target: ~16 min for slides 1–14** (raised from the earlier 15-min ceiling on 2026-07-26, deliberately — the extra minute (the eval-count reassurance on slide 8, the binary-vs-continuous aside on slide 8, and the "grounded judges still err" aside on slide 9) is coming directly out of demo time, which is being re-scoped smaller anyway; see `runbook-portal.md`). Timestamps are cumulative pacing targets, not hard stops; better to land under than to eat into demo time.

Matches `concept.html` 1:1 — 15 sections, in the exact order/wording currently on disk: slide 1 is the title card, slide 2 is the speaker/bio slide (visual beat, minimal narration), slides 3–14 are the numbered content covered below, and slide 15 is the Thank You / close card. Slide 14 ("A green gate is not safety") ends with the verbal cue into the live demo — there's no on-screen bridge slide anymore, so the switch to the terminal deck is a manual one (see the mechanics note under slide 14). Slide 15 is delivered after the live demo concludes, reached by jumping to `#15` rather than by pressing forward from 14 (see the mechanics note under slide 15).

---

## Slide 1 — Title card (0:00–0:40)

*[data-eyebrow: experts live melbourne 2026]*

*[on the title card, before advancing to slide 2]*

> My name is Koustubh, I am a platform engineer at PwC. Today I'll be talking about closing the gap between how confidently we ship AI agents and how little we actually test them — how we go from unit tests to eval gates, so a green pipeline means your agent's judgment was checked, not just your code.
>
> Before I get into it — here's what I actually want you to walk away with today. Not a specific tool, not a command to memorize. There are a hundred tools that'll do this for you, and if you want the deep links into Microsoft Foundry specifically, come find me after and I'll point you at them. What I care about is a mindset shift: that a green pipeline was never the finish line for an agent, the same way it never fully was for any complex system — and once you start looking at your agent's behavior the way you already look at your code, you can't really unsee it. Everything after this is just here to make that shift concrete.

**Delivery note:** the first paragraph is the fixed name/title/topic anchor — keep it to one breath. The second paragraph sets the actual objective of the talk: a mindset shift, not a toolkit — tools and Foundry specifics are explicitly deferred to a follow-up conversation, not part of the pitch itself. Say it a touch slower and warmer than the first paragraph — this is the one moment in the talk that's genuinely conversational rather than argument-building. Don't add "a bit about me," an agenda slide, or any mention of time/pacing on top of either paragraph; the title card is already doing that work.

---

## Slide 2 — "Who's talking" / speaker bio (0:20–0:35)

*[data-eyebrow: who's talking]*

**Delivery note:** this slide doesn't need its own dedicated paragraph — you've already covered name, role, and company in slide 1. Click forward to it as you finish the second paragraph of slide 1's narration ("Everything after this is just here to make that shift concrete") and let it sit silently for 2–3 seconds while the room reads your photo/bio, then move straight into slide 3's first hand-raise question with no dead air. If you want one optional spoken line to bridge the silence, something like *"—and yes, that's really me, home lab and all"* works as a light aside, but it's not required.

---

## Slide 3 — "Two quick shows of hands" (0:35–1:20)

*[data-eyebrow: before we start]*

> Quick show of hands, two questions. First — who here has shipped something with an LLM in it? *[pause, let hands go up — usually most of the room]* Right, that's what I expected.
>
> Second question. Keep your hand up only if you also have a test in your pipeline that fails the build the moment the model starts making things up. *[pause — usually the room thins out fast]*
>
> That gap — between shipping AI and actually testing its behavior — is the entire talk. We've collectively gotten very good at the first half and left the second half almost entirely to vibes. I want to spend the next ten minutes closing that gap, and then show it happening live.

**Delivery note:** genuinely pause for hands both times — it's audience-participation, not rhetorical. Don't rush past the second question; the visible drop-off in raised hands *is* the hook, let it land silently for a beat before you speak again.

**Mechanics note:** this slide click-to-reveals — it lands blank except the title, and each arrow-key press (or click) reveals the next beat: Question 1, then Question 2, then the "that gap is the whole talk" line. That's 3 presses before a 4th press moves you to slide 4. Time each press to your own pacing (ask Q1 → press → let hands go up → ask Q2 → press → let hands drop → press to reveal the gap line → deliver it → press to advance) rather than pressing ahead of what you're saying.

---

## Slide 4 — "Agent value-add: workflow automation" (1:00–2:15)

*[data-eyebrow: the shift]*

> So why does this gap even exist? Because of where agents sit in your workflow. This diagram, adapted from organizational-behavior research on teaming humans with intelligent systems, maps the three phases of any task — sense, respond, act — across how AI products have evolved.
>
> Top row: historically, all three were human. Then came RAG applications — still a human deciding and acting, but the model now helps you *comprehend*.
>
> Bottom row is where we live now: agentic workflows. The model senses, responds, and — this is the part that changes everything — *acts*. It calls the tool. Books the flight, sends the email, updates the record. No human in the loop catching the mistake before it becomes a real-world side effect.
>
> That's the actual shift. Not "the model got smarter" — we handed it the keys to act on our behalf, and our testing discipline hasn't caught up.

**Delivery note:** point at the diagram left to right, then trace down from "Human" to "Model" to "Tool" on the bottom row as you say "the model acts." This is the setup slide for the whole talk's stakes — don't rush it, but keep it under 75 seconds.

---

## Slide 5 — "95% isn't as safe as it sounds" (2:15–3:45)

*[data-eyebrow: the math]*

> Now that the model can act, here's the problem with letting it act *repeatedly*. Say each step — a tool call, a decision, a lookup — succeeds 95% of the time. On its own, nobody panics at 95%.
>
> But chain enough steps together and the odds catch up with you. At one step, still 95%. By twenty steps — a normal length for a multi-tool agent task — you're at 36%, worse than a coin flip. Fifty steps, under 8%.
>
> Overall success is step-reliability raised to the power of however many steps you chain. Your agent doesn't need to fail once — it needs to succeed at *every single step*, and every extra tool call is another coin flip stacked on the last.
>
> If failures become inevitable as agents get longer, then we need a way of detecting when those failures increase.

**Delivery note:** let the chart sit on screen for a beat before narrating numbers — don't talk over the visual's first impression. This slide is the entire mathematical justification for the rest of the talk; keep the delivery matter-of-fact, let the curve do the emotional work. The last line is the bridge into slide 6 — without it, "so let's test it" (slide 6's opener) can land as a non sequitur; someone in the room is otherwise entitled to think "so why not just build shorter agents?"

---

## Slide 6 — "Your CI passes. Your agent still fails" (3:45–5:15)

*[data-eyebrow: the black box]*

> So naturally, our instinct is: test it. We know how to do this — decades of muscle memory. Lint, types, unit tests, all green, merge. *[gesture at the green checklist]*
>
> Here's the uncomfortable part. Every one of those checks verifies the code *around* the agent, the plumbing — none of them verify the reasoning *inside* it. User asks, agent resolves intent, agent calls tools, agent responds — CI touches zero of those four steps. Zero.
>
> That's the black box. Fully green pipeline, and your agent can still confidently invent a flight number and nothing in your test suite would notice. Once the model *acts*, every one of those internal decisions needs its own check — an eval.

**Delivery note:** the checklist-then-teardown structure is deliberate — let the "all green, merged" moment feel like a false victory before you pull the rug with "CI touches zero of those four steps." This is the pivot slide; don't rush it, but don't overstay either — the payoff line is "every decision becomes an eval."

---

## Slide 7 — "An eval is just three things" (5:15–6:15)

*[data-eyebrow: what an eval is]*

> So what actually is an eval? Strip away the mystique and it's three ingredients. Data — the inputs your agent actually has to handle, plus an expected answer if you happen to have one. Task — your agent doing its actual job. And score — one verdict per answer, pass or fail.
>
> The first two are the easy part, honestly. The hard part, the part we're going to spend the rest of this talk on, is the score. There's no exact answer to assert against here — so how do you judge "good" at the scale of thousands of conversations, without reading every single one yourself?

**Delivery note:** keep this fast and definitional — it's a table-setting slide, not a payoff slide. Land hard on the word "score" since it's the pivot into slide 8.

---

## Slide 8 — "Grade a model with a model" (6:15–7:55)

*[data-eyebrow: the engine]*

> You can't hand-grade ten thousand conversations. So the answer the industry landed on is: grade a model, with a model. The agent produces an answer, you route it through a second model acting as a judge, and that judge outputs one of exactly two things.
>
> Two design rules matter here, and both are non-negotiable. First: binary — pass or fail, never a 1-to-5 score. Here's why that matters in practice: say your judge scores every response 1 to 5, and CI tells you "this PR averages 3.2, production was at 3.7." Now what? Is 3.2 a failure? Close enough? There's no line on that scale where "fine" ends and "broken" begins — it's just vibes with decimals. A gate needs a yes-or-no it can act on, so you force the judge to actually decide: pass, or fail.
>
> One nuance if you already work with classic ML metrics: BLEU, ROUGE, precision, recall — those are legitimately continuous, and that's fine when you're comparing models or doing research. The rule here is narrower than "every score must be binary." It's: whatever decides *whether a merge is blocked* has to be binary. Continuous scores are a fine input; they're a bad gate.
>
> Second: narrow — one judge, one specific failure mode, never "overall quality." Ask a judge "was this response good?" and it's silently blending tone, correctness, formatting, helpfulness into one mystery verdict. When it fails, you have no idea *why* — was it rude? did it invent a fact? you're debugging blind. Instead you build narrow judges: one that only checks "did it follow its own rules," another that only checks "is this backed by what the tool actually returned." Each one answers exactly one yes-or-no question, so when it fails, you already know exactly what broke.
>
> And before you start mentally budgeting for dozens of these — most teams that do this seriously land somewhere between four and seven. This is not a second test suite the size of your first one.
>
> On Azure, Microsoft Foundry ships a set of these as built-in evaluators, and its own docs literally call them binary Pass/Fail — same contract as a unit test.

**Delivery note:** say "binary" and "narrow" clearly and slowly — these are the two rules the rest of the deck assumes you already internalized. The 3.2-vs-3.7 and "was this rude or did it invent a fact" lines are the concrete anchors that make each rule click — don't cut them even if trimming for time elsewhere. The binary-nuance aside is aimed squarely at any ML engineers in the room who'll otherwise silently object "BLEU/ROUGE are continuous, this speaker doesn't know what they're talking about" — keep it to the one sentence, don't over-explain. The "four to seven" line is the single most concrete piece of audience reassurance in this slide — people are quietly doing the "how much work is this" math while you talk; don't cut it even under time pressure. The Azure aside is a supporting beat, not the headline; keep it brief.

---

## Slide 9 — "Would your judge catch this?" (7:55–9:30)

*[data-eyebrow: trust but verify]*

> Here's the catch: LLM judges sound confident. That doesn't mean they're right. Walk through this with me. Customer asks about the refund window. Agent answers: ninety days. The judge reads that, sounds plausible, grades it PASS — confidently. It ships, CI is green.
>
> Three weeks later: support ticket. Refund denied at day forty-five. "The bot told me ninety days." A human actually reviews the conversation and finds the judge was simply wrong — the real policy had changed, and the judge had no way to know that.
>
> This is the honest failure mode of LLM-as-judge: no domain context, verbosity bias, self-preference, a confident tone that reads as correctness. Some of you are already thinking "couldn't you just ground the judge — give it the real policy doc?" You should, and it helps. But even grounded judges make systematic mistakes; grounding shrinks the blind spots, it doesn't close them. Which means you can't skip this step — you have to judge the judge, against real human labels, before you trust it to gate anything.
>
> On Azure, Foundry traces link straight back to the run that produced them, and its safety evaluators ship a manual human-feedback column built for exactly this kind of audit.

**Delivery note:** this is a mini-story — let the "three weeks later" beat land as a genuine plot twist, not a bullet point. The room should feel the trap before you name it. The "couldn't you just ground it" aside heads off the most obvious objection an experienced RAG practitioner will have in this room — say it plainly and move on, don't turn it into its own tangent.

---

## Slide 10 — "Read the data before you grade it" (9:30–11:00)

*[data-eyebrow: error analysis]*

> So if you can't fully trust the judge on day one, where do you actually start? You start the same way people have started for over a decade in classic data science — error analysis. Andrew Ng — the Stanford professor half this room probably learned machine learning from — was teaching this long before "LLM evals" was a phrase anyone used. Read real conversations. Write down what's actually going wrong, *before* you build a single automated eval.
>
> The practice underneath it is called open coding, borrowed straight from qualitative research. You write a short, free-form note the moment you spot the first thing that's wrong in a trace — you're not scoring yet, you're just observing. Here's a real example: customer asks about a refund after forty-five days, agent confidently quotes a ninety-day window. The open code is simple: "quoted outdated return policy." One reader. Real conversations. One honest note per conversation — that's the whole method.
>
> On Azure, this is the Traces view in Microsoft Foundry, turn-by-turn — where error analysis physically happens.

**Delivery note:** this slide is the credibility anchor of the middle section — say "Andrew Ng" and "error analysis isn't new" clearly, it defuses the "this is just AI hype vocabulary" skepticism some engineers in the room will have. Don't rush the worked example.

---

## Slide 11 — "From notes to named failure modes" (11:00–12:15)

*[data-eyebrow: axial coding]*

> Once you've got a pile of open-code notes, the next step is axial coding — grouping similar observations into a smaller set of recurring, *named* failure modes. And alongside it, a rubric starts to form: your evolving definition of what "good" and "bad" actually look like, which gets sharper the more real data you read.
>
> Watch this in action. Notes like "wrong policy window," "quoted stale numbers," "made up a return date" — those all cluster into one bucket: no domain context, fourteen occurrences. "Never called the tool," "skipped inventory check," "guessed instead of the API" — tool grounding, nine occurrences. "Ignored handoff request" — task adherence, four occurrences. And critically, there's always a fourth bucket: whatever else your data shows. This list is never exhaustive on day one.
>
> Here's the payoff: your largest — and highest-impact — clusters usually become your first evaluation criteria. Frequency alone isn't the whole story: a rare failure that costs you a customer can outrank a common one that's just cosmetic. Humans discover the failure modes by reading. Evaluations measure them at scale, forever after.

**Delivery note:** the phrase "you'll see these three again" earns its keep here — task adherence and tool grounding are about to reappear as the actual CI-gated criteria in a couple of slides, so plant that continuity deliberately.

---

## Slide 12 — "Now wire that eval into CI" (12:15–13:30)

*[data-eyebrow: the gate]*

> Now take the eval you just built and change one thing: instead of running it against a single agent, run it against *two* — the candidate, this PR's version, and the baseline, whatever's live in production today. Same thirty test conversations, both agents, judged side by side.
>
> Notice the question the gate is actually asking. Not "is the candidate good?" — good is subjective. It asks something narrower and far more defensible: "is it *worse* than what's already shipped?" No worse, it passes. Regressed, it fails the build, same as any other failing check.
>
> On Azure this is a real, off-the-shelf artifact — `microsoft/ai-agent-evals`, a GitHub Action that does exactly this comparison as agents get promoted Dev to Test to Prod. This is not a science project. It's a checkpoint you could add to a pipeline you already run this afternoon.
>
> One honest caveat, and hold onto it: a comparison gate like this only stops things from getting *worse*. It quietly assumes today's baseline was acceptable to begin with. What happens when that assumption is wrong is exactly where we're headed.

**Delivery note:** say the phrase "is it worse than production today" slowly and distinctly — it's the thesis sentence of the entire CI-gate section, and it's the direct answer to the "why not an absolute threshold" question if anyone asks in Q&A. Say the package name clearly too; people will want to write it down. The caveat line is deliberate foreshadowing for slide 14; plant it lightly here so slide 14 reads as payoff, not surprise.

---

## Slide 13 — "What should fail CI?" (13:30–14:30)

*[data-eyebrow: reading the verdict]*

> Not everything you find in error analysis belongs in the CI gate, and this slide is the filter: only gate what a code change can actually break.
>
> Task adherence — did it follow its own rules, search first instead of inventing, book correctly — that's CI-gated, because a bad prompt change breaks it directly. Tool grounding — is the answer actually backed by what the tools returned, or fabricated — also CI-gated, same reason.
>
> But "no domain context" — like that stale refund-policy example — deliberately is *not* gated in CI. Why? Because that failure has nothing to do with your code. The policy changed; nobody touched the agent. Gating CI on it would mean blocking merges for a problem your pull request didn't cause and can't fix. That one belongs in production monitoring instead, watching for knowledge drift over time, not blocking ships.

**Delivery note:** this is a subtle but important distinction — spend a beat making sure the room understands *why* domain-context failures get excluded, not just that they are. It directly sets up the "green gate is not safety" argument on the very next slide.

---

## Slide 14 — "A green gate is not safety" (14:30–16:15)

*[data-eyebrow: the catch]*

> So here's the honest part, and I want to be straight with you about it. Real conversations feed error analysis. Error analysis builds your evals. Your evals sit inside the CI gate, checking task adherence and tool grounding, candidate versus baseline, statistically significant or not — pass ships to production, fail gets blocked.
>
> But look at what happens next. Production monitoring watches what actually happens out there, live. And new incidents — the ones nobody wrote a test for, because nobody knew to — feed straight back into error analysis. The loop closes on itself.
>
> That loop is the entire point of this slide: a green CI gate was never "safe." It only means *tested for what you already knew to test for*. Everything you didn't know to test for is still out there waiting, and the only way you find it is by watching production and feeding what you learn back into the next round of error analysis.
>
> That doesn't mean production runs undefended while that loop catches up, though. The gate we just built is *relative* — worse than baseline, or not. Underneath it you also want *absolute* gates: guardrails that just hold or don't, nothing to compare against. "Always search inventory, never invent an answer" is a hard boundary, not a statistical test — and in a few minutes, you'll watch someone quietly delete exactly that kind of instruction, sold as a latency win. Relative gates catch regressions. Absolute gates cap how bad an unknown failure gets.
>
> CI catches regressions. Guardrails catch violations. Production catches reality. And every incident production catches becomes tomorrow's regression test — so the goal was never zero bugs. It's a system that gets a little safer every single time it's wrong.
>
> So — let's stop talking about it in the abstract. Let's go watch it happen.

**Delivery note:** slow down here — this is the credibility beat of the entire talk *and* the literal hinge into the live demo. Walk the loop with your hand as you narrate it (real conversations → error analysis → build evals → CI gate → ships/blocked → production monitoring → new incidents → back to error analysis) so the audience sees the cycle, not just hears it. The "relative vs. absolute gates" paragraph is a genuine addition, not filler — it's the direct answer if anyone in Q&A pushes back with "so there's just no way to avoid shipping bugs?" Don't rush the final line — let "let's go watch it happen" be the exact moment you switch away from `concept.html`.

**Accuracy note:** the forward-reference to the demo is deliberately soft ("you'll watch someone delete exactly that kind of instruction") rather than claiming the demo shows a dedicated absolute/safety gate catching it — in the actual demo, that specific guardrail's removal gets caught by the *relative* quality gate (task adherence drops, p < 0.001), not a separate hard check. Don't let this line drift into implying otherwise on stage.

**Mechanics note:** unlike the old deck, there's no on-screen "bridge" slide after this one anymore — slide 15 (Thank You) sits directly behind it in the file, but you don't press forward into it here. Switch away from `concept.html` to the live/terminal demo (`demo.md` / `present.sh`) the moment you say "let's go watch it happen." Come back to `concept.html` and jump straight to slide 15 (type `15` + Enter, or load the `#15` URL) once the live demo is done, rather than clicking forward from 14 — pressing forward from 14 would land you on the Thank You slide before the demo has even happened.

---

## Slide 15 — Thank You / close (post-demo, untimed)

*[data-eyebrow: thank you]*

> That's the loop — error analysis, evals, a CI gate, production monitoring, and back again. Thank you all for your time.
>
> If you want to talk Foundry specifics, push back on anything I said, or just want the deep links — I'm on LinkedIn and I write some of this up on dev.to, both are up on screen. And a thank you to PwC for supporting the trip out here.
>
> Happy to take questions now, or find me after.

**Delivery note:** this is deliberately short — three or four sentences, not a second recap of the whole talk. The loop-callback opener ties back to slide 14 without re-explaining it. Let the room see the LinkedIn/dev.to links long enough to actually read them before you open the floor.

**Mechanics note:** this slide isn't part of the timed pre-demo budget above — it's delivered after the live demo wraps, reached via the `#15` jump described in slide 14's mechanics note, not by pressing forward through slides 1–14 in sequence.

---

## Pacing summary

| Slide | Cumulative time | Section |
|---|---|---|
| 1 | 0:20 | title card |
| 2 | 0:35 | speaker |
| 3 | 1:20 | opening |
| 4 | 2:35 | the shift |
| 5 | 4:05 | the math |
| 6 | 5:35 | the black box |
| 7 | 6:35 | what an eval is |
| 8 | 8:35 | the engine |
| 9 | 9:50 | trust but verify |
| 10 | 11:20 | error analysis |
| 11 | 12:35 | axial coding |
| 12 | 13:50 | the gate |
| 13 | 14:50 | reading the verdict |
| 14 | 16:35 | the catch → demo (manual switch) |
| 15 | — | thank you (post-demo, untimed) |

**If running long:** the safest cuts, in order, are (1) the two slide 8 asides (binary-vs-continuous nuance, "four to seven") and the slide 9 "couldn't you ground it" aside — cut newest content first, they were added deliberately at the expense of demo time and are the least load-bearing if the room is tight, (2) shorten the worked example on slide 10 to just the punchline note, (3) drop the "you'll see these three again" callback on slide 11, (4) as a last resort, the "relative vs. absolute gates" paragraph on slide 14 can compress to one sentence — but try not to, it's the direct answer if anyone pushes back with "so there's no way to avoid shipping bugs?" Do **not** cut the title/intro or the rest of slide 14 — the title and intro are a fixed ~1-minute cost, and slide 14 is the transition into the demo and needs to land at full weight. Slide 2 (speaker) and slide 15 (thank you) aren't in this cut list — they're already minimal, and slide 15 doesn't compete with the pre-demo budget anyway.

Note on the 16:35 total above: this table is a deliberately pessimistic pacing target that bakes in every pause (hand-raises, chart-reveal beats, the silent speaker-slide beat). The word-count-verified estimate for the spoken lines alone (intro through slide 14) is ~2,355 words, landing at 15.7–18.1 minutes depending on pace — slide 2 adds no material word count since it's designed to ride on slide 1's momentum rather than add its own paragraph. **This deck no longer fits in a 15-minute pre-demo budget** — that's an intentional trade made on 2026-07-26 to add real content (the eval-count reassurance, binary-vs-continuous nuance, and grounded-judge caveat), with the time explicitly taken from the demo rather than found here. **Do a timed run-through before the talk**, and confirm the trimmed demo (`runbook-portal.md`) still fits in whatever's left of the 20-minute slot after this lands. If it runs long, the cut list above is the fallback, in priority order — newest content first.

## Flow check against slide content (verified against `concept.html`)

- Every slide's script only references facts, numbers, and phrases that actually appear on that slide — no forward-spoiling of demo numbers (the real `8/30 vs 23/30`, `p < 0.001`, or the n=12 flip-flop example from `demo.md` are deliberately never mentioned here; those live in the demo itself and the appendix slides).
- Slide 11's "you'll see these three again" is intentional foreshadowing — task adherence and tool grounding do reappear as the literal CI-gated criteria on slide 13, so the callback is truthful, not a promise the deck doesn't keep.
- Slide 13's "no domain context" framing matches the deck's amber "production monitoring" tag exactly — the script doesn't invent a justification the slide doesn't already visually support.
- Slide 14's narration walks the SVG loop in the same left-to-right, top-to-bottom order the arrows actually render in, so pointing gestures will track what's on screen.
- Slide 15's narration only references what's actually on the Thank You slide (LinkedIn, dev.to, PwC sponsor credit) — no fabricated contact details or claims.
- Word count of the spoken lines is ~2,355 words across slides 1–14 (slide 2 and slide 15 excluded — both are deliberately near-wordless or post-demo), landing at 15.7–18.1 minutes at a natural conversational pace (130–150 wpm) — verified by counting (`grep '^> '` + `wc -w` across the whole file), not estimated. A live timed run-through is worth doing before the talk, with the cut list above ready if needed.
