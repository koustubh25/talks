# Using Copilot cloud agent via the GitHub MCP Server

> Source: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-with-mcp
> Snapshot: github/docs @ 02c25d1 (2026-10-23)

_Start Copilot cloud agent sessions from any IDE or agentic tool that supports Model Context Protocol (MCP)._

> **note:**
> * This capability is only available on the remote GitHub MCP Server and host applications where remote MCP Servers are supported.

## Starting a session

1. Install the GitHub MCP Server in your preferred IDE or agentic coding tool. See [AUTOTITLE](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/copilot-for-common-tasks/use-the-github-mcp-server).

1. Ensure the `create_pull_request_with_copilot` tool is enabled.

1. Open chat.

1. Type a prompt asking Copilot to create a pull request, with the details of what you want to change.

   For example, `Open a PR in my repository to expand unit test coverage.`

   > [!TIP]
   > * You can ask Copilot to open a pull request using a specific branch as the base branch by including it in your prompt.

1. Submit your prompt.

   Copilot will start a new session, open a draft pull request and work on the task in the background. As it works, it will push changes to the pull request, and once it has finished, it will add you as a reviewer. In most cases, the MCP host will show you the URL of the created pull request.

## Further reading

* [AUTOTITLE](../../copilot-on-github/use-copilot-agents/manage-and-track-agents.md)
* [AUTOTITLE](../../../tutorials/cloud-agent/get-the-best-results.md)
