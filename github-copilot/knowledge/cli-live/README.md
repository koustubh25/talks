# CLI live capture: 1.0.104-3 (prerelease)

Help output captured from the **installed prerelease CLI** on 2026-10-25, one version ahead of the changelog (1.0.103).
Only `--help` / `help <topic>` were run; no prompts, so no AI credits were used.
Re-capture with `../scripts/capture-cli-help.sh` after `copilot update`.

| File | What |
|---|---|
| `version.txt` | Version string |
| `help/copilot.txt` | `copilot --help`: every flag, subcommand and example |
| `help/topic-*.txt` | `copilot help <topic>`: billing, commands (all slash commands), config, environment, limits, logging, monitoring, permissions, providers, sandbox |
| `help/cmd-*.txt` | `copilot <subcommand> --help` |

**Source priority for "what exists right now":** this folder > `../changelog-by-topic.md` > `../docs/`. Docs remain best for "how it works".

## Talk-relevant findings (quotes from the help text)

### Gems for slides
- **The assisted judge is not a boundary.** `--assisted-approval`: "The judge is probabilistic and not a security boundary." (`help/copilot.txt`). This is GitHub saying an AI reviewer of AI actions is a soft-ish control.
- **What "sandbox off" means.** "Disabled (the default): Shell commands run directly on your machine with the same access your user account has. The agent can read, write, and delete anywhere you can, reach any network your machine can, and use your credentials without restriction." (`help/topic-sandbox.txt`)
- **The sandbox is Microsoft tech, which suits this audience.** "Sandboxing is powered by Microsoft Execution Containers (MXC)… https://github.com/microsoft/mxc". The backends are macOS Seatbelt, Linux bubblewrap and Windows ProcessContainer. (`help/topic-sandbox.txt`)
- **The sandbox still sees your env vars.** "the sandbox still inherits your shell environment apart from a fixed blocklist, so other credentials already present in your environment (for example `AWS_ACCESS_KEY_ID`) remain visible unless you configure them for masking." (`help/topic-sandbox.txt`)
- **Credential masking.** Sandboxed tools "receive fake values; the proxy supplies real values only in approved HTTPS request headers." "An approved bypass skips both masking and the local proxy." (`help/topic-sandbox.txt`)
- **`--secret-env-vars`:** "Environment variable names whose values are stripped from shell and MCP server environments and redacted from output". It works without the sandbox. (`help/copilot.txt`)
- **`COPILOT_ALLOW_ALL` trap.** "Setting it to exactly "true" additionally trusts the working directory without prompting, which loads that directory's skills, plugins, MCP servers, and hooks, including hooks that run shell commands; the other truthy spellings only auto-approve tools." (`help/topic-environment.txt`)
- **Path default.** "file access is restricted to paths within the current working directory and its subdirectories, plus the system temporary directory." Turn it off with `--allow-all-paths`; tighten it with `--disallow-temp-dir`. (`help/topic-permissions.txt`)
- **Autopilot cap default:** `--max-autopilot-continues` "[default: 5]". (`help/copilot.txt`)
- **Plan → Autopilot skips you:** `--plan` "combine with --mode autopilot to auto-approve the plan and implement it autonomously". (`help/copilot.txt`)

### Permission pattern kinds: **docs and CLI help disagree** (verify live before the demo)
- CLI help (`help/topic-permissions.txt`) lists: `shell(...)`, `write(path?)`, `<mcp-server>(tool?)`, `url(...)`.
  - Of `write`, it says: "Matches tools that create and modify files, **except shell tool invocations**".
  - And: "write(.env) matches a file named ".env" in any directory".
- Docs (`../docs/reference/copilot-cli-reference/cli-command-reference.md` → Tool permission patterns) also list `read` (e.g. `read(.env)`) and `memory`.
- **Demo impact:** a `read(.env)` / `write(.env)` deny rule probably covers only the built-in file tools, so the agent might still run `cat .env` through the shell. That gap could itself be the demo ("I denied it… and it used `cat`"). The robust walls are a sandbox deny path (OS-enforced for shell) or a `preToolUse` hook that checks shell commands too. **Test all three live.**

### Slash commands worth showing (`help/topic-commands.txt`)
- **Safety:**
  - `/permissions`, `/allow-all`, `/sandbox`, `/add-dir`, `/list-dirs`, `/reset-allowed-tools`
  - `/diagnose` ("including why a permission request needed approval")
  - `/env` (shows loaded instructions, MCP servers, skills, agents, **hooks**, plugins, LSPs). Good for proving a hook is loaded on stage.
  - `/instructions` (view and toggle instruction files)
- **Review:** `/diff`, `/review`, `/security-review`, `/rubber-duck`, `/pr`
- **Undo:** `/rewind` ("Rewind the last turn and revert file changes")
- **Isolation:** `/worktree`, `/move`, `/fork worktree`
- **To github.com:** `/delegate` ("Send this session to GitHub and Copilot will create a PR")
- **Autonomy:** `/autopilot` (accepts an objective with an AI-credit limit), `/fleet`, `/plan`

### New subcommands (not in the docs snapshot)
- `copilot instruction list`: inspect which instruction sources load.
- `copilot sandbox ca …`: manage the credential-masking certificate authority.
- `copilot workflow run`: dynamic workflows.
- `--trust-folder`: trust this checkout for one prompt-mode session only.
