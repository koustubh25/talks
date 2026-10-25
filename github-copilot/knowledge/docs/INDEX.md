# Copilot CLI docs index

Official docs.github.com pages rendered to markdown (github/docs @ 02c25d1 (2026-10-23)).
Each entry: title, one-line intro, word count, and its `##` sections. Grep this file to find the right page.

## concepts/agent-capabilities/about-agents/

- **[About GitHub Copilot agents](concepts/agent-capabilities/about-agents/about-github-copilot-agents.md)** (852 words): Copilot agents use context and tools to plan and complete tasks. You can choose where and how you work with them.
  - Sections: What is an agent? · Agents, chat, and automation · Where you can work with agents · Choosing an agent experience
- **[Third-party coding agents](concepts/agent-capabilities/about-agents/about-third-party-coding-agents.md)** (971 words): You can use third-party coding agents alongside Copilot cloud agent to work asynchronously on your development tasks on GitHub.
  - Sections: Introduction · Supported coding agents · Security validation · Usage costs · Partner agents · Next steps
- **[Agent apps](concepts/agent-capabilities/about-agents/agent-apps.md)** (661 words): Agent apps let you use partner-built agents directly in your workflows on GitHub, powered by your Copilot subscription.
  - Sections: Introduction · Where you can use agent apps · How agent apps work · Installing and enabling agent apps · Billing · Next steps

## concepts/agent-capabilities/agent-powered-workflows-and-operations/

- **[About rationale, confidence, and approvals for issues](concepts/agent-capabilities/agent-powered-workflows-and-operations/about-automation-rationale-and-approvals.md)** (625 words): When automations triage issues, it explains each change, rates its confidence, and holds lower-confidence changes for your review.
  - Sections: Rationale · Confidence · Approvals · Next steps
- **[Copilot automations](concepts/agent-capabilities/agent-powered-workflows-and-operations/about-automations.md)** (1156 words): Automations let you run Copilot cloud agent automatically, on a schedule or in response to events in a repository.
  - Sections: Overview · Availability and permissions · Triggers · Tools and actions · Configuration inherited from the repository · Visibility · Billing · Security and safety · Further reading
- **[GitHub Agentic Workflows](concepts/agent-capabilities/agent-powered-workflows-and-operations/about-github-agentic-workflows.md)** (1168 words): Automate repetitive repository work with natural language instructions executed by AI coding agents in GitHub Actions.
  - Sections: About agentic workflows · Benefits of using agentic workflows · Requirements · How agentic workflows work · Supported coding agents · Security guardrails · Usage and billing · Next steps
- **[Remote control of GitHub Copilot CLI sessions](concepts/agent-capabilities/agent-powered-workflows-and-operations/about-remote-control.md)** (1050 words): Remote control lets you monitor and steer a Copilot CLI session from GitHub.com or GitHub Mobile, even after you've stepped away from your machine.
  - Sections: When remote control helps · Prerequisites · Accessing a session remotely · What you can do remotely · Reconnection · Security and privacy · Administering remote control
- **[Allowing GitHub Copilot to work autonomously](concepts/agent-capabilities/agent-powered-workflows-and-operations/autopilot.md)** (647 words): Autopilot mode lets Copilot carry a well-defined coding task through multiple steps without waiting for you after each step.
  - Sections: Overview · Benefits of Autopilot mode · Things to consider · Autonomy and permissions · Typical workflow · Further reading
- **[GitHub Copilot code review](concepts/agent-capabilities/agent-powered-workflows-and-operations/code-review.md)** (3324 words): Copilot reviews your pull requests, identifies issues, and suggests fixes you can apply in a couple of clicks.
  - Sections: Introduction · Availability · Copilot code review without a Copilot license · Agentic capabilities for Copilot code review · Code review usage and billing · Model usage · Automatic pull request reviews · Review effort level · Copilot approvals · MCP servers and agent skills for code review · Excluded files · Enhancing Copilot's knowledge of a repository · Getting detailed code quality feedback across your repository · Validating Copilot code reviews · Next steps
- **[About computer use in GitHub Copilot](concepts/agent-capabilities/agent-powered-workflows-and-operations/computer-use.md)** (758 words): Copilot can interact with desktop applications to automate tasks that cannot be completed with a more direct tool.
  - Sections: About computer use · Capabilities · Controlling access for computer use · Limitations and risks · Next steps
- **[Copilot CLI in GitHub Actions](concepts/agent-capabilities/agent-powered-workflows-and-operations/copilot-cli-in-github-actions.md)** (481 words): You can run Copilot CLI in a GitHub Actions workflow using either a personal access token or the built-in `GITHUB_TOKEN`. The two approaches differ in how AI credits are billed and what setup is required.
  - Sections: Authentication and billing options · Controlling cost · Security considerations · Next steps
- **[Dynamic workflows](concepts/agent-capabilities/agent-powered-workflows-and-operations/dynamic-workflows.md)** (2269 words): Use GitHub Copilot to orchestrate work on complex tasks, potentially combining deterministic operations, agents, tools, API calls, and user interactions.
  - Sections: About dynamic workflows · Availability of dynamic workflows · How dynamic workflows differ from autopilot and fleet · When to use a dynamic workflow · Permissions for dynamic workflows · Creating a dynamic workflow · Revising a dynamic workflow · Reusing and sharing dynamic workflows · Limiting a dynamic workflow · Watching, stopping, pausing, and resuming runs
- **[Loading tools on demand with tool search](concepts/agent-capabilities/agent-powered-workflows-and-operations/tool-search.md)** (912 words): Tool search keeps your context small by letting Copilot CLI load external tools only when a task needs them.
  - Sections: Introduction · What happens during a session · Disabling tool search · Optimizing tools for tool search

## concepts/agent-capabilities/choosing-and-delegating-agent-work/

- **[Copilot integrations](concepts/agent-capabilities/choosing-and-delegating-agent-work/about-copilot-integrations.md)** (344 words): Integrate Copilot with other tools and platforms to streamline your workflow.
  - Sections: Overview · Supported integrations · Benefits of integrations · Data usage
- **[Agent management](concepts/agent-capabilities/choosing-and-delegating-agent-work/agent-management.md)** (585 words): Use one centralized control page to jump between agent sessions, check progress, and stay in control without losing your place.
  - Sections: About agents · Managing agents · Next steps
- **[Choosing the right AI tool for your task](concepts/agent-capabilities/choosing-and-delegating-agent-work/ai-tools.md)** (1399 words): Understand GitHub's AI tools and how they can be used to help develop software.
  - Sections: Overview · Planning · Creation · Reviews · Testing · Deployment · Operation · Next steps
- **[Delegating and parallelizing work with agents](concepts/agent-capabilities/choosing-and-delegating-agent-work/delegating-and-parallelizing-work-with-agents.md)** (615 words): Break complex development work into focused tasks and coordinate multiple agents in the GitHub Copilot app or GitHub Copilot CLI.
  - Sections: How agents coordinate work · When to use multiple agents · Using the `/fleet` command to delegate and parallelize work · Considerations when using the `/fleet` command · Next steps
- **[Getting a second opinion with the rubber duck agent](concepts/agent-capabilities/choosing-and-delegating-agent-work/getting-a-second-opinion.md)** (1214 words): Use the rubber duck agent to get an independent critique of plans, code, and tests in GitHub Copilot CLI or the GitHub Copilot app.
  - Sections: Introduction · Why "rubber duck"? · Second opinion from another model · What the rubber duck agent does · Manually invoking the rubber duck agent · Auto-invoking the rubber duck agent · Benefits of using the rubber duck agent · Further reading
- **[Researching with agents](concepts/agent-capabilities/choosing-and-delegating-agent-work/researching-with-agents.md)** (571 words): Use Copilot agents to investigate complex questions across code, repositories, and the web, then produce detailed findings with citations.
  - Sections: Producing a cited research report · Researching a repository with Copilot cloud agent · When to use agent-assisted research · Getting useful research results

## concepts/copilot-surfaces/

- **[GitHub Copilot CLI](concepts/copilot-surfaces/copilot-cli.md)** (3503 words): Find out about using Copilot from the command line.
  - Sections: Introduction · Supported operating systems · Modes of use · Running Copilot CLI commands in a sandbox · Use cases for GitHub Copilot CLI · Steering the conversation · Automatic context management · Customizing GitHub Copilot CLI · Security considerations · Model usage · Use Copilot CLI via ACP · Feedback · Further reading

## concepts/customizations/

- **[Agent skills](concepts/customizations/agent-skills.md)** (295 words): Give Copilot repeatable workflows with task-specific instructions, scripts, and resources.
  - Sections: About agent skills · Where you can use agent skills · Finding and storing skills · Next steps
- **[Comparing Copilot customization features](concepts/customizations/comparing-customizations.md)** (2602 words): Choose the right way to give Copilot guidance, specialized expertise, and access to tools.
  - Sections: Introduction · Custom instructions · Agent skills · Tools · MCP servers · Hooks · Subagents · Custom agents · Extensions · Plugins · Putting it together: choosing the right option · Next steps
- **[Custom agents](concepts/customizations/custom-agents.md)** (572 words): Give Copilot reusable specialist roles with tailored instructions and tools.
  - Sections: About agent profiles · Where you can use custom agents · Built-in agents · Custom agents and subagents · Next steps
- **[Extensions for GitHub Copilot](concepts/customizations/extensions.md)** (483 words): Extend Copilot with capabilities implemented in code.
  - Sections: Where you can use extensions · Choosing an extension scope · Extensions in Copilot CLI · Choosing between extensions and other customizations · Next steps
- **[Hooks for GitHub Copilot](concepts/customizations/hooks.md)** (1047 words): Run your own checks, logging, or other commands at defined points while a Copilot agent works.
  - Sections: What are hooks? · Where you can use hooks · Types of hooks · Hook configuration format · Example hook configuration file · Performance considerations · Security considerations · Next steps
- **[Using LSP servers with GitHub Copilot CLI](concepts/customizations/lsp-servers.md)** (703 words): LSP servers give Copilot CLI precise code intelligence, enabling it to navigate definitions, find references, and rename symbols accurately across your project.
  - Sections: Introduction · Benefits of LSP servers · What LSP servers allow Copilot CLI to do · How to add an LSP server · How LSP servers are loaded · Next steps · Further reading
- **[Model Context Protocol (MCP)](concepts/customizations/mcp.md)** (1609 words): Connect Copilot to external tools and data through Model Context Protocol (MCP) servers.
  - Sections: Overview of Model Context Protocol (MCP) · Where you can use MCP · MCP for Copilot cloud agent · Best practices · About the GitHub MCP server · About the GitHub MCP Registry · Agent finder · Next steps
- **[Plugins for GitHub Copilot](concepts/customizations/plugins.md)** (1232 words): Plugins are installable packages that extend Copilot with reusable agents, skills, hooks, and integrations.
  - Sections: Where you can use plugins · What plugins contain · Plugin formats · How plugins are structured · Why use plugins? · Where can I get plugins? · How plugin marketplaces work · Plugins compared with manual configuration · Further reading

## concepts/enterprise/

- **[Managing access to GitHub Copilot cloud agent](concepts/enterprise/cloud-agent-access.md)** (494 words): Find out about Copilot cloud agent policies available for GitHub Copilot Enterprise and GitHub Copilot Business, and about disabling the agent for specific repositories.
  - Sections: Overview · Copilot cloud agent policies for Copilot Business and Copilot Enterprise · Opting repositories out of Copilot cloud agent · Managing access to Automations · Further reading
- **[MCP server usage in your company](concepts/enterprise/mcp-management.md)** (342 words): You can manage MCP server usage to provide your developers with valuable tools while maintaining security and compliance.
  - Sections: MCP allowlists · Next steps · Further reading
- **[About enterprise-managed plugin standards](concepts/enterprise/plugin-standards.md)** (271 words): Enterprise administrators can centrally define plugin policies for users, ensuring consistent plugin availability.
  - Sections: Where plugin standards apply · How plugin standards work · Why use enterprise-managed plugin standards · Next step
- **[GitHub Copilot policies for enterprises and organizations](concepts/enterprise/policies.md)** (621 words): Control the availability of GitHub Copilot features and models for your users.
  - Sections: How do policies work? · Who do policies apply to? · What about users with multiple licenses? · What is the default status of policies? · Where do policies apply? · How can I prevent policy drift? · Setting policies

## concepts/security-governance-and-network-settings/

- **[About cloud and local sandboxes for GitHub Copilot](concepts/security-governance-and-network-settings/about-cloud-and-local-sandboxes.md)** (2472 words): Cloud and local sandboxes provide isolated execution environments that let Copilot safely interact with code, tools, filesystem, and network resources securely on your local machine or in fully isolated cloud environments.
  - Sections: Introduction · Local sandboxing · Cloud sandboxing · Authentication and access · Billing · Further reading
- **[Content exclusion for GitHub Copilot](concepts/security-governance-and-network-settings/content-exclusion.md)** (469 words): You can prevent Copilot from accessing certain files.
  - Sections: About content exclusion for Copilot · Further reading
- **[Network settings for GitHub Copilot](concepts/security-governance-and-network-settings/network-settings.md)** (654 words): You can connect to GitHub Copilot through an HTTP proxy and use custom certificates.
  - Sections: Proxy settings for Copilot · Custom certificates · Next steps
- **[Risks and mitigations for GitHub Copilot cloud agent](concepts/security-governance-and-network-settings/risks-and-mitigations.md)** (1086 words): How do Copilot cloud agent's built-in security protections mitigate known risks?
  - Sections: Unvalidated code can introduce vulnerabilities · Copilot cloud agent can push code changes to your repository · Copilot cloud agent has access to sensitive information · AI prompts can be vulnerable to injection · Administrators can lose sight of agents' work · Automations run without a person initiating each task
- **[About GitHub Copilot session data](concepts/security-governance-and-network-settings/session-data.md)** (994 words): Understand what session data is, where it is stored, who can access it, and how it is managed.
  - Sections: Understanding session location and access · Session syncing · Privacy and sharing · Access and retention of session data · Session management for Copilot CLI · Further reading
- **[Understanding filesystem policies for local sandboxing in GitHub Copilot CLI](concepts/security-governance-and-network-settings/understanding-local-sandboxing.md)** (2195 words): When local sandboxing is enabled, Copilot CLI runs each sandboxed process or operation under a filesystem policy that controls which files and directories it can read and write. Learn how that policy is built and how to check the access it grants.
  - Sections: Introduction · What the policy applies to · Permission levels · How the policy is built · When access rules overlap · Checking what the current policy allows · Troubleshooting filesystem access · Customizing the policy · Enterprise-managed policies · Further reading

## copilot-on-ghes/

- **[Set up GitHub Copilot CLI for GitHub Enterprise Server](copilot-on-ghes/set-up-copilot-cli.md)** (1139 words): Configure a model provider for your GitHub Enterprise Server instance, then connect Copilot CLI clients to the instance.
  - Sections: Prerequisites · Configuring your GitHub Enterprise Server instance · Configuring your Copilot CLI client (end user) · Understanding client (end user) tokens · Recommended end user setup · Examples · Supported capabilities on GitHub Enterprise Server

## get-started/

- **[Getting started with GitHub Copilot CLI](get-started/cli-quickstart.md)** (504 words): Quickly learn how to use GitHub Copilot CLI.
  - Sections: Introduction · Installation · Starting the CLI for the first time · Core shortcuts to master · Using GitHub Copilot CLI non-interactively · Next steps
- **[Adopting GitHub Copilot in your enterprise](get-started/enterprise-ai-governance.md)** (28 words): Adopt the latest GitHub Copilot features without compromising on control and governance.

## how-tos/administer-copilot/manage-for-enterprise/

- **[Managing policies and features for GitHub Copilot in your enterprise](how-tos/administer-copilot/manage-for-enterprise/manage-enterprise-policies.md)** (423 words): Control the availability of features for GitHub Copilot in your enterprise using policies.
  - Sections: Defining policies for your enterprise · Opting in to feedback collection · Further reading

## how-tos/administer-copilot/manage-for-enterprise/manage-agents/

- **[Enabling GitHub Copilot cloud agent in your enterprise](how-tos/administer-copilot/manage-for-enterprise/manage-agents/enable-copilot-cloud-agent.md)** (368 words): Choose which organizations can use Copilot cloud agent and connect it to MCP servers.
  - Sections: Prerequisites · Enabling Copilot cloud agent · Enabling MCP servers · Enabling agent apps and third-party agents

## how-tos/administer-copilot/manage-for-organization/

- **[Adding GitHub Copilot cloud agent to your organization](how-tos/administer-copilot/manage-for-organization/add-copilot-cloud-agent.md)** (644 words): Enable Copilot cloud agent for your members and control the repositories where it is available.
  - Sections: Enabling Copilot cloud agent for your members · Disabling or enabling Copilot cloud agent in your repositories · Controlling automations in your repositories · Managing the agent firewall for your organization · Next steps
- **[Managing policies and features for GitHub Copilot in your organization](how-tos/administer-copilot/manage-for-organization/manage-policies.md)** (614 words): Control the availability of GitHub Copilot features and models for users granted a license by your organization.
  - Sections: Enabling Copilot features and models in your organization · Enabling or disabling third-party coding agents in your repositories · Opting in to previews or feedback · Further reading

## how-tos/administer-copilot/manage-mcp-usage/

- **[Configure an MCP registry for your organization or enterprise](how-tos/administer-copilot/manage-mcp-usage/configure-mcp-registry.md)** (641 words): Create and host a list of MCP servers that your developers can access.
  - Sections: Prerequisites · Option 1: Self-hosting an MCP registry · Option 2: Using Azure API Center as an MCP registry · Next steps

## how-tos/cloud-and-local-sandboxes/

- **[Configuring local sandbox settings](how-tos/cloud-and-local-sandboxes/configuring-local-sandbox-settings.md)** (4187 words): Configure local sandboxing in the GitHub Copilot app or Copilot CLI to restrict filesystem access, network connectivity, and credential use.
  - Sections: About local sandbox configuration · Prerequisites · Configuring the Copilot app · Configuring Copilot CLI · Further reading
- **[Enabling or disabling cloud sandboxes for your organization or enterprise](how-tos/cloud-and-local-sandboxes/enabling-or-disabling-cloud-sandboxes-for-your-organization.md)** (414 words): You can control whether members of your organization or enterprise can use cloud sandboxes by managing the cloud sandbox access policy in your organization or enterprise settings.
  - Sections: About enabling and disabling cloud sandboxes · Enabling or disabling cloud sandboxes for your organization · Enabling or disabling cloud sandboxes for your enterprise · Further reading
- **[Using local sandboxing](how-tos/cloud-and-local-sandboxes/using-local-sandboxing.md)** (2599 words): Enable local sandboxing to restrict what Copilot can access on your machine in Copilot CLI or VS Code.
  - Sections: Introduction · Prerequisites · Using local sandboxing in Copilot CLI · Using local sandboxing in the Copilot app · Further reading

## how-tos/configure-content-exclusion/

- **[Excluding content from GitHub Copilot](how-tos/configure-content-exclusion/exclude-content-from-copilot.md)** (1447 words): Learn how to prevent Copilot from accessing certain content.
  - Sections: Configuring content exclusion for your repository · Configuring content exclusion for your organization · Configuring content exclusion for your enterprise · Testing changes to content exclusions · Manage content exclusions with the REST API · Further reading

## how-tos/copilot-cli/

- **[Administering Copilot CLI for your enterprise](how-tos/copilot-cli/administer-copilot-cli-for-your-enterprise.md)** (632 words): Control the use of Copilot CLI within your enterprise.
  - Sections: Enabling or disabling Copilot CLI · How do other AI controls affect Copilot CLI? · Why can't my developers access Copilot CLI? · Further reading
- **[Best practices for GitHub Copilot CLI](how-tos/copilot-cli/cli-best-practices.md)** (2513 words): Learn how to get the most out of GitHub Copilot CLI.
  - Sections: Introduction · 1. Customize your environment · Build Commands · Code Style · Workflow · 2. Plan before you code · Overview · Tasks · Detailed Steps · 3. Leverage infinite sessions · 4. Delegate work effectively · 5. Common workflows · 6. Advanced patterns · 7. Team guidelines · Getting help · Hands-on practice · Further reading
- **[Using Copilot CLI in GitHub Actions with GITHUB_TOKEN](how-tos/copilot-cli/use-copilot-cli-in-actions.md)** (448 words): Run Copilot CLI in a GitHub Actions workflow using the built-in `GITHUB_TOKEN`, without a personal access token.
  - Sections: Enabling the policy · Recommended approach: GitHub Agentic Workflows · Using Copilot CLI directly in a workflow

## how-tos/copilot-cli/automate-copilot-cli/

- **[Automating tasks with Copilot CLI and GitHub Actions](how-tos/copilot-cli/automate-copilot-cli/automate-with-actions.md)** (1201 words): Integrate GitHub Copilot CLI into your GitHub Actions workflows.
  - Sections: Recommended approach: GitHub Agentic Workflows · Using Copilot CLI in an Actions workflow · Trigger · Setup · Install · Authenticate · Run Copilot CLI · Next steps · Further reading
- **[Quickstart for automating with GitHub Copilot CLI](how-tos/copilot-cli/automate-copilot-cli/quickstart.md)** (408 words): Build an automation with Copilot CLI in minutes.
  - Sections: Overview · Run a prompt from the command line · Use Copilot CLI in a script · Further reading
- **[Running GitHub Copilot CLI programmatically](how-tos/copilot-cli/automate-copilot-cli/run-cli-programmatically.md)** (777 words): Use Copilot CLI in the terminal, in scripts, or in Actions workflows.
  - Sections: Introduction · Tips for using Copilot CLI programmatically · CI/CD integration · Examples of programmatic usage · Shell scripting patterns · Further reading
- **[Scheduling prompts in GitHub Copilot CLI](how-tos/copilot-cli/automate-copilot-cli/schedule-prompts.md)** (1241 words): Use the `/every` and `/after` slash commands to submit a prompt to Copilot on a recurring schedule, or after a specified delay.
  - Sections: Scheduling a recurring prompt with `/every` · Scheduling a once-only prompt with `/after` · Scheduling a skill · Interval and delay syntax · Identifying scheduled prompts in the session · Managing scheduled prompts · What happens when you close and reopen a session · Running a prompt from an external scheduler · Further reading

## how-tos/copilot-cli/customize-copilot/

- **[Adding custom instructions for GitHub Copilot CLI](how-tos/copilot-cli/customize-copilot/add-custom-instructions.md)** (992 words): Give Copilot additional context on how to understand your project and how to build, test and validate its changes.
  - Sections: Types of custom instructions · How multiple instruction files interact · Creating repository-wide custom instructions · Creating path-specific custom instructions · Custom instructions in use · Further reading
- **[Adding MCP servers for GitHub Copilot CLI](how-tos/copilot-cli/customize-copilot/add-mcp-servers.md)** (1830 words): Extend Copilot's capabilities by connecting Model Context Protocol (MCP) servers to provide additional tools and context.
  - Sections: Adding an MCP server · Using agent finder · Managing MCP servers · Using MCP servers · Further reading
- **[Adding agent skills for GitHub Copilot CLI](how-tos/copilot-cli/customize-copilot/add-skills.md)** (1449 words): Modify Copilot's behavior and abilities when it works on particular tasks.
  - Sections: Creating and adding a skill · Adding a skill that someone else has created · Using agent skills · Skills versus custom instructions
- **[Changing settings with the `/settings` command](how-tos/copilot-cli/customize-copilot/change-settings.md)** (1061 words): View and change your personal settings for GitHub Copilot CLI with the `/settings` slash command.
  - Sections: Opening the settings editor · Changing a single setting inline · Viewing valid values for a setting · Viewing the current value of a setting · Changing settings that require a restart · Settings you can't change from the command line · Commands replaced by `/settings` · Settings you might want to change · Further reading
- **[Creating and using custom agents for GitHub Copilot CLI](how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli.md)** (1183 words): Create specialized agents with tailored expertise for specific development tasks.
  - Sections: Introduction · Creating a custom agent · Using a custom agent · Applying your repository's custom instructions to a custom agent · Further reading
- **[Overview of customizing GitHub Copilot CLI](how-tos/copilot-cli/customize-copilot/overview.md)** (596 words): Copilot CLI works best when customized for your specific project and workflow.
  - Sections: Custom instructions · Hooks · Skills · Custom agents · MCP servers · Plugins · Personal CLI settings
- **[Creating a plugin for GitHub Copilot CLI](how-tos/copilot-cli/customize-copilot/plugins-creating.md)** (961 words): Create a plugin to share customizations in an easy-to-install package.
  - Sections: Introduction · Plugin structure · Creating a plugin · Distributing your plugin · Further reading
- **[Finding and installing plugins for GitHub Copilot CLI](how-tos/copilot-cli/customize-copilot/plugins-finding-installing.md)** (632 words): Extend Copilot's functionality by installing plugins created by the community or by your team.
  - Sections: Introduction · Finding plugins · Installing plugins · Managing installed plugins · Adding plugin marketplaces · Removing plugin marketplaces · Further reading
- **[Creating a plugin marketplace for GitHub Copilot CLI](how-tos/copilot-cli/customize-copilot/plugins-marketplace.md)** (480 words): You can make CLI plugins that you've created easy to install by adding them to a marketplace.
  - Sections: Introduction · Prerequisite · Creating a plugin marketplace · Further reading
- **[Adding LLM models to GitHub Copilot CLI](how-tos/copilot-cli/customize-copilot/use-byok-models.md)** (877 words): Use a model from an external provider of your choice in Copilot by supplying your own API key.
  - Sections: Prerequisites · Supported providers · Model requirements · Configuring your provider · Connecting to an OpenAI-compatible endpoint · Connecting to Azure OpenAI · Connecting to Anthropic · Running in offline mode
- **[Using hooks with GitHub Copilot CLI](how-tos/copilot-cli/customize-copilot/use-hooks.md)** (1026 words): Extend GitHub Copilot agent behavior with custom shell commands at key points during agent execution.
  - Sections: Prerequisite · Creating a repository-level hook · Creating a user-level hook · Troubleshooting · Debugging · Further reading

## how-tos/copilot-cli/set-up-copilot-cli/

- **[Adding LSP servers for GitHub Copilot CLI](how-tos/copilot-cli/set-up-copilot-cli/add-lsp-servers.md)** (1416 words): You can add LSP servers to give Copilot CLI precise code intelligence, improving its ability to navigate definitions, find references, and rename symbols.
  - Sections: Introduction · Installing and configuring an LSP server · Using the `lsp-setup` skill to add a language server · Manually installing and configuring an LSP server · Configuring the language server · Managing language servers with the `/lsp` command · Further reading
- **[Authenticating GitHub Copilot CLI](how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli.md)** (1856 words): Authenticate Copilot CLI so that you can use Copilot directly from the command line.
  - Sections: About authentication · Unauthenticated use · Authenticating with OAuth · Authenticating with environment variables · Authenticating with GitHub CLI · Switching between accounts · Signing out and removing credentials · Next steps
- **[Configuring GitHub Copilot CLI](how-tos/copilot-cli/set-up-copilot-cli/configure-copilot-cli.md)** (1762 words): Configure trusted directories, tool access, path and URL permissions, and client-side telemetry for Copilot CLI.
  - Sections: Introduction · Setting trusted directories · Setting allowed tools · Setting path permissions · Setting URL permissions · Allowing all tools, paths, and URLs · Restrict access to files · Disabling client-side telemetry · Further reading
- **[Installing GitHub Copilot CLI](how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli.md)** (577 words): Learn how to install Copilot CLI so that you can use Copilot directly from the command line.
  - Sections: Prerequisites · Installing or updating Copilot CLI · Authenticating with Copilot CLI · Next steps
- **[Troubleshooting GitHub Copilot CLI authentication](how-tos/copilot-cli/set-up-copilot-cli/troubleshoot-copilot-cli-auth.md)** (1186 words): Diagnose authentication failures when signing in to Copilot CLI.
  - Sections: Authentication errors · No authentication information found · Token expired or revoked · Token (classic) rejected · Access denied · Keychain access failure · Wrong account

## how-tos/copilot-cli/use-copilot-cli/

- **[Requesting a code review with GitHub Copilot CLI](how-tos/copilot-cli/use-copilot-cli/agentic-code-review.md)** (163 words): Use Copilot CLI to review your code changes directly from the terminal.
  - Sections: About agentic code review · Further reading
- **[Allowing and denying tool use](how-tos/copilot-cli/use-copilot-cli/allowing-tools.md)** (1255 words): Control which tools Copilot CLI can use to avoid unintended changes.
  - Sections: Introduction · Persisted permissions · Layers of tool controls · Restricting the choice of tools available to the AI model · Allowing or denying permission for specific tools · Permissive options · Resetting permissions · Further reading
- **[Asking a side question in GitHub Copilot CLI](how-tos/copilot-cli/use-copilot-cli/ask-a-side-question.md)** (299 words): During a CLI session, you can ask Copilot a question without adding the prompt, or the answer, to your conversation history.
  - Sections: Asking a quick question · Further reading
- **[Browsing issues, pull requests, and gists from GitHub Copilot CLI](how-tos/copilot-cli/use-copilot-cli/browse-issues-prs-gists.md)** (1397 words): Use the tabs in an interactive Copilot CLI session to browse issues, pull requests and gists, without leaving the terminal.
  - Sections: Switching between tabs · Common keyboard controls · Browsing issues · Browsing pull requests · Searching issues and pull requests · Browsing your gists · Modifying issues, pull requests, and gists · Customizing the tabs · Keyboard reference · Further reading
- **[Using GitHub Copilot CLI session data](how-tos/copilot-cli/use-copilot-cli/chronicle.md)** (2558 words): Resume previous Copilot CLI sessions, use the `/chronicle` slash command to get insights from your session history, and ask Copilot questions about your CLI usage.
  - Sections: Resuming a previous session · Renaming a session · Sharing a session · Using the `/chronicle` slash command · Asking questions about your session history · Deleting sessions · Reindexing the session store · Further reading
- **[Using GitHub Copilot CLI to interact with desktop applications](how-tos/copilot-cli/use-copilot-cli/computer-use.md)** (508 words): With computer use, allow Copilot to interact with local desktop applications from GitHub Copilot CLI.
  - Sections: About computer use · Checking computer use status · Enabling computer use · Using computer use · Disabling computer use · Troubleshooting computer use
- **[Connecting GitHub Copilot CLI to VS Code](how-tos/copilot-cli/use-copilot-cli/connecting-vs-code.md)** (1149 words): Connect Copilot CLI to VS Code to share context, trust settings, and output.
  - Sections: Connecting to VS Code · Managing the connection with the `/ide` slash command · Using VS Code context in prompts · Reviewing file changes as diffs · Viewing and resuming CLI sessions in VS Code · Further reading
- **[Delegating tasks to Copilot](how-tos/copilot-cli/use-copilot-cli/delegate-tasks-to-cca.md)** (402 words): Use autopilot mode, or the `/delegate` slash command, to get Copilot to work autonomously on your behalf.
  - Sections: Get autopilot to complete tasks autonomously on your local machine · Delegate tasks to Copilot cloud agent · Next steps
- **[Invoking custom agents](how-tos/copilot-cli/use-copilot-cli/invoke-custom-agents.md)** (682 words): Use custom agents, skills, and MCP servers in Copilot CLI to extend its capabilities.
  - Sections: Use custom agents · Use skills · Add an MCP server · Next steps
- **[Managing pull requests with the /pr command](how-tos/copilot-cli/use-copilot-cli/manage-pull-requests.md)** (1278 words): Use the `/pr` slash command to view, create, and fix pull requests directly from Copilot CLI.
  - Sections: Overview · Prerequisite · Subcommands · Viewing pull request status · Creating a pull request · Fixing review feedback · Resolving merge conflicts · Fixing CI failures · Fixing all issues at once · Automating the full pull request workflow · Further reading
- **[Using GitHub Copilot CLI](how-tos/copilot-cli/use-copilot-cli/overview.md)** (2786 words): Learn how to use GitHub Copilot from the command line.
  - Sections: Prerequisite · Using Copilot CLI · Tips · Find out more · Feedback · Next steps · Further reading
- **[Researching with GitHub Copilot CLI](how-tos/copilot-cli/use-copilot-cli/research-with-copilot-cli.md)** (889 words): Use the `/research` slash command to investigate a complex topic and produce a cited report from your codebase, repositories on GitHub, and web sources.
  - Sections: About research in Copilot CLI · Running a research investigation · Writing an effective research prompt · Viewing and sharing a research report · Considerations
- **[Canceling operations and rolling back changes in GitHub Copilot CLI](how-tos/copilot-cli/use-copilot-cli/roll-back-changes.md)** (1288 words): Stop an active Copilot CLI operation, or rewind a session to undo changes in conversation history and optionally restore files.
  - Sections: Introduction · Canceling an operation · Rolling back with a double Esc keypress · Rolling back with the `/undo` slash command · What happens when you roll back · Changes that can't be restored · Verifying the rollback · Further reading
- **[Setting an AI credit session limit in GitHub Copilot CLI](how-tos/copilot-cli/use-copilot-cli/set-session-limit.md)** (416 words): Limit the amount of AI credits Copilot can spend on a session to control costs and keep tasks predictable.
  - Sections: Setting an AI credit session limit · What happens when the limit is reached · Further reading
- **[Speeding up task completion with the `/fleet` command](how-tos/copilot-cli/use-copilot-cli/speed-up-task-completion.md)** (721 words): Learn how you can speed up the completion of a multi-step implementation plan by using the `/fleet` slash command.
  - Sections: Using the `/fleet` slash command · Starting in fleet mode from the command line · Further reading
- **[Steering agents in GitHub Copilot CLI](how-tos/copilot-cli/use-copilot-cli/steer-agents.md)** (195 words): Guide Copilot during task execution to keep work on track with your intent.
  - Sections: Steer the conversation while Copilot is thinking · Queue a prompt to be processed next · Next steps
- **[Steering a GitHub Copilot CLI session from another device](how-tos/copilot-cli/use-copilot-cli/steer-remotely.md)** (1367 words): Enable remote control for a Copilot CLI session so you can monitor progress, respond to prompts, and continue working from GitHub.com or GitHub Mobile.
  - Sections: Prerequisites · Enabling remote control for a session · Accessing a session from GitHub.com · Accessing a session from GitHub Mobile · Preventing your machine from going to sleep · Reviewing previous sessions · Resuming a session · Preventing remote control · Further reading
- **[Using Autopilot mode in GitHub Copilot CLI](how-tos/copilot-cli/use-copilot-cli/use-autopilot-mode.md)** (1140 words): Give Copilot CLI a well-defined task and let it work through the implementation, testing, and iteration without waiting for input after each step.
  - Sections: Starting or switching to Autopilot mode · Moving from a plan to Autopilot mode · Configuring permissions · Comparing Autopilot mode, `--allow-all`, and `--no-ask-user` · Limiting autonomous work · Stopping and reviewing work · Choosing the mode for the next task · Running Autopilot mode programmatically
- **[Use voice input with Copilot CLI](how-tos/copilot-cli/use-copilot-cli/voice-input.md)** (735 words): Speak your prompts to GitHub Copilot CLI instead of typing them, using the CLI's speech-to-text feature.
  - Sections: Prerequisites · Limitation · Enabling voice input · Using voice input · Switching microphones · Switching voice models · Further reading
- **[Working with multiple GitHub Copilot CLI sessions](how-tos/copilot-cli/use-copilot-cli/work-with-multiple-sessions.md)** (2243 words): Run several Copilot CLI sessions at once and use the sidebar to quickly move between them.
  - Sections: Introduction · The sessions sidebar · The Sessions tab · Choosing between the sidebar and the Sessions tab · Returning to a previous session · Active and inactive sessions · Session slash commands · Customizing the sidebar

## how-tos/copilot-on-github/customize-copilot/

- **[Customizing or disabling the firewall for GitHub Copilot](how-tos/copilot-on-github/customize-copilot/customize-the-firewall.md)** (1297 words): Learn how to control the domains and URLs that Copilot cloud agent and Copilot code review can access.
  - Sections: Overview · Limitations · Understanding the recommended firewall allowlist · Configuring the firewall at the organization level · Configuring the firewall at the repository level · Further reading

## how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/

- **[Configure secrets and variables for Copilot cloud agent](how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/configure-secrets-and-variables.md)** (846 words): Securely pass secrets and variables to Copilot cloud agent so it can access private resources and configure MCP servers.
  - Sections: About secrets and variables for Copilot cloud agent · Configuring repository-level secrets and variables · Configuring organization-level secrets and variables · Using secrets and variables · Naming requirements for secrets and variables · Further reading
- **[Creating custom agents for Copilot cloud agent](how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents.md)** (1126 words): You can create specialized agents with tailored expertise for specific development tasks.
  - Sections: Creating a custom agent profile in a repository on GitHub · Configuring an agent profile · Example agent profiles · Using custom agents · Next steps
- **[Configure the development environment](how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment.md)** (1946 words): Pre-install tools and dependencies so Copilot cloud agent can build, test, and validate changes reliably.
  - Sections: About customizing Copilot cloud agent's development environment · Customizing Copilot's development environment with Copilot setup steps · Preinstalling tools or dependencies in Copilot's environment · Upgrading to larger GitHub-hosted GitHub Actions runners · Using self-hosted GitHub Actions runners · Switching Copilot to a Windows development environment · Enabling Git Large File Storage (LFS) · Further reading
- **[Customize agent workflows with hooks](how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks.md)** (601 words): Run automated checks—like linting, formatting, or security scans—at key points during agent execution to enforce quality standards.
  - Sections: Creating a hook in a repository on GitHub · Troubleshooting · Debugging · Further reading

## how-tos/copilot-on-github/set-up-copilot/

- **[Configuring code review by GitHub Copilot](how-tos/copilot-on-github/set-up-copilot/configure-code-review.md)** (2102 words): Set up Copilot to review pull requests.
  - Sections: Introduction · Configuring automatic code review for your own pull requests · Configuring your Copilot review effort · Configuring automatic code review for a repository · Configuring automatic code review for repositories in an organization · Configuring automatic code review for an enterprise

## how-tos/copilot-on-github/use-copilot-agents/

- **[Using GitHub Copilot code review on GitHub](how-tos/copilot-on-github/use-copilot-agents/copilot-code-review.md)** (1135 words): GitHub Copilot reviews your pull requests and suggests ready-to-apply changes, so you get fast, actionable feedback on every commit.
  - Sections: Request a review from Copilot · Work with suggested changes · Provide feedback on reviews · Request a re-review · Enable automatic reviews · Customize reviews with custom instructions · MCP servers and agent skills · Further reading
- **[Kick off a task with Copilot agents on GitHub](how-tos/copilot-on-github/use-copilot-agents/kick-off-a-task.md)** (813 words): Decide whether Copilot cloud agent creates a pull request immediately or works on a branch you review and iterate on first.
  - Sections: Assign an issue to Copilot · Start a task with a prompt · Seed a new repository · Further reading
- **[Managing agent sessions](how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents.md)** (902 words): Monitor an agent's progress in real time, steer it with follow-up prompts, and stop or archive sessions.
  - Sections: Monitor agent activity · Review session logs · Trace commits to session logs · Steer an agent session · Stop a session · Archive sessions · Share a session · Query past sessions · Continue a session's work in GitHub Copilot Chat · Further reading
- **[Review output from Copilot](how-tos/copilot-on-github/use-copilot-agents/review-copilot-output.md)** (313 words): Copilot pull requests deserve the same thorough review as any contribution.
  - Sections: Review Copilot's changes · Manage GitHub Actions workflow runs · Give feedback on Copilot's work · Further reading

## how-tos/use-copilot-agents/

- **[Using GitHub Copilot code review](how-tos/use-copilot-agents/use-code-review.md)** (3568 words): Learn how to request a code review from GitHub Copilot.
  - Sections: Introduction · Using Copilot code review · Enabling automatic reviews · Requesting a re-review from Copilot · Choosing a review effort level · Pull request approvals from Copilot · Customizing Copilot's reviews with custom instructions · MCP servers and agent skills · Customizing Copilot code review's environment · Providing feedback on Copilot's reviews · Working with suggested changes provided by Copilot · Providing feedback on Copilot's reviews · Customizing Copilot's reviews with custom instructions · Prerequisite · Using Copilot code review · Using Copilot code review · Prerequisite · Using Copilot code review · Prerequisites · Using Copilot code review · Prerequisites · Using Copilot code review
- **[Using dynamic workflows](how-tos/use-copilot-agents/use-dynamic-workflows.md)** (2044 words): Find, run, monitor, and resume dynamic workflows in GitHub Copilot CLI and the GitHub Copilot app.
  - Sections: Prerequisite · Finding out about available dynamic workflows · Running a dynamic workflow · Running a dynamic workflow from the command line · Creating a dynamic workflow · Reusing and sharing dynamic workflows · Monitoring and managing dynamic workflow runs · Scheduling a dynamic workflow run

## how-tos/use-copilot-agents/cloud-agent/

- **[Configuring settings for GitHub Copilot cloud agent](how-tos/use-copilot-agents/cloud-agent/configuring-agent-settings.md)** (473 words): Learn how to configure settings for Copilot cloud agent
  - Sections: Enabling or disabling built-in code quality and security validation tools · Allowing GitHub Actions workflows to run automatically when Copilot pushes
- **[Creating automations with Copilot cloud agent](how-tos/use-copilot-agents/cloud-agent/create-automations.md)** (759 words): Create and manage automations to run Copilot cloud agent on a schedule or in response to events.
  - Sections: Introduction · Prerequisites · Creating an automation · Testing an automation · Managing your Automations · Further reading
- **[Managing rationale, confidence, and approvals for issues](how-tos/use-copilot-agents/cloud-agent/manage-rationale-confidence-approvals.md)** (1022 words): Set up and manage rationale, confidence, and approvals for issues handled by automation.
  - Sections: Setting your repository's automation level · With Copilot cloud agent · With GitHub Agentic Workflows · With the REST or GraphQL API · Finding issues with pending suggestions · Reviewing suggestions in the approvals panel
- **[Starting GitHub Copilot sessions](how-tos/use-copilot-agents/cloud-agent/start-copilot-sessions.md)** (170 words): Choose your preferred way to start Copilot cloud agent sessions.
- **[Using Copilot cloud agent from the GitHub CLI](how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-from-cli.md)** (286 words): Start and track Copilot cloud agent sessions from the GitHub CLI.
  - Sections: Starting a session · Tracking your sessions · Further reading
- **[Using Copilot cloud agent on GitHub](how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github.md)** (2615 words): Start Copilot cloud agent sessions directly on GitHub, then iterate on the results without leaving your browser.
  - Sections: Introduction · Starting a session from the agents tab or panel · Starting a session from the dashboard · Starting from Copilot Chat · Assigning an issue to Copilot · Seeding a new repository · Fixing a failing GitHub Actions workflow run · Continuing work on a pull request · Resolving merge conflicts · Running Copilot cloud agent automatically with automations · Managing GitHub Actions workflow runs · Giving feedback on Copilot's work · Further reading
- **[Using Copilot cloud agent via the GitHub MCP Server](how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-with-mcp.md)** (219 words): Start Copilot cloud agent sessions from any IDE or agentic tool that supports Model Context Protocol (MCP).
  - Sections: Starting a session · Further reading

## reference/

- **[Custom agents configuration](reference/custom-agents-configuration.md)** (1977 words): Reference for configuring custom agents.
  - Sections: YAML frontmatter properties · Tools · MCP server configuration details · Example agent profile configurations · Processing of custom agents · Further reading
- **[GitHub Copilot hooks reference](reference/hooks-reference.md)** (7011 words): Find hook events, configuration formats, and input payloads for hooks in Copilot CLI and Copilot cloud agent.
  - Sections: Introduction · Hooks locations · Cloud agent execution environment · Hook configuration format · Hook events · Hook event input payloads · `preToolUse` decision control · `agentStop` / `subagentStop` decision control · `postToolUse` output · `permissionRequest` decision control · `notification` hook · Matcher filtering · Tool names for hook matching · Exit codes for command hooks · Disable all hooks · Further reading
- **[Files excluded from GitHub Copilot code review](reference/review-excluded-files.md)** (282 words): Understand the types of files that are excluded from a review by Copilot.
- **[Supported surfaces for GitHub Copilot policies](reference/supported-surfaces-for-policies.md)** (310 words): Which policies affect which Copilot features and surfaces?

## reference/copilot-cli-reference/

- **[Copilot CLI ACP server](reference/copilot-cli-reference/acp-server.md)** (1806 words): Learn about GitHub Copilot CLI's Agent Client Protocol server.
  - Sections: Overview · Use cases · Starting the ACP server · Example: integrating with the ACP server · Using slash commands · Further reading
- **[GitHub Copilot CLI command reference](reference/copilot-cli-reference/cli-command-reference.md)** (23613 words): Find commands and keyboard shortcuts to help you use Copilot CLI effectively.
  - Sections: Command-line commands · The sessions sidebar · Global shortcuts in the interactive interface · Timeline shortcuts in the interactive interface · Tasks dialog shortcuts · Restoring an interrupted session · Session picker shortcuts · Pre-conversation environment picker · Sidebar and sessions tab shortcuts · Diff mode shortcuts · Navigation shortcuts in the interactive interface · Slash commands in the interactive interface · Command-line options · Supported models · Tool availability values · Tool permission patterns · Environment variables · Configuration file settings · Project initialization for Copilot · Hooks reference · MCP server configuration · Skills reference · Extension modes · Custom agents reference · Sidekick agents · Permission approval responses · Security · OpenTelemetry monitoring · Further reading
- **[GitHub Copilot CLI configuration directory](reference/copilot-cli-reference/cli-config-dir-reference.md)** (10126 words): Find information about the `~/.copilot` directory, where Copilot CLI stores configuration, session data, and customizations.
  - Sections: Directory overview · User-editable files · Automatically managed files · Changing the location of the configuration directory · What you can safely delete · Configuration file settings · MDM managed settings · Managed MCP server allow/deny list · Further reading
- **[GitHub Copilot CLI plugin reference](reference/copilot-cli-reference/cli-plugin-reference.md)** (4080 words): Find commands and configuration details for CLI plugins.
  - Sections: CLI commands · `plugin.json` · `marketplace.json` · File locations · Loading order and precedence · Further reading
- **[GitHub Copilot CLI programmatic reference](reference/copilot-cli-reference/cli-programmatic-reference.md)** (2279 words): Find options for running Copilot CLI programmatically.
  - Sections: Command line options · Running dynamic workflows · Tools for the `--allow-tool` option · Environment variables · Choosing a model · Using custom agents · Further reading

## reference/enterprise-administrators/

- **[Available filters for agent sessions](reference/enterprise-administrators/agent-session-filters.md)** (134 words): Search agentic activity in your enterprise with filters for agent sessions.
- **[Audit log events for agents](reference/enterprise-administrators/agentic-audit-log-events.md)** (374 words): Understand the structure of audit log events for agents in your enterprise.
  - Sections: Streaming audit log events
- **[Enterprise managed settings](reference/enterprise-administrators/enterprise-managed-settings.md)** (4704 words): Understand the enterprise managed settings schema used by Copilot clients.
  - Sections: Supported keys · Example configuration · features.computerUse · enabledPlugins · extraKnownMarketplaces · strictKnownMarketplaces · model · autoTier · forceRemoteSettingsRefresh · permissions · telemetry · remoteControl · allowedMcpServers · deniedMcpServers · `sandbox`
- **[MCP private registry enforcement](reference/enterprise-administrators/mcp-private-registry-enforcement.md)** (377 words): Understand the logic and limitations of MCP private registry enforcement using a private registry server.
  - Sections: Supported surfaces · Current enforcement limitations · Enforcement for local servers · Policy resolution for users with multiple seats
- **[Feature availability when GitHub Copilot policies conflict in organizations](reference/enterprise-administrators/policy-conflicts.md)** (553 words): Delegating Copilot policy decisions to organizations affects users granted a license by organizations with different policies.
  - Sections: About delegating policy decisions to organizations · How availability is determined · Availability for members with Copilot from multiple organizations · Availability for members with Copilot from multiple enterprises · Next steps

## responsible-use/

- **[Application card: GitHub Copilot Agents](responsible-use/agents.md)** (7209 words): Learn how to use GitHub Copilot agentic features responsibly by understanding their purposes, capabilities, and limitations.
  - Sections: What is an Application Card? · 1. Overview · 2. Key terms · 3. Key features or capabilities · 4. Intended uses · 5. Models and training data · 6. Performance · 7. Limitations · 8. Evaluations · 9. Safety components and mitigations · 10. Best practices for deploying and adopting GitHub Copilot agentic features · 11. Learn more about GitHub Copilot agentic features

## tutorials/

- **[Using hooks with Copilot CLI for predictable, policy-compliant execution](tutorials/copilot-cli-hooks.md)** (3119 words): Use hooks to log user prompts and control which tools Copilot CLI can run in a repository, so teams can automate safely within your organization's security and compliance requirements.
  - Sections: Prerequisites · 1. Define an organizational policy · 2. Set up repository hook files · 3. Add a policy banner at session start · 4. Log prompts for auditing · 5. Enforce policies with `preToolUse` · 6. Test end-to-end in the repository · 7. Roll out safely across teams · Further reading

## tutorials/cloud-agent/

- **[Building guardrails for GitHub Copilot cloud agent](tutorials/cloud-agent/build-guardrails.md)** (659 words): Configure your enterprise so that Copilot cloud agent will operate in a secure, compliant environment.
  - Sections: Learn about built-in protections · Plan policy settings · Adapt rulesets · Set up your GitHub Actions environment
- **[Best practices for using GitHub Copilot to work on tasks](tutorials/cloud-agent/get-the-best-results.md)** (1965 words): Learn how to get the best results from Copilot cloud agent.
  - Sections: Making sure your issues are well-scoped · Choosing the right type of tasks to give to Copilot · Researching, planning, and iterating before opening a pull request · Using comments to iterate on a pull request · Adding custom instructions to your repository · Code Standards · Repository Structure · Key Guidelines · Playwright test requirements · Organization-wide custom instructions · Using the Model Context Protocol (MCP) · Creating custom agents · Pre-installing dependencies in GitHub Copilot's environment
- **[Giving GitHub Copilot cloud agent access to resources in your organization](tutorials/cloud-agent/give-access-to-resources.md)** (1110 words): Get more out of Copilot by giving it access to approved MCP servers and internal packages.
  - Sections: Example scenario · Storing secrets securely · Configuring access to MCP servers · Installing private packages · Controlling who can configure these settings
- **[Piloting GitHub Copilot cloud agent in your organization](tutorials/cloud-agent/pilot-cloud-agent.md)** (1044 words): Follow best practices to enable Copilot cloud agent in your organization.
  - Sections: 1. Evaluate · 2. Secure · 3. Pilot · Next steps
