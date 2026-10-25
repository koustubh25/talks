# Building guardrails for GitHub Copilot cloud agent

> Source: https://docs.github.com/en/copilot/tutorials/cloud-agent/build-guardrails
> Snapshot: github/docs @ 02c25d1 (2026-10-23)

_Configure your enterprise so that Copilot cloud agent will operate in a secure, compliant environment._

Before you enable Copilot cloud agent, it is good practice to set up your enterprise so you can be confident Copilot will operate within secure, predictable guardrails.

## Learn about built-in protections

Copilot cloud agent has a strong base of built-in security protections designed to protect against common risk points of AI agents. See [AUTOTITLE](../../concepts/security-governance-and-network-settings/risks-and-mitigations.md).

## Plan policy settings

Plan your policies for Copilot cloud agent in advance. Policies allow you to set a baseline for restrictions at the enterprise level, which organization owners can restrict further if needed.

Some questions to ask are:

* Which organizations and repositories will Copilot cloud agent be enabled in? See [AUTOTITLE](../../concepts/enterprise/cloud-agent-access.md).
* Which MCP servers will you configure to give Copilot cloud agent access to external tools? See [AUTOTITLE](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/configure-mcp-servers).

### Which policies don't apply?

The following Copilot policies don't apply to Copilot cloud agent:

* Custom models (providing your own LLM API keys)
* Private MCP registries

## Adapt rulesets

Copilot cloud agent is already restricted from actions like pushing to a default branch or merging pull requests. You can build on these default protections in branch rulesets. Copilot cloud agent is subject to rulesets just like human developers.

To adapt your rulesets for Copilot cloud agent:

* **Consider whether additional rules are required** in repositories where agents will operate, such as requiring results from code scanning or Code Quality. If you have identified the organizations or repositories where Copilot cloud agent will be enabled, you can apply a custom property to them so they're easy to target in a ruleset.
* **Consider whether Copilot cloud agent will be blocked** by any of your existing rulesets. Copilot _can_ sign its commits, but it may not be able to follow other rules that restrict commit metadata.
* **Protect important Copilot and MCP configuration files** with a `CODEOWNERS` file, and enable the "Require review from Code Owners" rule, so that edits to these files must be approved by specific teams. For filepaths to target, see [AUTOTITLE](https://docs.github.com/en/copilot/reference/customization-cheat-sheet).

## Set up your GitHub Actions environment

Copilot cloud agent operates on GitHub Actions runners. Set up your runners and policies so that Copilot operates securely.

### Store data and secrets

Continue to store data and tokens that you _don't_ want Copilot to access as **GitHub Actions variables or secrets**. Copilot won't be able to access these in its sessions or environment setup steps.

If you need to provide data and secrets that Copilot cloud agent _does_ need, you'll be able to do this by configuring Agents secrets and variables at the organization or repository level. For more information, see [AUTOTITLE](../../how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/configure-secrets-and-variables.md).

### Configure runners

Decide which runners you will use for Copilot cloud agent. We recommend using **GitHub-hosted runners**, so that each Copilot cloud agent runs on a fresh virtual machine. If you use self-hosted runners, we recommend using ephemeral runners.

Organization owners can restrict the Copilot cloud agent's runners to a specific runner label, to be used automatically in all repositories. See [AUTOTITLE](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/configure-runner-for-coding-agent).

### Configure workflow policies

Decide whether **GitHub Actions workflows should be blocked from running** in pull requests that Copilot cloud agent creates. See [AUTOTITLE](../../how-tos/use-copilot-agents/cloud-agent/configuring-agent-settings.md#allowing-github-actions-workflows-to-run-automatically-when-copilot-pushes).

By default, workflows are blocked from running until someone with write access approves them. Repository administrators will be able to disable this feature, so communicate with them in advance about your preferred setting.

### Review default permissions

Review the default permissions for the `GITHUB_TOKEN` in your enterprise. See [AUTOTITLE](/enterprise-cloud@latest/admin/enforcing-policies/enforcing-policies-for-your-enterprise/enforcing-policies-for-github-actions-in-your-enterprise#workflow-permissions).

This policy does **not** affect the token that Copilot will receive for its sessions, but the `GITHUB_TOKEN` _is_ used in environment setup steps defined in `copilot-setup-steps.yml` workflow files.

Bear in mind that developers will be able to set their own `permissions` in these workflow files, and you should encourage them to use the minimum required permissions in all workflows.
