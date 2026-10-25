# Copilot CLI + github.com safety controls: talk fact sheet

Curated for "Soft Rules vs Hard Controls". Every claim has an exact quote and a file under `docs/` or `copilot-cli/changelog.md`.
Docs snapshot: github/docs @ 02c25d1 (2026-10-23). CLI changelog: up to 1.0.103 (2026-10-22).
If something here disagrees with the source file, the source file wins. Re-check after `scripts/refresh.sh`.

## The thesis, in GitHub's own words

| Quote | File |
|---|---|
| "Instructions guide the model, but do not guarantee that it will follow every rule." | `docs/concepts/customizations/comparing-customizations.md` |
| "Unlike custom instructions, hooks run code rather than asking the model to follow a rule." | `docs/concepts/customizations/hooks.md` |
| Plan mode: "this isn't just a suggestion to the model, it's enforced directly, so it doesn't depend on the model choosing to behave." | `docs/reference/copilot-cli-reference/cli-command-reference.md` (Security → Plan mode) |
| "Autopilot mode and tool permissions are separate controls" | `docs/concepts/agent-capabilities/agent-powered-workflows-and-operations/autopilot.md` |

## A ladder for the talk: who can switch it off?

A useful second axis besides soft vs hard. Each rung is harder to get around than the one below.

| Rung | Who can bypass it | Controls |
|---|---|---|
| 0. Soft | **The model** (it can just not follow it) | Custom instructions, `AGENTS.md`, skills, custom agent prompt text |
| 1. Session | **You, mid-session** (`/yolo`, `/sandbox disable`, approving a prompt) | Approval prompts, Plan mode, `--deny-tool`, local sandbox, repo/user hooks (`disableAllHooks`) |
| 2. Repo / team | **Someone with merge rights** | `.github/hooks/*.json`, `.github/copilot/settings.json`, CODEOWNERS on those files, branch rulesets, PR review |
| 3. Org / enterprise | **Only an admin** | Managed settings (`permissions.deny`/`ask`, `disableBypassPermissionsMode`, `sandbox.enabled` + `allowBypass:false`), policy hooks, MCP allowlist, content exclusion, CLI enable/disable policy |

---

## Soft controls (guide the model)

### Custom instructions
- Locations the CLI reads: `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `~/.copilot/copilot-instructions.md`. Source: `docs/how-tos/copilot-cli/customize-copilot/add-custom-instructions.md`.
- No precedence order: "does not define a general precedence order between these files. Avoid conflicting instructions." (same file)
- Talk point: an instructions file is a request, and so is any text the agent reads (an issue, a README, a web page). Prompt injection travels the same way your rules do.

### Skills and custom agents
- Custom agent `tools`: "List of tool names the custom agent can use… If unset, defaults to all tools." (`docs/reference/custom-agents-configuration.md`)
  - So a custom agent's **prompt** is soft, but its **`tools` list** is a hard limit. Good example of soft and hard in one file.
- Agent-scoped hooks can be declared in a custom agent's frontmatter (CLI only). (`docs/reference/hooks-reference.md` → Agent-scoped hooks)

---

## Hard controls (enforced by the CLI or OS)

### 1. Modes: Interactive / Plan / Autopilot (`Shift+Tab`)
- Autopilot = continuation, not permission: "Autopilot mode does not automatically grant unrestricted access." (`autopilot.md`)
- Three separate knobs (`docs/how-tos/copilot-cli/use-copilot-cli/use-autopilot-mode.md`):
  - **Autopilot** "controls continuation."
  - **`--allow-all` / `--yolo`** "control approvals… but do not enable autonomous continuation."
  - **`--no-ask-user`** "suppresses clarifying questions."
- On entering Autopilot the CLI offers: "1. Enable all permissions (recommended) / 2. Use Manual Approval for this session / 3. Cancel". With manual approval, "Copilot will automatically deny any tool requests that require approval." (same file)
  - **Talk gem:** the product's default recommendation on entering Autopilot is *enable all permissions*. That's the moment the talk is about.
- Autopilot is "sticky" by default (`stayInAutopilot`). (same file)
- Caps: `--max-autopilot-continues=COUNT`, `--max-ai-credits=CREDITS`, `/limits`. (same file)
- Plan-then-autopilot without a human check: `copilot --plan --mode autopilot` "does not wait for interactive plan approval." (same file)
- **Plan mode is enforced but not airtight:** "It's a safety net, not a guarantee… shell commands whose effect can't be clearly determined in advance, and calls to external/MCP tools you've connected" are allowed through. (`cli-command-reference.md` → Security → Plan mode)
- History: Autopilot added 0.0.400 (2026-01-30, experimental). (changelog)

### 2. Tool approvals and permissions
- Default: "read-only operations… are allowed automatically", while destructive shell commands, file edits and URL access "require your explicit approval". "a shell command can do anything your user account can do". (`docs/how-tos/copilot-cli/use-copilot-cli/allowing-tools.md`)
- **Talk gem, approval scope creep:** choosing "approve TOOL for the rest of the running session" on `rm ./this-file.txt` means "Copilot can run any `rm` command (for example, `rm -rf ./*`)". (`docs/concepts/copilot-surfaces/copilot-cli.md` → Allowed tools)
- Two layers (`allowing-tools.md`):
  - What the model can even see: `--available-tools`, `--excluded-tools`.
  - What it may use without asking: `--allow-tool`, `--deny-tool`, e.g. `--allow-tool='shell(git:*)' --deny-tool='shell(git push)'`.
- "Deny rules always take precedence over allow rules, even when `--allow-all` is set or a matching approval has been saved". (`allowing-tools.md`)
- Persisted approvals: "don't ask again in this repo" goes to `~/.copilot/permissions-config.json`; URL approvals go to `allowedUrls` in `~/.copilot/settings.json`. (`allowing-tools.md`)
- `/reset-allowed-tools` revokes session grants and saved approvals for the current location. (`allowing-tools.md`)
- Permission modes: `/permissions [default|assisted|allow-all|show]`; `/allow-all` and `/yolo` are aliases. (`cli-command-reference.md`)
  - **Assisted**: "still prompts for each request, but attaches an LLM safety recommendation so the CLI can auto-approve requests the model evaluates as acceptable." (`cli-command-reference.md`). Note that this is an AI judging an AI: firmer than soft, softer than hard.
- Docs warning: "You should never use an alias to apply one of these options every time you start Copilot CLI". (`allowing-tools.md`)
- Trusted directories: you confirm trust at startup; "Typically, you should not launch Copilot CLI from your home directory." and "Scoping of permissions is heuristic and GitHub does not guarantee that all files outside trusted directories will be protected." (`copilot-cli.md`)

### 3. Local sandbox (`/sandbox`): yes, the CLI has one
- "Copilot CLI runs the commands it invokes on your behalf inside an operating-system sandbox." "The sandbox is **deny-by-default**". (`docs/concepts/security-governance-and-network-settings/understanding-local-sandboxing.md`)
- Commands: `/sandbox status`, `/sandbox policy`, `/sandbox policy npm install` (preview without running), `/sandbox config`, `/sandbox disable` (session-only), flags `--sandbox` / `--no-sandbox`. (same file + changelog 1.0.103)
- What's covered, and **how hard**:
  - Shell commands, grep/glob, local MCP and LSP servers: enforced **by the OS**.
  - Built-in file read/edit tools: "a software-only safeguard rather than one the operating system enforces."
  - Remote MCP servers: "the filesystem policy does not constrain them".
  - (all from the same file) **Talk gem: even hard controls come in different strengths.**
- Default grants: the working directory is read/write; in a Git repo the **whole repo is readable**, so "a sandboxed command can read files outside your current subdirectory, including anything sensitive". Fix: add deny rules (e.g. an existing `.env`). (same file)
- `PATH` tool directories are read-only; package-manager caches are partly writable; "Some granted configuration files contain registry credentials". (same file)
- Sandbox + Autopilot: anything "that needs to escape the sandbox… is denied." (`use-autopilot-mode.md`)
- Sandbox escape always needs a human: a hook `allow` "does not pre-approve the request… leaving the sandbox is a privilege escalation the user must always confirm interactively." (`docs/reference/hooks-reference.md` → permissionRequest)
- Docs recommend a sandbox before any allow-all: "Before you grant Copilot wide-ranging permissions with an allow-all option, consider using local sandboxing". (`allowing-tools.md`)
- **Off until you turn it on:** `/sandbox enable` saves `sandbox.enabled` in `~/.copilot/settings.json` and applies to future sessions. `--sandbox` turns it on for one session only. Bypass requests are "enabled by default". (`docs/how-tos/cloud-and-local-sandboxes/using-local-sandboxing.md`)
- OS requirements (same file):
  - macOS: built in (Seatbelt).
  - Linux: needs `bwrap` ≥ 0.5.0 and `slirp4netns`.
  - Windows: needs Windows 11 25H2 + KB5124010 or 26H1 + KB5124006.
- **Credentials gem:** "Sandboxed commands and scripts receive placeholder Git and `gh` credentials. A local proxy replaces these with your real" credentials. The real token never enters the sandbox. (same file)
- The status line shows `sandbox enabled`. Good to show on a slide or in the demo. (same file)
- Setup how-tos: `docs/how-tos/cloud-and-local-sandboxes/using-local-sandboxing.md`, `configuring-local-sandbox-settings.md`.
- History: sandbox entries start around 1.0.57 (2026-06-01). (changelog)

### 4. Hooks
- Where: `.github/hooks/*.json` (repo), `~/.copilot/hooks/*.json` (user), inline in `.github/copilot/settings.json`, plugins, **policy hooks** in `/etc/github-copilot/policy.d/*.json` (admin). The CLI "also" reads `.claude/settings.json` hooks. (`docs/reference/hooks-reference.md` → Hooks locations)
- Events: `sessionStart`, `sessionEnd`, `userPromptSubmitted`, `userPromptTransformed`, `preToolUse`, `postToolUse`, `postToolUseFailure`, `permissionRequest`, `agentStop`, `subagentStart`, `subagentStop`, `errorOccurred`, `preCompact`, `notification`. (same file → Hook events)
- `preToolUse` output: `permissionDecision` = `allow` | `deny` | `ask`, plus `permissionDecisionReason` and `modifiedArgs`. "In Copilot CLI autopilot mode, no prompt is shown and `"ask"` is denied". (same file)
- **Fail behaviour (talk gem):**
  - Command `preToolUse` hooks are **fail-closed** on crash or non-zero exit (exit `2` = deny).
  - But "Command hook **timeouts are always fail-open, even for `preToolUse` and admin-deployed policy hooks**".
  - HTTP hooks are fail-open.
  - Default timeout: 30 s.
  - (same file + `docs/how-tos/copilot-cli/customize-copilot/use-hooks.md`)
- Who can turn them off: `disableAllHooks` in repo `settings.json` skips repo, user and plugin hooks, but "Policy hooks are not affected". Policy hooks "cannot be disabled by `disableAllHooks`", "End users cannot modify them", and on POSIX "must be owned by root". (`hooks-reference.md`)
- Hooks load at startup: "Changes to hook configurations are loaded when the CLI starts." (`use-hooks.md`)
- With the sandbox on, repo/user/plugin hooks run inside it; policy hooks "always run on the host". (`hooks-reference.md` → Sandboxed sessions)
- Walkthrough tutorial: `docs/tutorials/copilot-cli-hooks.md`.
- History: "preToolUse hooks can deny tool execution and modify arguments" 0.0.396 (2026-01-27). (changelog)

### 5. Undo / rewind
- `Esc Esc` when idle, or `/undo` (alias `/rewind`). You can rewind only the conversation or also restore files. "Rewind works in any directory, including folders that aren't Git repositories. It restores only the files that Copilot changed." (`docs/how-tos/copilot-cli/use-copilot-cli/roll-back-changes.md`)
- Caveat: "Stopping the current work does not undo changes the agent has already made." (`autopilot.md`). Rewind can't undo side effects outside files (a pushed commit, an API call).

### 6. Review before merge (CLI side)
- `/diff` to review changes. Autopilot docs: "Run the relevant tests, linters, and security checks before committing or pushing the changes." (`use-autopilot-mode.md`)
- PR commands and agentic review: `docs/how-tos/copilot-cli/use-copilot-cli/manage-pull-requests.md`, `agentic-code-review.md`.

---

## github.com layer (Copilot cloud agent and the PR gate)

Built-in guardrails on the cloud agent (`docs/concepts/security-governance-and-network-settings/risks-and-mitigations.md`):
- "Only users with write access to the repository can trigger Copilot cloud agent".
- It can push only to its own `copilot/` branch (or the PR's branch), and "is also subject to any branch protections and required checks".
- "It cannot directly run `git push` or other Git commands."
- "Copilot cloud agent cannot mark its pull requests as 'Ready for review' and cannot approve or merge a pull request."
- Actions workflows don't run on its PRs until someone with write access clicks **Approve and run workflows**.
- The person who asked for the PR can't approve it.
- The internet is restricted by a firewall (`docs/how-tos/copilot-on-github/customize-copilot/customize-the-firewall.md`).
- Prompt-injection mitigation: hidden characters and HTML comments in issues are filtered out.
- Commits are signed and co-authored, with session logs linked.

From `docs/tutorials/cloud-agent/build-guardrails.md`:
- "Copilot cloud agent is subject to rulesets just like human developers."
- **Talk gem, protecting the soft rules with a hard control:** "Protect important Copilot and MCP configuration files with a `CODEOWNERS` file, and enable the 'Require review from Code Owners' rule". Otherwise an agent (or anyone) can quietly edit the instructions that guide it.
- Keep secrets in Actions secrets: "Copilot won't be able to access these". Give the agent only what it needs via Agents secrets. (`configure-secrets-and-variables.md`)

CLI ↔ github.com bridge: `/delegate` hands a task to the cloud agent. It needs both the CLI policy and the cloud agent policy enabled. (`docs/how-tos/copilot-cli/administer-copilot-cli-for-your-enterprise.md`, `docs/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-from-cli.md`)

---

## Org / enterprise controls (Business and Enterprise)

From `docs/how-tos/copilot-cli/administer-copilot-cli-for-your-enterprise.md`:
- Policies that apply to the CLI: CLI enable/disable, model selection, enterprise custom agents, **content exclusion** ("Excluded files are not used as context"), **MCP server policies** (registry plus allowlist), cloud agent enablement (for `/delegate`), audit logging, seat assignment.
- Policies that don't apply: IDE-specific policies.
- "Disabling Copilot CLI does not disable the GitHub Copilot app."

MCP limits (`docs/concepts/copilot-surfaces/copilot-cli.md`): the CLI "can't currently support" the org policies **MCP servers in Copilot** and **MCP Registry URL**. Use managed settings `allowedMcpServers` / `deniedMcpServers` instead. "Trusted first-party servers (for example, the built-in GitHub MCP server) are always exempt". (`docs/reference/copilot-cli-reference/cli-config-dir-reference.md`)

Managed settings (`docs/reference/enterprise-administrators/enterprise-managed-settings.md`, plus the CLI notes in `cli-command-reference.md`):
- `permissions.deny` / `ask` / `allow` follow "deny > ask > allow" precedence.
  - A managed `ask` "can't be satisfied by bypass mode… an auto-approval setting, a hook or other approval shortcut, or a grant persisted from an earlier approval."
  - Selectors: `Shell(git push *)`, `Read(...)`, `Edit(...)`, `Domain(...)`.
- `permissions.disableBypassPermissionsMode`:
  - `"disable"` suppresses `--yolo`, `--allow-all*`, `/yolo` and `/allow-all`.
  - `"allow-auto-only"` blocks allow-all but permits Assisted mode.
  - Unknown values fail closed to `"disable"`.
  - Added 1.0.55 (2026-05-28).
- `sandbox`:
  - `enabled: true` means users can't use `--no-sandbox`.
  - `allowBypass: false` blocks per-command escapes and `/sandbox disable`.
  - `failIfUnavailable: true` blocks execution if the sandbox can't be enforced.
  - Also: `sandboxMcpServers`, `auth.git` / `auth.gh` (token injection), `allowDevToolAccess`.
  - Sources combine in "the **most restrictive** direction".
- "If a device has a managed policy that could not be read, the CLI fails closed and enforces sandboxing at its most restrictive level."
- Delivery: server-managed, MDM, or a file.

---

## Added from the live CLI help (1.0.104-3), details in `cli-live/README.md`
- `--assisted-approval`: "The judge is probabilistic and not a security boundary."
- Sandbox off (the default): "The agent can read, write, and delete anywhere you can… and use your credentials without restriction."
- The sandbox is built on **Microsoft Execution Containers (MXC)**.
- The sandbox inherits env vars like `AWS_ACCESS_KEY_ID` unless they're masked. Strip them with `--secret-env-vars`.
- `COPILOT_ALLOW_ALL=true` (exactly "true") also trusts the folder and loads its hooks, MCP servers and skills.
- **Permission kinds disagree:**
  - The docs list `read(.env)`.
  - The CLI help lists only `shell`, `write`, `url` and MCP.
  - `write(...)` "except shell tool invocations".
  - So a path deny rule may not stop `cat .env`. Test before the demo.

## Things still to confirm (not found or unclear in the sources)
- Does `--deny-tool='read(.env)'` exist in 1.0.104, and does it block `cat .env` via the shell? (It probably doesn't.)
- Exact on-screen wording of the approval prompt in today's build. The docs show "Yes / Yes, and approve TOOL for the rest of the running session / No…", but the CLI now also has "This location" persistence. **Check live before putting it on a slide.**
- Whether content exclusion applies to Copilot Free/Pro users. The docs say it applies "For Copilot Business and Copilot Enterprise users".
- Sandbox behaviour on the demo laptop (macOS). Run `/sandbox policy` live once to see the real output before scripting the demo.
- CLI 1.0.104-3 (prerelease) is now installed; help text was captured in `cli-live/`. Interactive behaviour hasn't been tested yet.
