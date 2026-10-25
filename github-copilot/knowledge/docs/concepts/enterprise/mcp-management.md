# MCP server usage in your company

> Source: https://docs.github.com/en/copilot/concepts/enterprise/mcp-management
> Snapshot: github/docs @ 02c25d1 (2026-10-23)

_You can manage MCP server usage to provide your developers with valuable tools while maintaining security and compliance._

The Model Context Protocol (MCP) is an open standard that defines how applications share context with large language models (LLMs). MCP provides a standardized way to connect AI models to different data sources and tools, enabling them to work together more effectively.

You can manage MCP server usage in your organization or enterprise by configuring MCP policies on GitHub.

The **MCP servers in Copilot** policy defines whether MCP servers can run at all across Copilot clients. We recommend keeping this policy enabled and, if necessary, restricting the MCP servers that users can run to an approved list.

## MCP allowlists

The recommended method for creating an allowlist is to use your enterprise's `managed-settings.json` file. This allows you to apply settings across clients that users cannot override.

Alternatively, you can host your own MCP registry and restrict access to servers in the registry. However, this method has weaker enforcement than `managed-settings.json`.

| Method | Managed settings file | Custom registry |
| ------ | --------------------- | --------------- |
| Release phase | Generally available | Public preview, not prioritized for development |
| Ease of setup | You can host a configuration file on GitHub that applies automatically to clients. | You must host your own registry that matches the MCP specification and serves HTTPS requests. |
| Enforcement level | Enterprise-wide settings, overridable for enterprise teams | Enterprise-wide or for individual organizations |
| Supported clients | Clients supported by the `managed-settings.json` file, see [AUTOTITLE](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/use-managed-settings/get-started). Planned to expand in the near future. | See [AUTOTITLE](../../reference/enterprise-administrators/mcp-private-registry-enforcement.md). |
| Server matching method | Secure matching based on name, URL, or `stdio` commands | Less secure matching, based on name or ID only. Users can bypass the restriction by editing configuration files. |

## Next steps

To configure an allowlist on GitHub, see [AUTOTITLE](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-enterprise-allowlist).

## Further reading

* [AUTOTITLE](../../reference/supported-surfaces-for-policies.md)
* [AUTOTITLE](../../how-tos/administer-copilot/manage-mcp-usage/configure-mcp-registry.md)
