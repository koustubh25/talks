# Copilot CLI knowledge base

Accurate, local reference for GitHub Copilot CLI and the github.com agent features, built for the "Soft Rules vs Hard Controls" talk.

## What's here

| Path | What it is | Freshness |
|---|---|---|
| [cli-safety-controls.md](cli-safety-controls.md) | **Start here for the talk.** Curated fact sheet: every soft and hard control, with exact quotes and source files. | Hand-written 2026-10-25 |
| [docs/INDEX.md](docs/INDEX.md) | Index of 132 official docs pages: title, one-line intro, word count, sections | github/docs @ 02c25d1 (2026-10-23) |
| `docs/` | The pages themselves, rendered from github/docs to plain markdown (templates resolved, links made local where possible). Same paths as on docs.github.com/en/copilot/… | same |
| [changelog-by-topic.md](changelog-by-topic.md) | All 2,955 CLI changelog bullets grouped into 18 topics (sandbox, permissions, hooks, modes, MCP, policy…) | CLI 1.0.103 (2026-10-22) |
| [cli-live/](cli-live/README.md) | Help text captured from the **installed prerelease CLI** (every flag, slash command and help topic), plus findings. **Most current source.** | CLI 1.0.104-3 (2026-10-25) |
| `copilot-cli/` | Clone of github/copilot-cli: README, `changelog.md`, `install.sh`. **Not the source code**: the CLI is closed source. | git pull to update |
| `scripts/` | `refresh.sh` rebuilds everything; `selected-pages.txt` lists which doc pages to include | |

## How to look things up

1. Talk fact? Check `cli-safety-controls.md` first.
2. Otherwise, grep `docs/INDEX.md` for the topic, then read the page.
3. The big references:
   - `docs/reference/copilot-cli-reference/cli-command-reference.md`: every flag, slash command, shortcut, and env var.
   - `docs/reference/copilot-cli-reference/cli-config-dir-reference.md`: `settings.json`, `permissions-config.json`, and the config directory.
   - `docs/reference/hooks-reference.md`
   - `docs/reference/enterprise-administrators/enterprise-managed-settings.md`
4. "Is this new / when did it change?" Check `changelog-by-topic.md`, or grep `copilot-cli/changelog.md`.

## Which source wins

- **What exists now:** `cli-live/` (installed prerelease) > changelog > docs. If they disagree, say so.
- **How it works:** the docs, which explain far more than the help text.
- **Docs vs workshops/blogs in `../research/`:** the docs win for CLI behaviour.
- **UI wording** (approval prompts, status line) has only been seen in docs and help text, not in a running session yet. Check live before putting it on a slide.
- Re-capture help with `scripts/capture-cli-help.sh` (no credits used).

## Scope

- **Copilot CLI:** setup, use, customize, automate, reference, and administer.
- **Shared customization concepts:** instructions, skills, agents, hooks, MCP, and plugins.
- **Security and governance:** sandboxes, content exclusion, risks, and network settings.
- **Enterprise:** managed settings, policies, and the MCP allowlist.
- **github.com:** cloud agent, PR review, firewall, and the guardrails tutorial.
- Not included: IDE-specific pages and the Copilot SDK (except where CLI-related).

To add a page, append it to `scripts/selected-pages.txt`, then run `scripts/refresh.sh`.
