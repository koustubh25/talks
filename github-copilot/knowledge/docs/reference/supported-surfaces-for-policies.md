# Supported surfaces for GitHub Copilot policies

> Source: https://docs.github.com/en/copilot/reference/supported-surfaces-for-policies
> Snapshot: github/docs @ 02c25d1 (2026-10-23)

_Which policies affect which Copilot features and surfaces?_

GitHub Copilot is available across various surfaces: in IDEs, in the CLI, and as multiple agents and chat interfaces on the GitHub website.

A dedicated policy exists to enable or disable each supported feature or surface. Additionally, you can set various policies to customize or control the Copilot experience. However, not every policy applies to every available surface.

> **note:** The following table documents whether specific policies apply to different surfaces, but does not necessarily reflect whether the equivalent functionality is available. For example, Copilot cloud agent **can** access the Internet, but the "Copilot can search the web" policy does not affect this capability.

| Policy name | IDEs | Copilot cloud agent | Third-party agents | Copilot CLI | The GitHub Copilot app | Copilot Chat in GitHub | Copilot code review | Spark |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Editor preview features |  |  |  |  |  |  |  |  |
| Copilot can search the web |  |  |  |  |  |  |  |  |
| Configure custom models |  |  |  |  |  |  |  |  |
| Suggestions matching public code |  | [^1] | [^1] |  |  |  |  |  |
| MCP servers in Copilot |  |  |  |  |  |  |  |  |
| Restrict MCP access to registry servers |  |  |  |  |  |  |  |  |
| Content exclusion |  |  |  |  |  |  |  |  |
| Configure models |  |  |  |  |  |  |  |  |
| Copilot Memory |  |  |  |  |  |  |  |  |

[^1]: Only supported in annotate mode. See [AUTOTITLE](../responsible-use/agents.md#7-limitations).
