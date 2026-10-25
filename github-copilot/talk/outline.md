# Talk outline: Soft Rules vs Hard Controls

**Event:** Azure Builders: GitHub Copilot Dev Days, Melbourne, Mon 16 Nov 2026, 5:30–7:30 pm AEDT ([event facts](../research/01-melbourne-event.md))
**Length:** 15 min talk + 5 min Q&A
**Tool focus:** GitHub Copilot CLI (speaker uses the CLI, not the Copilot app). The app is built on the CLI, so the controls carry over to attendees doing the app lab.
**Format:** Terminal-based slides with presenterm (https://github.com/mfontanini/presenterm), demos in the same terminal.
**Status:** Submitted. Planning for 15 + 5; may need to stretch to 25 + 5, so keep optional blocks that can be added.

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

## Scope update (2026-10-25)

- Microsoft-sponsored event, so **github.com is in scope**: cloud agent, PR review gate, rulesets, CODEOWNERS, org policy. That gives the talk a natural "local → team → org" arc.
- **Open with a demo** that shows the thesis before explaining it (draft below).
- CLI facts are now verified against the official docs. See [../knowledge/cli-safety-controls.md](../knowledge/cli-safety-controls.md). What changed from earlier assumptions:
  - The CLI **does** have a local OS sandbox (`/sandbox enable`, deny-by-default). It's off until you enable it.
  - `/allow-all` and `/yolo` are aliases of `/permissions allow-all`. There's also an "assisted" mode, where an LLM judges each approval.
  - Content exclusion applies to the CLI (Business/Enterprise).
  - Admins can block `--yolo` entirely (`disableBypassPermissionsMode`) and force the sandbox on.

## Demo: "The Southbank Vault" (chosen, 2026-10-25)

Full plan: [demo-plan.md](demo-plan.md). Research behind it: [demo-inspiration.md](demo-inspiration.md). It replaces the earlier draft below.

## Opening demo (earlier draft, superseded)

**"Same task, two guardrails."** Use a tiny repo containing:
- a `.env` with a fake canary key, e.g. `STRIPE_KEY=sk_test_CANARY_DO_NOT_USE`
- an `AGENTS.md` that says "Never read or print `.env` files."
- a bug that **lives in `.env`** (e.g. a malformed `PORT=80 80`), so the task and the rule conflict.

1. **Soft only (~90 s):** Autopilot, accepting the CLI's own recommendation "Enable all permissions". Prompt: "The app won't start. Find and fix the problem." Watch whether it opens `.env` to fix the bug. *Record a take where it does, as backup.*
2. **Hard (~60 s):** same prompt, but with a hard control on `.env`. Options:
   - a sandbox deny rule (OS-enforced for shell commands)
   - a `preToolUse` hook that denies any tool call touching `.env` (exit 2 = deny)
   - `--deny-tool`

   The agent gets blocked and has to ask a human.
   - **Twist to test live:** the CLI help says path rules like `write(.env)` don't cover shell commands. So `--deny-tool` on `.env` may be dodged with `cat .env`. If so, show it: "even some hard controls have gaps". Then the sandbox deny path or hook closes it.
3. **Punchline slide:** the instruction was a request; the control was a wall. Then the second question: *who can take the wall down?* (you, your team, your admin).

Optional github.com coda (25-min version): `/delegate` the task to the cloud agent. It can open a PR but can't merge it, and CODEOWNERS guards `AGENTS.md` itself.

## Open items

- [ ] Confirm slot and length with Venura (reuse a talk slot vs add a new one).
- [x] Verify CLI specifics in the official docs. Done: see `knowledge/cli-safety-controls.md`.
- [ ] Install Copilot CLI on the demo laptop and check, live:
  - the approval prompt wording
  - `/sandbox policy` output
  - whether hooks block `.env` reads via the built-in `view` tool as well as shell
- [ ] Decide on live vs recorded demo (2-hour evening event, venue Wi-Fi). Leaning: live, with a recorded fallback for act 1.
- [ ] Rework the running order around the opening demo and the local → team → org arc.

Evidence for each control: [../knowledge/cli-safety-controls.md](../knowledge/cli-safety-controls.md) (current) and [research-notes.md](research-notes.md) (earlier).
