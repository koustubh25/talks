---
name: copilot-cli-talk
description: Accurate knowledge base for GitHub Copilot CLI (and Copilot cloud agent on github.com) plus context for Koustubh's talk "Soft Rules vs Hard Controls: Keeping Copilot CLI Agents Safe at Work" (Azure Builders: GitHub Copilot Dev Days, Melbourne, Mon 16 Nov 2026). Use for any question about Copilot CLI flags, slash commands, modes (Plan/Autopilot), permissions, sandbox, hooks, custom instructions, skills, custom agents, MCP, enterprise managed settings, content exclusion, or cloud agent guardrails, and when brainstorming, outlining, or building the presenterm slides and demo for this talk.
---

# Copilot CLI talk: knowledge base

All files live in `talks/github-copilot/`. Paths below are relative to that folder.

## Rules for answering
1. **Answer from the local files, not from memory.** Copilot CLI ships almost daily (1.0.103 on 2026-10-22), and older knowledge is often wrong (for example, "the CLI has no sandbox" is false).
2. **Cite the file** (and quote it) for any claim that could end up on a slide.
3. For "what exists now": `knowledge/cli-live/` (help text from the installed prerelease CLI, `/opt/homebrew/bin/copilot`) > changelog > docs. The docs explain how things work. Point out any disagreement.
4. You may run `copilot --help`, `copilot help <topic>` and `copilot <cmd> --help` freely. **Don't run prompts (`-p`, `-i`, or an interactive session) without asking**, because they use the user's AI credits. UI wording (approval prompts, status line) is still "verify live".
5. Event facts come only from `research/01-melbourne-event.md` (Meetup page is the source of truth). `research/` is the older dev-days topic research; for CLI behaviour, `knowledge/` wins.
6. The speaker uses **Copilot CLI only**, not the Copilot app. The event is Microsoft-sponsored, so the **github.com side (cloud agent, PR gate, rulesets, org policy) is in scope**.
7. `talks/` is a git repo with the user's own uncommitted work. Don't commit unless asked.

## Where to look
| Need | File |
|---|---|
| Talk-ready facts on every soft/hard control, with quotes | `knowledge/cli-safety-controls.md` (**read first**) |
| Latest flags, slash commands, help topics (prerelease CLI) | `knowledge/cli-live/README.md` (findings), `knowledge/cli-live/help/*.txt` |
| Find a docs page | `knowledge/docs/INDEX.md` (grep it) |
| Flags, slash commands, shortcuts, env vars | `knowledge/docs/reference/copilot-cli-reference/cli-command-reference.md` |
| `settings.json`, `permissions-config.json`, config dir | `knowledge/docs/reference/copilot-cli-reference/cli-config-dir-reference.md` |
| Hooks (events, fail-open/closed, policy hooks) | `knowledge/docs/reference/hooks-reference.md` |
| Sandbox | `knowledge/docs/concepts/security-governance-and-network-settings/understanding-local-sandboxing.md`, `knowledge/docs/how-tos/cloud-and-local-sandboxes/` |
| Admin / managed settings | `knowledge/docs/reference/enterprise-administrators/enterprise-managed-settings.md`, `knowledge/docs/how-tos/copilot-cli/administer-copilot-cli-for-your-enterprise.md` |
| Cloud agent guardrails (github.com) | `knowledge/docs/concepts/security-governance-and-network-settings/risks-and-mitigations.md`, `knowledge/docs/tutorials/cloud-agent/build-guardrails.md` |
| When something shipped or changed | `knowledge/changelog-by-topic.md`, `knowledge/copilot-cli/changelog.md` |
| Talk plan, running order, open items | `talk/outline.md` |
| The demo ("The Southbank Vault", a heist game driven by CLI hooks) | `talk/demo-plan.md` |
| Incidents, research and other people's demos | `talk/demo-inspiration.md` |
| Older source quotes for the talk | `talk/research-notes.md` |

## Talk in one paragraph
Telling an agent what not to do isn't the same as stopping it.
- **Soft controls** (instructions, `AGENTS.md`, skills, custom-agent prompts) guide the model. GitHub's own docs: "Instructions guide the model, but do not guarantee that it will follow every rule."
- **Hard controls** are enforced by the CLI, the OS, or GitHub:
  - modes (Plan is enforced; Autopilot is about continuation, not permission)
  - tool allow/deny
  - the local sandbox
  - `preToolUse` hooks
  - rewind
  - the PR / ruleset / CODEOWNERS gate on github.com
  - enterprise managed settings

The second axis is **who can switch each control off**: the model, you mid-session, someone with merge rights, or only an admin. Format: 15 min + 5 Q&A (may grow to 25 + 5). Terminal slides in presenterm, opening with a demo.

## Keeping it fresh
Run `knowledge/scripts/refresh.sh`. It pulls the changelog, re-renders the docs pages and rebuilds the indexes. Afterwards, re-check the quotes in `cli-safety-controls.md`.
