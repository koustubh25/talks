# 04. Workshops (dev-days.github.com)

Site: https://dev-days.github.com/ — "5 workshops, 2–3 hours total, free to start." Source repo for the app/CLI workshops: https://github.com/github-samples/copilot-workshops (by James Montemagno and others, MIT).

| Workshop | Level | Time | URL |
|---|---|---|---|
| First Steps with the Copilot app | Beginner | 1–1.5 hr | https://github-samples.github.io/copilot-workshops/first-steps/copilot-app/ |
| Real-world Development with the Copilot app | Intermediate | 1–1.5 hr | https://github-samples.github.io/copilot-workshops/real-world-development/app/ |
| Copilot CLI first steps (linked as "Copilot CLI Workshop") | Beginner | 1–1.5 hr | https://github-samples.github.io/copilot-workshops/first-steps/copilot-cli/ (gh.io/dev-days/workshop/cli) |
| Mona Mayhem (CLI track) | — | ~60 min | https://copilot-dev-days.github.io/mona-mayhem/?track=cli |
| Copilot SDK Workshop | Beginner→ | 30–115 min | https://github.github.com/copilot-sdk-workshop/ |

Note: the content README names "Tailspin Toys" as the CLI lab (~2 hr), but the site's link now points to the CLI *first steps* (Space Quiz). The Tailspin Toys CLI version lives under real-world-development/cli.

---

## A. First Steps with the GitHub Copilot app (Beginner)

Build a colorful **Space Quiz** (single HTML file) from an empty folder through to a reviewed PR and a live GitHub Pages site.

| # | Lesson | Feature taught |
|---|---|---|
| 0 | Prereqs & setup | Install app, pick model, tour workspace |
| 1 | Create the workspace | Interactive session in an empty folder |
| 2 | Build and polish | Prompting, integrated browser |
| 3 | Inspect and test | Context/usage inspection, browser smoke test |
| 4 | Project instructions | `/init` |
| 5 | Publish | Create public GitHub repo from local project |
| 6 | Issues and sessions | Backlog, implement issue in isolated **worktree**, diff review |
| 7 | Plan before you edit | **Plan mode** |
| 8 | Review loop | PR, Copilot review feedback, **Agent Merge** |
| 9 | Automate triage | Scheduled **automation** (weekly issue triage) |
| 10 | Continue remotely (opt.) | `/remote` from web/mobile |
| 11 | Explore a Canvas | Repository Issues Kanban **Canvas** |
| 12 | Deploy | GitHub Pages workflow |
| 13 | Review & next steps | — |

## B. Real-world Development with the Copilot app (Intermediate)

Work a seeded **Tailspin Toys** backlog (crowdfunding site for games). Requires Copilot Student/Pro/Pro+/Business/Enterprise (not Free), Git, Node.js; Business/Enterprise need the Copilot CLI policy enabled.

| # | Module | Feature taught |
|---|---|---|
| 0 | Prerequisites | Node.js, project copy |
| 1 | Install the app | Connect project, navigate |
| 2 | Add star ratings | First change, browser review, manual merge (PR 1) |
| 3 | Agent modes | **Plan** from issue → **Autopilot** build → **Interactive** review |
| 4 | Custom instructions | Update repo instructions |
| 5 | Quality-checks skill | Customize and run an **agent skill** |
| 6 | Playwright MCP | Add MCP via Customize; browser inspection |
| 7 | QA agent | Create/select a custom agent profile; verification evidence |
| 8 | Feature PR | Review + **Agent Merge** (PR 2) |
| 9 | Canvases | Database Explorer canvas; build a triage canvas |
| 10 | Wrap-up | — |
| opt | Foundry | Foundry canvas (Azure AI Foundry hosted agent) |

## C. Copilot CLI first steps

Same Space Quiz, from the terminal.

| # | Lesson | CLI feature |
|---|---|---|
| 0 | Setup | Install, sign in, model choice |
| 1 | Build the quiz | Review diffs before Git writes |
| 2 | Project instructions | `/init` |
| 3 | Publish | Commit/publish by prompt or by hand |
| 4 | Issues in parallel | Add issue to chat, `/diff`, second session in a worktree |
| 5 | Plan | `/plan` |
| 6 | Context | `/context`, `/clear` |
| 7 | Resume / remote | `/resume`, `/remote` |
| 8 | PRs | `/pr create`, `/pr agentmerge` |
| 9 | Delegate | `/delegate` to a cloud session |
| 10 | Review | — |

## D. Real-world Development with the Copilot CLI (Tailspin Toys)

Codespace-based. Modules: install CLI → star ratings → Plan/Autopilot/Interactive modes → custom instructions → quality-checks skill → Playwright MCP → QA agent → feature PR with Agent Merge → slash commands (context, models, sharing, optional delegation) → wrap-up → optional Foundry hosted agent.

Other tracks on the same site: VS Code first steps, Real-world VS Code (agent mode, Playwright MCP, custom agents, Foundry Toolkit), Real-world **cloud agent** (custom instructions, cloud agent, custom agents, managing agents).

## E. Mona Mayhem

Retro arcade "GitHub Contribution Battle Arena" (Astro + TypeScript). VS Code and CLI tracks share steps; instructions switch per track. ~60 min stated (parts sum to ~80).

00 Overview (5) → 01 Setup & Context Engineering: workspace instructions, background agents, Ask (15) → 02 Plan & Scaffold: Plan mode (15) → 03 Build: Agent mode (10) → 04 Design-first theming (10) → 05 Polish & parallel work: background/cloud agents (10) → 06 Bonus (15+).

## F. Copilot SDK Workshop

https://github.github.com/copilot-sdk-workshop/ · SDK: https://github.com/github/copilot-sdk
Languages: .NET, Go, Java, Node.js, Python, Rust. No prior agent experience needed.

| Track | Time | What you build / learn |
|---|---|---|
| SDK 101 | ~30 min | Streaming hello world → podcast agent; client/session setup, streaming, local tools, approvals |
| Review web accessibility | ~115 min | SDLC agent that inspects a page against WCAG and reports; local tools, Playwright MCP, permissions |
| Curate a museum exhibit | ~90 min | Non-SDLC agent turning approved facts into exhibit copy; persona, one app-owned tool, output validation, evaluation |

SDK landing-page learning goals (all tracks): "Separate durable agent policy from task data." "Explain where prompt guidance ends and hard controls begin."
