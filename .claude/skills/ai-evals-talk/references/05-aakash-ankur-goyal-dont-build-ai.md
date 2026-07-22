# If You Don't Understand AI Evals, Don't Build AI
Speaker: Aakash Gupta interviewing Ankur Goyal (CEO, Braintrust) | ~52min | YouTube

## Core thesis
LLMs are powerful but fundamentally unpredictable, and the durable competitive moat in AI products isn't the prompt or agent scaffolding (which will be obsolete in months) — it's the evaluation harness a team builds around the model. Evals are reframed as the modern evolution of the PRD: a quantifiable, living spec that product and engineering can both act on, replacing the old unstructured document nobody actually followed. Teams that treat evals as a core iterative loop (not a gate) build real differentiation; teams that don't are flying blind on quality.

## Key frameworks / mental models
- **Vibe checks are a legitimate first rung of evals** — using your own brain as a scoring function — but they stop scaling once a product hits real usage and more stakeholders need to weigh in.
- **The "distance from the end user" principle**: the more organizational/domain distance between the people building the AI and the people using it, the more essential formal evals become. Anthropic's Claude Code can get away with informal evals because model trainers, harness builders, and power users are all inside one company; a healthcare AI startup has no such luxury.
- **Evals = Data + Task + Scores**, a three-part framework: Data (inputs, optionally a ground-truth answer), Task (the thing under test — a single LLM call or a full agent), Scores (a function that grades output, normalized to a 0–1 range for comparability over time).
- **Categorical/rubric scoring over free-form numeric scores** — don't let the LLM invent an arbitrary float; give it clear discrete criteria (e.g., pass/partial/fail) so grading is legible and consistent.
- **Evals should sometimes fail on purpose.** An eval suite that never fails means you don't actually know your product's limits — you need visibility into both what users struggle with and what's currently impossible.
- **Offline vs. online evals**: offline evals run against a curated/golden dataset in a sandbox; online evals run the same scoring functions against live production logs. Discrepancies between the two (e.g., 0.75 offline vs 0.3 online) signal the offline dataset doesn't represent real usage — mine the failing live examples and feed them back into the offline set, creating a flywheel.
- **Evals as durable investment**: models, frameworks, and agent architectures change constantly; a well-built eval (grounded in real user data and clear scorers) survives those changes and keeps compounding in value.

## Concrete examples / horror stories discussed
- The viral tweet/controversy claiming Claude Code ships without formal evals, which rattled PMs at other companies; Goyal argues this is misleading — Anthropic's tight feedback loop (trainers, builders, and users under one roof) functions as an eval even without a formalized tool.
- A live, unscripted demo building an eval for a "linear task assistant" from scratch: initial system prompt produced vague, non-answering responses; scoring came back near-zero, confirming the vibe check; after iterating on the prompt (removing clarifying-question behavior, adding few-shot examples, connecting the real Linear MCP server, trying different models), the score climbed to 0.75.
- Anecdote about Gemini 3 Flash outperforming Gemini 3 Pro on some coding benchmarks while actually hallucinating more — illustrating that a benchmark score going up doesn't automatically mean "better," and can also indicate a broken benchmark.
- The Claude 3.7 "watershed moment": before that model, agents attempting to self-review their own work behaved almost randomly (Goyal's metaphor: a dog not recognizing itself in a mirror); Braintrust's own internal eval for a self-improving-agent product ("Loop") failed until Claude 3.7 shipped, at which point performance jumped enough to justify releasing the feature.
- Braintrust's growth data as a proxy for industry-wide eval adoption: roughly 10x more experiments run per user year-over-year, 2x more data logged per day than in the company's entire first year — attributed to bigger prompts, more agentic LLM calls per request, and more products reaching real product-market fit.

## Practical takeaways / how-to steps
1. Start with a vibe check to build intuition, but plan to formalize it into a structured eval once more people (engineers, PMs, subject-matter experts) are involved.
2. Define your eval loop in three parts: assemble representative input data (real or synthetic), define the task under test, write a scoring function.
3. Don't over-invest in a "perfect" golden dataset upfront — generate quick, even silly, synthetic questions and start iterating immediately rather than spending a month on prep.
4. Prefer clear categorical/rubric-based scoring criteria over unconstrained numeric scores, especially for LLM-graded outputs.
5. Run the eval, then treat a bad initial score as expected and useful — it validates that your scorer is aligned with reality.
6. Iterate on three separate levers independently: the dataset, the task (prompt/model/tools), and the scoring function itself — don't conflate fixing the prompt with fixing the grader.
7. Deploy the same scorer online against production logs; compare online vs. offline scores as a health check.
8. Build a daily ritual: review a sample of yesterday's production logs/failures, reconcile against eval scores, and add newly discovered failure patterns into the offline dataset.
9. Don't gate shipping strictly on eval pass/fail as a checkbox — use evals as the mechanism for continuous improvement, not a bureaucratic blocker.
10. Open access to the eval tool beyond AI engineers — PMs and domain experts should be able to write/adjust scorers directly.

## Notable soundbites (paraphrased, not verbatim)
- An eval that never fails is actually a sign of ignorance, not success — it means you don't know your product's real edges.
- The prompt and agent wiring you're proud of today is not your moat; it'll likely be replaced in a couple months — the eval harness around it is what actually endures.
- Treat the modern eval the way teams used to treat the PRD: a spec you can mechanically check software against, instead of a document everyone quietly ignores.
- A benchmark score moving is just a signal that something interesting happened — not proof that something got better.
- The best teams don't use evals as a gate before shipping; they use evals as the daily habit that tells them what to work on next.
- Don't spend a month building the "perfect" dataset before you start — run something dumb today and improve it tomorrow.

## Anything conference-talk-relevant
- Strong opening hook potential: the framing "if you don't understand evals, don't build AI" is itself a punchy, slightly provocative title/thesis that could open a talk — pairs well with the "vibe check vs. structured eval" spectrum as a way to meet the audience where they are before pushing toward CI/CD gates.
- The "distance from the end user" model maps directly onto a CI/CD argument: as more people (across roles, and eventually across an org's deploy pipeline) touch an AI feature without direct visibility into its behavior, informal/manual eval checks stop being sufficient — this is a natural bridge into "why you need gates, not vibes, in your pipeline."
- "Evals that fail are valuable" is a great counter-intuitive point for a CI/CD talk: unlike traditional unit tests (where 100% green is the goal), a healthy eval suite for agents should intentionally surface known-hard cases, and CI gates should track failure trendlines, not just pass/fail thresholds.
- The online/offline eval flywheel (production failures feeding back into the offline/regression dataset) is essentially a CI/CD analogy already — it's the AI-native version of "add a regression test when you find a bug," and could be presented as a direct parallel to traditional test-suite hygiene.
- The Claude 3.7 anecdote (eval failing for months, then suddenly passing when the underlying model crossed a capability threshold) is a good story for illustrating why gates must be re-run against new model versions automatically, not just once at ship time — a natural case for automating eval reruns in CI whenever a model/dependency updates.
- Useful fear/urgency framing: benchmark improvements can mask regressions elsewhere (the Gemini Flash-outperforms-Pro-but-hallucinates-more example) — a strong illustration for why you can't trust a single aggregate score gating a deploy; multi-metric gates are needed.
