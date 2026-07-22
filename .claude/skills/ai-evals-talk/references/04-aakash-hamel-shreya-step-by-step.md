# How to Build AI Evals in 2026 (Step-by-Step, No Hype)
Speaker: Aakash Gupta interviewing Hamel Husain and Shreya Shankar | ~1h07m | YouTube

## Core thesis
Every non-trivial AI product needs evals, but most teams skip the highest-leverage step: manually reading traces and doing structured error analysis before writing any automated metric. Generic quality scores (helpfulness, conciseness) and naive LLM-as-judge setups miss the nuanced, product-specific failures that actually matter. The real "secret sauce" of an AI product is the human (ideally a domain-expert PM) reading real traces, cataloguing what goes wrong, and only then building targeted evals for the highest-priority problems.

## Step-by-step process
1. **Instrument observability** — capture full traces (system prompt, tool calls, turns) using any tool (Braintrust, LangSmith, Arize) or even a plain CSV/JSON/text log. Tool choice doesn't matter; capturing traces does.
2. **Read traces manually and take freeform notes ("open coding")** — scan ~30 seconds per trace, jot down anything that looks wrong (a "note" field), don't chase root cause, don't aim for completeness. Do this across roughly 100 traces. Skip traces with no issues.
3. **Categorize the notes ("axial coding")** — export notes, feed them to an LLM to propose ~5-6 candidate categories, then manually edit/rename them so they're specific and actionable (not vague labels like "quality" or "temporal issues"). Use the LLM again to classify each note into a category, include a "none of the above" bucket to catch missing categories, and iterate by hand.
4. **Count and prioritize** — pivot-table the categorized errors to see frequency; combine that with product judgment about severity/impact to decide what to fix first. Some issues can just be fixed directly in the prompt (e.g., missing an instruction); others warrant a formal eval.
5. **Decide eval type per issue** — code-based eval (deterministic assertion, cheap) for objective/structural failures (e.g., markdown in a text message); LLM-as-judge for subjective failures (e.g., "should have handed off to a human").
6. **Write the LLM-judge prompt as a binary classifier** — return only true/false, not a 1-5 or Likert scale, because binary is easier to align and mirrors the binary ship/no-ship decisions PMs actually make. Define the rubric (what counts as failure vs. not) explicitly, optionally with examples, and iterate on the prompt rather than treating it as a one-shot recipe.
7. **Validate the judge against human labels** — run the judge on already-labeled traces and compute alignment. Don't rely on raw "agreement" (a judge that always says "pass" can look ~90% accurate if failures are rare); instead check true positive rate and true negative rate separately (sensitivity to real failures vs. specificity on real passes).
8. **Deploy and iterate at scale** — once trustworthy, run the judge across a large sample of production traces to quantify error rate, make prompt/product changes, and re-run the eval suite to confirm fixes don't regress other behaviors.

## Key frameworks / mental models
- Two eval types: code-based (cheap, deterministic) vs. LLM-as-judge (for subjective/nuanced judgment calls).
- Binary scoring over Likert/1-5 scales — LLMs are poor at consistent numeric scales, and business decisions are binary anyway.
- Agreement is a "trap metric" — always check TPR/TNR (or equivalent precision/recall-style splits) separately.
- Error analysis is the moat: it's where product taste and domain knowledge get encoded into the system; outsourcing it (to engineers or a vendor) strips a company's competitive differentiation.
- Domain expert / PM should drive error analysis, not engineers by default — engineers often lack the product context to judge if a behavior is actually wrong.
- Prompts should be treated as a PM-editable artifact (they're just English), not something siloed away in engineering; admin UIs that expose prompt editing to non-technical people are valuable.
- If no production data exists yet: recruit friends/dogfood, or generate synthetic user inputs via an LLM simulating a user at scale.

## Concrete examples / tools discussed
- **Nurture Boss** (nurtureboss.io) — AI assistant for apartment/property managers handling tenant chat, tours, leasing via voice/text/chatbot; used as the running real-data example, including specific traces showing: a bot promising to check something and never following up, ignoring a stated preference (bathroom not connected to bedroom), rendering markdown in a plain text message, failing to answer "let me know when available" (should have escalated to a human), and — most notably — a "virtual tour" booked when only in-person tours exist, plus a duplicate booking created when the user asked to reschedule.
- Nurture Boss's founder/CEO Jacob Carter reportedly got so much value from just doing error analysis that he fixed many issues before formal evals were even built.
- Observability tools mentioned (interchangeable, tool-agnostic message): Braintrust, LangSmith, Arize, or just Datadog/plain file logging.
- Google Sheets + Gemini ("AI function") used live to demo the workflow — explicitly caveated as a fast, low-fidelity demo model, not a recommendation for production judge quality.
- Aside: dumping a trace into ChatGPT and asking "was this correct?" was shown to give a false "yes," missing nuance (markdown-in-text issue, ignored stated preference) — illustrating why generic LLM critique isn't a substitute for structured human error analysis.
- Nurture Boss built ("vibe-coded") their own internal trace-viewer/labeling tool with channel breakdowns and semi-automated axial coding, rather than relying on an off-the-shelf observability platform.

## Practical takeaways
1. Don't buy/build an eval tool before you've manually read ~100 traces yourself.
2. Keep the first pass fast and low-friction: freeform notes, no rigor, no root-causing.
3. Let an LLM propose categories, but always hand-edit them for specificity before trusting them.
4. Prioritize by both frequency (pivot table counts) and product-judged severity — they can diverge.
5. Match eval type to failure type: code assertions for objective bugs, LLM judges for subjective/contextual failures.
6. Always report/validate TPR and TNR for any LLM judge before trusting its scores.
7. Put the PM/domain expert in the driver's seat for error analysis and prompt editing; don't fully delegate to engineering.
8. If pre-launch, use dogfooding or synthetic user simulation to generate the traces you need to start this process.

## Notable soundbites (paraphrased, not verbatim)
- Skipping error analysis is the single biggest reason people fail at evals — it looks time-consuming but usually isn't.
- A judge that just always outputs "pass" can look ~90% accurate on rare failures — agreement alone is a trap metric.
- Separating the prompt from the PM is almost absurd, since a prompt is just English.
- Once you actually do error analysis once, you get hooked and never stop — it's described almost like a "secret club."
- Handing error analysis off to someone else means giving away the one place where your product's real differentiation gets built.

## Anything conference-talk-relevant
- The whole video is structured as a **linear pipeline with numbered stages** (traces → notes → categories → counts → eval choice → judge validation → deployment), which maps almost directly onto a "gates in a CI/CD pipeline" narrative — each stage could become a visual "gate" slide.
- The binary-pass/fail framing for judges pairs naturally with CI's pass/fail gate semantics — a strong analogy: "just like CI gates are binary, your eval judges should be binary too."
- The TPR/TNR validation step is a great parallel to "testing your tests" — before trusting an eval as a CI gate, you must validate the gate itself against ground truth, otherwise it's a flaky/lying gate.
- The code-eval vs. LLM-judge split maps cleanly onto "fast/cheap unit-test-like checks" vs. "slower, more expensive integration-style checks" — useful for framing tiered CI stages (fast gate first, expensive judge gate later).
- The "agreement is a trap metric" point is a vivid, quotable warning for the talk: a naive gate can look like it's working while being useless.
- The Jacob Carter dogfooding anecdote (fixed most issues before ever building a formal eval) is a good real-world proof point that error analysis alone delivers value before any pipeline/gate exists — useful as a "start here before you automate" beat.
