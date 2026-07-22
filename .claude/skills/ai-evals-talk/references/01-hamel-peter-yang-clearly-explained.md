# AI Evaluations Clearly Explained in 50 Minutes (Real Example)
Speaker: Hamel Husain (interviewed by Peter Yang) | ~52 min | YouTube

## Core thesis
Evals are worthless if disconnected from actually reading your data. The highest-leverage activity in the whole eval process is manually reading ~100 real conversation traces and jotting freeform notes on what went wrong — everything else (categorization, LLM judges, dashboards) is built on top of that foundation. Skipping straight to generic metrics (helpfulness, toxicity, 1-5 Likert scores) wastes time because those scores rarely map to the specific failures your product actually has.

## Key frameworks / mental models
- **Error analysis via open/axial coding**: borrowed from social-science qualitative research. "Open codes" = the freeform notes you write while reading each trace. "Axial codes" = the small set of categories (5-6) you cluster those notes into afterward, often with LLM help. This turns messy qualitative reading into a countable taxonomy of failure modes.
- **Traces**: the full log of one user interaction including hidden tool calls, system prompt, and internal steps — not just the visible chat.
- **Two eval types**: code-based/reference evals (cheap, deterministic assertions, used when there's a clear right answer, e.g. date correctness) vs. LLM-as-judge (expensive, used for subjective/ambiguous failures like "was this handoff to a human handled correctly").
- **Judging the judge**: before trusting an LLM judge, measure it against human-labeled data using true positive rate (TPR) and true negative rate (TNR) — not raw "agreement," which is misleading when failures are rare (a judge that always says "no failure" can hit 90% agreement while being useless). A confusion matrix makes this concrete.
- **Binary over Likert scales**: LLM judges should output true/false, not 1-5 scores. Continuous scores create false precision, are hard for LLMs to produce reliably, and don't drive a ship/no-ship decision.
- **Synthetic data via dimensions**: instead of asking an LLM to "generate plausible user questions," first brainstorm structured dimensions (e.g. customer type × apartment class) and generate inputs across combinations — this avoids homogeneous, low-coverage synthetic data.
- **Theoretical saturation**: keep doing error analysis (reading traces) until you stop learning anything new; 100 traces is the practical starting target, not a magic number.

## Concrete example walked through
Nurture Boss, an AI property-management leasing assistant (voice/chat), built with a real client named Jacob. Hamel and Jacob read ~100 real traces from the tool Brain Trust, writing short notes on failures (e.g., a conversation that silently dead-ended after a tool call, a frustrating loop where the bot wouldn't hand off to a human, wrong dates for tour scheduling, markdown leaking into text messages). Those notes were dumped into a spreadsheet, clustered into categories using an LLM (tour scheduling issues, human handoff failures, formatting errors, conversational flow breaks, broken promises), then counted via a pivot table to reveal that human-handoff failures and conversational flow issues were the biggest problems. The date-handling bug turned out to need no eval at all — just fixing the prompt to include today's date. The handoff problem was subjective enough to warrant building and calibrating an LLM judge, walked through live in Google Sheets for transparency.

## Practical takeaways / how-to steps
1. Before building any eval, read ~100 real traces yourself and write short unstructured notes on what's wrong — don't try to root-cause or fix yet.
2. Export notes to a spreadsheet; use an LLM to propose 5-6 categories (axial codes) from your notes (open codes).
3. Categorize each note into a category (LLM-assisted), then pivot-table/count to find your biggest failure clusters.
4. For each cluster, decide code-based eval vs. LLM-as-judge based on whether there's a clear right answer.
5. Write a judge prompt with explicit binary pass/fail criteria (avoid 1-5 scores); include an explanation field if it helps debugging.
6. Calibrate the judge against your human labels using TPR/TNR (not raw agreement); inspect the confusion matrix and iterate on the prompt.
7. Hold out data when adding few-shot examples to the judge prompt to avoid overfitting/cheating your own metric.
8. Once a judge is trustworthy, wire it into CI (block regressions on code changes) and into production monitoring (sample live traffic).
9. Keep the eval suite small — usually under a dozen judges/evals total; prioritize by cost and value.
10. Repeat the manual trace-reading on a regular cadence (weekly/monthly) and after major changes — don't treat error analysis as a one-time setup step.
11. Before launch, prefer dogfooding and small-scale real usage over building elaborate synthetic eval infrastructure; ramp up rigor as user/traffic scale exceeds what one person can personally observe.

## Notable soundbites (paraphrased, not verbatim)
- An average score of "3.2 vs 3.7" tells nobody anything actionable — it's false precision dressed up as rigor.
- If a product manager ever hears the word "agreement" reported for a judge, that's the moment to get suspicious and ask what the baseline failure rate is.
- Once stakeholders stop trusting your evals, they stop trusting you, full stop.
- Generic off-the-shelf metrics (toxicity, hallucination scores) are appealing because vendors sell them as plug-and-play, but they usually don't match the actual failure modes in your specific product.
- The unglamorous work — just reading and labeling data — is the single most valuable and most-skipped part of the entire eval process.

## Anything conference-talk-relevant
- Strong opening hook: contrast "average score of 3.2 vs 3.7 means nothing" against a binary pass/fail gate — directly maps to "CI gates need clear ship/no-ship signals, not vibes-based scores."
- The CI/production split Hamel describes (judge in CI on held-out data to block regressions on commits, same judge sampling production traffic for monitoring) is essentially the eval-gate architecture for the talk — could be presented as a two-lane diagram: pre-merge gate vs. live monitor.
- The "confusion matrix / judge the judge" concept is a great analogy for "don't trust your CI gate until you've validated the validator" — directly parallels testing-the-test-suite in traditional software.
- The narrative arc (skeptical client Jacob doubting the "just read 100 traces" approach, then getting converted) is a ready-made mini-story structure for a talk: start with resistance to "unglamorous" manual review, show the payoff.
- Good concrete metaphor: comparing LLM judge false-negative vs false-positive costs to real engineering tradeoffs (e.g., a CI gate that's too lax vs. too noisy/annoying) — could map directly to "how strict should your eval gate be" section.
- The point about generic metrics still being useful as a *sampling/sorting mechanism* (sort traces by hallucination score to find interesting cases) rather than as a reported number is a nuanced, talk-worthy nugget: "use the score to find bugs, not to report health."
