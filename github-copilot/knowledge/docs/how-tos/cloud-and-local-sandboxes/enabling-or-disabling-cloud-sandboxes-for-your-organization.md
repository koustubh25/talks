# Enabling or disabling cloud sandboxes for your organization or enterprise

> Source: https://docs.github.com/en/copilot/how-tos/cloud-and-local-sandboxes/enabling-or-disabling-cloud-sandboxes-for-your-organization
> Snapshot: github/docs @ 02c25d1 (2026-10-23)

_You can control whether members of your organization or enterprise can use cloud sandboxes by managing the cloud sandbox access policy in your organization or enterprise settings._

> **note:**
> Cloud sandboxes for GitHub Copilot are in public preview and subject to change.

## About enabling and disabling cloud sandboxes

Organization owners can control whether members of their organization have access to cloud sandboxes by configuring the cloud sandbox access policy. Enterprise owners can control cloud sandbox access for all organizations in the enterprise. By default, cloud sandbox access is disabled.

For more information about cloud sandboxes, see [AUTOTITLE](../../concepts/security-governance-and-network-settings/about-cloud-and-local-sandboxes.md).

## Enabling or disabling cloud sandboxes for your organization

1. In the upper-right corner of GitHub, click your profile picture, then click ** Organizations**.
1. Select an organization by clicking on it.
1. Under your organization name, click ** Settings**. If you cannot see the "Settings" tab, select the **** dropdown menu, then click **Settings**.

   ![Screenshot of the tabs in an organization's profile. The "Settings" tab is outlined in dark orange.](/assets/images/help/discussions/org-settings-global-nav-update.png)
1. In the sidebar, under "Code, planning, and automation", click **Sandboxes**.
1. Under "Cloud sandbox access", select your preferred setting:
   * **Disabled**: Cloud sandbox access is not available for organization members.
   * **Enabled**: Members of this organization can use cloud sandboxes.
1. Click **Save**.

## Enabling or disabling cloud sandboxes for your enterprise

Enterprise owners can control cloud sandbox access for all organizations in the enterprise from the **Policies** tab of the enterprise settings. By default, cloud sandbox access is disabled for all organizations in the enterprise.

{%- ifversion ghes %}
1. In the top-right corner of GitHub Enterprise Server, click your profile picture, then click **Enterprise settings**.
{%- else %}
1. Navigate to your enterprise. For example, from the [Enterprises](https://github.com/settings/enterprises?ref_product=ghec&ref_type=engagement&ref_style=text) page on GitHub.com.
{%- endif %}
1. At the top of the page, click ** Policies**.
1. Click **Sandboxes**.
1. Under "Cloud sandbox access", select your preferred setting:
   * **Disabled**: Cloud sandbox access is not available for any organizations in this enterprise.
   * **Let organizations enable (opt-in)**: Organization owners can choose to enable cloud sandbox access for their members. New organizations default to disabled.
   * **Enabled by default for all organizations (opt-out)**: Cloud sandbox access is enabled for all organizations. Organization owners can still disable access for their organization if needed.
1. Click **Save**.

## Further reading

* [AUTOTITLE](../../concepts/security-governance-and-network-settings/about-cloud-and-local-sandboxes.md)
* [AUTOTITLE](/billing/concepts/product-billing/cloud-and-local-sandboxes)
* [AUTOTITLE](../../reference/enterprise-administrators/enterprise-managed-settings.md#sandbox)
