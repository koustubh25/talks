# Enabling GitHub Copilot cloud agent in your enterprise

> Source: https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-agents/enable-copilot-cloud-agent
> Snapshot: github/docs @ 02c25d1 (2026-10-23)

_Choose which organizations can use Copilot cloud agent and connect it to MCP servers._

## Prerequisites

You may want to run a trial before enabling Copilot cloud agent for the enterprise. See [AUTOTITLE](../../../../tutorials/cloud-agent/pilot-cloud-agent.md).

## Enabling Copilot cloud agent

Copilot cloud agent and use of third-party MCP servers are disabled by default. You can enable these features for users who receive a Copilot license from your enterprise or organizations.

{%- ifversion ghes %}
1. In the top-right corner of GitHub Enterprise Server, click your profile picture, then click **Enterprise settings**.
{%- else %}
1. Navigate to your enterprise. For example, from the [Enterprises](https://github.com/settings/enterprises?ref_product=ghec&ref_type=engagement&ref_style=text) page on GitHub.com.
{%- endif %}
1. At the top of the page, click ** AI controls**.
1. In the left sidebar, click  **Agents**.
1. Under "Available agents", click **Copilot Cloud Agent**.
1. Select a global policy for Copilot cloud agent, then communicate your decision with your organizations.

   >[!TIP] If you select **Enabled for selected organizations**, you can select individual organizations in the UI. To select organizations based on custom properties instead, use the REST API. See [AUTOTITLE](/rest/copilot/copilot-coding-agent-management#selecting-organizations-with-custom-properties).

1. By default, the agent will be available in all repositories in selected organizations. If there are repositories where Copilot cloud agent should be blocked for all users, tell organization owners to configure this setting. See [AUTOTITLE](../../manage-for-organization/add-copilot-cloud-agent.md#disabling-or-enabling-copilot-cloud-agent-in-your-repositories).

## Enabling MCP servers

Copilot cloud agent automatically has access to a small number of default MCP servers. See [AUTOTITLE](../../../../concepts/customizations/mcp.md#default-mcp-servers).

You can enable third-party MCP servers to allow developers to integrate Copilot cloud agent with other services in your DevOps toolchain, such as error-tracking platforms or logging systems.

1. In the sidebar, click  **MCP**.
1. Set a policy for **MCP servers in Copilot**.

> **note:** The "MCP Registry URL" and "Restrict MCP access to registry servers" policies do **not** apply to Copilot cloud agent.

## Enabling agent apps and third-party agents

Enterprise owners can enable third-party agents, including agent apps, for their organizations. Once enabled at the enterprise level, organization owners can choose which agents to allow. For an overview of agent apps, see [AUTOTITLE](../../../../concepts/agent-capabilities/about-agents/agent-apps.md).

To manage agent and enterprise policies, see [AUTOTITLE](../manage-enterprise-policies.md).
