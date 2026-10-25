# Review output from Copilot

> Source: https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output
> Snapshot: github/docs @ 02c25d1 (2026-10-23)

_Copilot pull requests deserve the same thorough review as any contribution._

## Review Copilot's changes

When Copilot finishes a coding task and requests your review, check the pull request thoroughly before merging.

> **important:**
> If your repository requires pull request approvals, **your approval of a Copilot pull request won't count** toward the required number. Another reviewer must approve the pull request before it can be merged.

To request changes from Copilot on its pull request, mention `@copilot` in a comment, or push commits directly to the branch. For more information, see [AUTOTITLE](../../use-copilot-agents/cloud-agent/use-cloud-agent-on-github.md).

## Manage GitHub Actions workflow runs

By default, GitHub Actions workflows will not run automatically when Copilot pushes changes to a pull request.

GitHub Actions workflows can be privileged and have access to sensitive secrets. Inspect the proposed changes in the pull request and ensure that you are comfortable running your workflows on the pull request branch. You should be especially alert to any proposed changes in the `.github/workflows/` directory that affect workflow files.

To allow GitHub Actions workflows to run, click the **Approve and run workflows** button in the pull request's merge box.

![Screenshot of the merge box on a pull request from Copilot with the "Approve and run workflows" button.](/assets/images/help/copilot/cloud-agent/approve-and-run-workflows.png)

Optionally, you can configure Copilot cloud agent to allow GitHub Actions workflows to run without human intervention. For more information, see [AUTOTITLE](../../use-copilot-agents/cloud-agent/configuring-agent-settings.md).

## Give feedback on Copilot's work

Use the feedback buttons on Copilot's pull requests and comments to rate the output. Your feedback helps improve Copilot's quality.

1. On a pull request or comment from Copilot, click the thumbs up (:+1:) or thumbs down (:-1:) button.
1. If you click the thumbs down button, optionally select a reason and leave a comment, then click **Submit feedback**.

## Further reading

* [AUTOTITLE](../../../tutorials/cloud-agent/get-the-best-results.md)
* [AUTOTITLE](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/troubleshoot-cloud-agent)
