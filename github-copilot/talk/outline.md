# Talk outline: Soft Rules vs Hard Controls

**Event:** Azure Builders: GitHub Copilot Dev Days, Melbourne, Mon 16 Nov 2026, 5:30–7:30 pm AEDT ([event facts](../research/01-melbourne-event.md))
**Length:** 15 min talk + 5 min Q&A
**Tool focus:** GitHub Copilot CLI (speaker uses the CLI, not the Copilot app). The app is built on the CLI, so the controls carry over to attendees doing the app lab.
**Format:** Terminal-based slides with presenterm (https://github.com/mfontanini/presenterm), demos in the same terminal.
**Status:** Draft. Slot not yet confirmed with the organizer (Venura A.).

## Submission (chosen)

**Title:** Soft Rules vs Hard Controls: Keeping Copilot CLI Agents Safe at Work

**Description:** Telling an agent what not to do isn't the same as stopping it. Learn which GitHub Copilot CLI features only guide the agent and which actually enforce limits, and how to combine them before you let it run unattended.

Other options considered:
- **Before You Hit Autopilot: Guardrails for AI Coding Agents** — AI coding agents can now run shell commands, edit files and merge pull requests on their own, so where should you draw the line? This terminal-first tour of GitHub Copilot CLI covers both kinds of guardrail: soft rules like custom instructions and skills, and hard controls like Plan mode, tool approvals, hooks and pull-request review.
- **Trust, but Verify: Guardrails for GitHub Copilot CLI** — A practical, live-in-the-terminal look at how to give AI coding agents real autonomy without giving them the keys to everything.

Combines two candidate topics:
- **Instructions vs skills vs custom agents vs MCP** (which customization to use when)
- **Using AI coding agents safely at work** (permissions, sandboxes, policies)

## Core idea

From the Copilot SDK workshop's learning goals: "Explain where prompt guidance ends and hard controls begin."

- **Soft controls** steer the agent, but it can ignore them: custom instructions, skills, custom agents.
- **Hard controls** enforce limits: modes, tool approvals/permissions, hooks, worktrees, PR review, admin policies.

## Running order (15 min)

| Time | Section | Content |
|---|---|---|
| 0–2 | Hook | An agent in Autopilot mode with shell access. What could go wrong: deleted files, leaked secrets, a risky MCP server. |
| 2–4 | Where the risk is | Shell commands, file edits, MCP tools, credentials, network access |
| 4–7 | Soft controls | Custom instructions (`/init`), skills, a custom agent limited to one job (e.g., read-only reviewer). Why these aren't enough on their own. |
| 7–11 | Hard controls | Mode per task (Plan → Autopilot → Interactive), tool approvals and permissions (incl. `/allow-all-tools`, `/yolo` as anti-patterns), hooks, worktrees, PR as the human merge gate |
| 11–13 | Team level | Admin policies for Business/Enterprise, trusted MCP servers only, content exclusion |
| 13–15 | Takeaway | One-slide checklist: "before you turn on Autopilot…" |
| 15–20 | Q&A | |

## Open items

- [ ] Confirm slot and length with Venura (reuse a talk slot vs add a new one).
- [ ] Verify CLI specifics in official Copilot CLI docs (docs.github.com/en/copilot):
  - permission / tool-approval settings and flags
  - hook configuration
  - whether a local sandbox exists in the CLI (sources only confirm it for the app)
  - content exclusion support in the CLI
  - Business/Enterprise CLI policy
- [ ] Decide on live demo vs recorded demo (2-hour evening event, venue Wi-Fi).

Evidence for each control: [research-notes.md](research-notes.md).
