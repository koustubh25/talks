# Managing policies and features for GitHub Copilot in your enterprise

> Source: https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-enterprise-policies
> Snapshot: github/docs @ 02c25d1 (2026-10-23)

_Control the availability of features for GitHub Copilot in your enterprise using policies._

When an organization owner assigns a Copilot license to a member of their organization, the availability of features and models is controlled by policies.

If you're setting up Copilot for the first time, see [AUTOTITLE](https://docs.github.com/en/copilot/tutorials/roll-out-at-scale/govern-at-scale/govern-for-adoption) for guidance on setting a governance posture that balances compliance with developer productivity.

## Defining policies for your enterprise

Enterprise owners can define a policy for the whole enterprise, or delegate the decision to individual organization owners. See [AUTOTITLE](../../../concepts/enterprise/policies.md).

{%- ifversion ghes %}
1. In the top-right corner of GitHub Enterprise Server, click your profile picture, then click **Enterprise settings**.
{%- else %}
1. Navigate to your enterprise. For example, from the [Enterprises](https://github.com/settings/enterprises?ref_product=ghec&ref_type=engagement&ref_style=text) page on GitHub.com.
{%- endif %}
1. At the top of the page, click ** AI controls**.
1. Navigate to the page containing the policies you want to manage:

   * To view policies for **AI agents**, in the sidebar, click  **Agents**.
   * To view administration, privacy, model, billing, and usage policies for **Copilot**, in the sidebar, click  **Copilot**.
   * To view policies for **Copilot** features and clients, in the sidebar, click  **Copilot**, then, under "Features & clients," click **Configure features & clients**.
   * To view policies for **Model Context Protocol (MCP)**, in the sidebar, click  **MCP**.
1. Configure your policies as follows:
   * For policies with a **dropdown menu**, select the menu and click an enforcement option.
   * For policies with a **toggle**, click the toggle to set availability or enforcement.
   * For policies with **no visible dropdown menu or toggle**, click the name of the policy for configuration options.

> **note:**
> The **MCP servers in Copilot** policy controls use where MCP server support is generally available (GA). This policy does not control access and permissions for the GitHub MCP server in third-party host applications (like Cursor, Windsurf or Claude). For more information on controlling access to the GitHub MCP server, see the [Policies and Governance](https://github.com/github/github-mcp-server/blob/main/docs/policies-and-governance.md#control-mechanisms) documentation in the GitHub MCP Server repository.

**Suggestions matching public code** is set to **Allowed** by default for Copilot Business users. You can change this setting in the **Privacy** section of the Copilot policy page.

## Opting in to feedback collection

If you enable "Copilot in GitHub.com" from the "Features & clients" page, you can also opt in to user feedback collection to help GitHub improve Copilot features.

## Further reading

* [AUTOTITLE](../../../reference/enterprise-administrators/policy-conflicts.md)
* [AUTOTITLE](../../../reference/supported-surfaces-for-policies.md)
