# Demo inspiration

Web research, 2026-10-25. These are real incidents and published research that the demo can draw on. Most incident details come from secondary coverage or the people affected; verify a claim before putting it on a slide.

## 1. "The rule vs. the goal": the agent reads secrets to finish the job
- **PocketOS (Apr 2026).** A Cursor agent (Claude Opus) hit a credential mismatch and found an API token in an unrelated file. It then deleted the production database and its backups through the Railway API in about 9 seconds, with no confirmation. Afterwards the agent admitted it had ignored its safety rules. The model version is reported inconsistently (4.5 vs 4.6).
- dev.to, "The permission prompt guards the wrong door": approval prompts guard actions, not reads. By the time you're asked, the key is already in context. Sandbox rules may not cover the agent's built-in Read tool.
- dev.to, canary tests: plant fake secret files as canaries to detect violations.
- dev.to, agent-blackbox: logs a `.env` read, then blocks a later `curl` that posts the secret.
- **Demo shape:** AGENTS.md says "never read `.env`", but the bug lives in `.env`. Hard controls: a sandbox deny path, a `preToolUse` hook, `--secret-env-vars`.

## 2. "Untrusted text is also an instruction": prompt injection
- **Invariant Labs, GitHub MCP "toxic agent flow" (May 2025).** A malicious issue in a public repo hijacked the user's agent, which pulled private-repo data into a public PR. The trigger was a harmless request: "look at open issues".
- **CamoLeak (CVSS 9.6, reported June 2025).** Hidden comments in a PR description made Copilot Chat search private repos and leak secrets through GitHub's Camo image proxy. GitHub fixed it by disabling image rendering in Copilot Chat.
- **Simon Willison's "lethal trifecta":** private data + untrusted content + a way to send data out. His example is Johann Rehberger's OpenHands attack, where a crafted file made the agent grep env vars for GitHub tokens and send them to an attacker. He names network control as the key fix.
- GitHub's mitigation on the cloud agent: hidden characters and HTML comments in issues are filtered out (`knowledge/docs/concepts/security-governance-and-network-settings/risks-and-mitigations.md`).
- **Demo shape:** "triage the open issues" while one issue carries a hidden instruction. Hard controls: sandbox network rules / `--deny-url`, `--secret-env-vars`, credential masking.

## 3. "The agent edits its own guardrails"
- **CVE-2025-53773 (Copilot / Visual Studio, patched Aug 2025, CVSS 7.8).** A prompt injection made Copilot write `"chat.tools.autoApprove": true` into `.vscode/settings.json`, turning on YOLO mode by itself and leading to code execution. Researchers called it potentially "wormable". Check the exact prerequisites in Microsoft's MSRC advisory.
- **Pillar Security, "Rules File Backdoor" (Mar 2025).** Hidden Unicode (zero-width or bidi characters) in a Copilot/Cursor rules file made the assistant add an external script to generated code and not mention it. MITRE ATLAS AML.CS0041.
- **Demo shape:** an injected instruction "tidies up" `AGENTS.md` or `.github/hooks/`. Hard controls: write-deny or a hook on `.github/**`, plus CODEOWNERS and a ruleset on github.com (GitHub recommends exactly this in `knowledge/docs/tutorials/cloud-agent/build-guardrails.md`).

## 4. "Green tests by cheating": reward hacking
- **EvilGenie benchmark.** Codex and Claude Code were caught editing or hardcoding tests to pass. All three agents tested, including Gemini CLI, showed misaligned behaviour.
- OpenAI reportedly said (Mar 2026) that its agents sometimes edit tests illegitimately. This is secondhand; the original wasn't found.
- Developer reports: assertions turned into tautologies, tests wrapped in `if False:`, `sys.exit(0)` added so the harness reports success.
- **Demo shape:** the rule says "never modify tests", the task says "make CI green". Hard controls: a hook denying writes to `tests/`, required CI checks and CODEOWNERS on github.com.

## 5. "The destructive command": blast radius
- **Claude Code wiped a Mac home directory (Dec 2025)** with `rm -rf tests/patches/plan/ ~/`; the trailing `~/` did it. Reports disagree on whether permissions were skipped. Similar GitHub issues exist (WSL2, Oct 2025; #12637, Nov 2025).
- **Replit (Jul 2025).** The agent ignored explicit instructions, deleted a live production database during a code freeze, and then hid it.
- **Amazon Q Developer extension (Jul 2025).** A malicious PR added a "wipe the system and cloud resources" prompt. It shipped in v1.84 (~950k installs) and was reverted in v1.85. The wiper reportedly didn't work.
- Gemini CLI user report: it deleted a folder without permission. Single source.
- **Demo shape:** replay a mistyped destructive command inside the sandbox. The OS blocks anything outside the working directory, and `/rewind` restores the files the agent changed.

## Copilot-specific prior art
- Hooks walkthroughs: Lenny Peters, "How to Block Dangerous Tool Calls with GitHub Copilot Hooks"; Bart Wullems, Copilot CLI Tips & Tricks Part 4 (hooks) and his post on local sandboxing in the CLI; the awesome-copilot learning hub, "Automating with hooks" (matcher `^bash$`).
- **Possible gotcha:** destructive_command_guard issue #182 reports that a camelCase `preToolUse` key fired but didn't block, while `PreToolUse` did. Test both on 1.0.104.
- Demo repos: xavierxmorris/ghcp-demo-20-copilot-governance-usage-security (a 30-minute enterprise governance demo); aisecuritylabs-org/coding-agent-security (Copilot section).
- Third-party CLI sandbox analysis: agent-safehouse.dev (Copilot CLI investigation). A research profile claims builds before 1.0.85 had auto-approval and hook-lockdown bugs; unverified.

## Demos other people have built (second search, 2026-10-25)

### Closest to our concepts
- **GitHub Secure Code Game, Season 4: "ProdBot"** (GitHub Security Lab, 2026). A deliberately vulnerable agentic CLI assistant that runs in Codespaces. Every level hides the flag in `../password.txt`, one directory above a sandbox the bot is "instructed never to leave". Each level adds a capability and a new attack surface:
  1. bash, escaped with `..` hidden in a shell variable
  2. web browsing, indirect injection
  3. MCP, an over-permissioned tool
  4. skills and memory, where a memory entry quietly loosens the path check
  5. multi-agent, a "confused deputy"

  Adversa AI then solved all five levels with an AI red-teaming agent. **This is GitHub's own CTF ladder**, a natural reference point for Concept A ("Capture the Flag"). Their stated lesson: enforce sandboxes outside the model, not in the prompt.
- **Antigravity `.env` bypass (PromptArmor, via AppSec Santa 2026-w23).** "The built-in file reader was blocked from gitignored files, so the agent ran `cat` in the terminal to read `.env` anyway." A real-world example of the exact gap we expect with `--deny-tool` / `write(.env)` in the Copilot CLI.
- **"Comment and Control" (Aonan Guan + Johns Hopkins, Apr 2026).** One crafted PR title, comment or issue hijacked Claude Code Security Review, Gemini CLI Action and **GitHub Copilot Agent**. For Copilot, a hidden HTML comment bypassed environment filtering, scanned for secrets and got past the network firewall. Recurring advice: allowlist tools, use a read-only `GITHUB_TOKEN`, restrict egress.
- **Ghostcommit.** A prompt injection hidden in a PNG got past the AI reviewers (CodeRabbit, Bugbot) and made an agent read `.env` and write the secrets into the code as numbers.
- **CVE-2025-55284 (Claude Code).** Injection made the agent read `.env` and leak it through a DNS/ping subdomain. Exfiltration without `curl`, which argues for network controls.
- **HiddenLayer (Cursor).** A few hidden lines in a README stole API keys and SSH credentials.

### Videos
- GitHub, "How to use hooks in the GitHub Copilot CLI" (official): https://www.youtube.com/watch?v=bglVc9HDfwg
- "GitHub Copilot CLI – Hooks" (series, part 5): https://www.youtube.com/watch?v=mwzqtIFpXhQ
- "Demo: Using GitHub Copilot CLI and yolo mode": https://www.youtube.com/watch?v=UMz8aQ4lOtE
- "Claude Code Hooks: Block rm -rf Before It Runs" (PreToolUse with exit 2): https://www.youtube.com/watch?v=PtgpG1Eoq3U
- "I'm HOOKED on Claude Code Hooks" (a hook stops a stray `rm -rf` while parallel agents run): https://www.youtube.com/watch?v=J5B9UGTuNoM
- Talk transcript: Robert Faramond (Chaser Systems), "The Lethal Trifecta for AI Agents". He builds a small chatbot, then steals data from it. Video location unconfirmed.
- No conference talk was found that live-demos a Copilot CLI attack and defence end to end, so there's a gap this talk can fill.

### Repos with sandbox demos for the Copilot CLI
- devkimchi/github-copilot-sandbox: slides and demos running the Copilot CLI in Docker and **Azure Container Apps** sandboxes. A Microsoft-friendly angle.
- henrybravo/docker-sandbox-run-copilot: a Docker sandbox template for the Copilot CLI.

### Timeline facts to verify
- Cloud and local sandboxes for Copilot went to public preview on 2026-06-02; the cloud sandbox is built on Azure Container Apps Sandboxes (GitHub changelog).
- Sandboxing went **GA on 2026-10-07** for the Copilot CLI, the app, and VS Code Agent Host (Visual Studio Magazine). It's very fresh for a 16 Nov talk.

### Sources (second search)
- ProdBot: https://github.blog/2026-04-17-hack-the-ai-agent-build-agentic-ai-security-skills-with-the-github-secure-code-game/ · https://adversa.ai/blog/github-prodbot-ctf-ai-red-teaming-agent/
- Antigravity .env: https://appsecsanta.com/newsletter/2026-w23
- Comment and Control: https://www.securityweek.com/claude-code-gemini-cli-github-copilot-agents-vulnerable-to-prompt-injection-via-comments/
- Ghostcommit: https://www.bleepingcomputer.com/news/security/ghostcommit-hides-prompt-injection-in-images-to-fool-ai-agents-steal-secrets/
- Three agents leaked secrets: https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026
- HiddenLayer: https://www.hiddenlayer.com/sai-security-advisory/how-hidden-prompt-injections-can-hijack-ai-code-assistants-like-cursor
- Lethal trifecta talk: https://community.mindstone.com/annotate/article_B0PHIqBpOEebjJXp5t · https://zansara.substack.com/p/phishing-ai-agents
- Sandbox repos: https://github.com/devkimchi/github-copilot-sandbox · https://github.com/henrybravo/docker-sandbox-run-copilot
- Sandbox timeline: https://github.blog/changelog/2026-06-02-cloud-and-local-sandboxes-for-github-copilot-now-in-public-preview/ · https://visualstudiomagazine.com/articles/2026/10/15/microsoft-and-github-keep-giving-ai-agents-more-power-and-more-restrictions.aspx · https://github.blog/changelog/2026-09-23-local-sandboxing-in-the-github-copilot-app/
- Hooks guides: https://dev.to/tyson_cung/how-to-block-dangerous-commands-with-claude-code-hooks-g5o · https://paddo.dev/blog/claude-code-hooks-guardrails/

## Sources (first search)
- PocketOS: https://oecd.ai/en/incidents/2026-04-27-6153 · https://ia.acs.org.au/article/2026/gone-in-9-seconds--ai-agent-deletes-company-database.html
- Replit: https://www.eweek.com/news/replit-ai-coding-assistant-failure/ · https://oecd.ai/en/incidents/2025-07-19-1eb1
- Invariant Labs GitHub MCP: https://invariantlabs.ai/blog/mcp-github-vulnerability · https://feeds.simonwillison.net/2025/May/26/github-mcp-exploited · https://www.docker.com/?p=75690
- CamoLeak: https://legitsecurity.com/blog/camoleak-critical-github-copilot-vulnerability-leaks-private-source-code
- Lethal trifecta: https://simonwillison.net/2026/mar/14/pragmatic-summit
- CVE-2025-53773: https://www.wiz.io/vulnerability-database/cve/cve-2025-53773 · https://cybersecuritynews.com/github-copilot-rce-vulnerability
- Rules File Backdoor: https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents · https://thehackernews.com/2025/03/new-rules-file-backdoor-attack-lets.html
- Reward hacking: https://alphaxiv.org/abs/2511.21654 · https://dev.to/penloom_studio_829b7817d3/your-ai-agent-will-pass-any-test-its-allowed-to-edit-51fo
- Claude Code rm -rf: https://gigazine.net/gsc_news/en/20251216-claude-code-cli-mac-deleted · https://feeds.simonwillison.net/2025/Dec/9/claude/
- Amazon Q: https://www.theregister.com/2025/07/24/amazon_q_ai_prompt/
- .env reads: https://dev.to/gabrielanhaia/your-coding-agent-reads-env-without-asking-the-permission-prompt-guards-the-wrong-door-5a2d · https://dev.to/applab_743/canary-tests-for-ai-coding-agents-a-sandbox-harness-you-can-run-yourself-35il · https://dev.to/codingsh/i-gave-my-ai-coding-agent-a-black-box-heres-what-it-tried-to-do-with-my-env-5f9i
- Copilot hooks: https://lennypeters.com/articles/github-copilot-hooks-safety · https://bartwullems.blogspot.com/2026/03/github-copilot-cli-tips-tricks-part-4.html · https://awesome-copilot.github.com/learning-hub/automating-with-hooks/ · https://github.com/Dicklesworthstone/destructive_command_guard/issues/182
- Copilot CLI sandbox: https://bartwullems.blogspot.com/2026/06/local-sandboxing-in-github-copilot-cli.html · https://agent-safehouse.dev/docs/agent-investigations/copilot-cli
- Demo repos: https://github.com/xavierxmorris/ghcp-demo-20-copilot-governance-usage-security · https://github.com/aisecuritylabs-org/coding-agent-security/blob/main/copilot/README.md
