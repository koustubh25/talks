# Agent management

> Source: https://docs.github.com/en/copilot/concepts/agent-capabilities/choosing-and-delegating-agent-work/agent-management
> Snapshot: github/docs @ 02c25d1 (2026-10-23)

_Use one centralized control page to jump between agent sessions, check progress, and stay in control without losing your place._

## About agents

AI agents are autonomous systems that can evaluate their environment, make decisions, and take actions to complete tasks. Agents can break down complex tasks into steps, use various tools and resources, plan their approach, and adapt based on human feedback until they accomplish their assigned objective.

Agents bring automation and assistance to every stage of the software development process on GitHub. You can run multiple agent sessions concurrently, allowing you to efficiently delegate work items.

Alongside Copilot, you can use Anthropic Claude and OpenAI Codex, giving you more flexibility and choice to find the right agent for a task. See [AUTOTITLE](../about-agents/about-third-party-coding-agents.md).

GitHub partners can also offer their own agents as agent apps, which you install as GitHub Apps and trigger from issues, pull requests, and the Agents UI. See [AUTOTITLE](../about-agents/agent-apps.md).

Utilizing custom agents you can build out a team of task-specific agents with customized system prompts to handle simpler tasks like writing tests and refactoring, giving you bandwidth to prioritize problem-solving and collaboration. See [AUTOTITLE](../../customizations/custom-agents.md).

Model choice allows you to choose from a selection of AI models to use with your agents, each with its own particular strengths. See [AUTOTITLE](https://docs.github.com/en/copilot/reference/ai-models/supported-models).

To learn more about Copilot cloud agent, see [AUTOTITLE](https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github).

## Managing agents

When utilizing GitHub's agentic features, you can use the **Agents** tab within a repository that has Copilot cloud agent enabled to initiate, monitor, and manage agent sessions without leaving your workflow. You can also use the [Agents page](https://github.com/copilot/agents?ref_product=copilot&ref_type=engagement&ref_style=text) to view and start agent sessions. To learn how to enable Copilot cloud agent, see [AUTOTITLE](../../enterprise/cloud-agent-access.md).

From the Agents tab, you can:

* **Kick off new agent tasks**: Select an AI model of your choice, and optionally choose from third-party agents or custom agents best suited for the task. See [AUTOTITLE](../../../how-tos/use-copilot-agents/cloud-agent/start-copilot-sessions.md).
* **Monitor live session logs**: Once the agent starts working, you can click any agent session to open the session log and follow its progress and thought process in real time.
* **Track active sessions**: You can view all active agent sessions that have been started in the repository.
* **Steer agents mid-session**: If you realize you didn't scope a request correctly, or want the agent to use a specific tool or service, you can step in and provide **steering input** without stopping the run. Steering consumes AI credits per message. See [AUTOTITLE](../../../how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents.md#steer-an-agent-session).
* **Open a session in VS Code or GitHub Copilot CLI**: When you want to start working on changes to an agent session in your local development environment, click ** Open in VS Code** or ** Continue in GitHub Copilot CLI** to bring the session to your local machine.
    > [!NOTE]
> Opening a session in VS Code requires the latest versions of VS Code, the GitHub Copilot extension, and the GitHub Pull Requests extension.
* **Review and merge agent code**: Once the agent completes a session, you can jump to the pull request to review the changes, request further improvements, or approve and merge. See [AUTOTITLE](../../../how-tos/copilot-on-github/use-copilot-agents/review-copilot-output.md).
* **Set up automations**: Run Copilot cloud agent automatically, on a schedule or in response to events such as an issue being opened. See [AUTOTITLE](../agent-powered-workflows-and-operations/about-automations.md).
* **Query your past sessions**: You can search and reference your past agent sessions using natural language from Copilot CLI or VS Code. See [AUTOTITLE](../../security-governance-and-network-settings/session-data.md).

## Next steps

To start managing agents, see [AUTOTITLE](../../../how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents.md).
