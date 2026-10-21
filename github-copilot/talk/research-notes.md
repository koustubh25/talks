# Research notes: source quotes for the guardrails talk

Quotes copied from each page on 2026-10-22. Gaps are marked **[gap]**.

Page shorthand:
- **CLI first steps:** https://github-samples.github.io/copilot-workshops/first-steps/copilot-cli/
- **Real-world CLI:** https://github-samples.github.io/copilot-workshops/real-world-development/cli/
- **Agent modes lesson:** https://github-samples.github.io/copilot-workshops/real-world-development/cli/3-agent-modes/
- **App docs:** https://docs.github.com/en/copilot/concepts/agents/github-copilot-app
- **App changelog:** https://github.com/github/app/blob/main/changelog.md
- **SDK workshop:** https://github.github.com/copilot-sdk-workshop/

## 1. Modes (Interactive / Plan / Autopilot) — CLI source ✔
Agent modes lesson:
> "The conversation mode controls how much autonomy the agent has. Press Shift+Tab to cycle between modes:
> Interactive: You and the agent work together. The agent suggests changes and waits for your input before proceeding.
> Plan: The agent creates a plan first and is blocked from editing project files.
> Autopilot: The agent works autonomously — writing code, running tests, and iterating until the task is complete."

> "You'll use Plan mode to resolve those decisions, then authorize a bounded implementation with Autopilot."

App docs:
> "Use Plan mode to validate scope and approach, use Interactive mode when you want tighter steering, and move to Autopilot when the task is well-defined."

## 2. `/plan` — CLI source ✔
CLI first steps:
> "5. Plan before you edit — Use /plan to agree on an approach for the second issue"

## 3. Tool permissions / approvals — app & SDK only [gap: confirm for CLI]
SDK workshop:
> "Client and session · streaming · prebuilt local tools · approvals"
> "Streaming · local tools · Playwright MCP · permissions"

App changelog:
> "Set tool permissions directly from the composer's mode menu, in addition to the /permissions slash command."
> "Fixed the /permissions, /allow-all-tools, and /yolo commands so they now work in a new chat before a session has started, updating your default tool-approval setting for future sessions."
> "When switching to Autopilot mode with tool permissions set to Always ask, Copilot now recommends a permission mode that lets it keep working unattended…"

## 4. Hooks — thinnest [gap: how they work in the CLI]
App changelog:
> "Fixed a security issue where tool approval prompts requested by a hook could be skipped instead of always requiring your explicit approval."
> "…a reminder now appears above the composer so you can revisit and accept hooks and extensions for the session."

CLI deep-dive workshop README (https://github.com/copilot-dev-days/copilot-cli-deep-dive-workshop). Not linked from dev-days.github.com:
> "Covers operating modes, custom instructions, MCP servers, agent skills, plugins, custom agents, hooks, context management, and more"

## 5. Sandbox — app only [gap: does the CLI have one?]
App docs:
> "You can run a session in a cloud sandbox, or configure a local sandbox to restrict the resources available to agent-run tools on your machine."

App changelog:
> "Added a project setting and `/sandbox` command that let you run the agent's shell commands in a local sandbox, restricting filesystem access to the session's workspace."

## 6. Worktrees — CLI source ✔
CLI first steps:
> "Create a backlog, add an issue to chat, review with /diff, and start a second session in a worktree"

## 7. PR review gate — CLI source ✔
CLI first steps:
> "build and review diffs before Git writes anything"
> "Create and merge a pull request with /pr create and /pr agentmerge"

Real-world CLI:
> "Review the complete filtering change and use Agent Merge for the filtering PR."

## 8. Custom instructions — CLI source ✔
CLI first steps:
> "Generate and tailor agent instructions with /init"

Real-world CLI:
> "Update the repository instructions and apply them to the filtering work."

## 9. Skills / custom agents — CLI source ✔
Real-world CLI:
> "Customize the existing quality-checks skill and use it to run the project checks."
> "Create a quality assurance (QA) custom agent and use it to review requirements, coverage, and verification evidence."

## 10. MCP servers — CLI source ✔
Real-world CLI:
> "Add the Playwright Model Context Protocol (MCP) server and use it to explore filtering in a browser."
> "Configure MCP in the CLI and inspect filtering behavior"

## 11. Admin policies — CLI source ✔
Real-world CLI:
> "If you are using Copilot Business or Copilot Enterprise, ensure your administrator has enabled Copilot CLI for use."

App docs:
> "For Copilot Business and Copilot Enterprise users, the GitHub Copilot app policy must remain enabled. This policy is enabled by default and is separate from the Copilot CLI policy."

## 12. Content exclusion — app only [gap: confirm for CLI]
App docs:
> "…the GitHub Copilot app respects content exclusion policies configured at the enterprise, organization, and repository levels. Excluded files are not used as context."
> "The GitHub Copilot app may generate code that is a match or near match of publicly available code, even if the 'Suggestions matching public code' policy is set to 'Block.'"

## 13. Prompt guidance vs hard controls — framing line
SDK workshop landing page, learning goals for all three workshops:
> "Separate durable agent policy from task data."
> "Explain where prompt guidance ends and hard controls begin."
