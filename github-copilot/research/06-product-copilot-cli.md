# 06. GitHub Copilot CLI

Install: https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli
Docs: https://docs.github.com/en/copilot/how-tos/copilot-cli
Beginner course: https://github.com/github/copilot-cli-for-beginners

## Positioning in Dev Days
"An autonomous coding agent that can plan complex tasks, run multistep workflows, edit files, run tests, and iterate until the job is done." The Copilot app is built on it. Option 2 track for terminal-first audiences. Included on Copilot Free.

## Features taught across the workshops
- Operating modes: Interactive, **Plan** ("blocked from editing project files"), **Autopilot**; Shift+Tab cycles modes
- Custom instructions (`/init` to generate them)
- MCP servers (e.g., Playwright MCP)
- Agent skills (reusable, domain-specific)
- Custom agents (e.g., QA agent)
- Plugins, hooks (named only in the copilot-cli-deep-dive-workshop README, which isn't linked from dev-days.github.com)
- Parallel sessions in worktrees
- Delegation to the cloud agent
- Context management

## Slash commands seen in the materials
| Command | Use |
|---|---|
| `/init` | Generate project instructions |
| `/plan` | Plan before editing |
| `/diff` | Review changes |
| `/context`, `/clear` | Inspect / reset what the agent sees |
| `/resume` | Return to an earlier session |
| `/remote` | Follow a session from another device |
| `/pr create`, `/pr agentmerge` | Create a PR; agent carries it to merge |
| `/delegate` | Hand off to a cloud agent session |
| `/model`-style model switching, sharing commands | Covered in the real-world CLI module 9 |
