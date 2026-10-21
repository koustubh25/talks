# Stage runbook v2 — portal-only trace review (trimmed for 12 slides)

Supersedes `runbook.md` for the demo portion. Cuts the GitHub PR walkthrough to a
single static screenshot; the live/recorded surface is entirely the Foundry
portal, project `proj-evals-demo`. Target: **~4-5 min**, zero terminal commands
on stage.

**Caveat carried over from `demo-plan.md`:** Traces to dataset and Trace replay
are preview + region-gated. This whole sequence should be **screen-recorded in
advance** and presented as "here's a trace we pulled," per the original risk
call — live portal navigation on a projector is the riskiest surface here, not
less risky just because it's not a terminal.

## Pre-stage checklist

- [ ] Signed into `ai.azure.com`, project `proj-evals-demo` already open
- [ ] Degrade mode already flipped on *before* walking on (no live toggle) —
      confirm via `./runbook/degrade.sh status` beforehand, off-stage
- [ ] Confirm the capture-run traces are visible: 18 hallucinated conversations
      (17 Jul capture) + Act 1 sabotage run traces, both queryable in Tracing
- [ ] Tabs pre-opened, in this order:
  1. GitHub PR #1 — **Checks** tab, job summary already scrolled to the
     comparison table (this is the one static screenshot beat, not live)
  2. Foundry portal → **Tracing**
  3. Foundry portal → **Data Generation**
  4. Foundry portal → **Evaluations** → the incident eval run, pre-opened
- [ ] A dataset already created from the 18-conversation capture (yesterday,
      off-stage) as the fallback if live "Create dataset" hits ingestion lag
- [ ] Recording cued as the primary path, live portal as backup — not the
      other way around

## Beat 1 — the gate story, static (~30 sec)

Tab 1 (screenshot, not live navigation): point at the job summary comparison
table. "Task adherence dropped 50 points, p < 0.001 — that's slide 4 and 5
made real. I'm not going to click through GitHub live for this, you've already
seen the shape of a CI check going red."

Move straight to tab 2.

## Beat 2 — open the trace list, categorize live (~2 min)

Foundry portal → left nav → **Tracing**.

1. The trace list loads as rows (`invoke_agent` spans, one per conversation),
   most recent first. Point at the volume: "this is every conversation this
   agent has had, traced automatically — no code for this, it's OpenTelemetry
   under the hood."
2. Open **one trace from the Act 1 capture run** (search-skip sabotage). Click
   the row → detail pane shows the span tree. Point at the missing
   `search_flights` tool-call span. Narrate the category out loud: *"this
   bucket is 'skipped the tool it needed' — that's the one the gate already
   catches."*
3. Open **one or two traces from the 17 Jul hallucination capture** (18
   available — pick ones you've pre-verified render cleanly). In the span
   tree: click the `book_flight` tool span → show the raw output
   (`confirmation_code: null`, "seat held for passenger"). Then click the
   sibling assistant-output span → show the text claiming "Booking
   confirmed." Narrate: *"different bucket — the tool told the truth, the
   model didn't repeat it. That's a fabrication, not a skipped step."*
4. Land the line: two categories, two traces, and neither came from staring at
   a spec — they came from reading what the system actually did. That's open
   coding: no portal button does this for you, you're doing it by eye right
   now.

*(No tagging/labeling control in the portal has been verified to exist — this
beat is narrated over the trace list and detail view, not clicked into
categories. Don't imply otherwise on stage.)*

## Beat 3 — close the loop: traces to dataset (~1 min)

Foundry portal → left nav → **Data Generation**.

1. Click **Create dataset**.
2. Choose the **From traces** source option.
3. Pin **agent** = `flight-booking-agent`, **version** = the incident version.
4. Select the hallucination-bucket traces (or accept intelligent sampling
   across the 18-conversation capture window — min 15 samples needed for a
   generation job).
5. Click **Create** — then **cut to the pre-made dataset** (created off-stage
   the day before; ingestion lag is 30-90s+ and live "Create" will stall a
   room). Say so explicitly: *"that job takes a couple of minutes to land —
   here's the one I ran yesterday from the same 18 conversations."*
6. Show the resulting dataset under **Data** (a.k.a. Data + indexes) — a
   versioned, named eval dataset, no hand-written JSONL.

## Beat 4 — trace replay against the fix (~1 min)

Foundry portal → left nav → **Evaluations** → open the pre-opened incident eval
run.

1. Point at the run's per-conversation scores — the hallucinated row scored
   against the new code-based check (tool never confirmed + answer claims
   confirmed ⇒ fail).
2. Click **Replay** on that specific run/trace.
3. Select the **fixed agent version** as the replay target.
4. Watch the replayed output: the fixed agent now surfaces uncertainty
   ("I wasn't able to confirm this booking — let me check again") instead of
   fabricating. This is the closer, not the dataset creation — a side-by-side
   old-answer vs new-answer on the *same* captured incident is the strongest
   visual you have.

## Closing line into slide 8

"That whole loop — read the trace, name the failure, turn it into a test,
replay it against the fix — is the system slide 6 promised you. The gate
didn't do that alone. It never was going to."

## Reset after rehearsal

    ./runbook/degrade.sh off

Leave PRs, traces, and the pre-made dataset as artifacts — don't delete
anything between rehearsal and the talk.
