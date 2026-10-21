# 05. GitHub Copilot app (the centerpiece of this round)

Marketing page: https://github.com/features/ai/github-app ("the only desktop experience for agent-driven development built natively on GitHub")
Docs: https://docs.github.com/copilot/concepts/agents/github-copilot-app · Quickstart: https://docs.github.com/en/copilot/get-started/quickstart-copilot-app
Repo/feedback: https://github.com/github/app · Changelog: https://github.com/github/app/blob/main/changelog.md

## What it is
- Desktop app (macOS, Windows, Linux), **built on top of Copilot CLI**, native to GitHub repos, branches, issues, PRs, and CI.
- Available on all Copilot plans (incl. Free), or with your own API key (BYOK). Business/Enterprise: "Copilot app" policy, on by default.
- Runs locally (not in a codespace).

## Core concepts
| Concept | Meaning |
|---|---|
| Sessions | One isolated agent task each; run many in parallel. Start from an issue, a prompt, or a PR. |
| Worktrees | Each session can get its own git worktree + branch, so parallel work doesn't collide. |
| Modes | **Interactive** (collaborative), **Plan** (agent proposes, you approve), **Autopilot** (autonomous). `/goal` sets a persistent objective for Autopilot. |
| Chats | Brainstorm without a branch/workspace. Chats can spawn child chats. Side questions via `/ask`, `/btw`. |
| Validation loop | In-session diffs, in-app browser preview, terminal checks, merge PRs. |
| Agent Merge | Agent carries a PR through rebases, review feedback, CI fixes, and merge. |
| Automations | Saved recurring agent tasks: scheduled, on demand, or on repo events; cloud schedules run while your machine is off. |
| Canvases | Custom agent-driven UIs where people and agents collaborate (e.g., Kanban of issues, Database Explorer, Sentry triage canvas). |
| Customize | One place for plugins, skills, MCP servers, canvases; create personal skills; org plugin marketplaces. |
| Custom agents | Specialist profiles (e.g., QA agent); can suggest handoff to another agent. Coordinator agents with child sessions. |
| Sandboxes | Cloud sandbox or local sandbox (`/sandbox`) restricting shell to the workspace. |
| Models | Multiple LLMs, reasoning effort and context size per session; Auto mode explains its model choice; retry with a different model. Default for new sessions: GPT-5.6 Sol (medium). |
| Computer use | On local macOS/Windows sessions, agents can drive desktop apps lacking API/CLI/MCP. |
| `/chronicle` | Insights from past sessions; `/chronicle cost tips` flags costly usage. |
| `/remote` | Follow a local session from web or mobile. |
| Design | Impeccable design skill (23 commands like `/critique`, `/polish`), under Experimental settings. |
| Third-party agents | Pro and up: Claude Code and Codex agents. |

## Changelog snapshot (fetched 2026-10-22)
- 92 releases, v0.2.0 → **v1.1.30** (latest).
- Recent highlights: install skills from folder/ZIP/URL; change model mid-run; cloud automations with repo-event triggers restored; org plugin marketplace tab; custom agents suggest next steps; resume interrupted coordinator + child sessions; child chats; run Bash/PowerShell snippets in session terminal; Ctrl+R prompt history; voice dictation on by default; local sandbox `/sandbox`; Sentry canvas; Power BI MCP and Azure DevOps in catalog; MCP install via deep link; `/goal`; "Fix with instructions" on PRs; branch update strategy (merge vs rebase); session auto-archive; generated files collapsed in diffs; security fix so hook-requested tool approvals can't be skipped.
