# Deploy Zava ExM Meeting Concierge

**GitHub Actions is the main deployment path.** The workflow builds and checks the solution, saves a downloadable package, and imports it into an authorized target environment when explicitly requested. The Gatekeeper architecture and calendar controls remain the same.

**First-time authorization belongs to the receiving tenant. Its administrator must authorize the deployment identity, create the account connections, and provide the target settings.** GitHub cannot bring the original lab's sign-ins or permissions into another tenant.

The workflow imports and checks components. It does not provision a tenant, create OAuth connections, publish the agent, or enable calendar processing. Rule data, authentication, publication, and the calendar acceptance test are completed below. A successful workflow is not proof that those runtime steps are finished.

## Before you start

- A separate Power Platform environment with Dataverse and Copilot Studio available, with suitable licensing/capacity for the agent and flows. The ZIP does not provision a tenant, environment, mailbox, or licenses.
- An installer with permission to import solutions, configure connections and environment variables, publish the agent, and administer the custom rule table. Use an authorized environment administrator for the initial POC setup if needed; ordinary demo users do not need administrator access.
- An Exchange Online account with a primary calendar and valid Outlook working hours. Use an isolated test mailbox. This POC reads and updates the **connected account's primary calendar** through Graph `/me`; it does not support a delegated, shared, or secondary calendar.
- Tenant connector policies that allow Office 365 Outlook (including its HTTP request action), Microsoft Copilot Studio, and Microsoft Dataverse together. Confirm the agent's model and authentication are supported in the target environment.

## Create the account connections

In the target environment, create or choose these connections:

| Connection label | Connector | Account and purpose |
| --- | --- | --- |
| Calendar connection | Office 365 Outlook | The test account whose primary calendar the POC may read and change; also sends assistant notifications |
| Agent connection | Microsoft Copilot Studio | An authorized target-tenant account that can invoke the imported agent |
| Meeting rules connection | Microsoft Dataverse | An authorized account in this environment with read access to active Calendar Governance Rule rows |

The flow uses saved owner connections. A caller does not supply a different mailbox or calendar. Restrict flow sharing and agent access to the intended POC users, and explicitly review run-only connection settings after import. Do not carry over assumptions about permissions from the original lab.

## Choose the calendar settings

| Setting | What to enter |
| --- | --- |
| **Calendar mailbox** | Email address of the account used by Calendar connection |
| **Calendar ID** | Outlook ID of that same account's primary calendar |
| **Executive assistant email** | One test recipient who should receive unresolved-conflict notifications |

To find the Calendar ID, use a temporary instant flow in the target environment with Outlook **Get calendars (V2)**, using the same Calendar connection. Run it and inspect the returned calendar IDs. Select the account's primary calendar; display names can be localized. If needed, confirm the primary calendar ID using Microsoft Graph `GET /me/calendar` while signed into that same account. Remove the temporary helper afterward. Do not copy an event ID or an ID from another mailbox.

These settings have no lab defaults. They are configuration, not policy overrides. The mailbox setting supplies the working-hours lookup; calendar reads and writes still use the connected account. **The installer must verify that the account, mailbox setting, and primary Calendar ID agree.** Email syntax checks cannot establish that identity match.

## Authorize GitHub in the receiving tenant

The tenant administrator completes these steps once for each target tenant/environment:

1. **Choose the GitHub repository.** Use this repository if its maintainers will deploy, or fork it into the receiving organization's GitHub account. Enable GitHub Actions. The workflow must be present on `main` before its Run workflow button is available.
2. **Register a deployment application in Microsoft Entra ID.** Use a dedicated, single-tenant app registration. Record its Application (client) ID and Directory (tenant) ID. No client secret is needed.
3. **Add its application user to the target Dataverse environment.** Assign a role that can import/export this solution and its components. For an isolated POC, a dedicated application user with System Administrator in that POC environment is a straightforward starting point; this is broad access, not a verified least-privilege production role. The deployment application is separate from the Outlook runtime account.
4. **Authorize the connections for that application user.** Make the target connections available to the service principal where connector sharing supports it. Confirm flow ownership and licensing for service-principal imports with the tenant administrator. Merely knowing a connection ID does not grant its use. See [Microsoft's connection-reference guidance](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-connection-reference).
5. **Create a GitHub environment** under repository **Settings > Environments**, for example `poc`. Restrict its deployment branches to **main**. Add a required reviewer if your GitHub plan supports that protection. The workflow also blocks tenant deployment from other branches and serializes deployments to the same GitHub environment. Use one GitHub environment per target and do not configure different names for the same target if you want that serialization.
6. **Add a federated credential to the Entra app registration.** In **Certificates & secrets > Federated credentials**, choose the GitHub Actions scenario and enter the repository owner, repository name, and **Environment** entity type with the exact GitHub environment name. For `poc`, the subject is `repo:OWNER/REPOSITORY:environment:poc`. The issuer is `https://token.actions.githubusercontent.com` and audience is `api://AzureADTokenExchange`. These values are case-sensitive. No Azure subscription role is needed merely to import a Dataverse solution; the Dataverse application-user role controls that access.

Microsoft documents [GitHub federated trust](https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation-create-trust?pivots=identity-wif-app-reg-github-actions) and the CLI's [GitHub federated sign-in](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/auth#pac-auth-create).

## Add the GitHub environment settings

Under the selected GitHub environment, add these **environment variables**:

| Name | Value |
| --- | --- |
| `ENVIRONMENT_URL` | Target Dataverse organization URL, such as `https://YOUR-ORG.crm.dynamics.com` |
| `TENANT_ID` | Receiving tenant's Directory ID |
| `CLIENT_ID` | Deployment app's Application ID |

Then create one **environment secret**, `DEPLOYMENT_SETTINGS_JSON`:

1. Copy [settings.example.json](../deployment/settings.example.json) to a local working file. If using the checkout, `deployment/settings.local.json` is ignored by Git.
2. Fill all three `EnvironmentVariables` values with the calendar settings above.
3. Fill each `ConnectionId` with the matching connection from the target environment. Keep the supplied logical names and connector IDs intact. The connection detail page/URL identifies its connection ID; use that connection's ID rather than a connector name or connection-reference name. PAC can also list accessible connections with `pac connection list` after target sign-in.
4. Paste the entire completed JSON into `DEPLOYMENT_SETTINGS_JSON`. Do not put account passwords, client secrets, or tokens into that JSON. Do not commit the completed settings file.

The template contains all three mappings: Calendar connection, Agent connection, and Meeting rules connection. The workflow validates required values, email syntax, and the artifact checksum before signing into the tenant. Invalid settings stop deployment.

## Run the deployment

1. If updating an existing installation, turn off **Check new meeting** and let active runs finish, then turn off **Check and move meeting**. Review/export a backup first. An unmanaged import does not guarantee that previously enabled flows become disabled.
2. In GitHub, open **Actions > Meeting Concierge > Run workflow**.
3. Choose branch **main**, choose the configured GitHub environment, check **Deploy after the package checks pass**, and run it. Leave that box unchecked when you only want to build a package.
4. **Build and check** validates the repository, runs scheduling tests, builds the ZIP, checks the built package, and tests import-script safeguards without tenant access. It saves the **ZavaExMMeetingConcierge** artifact containing `ZavaExMMeetingConcierge.zip` and `SHA256SUMS.txt`.
5. **Deploy to tenant** waits for any configured environment approval, signs in using GitHub federation, and imports that same artifact with the target settings. It does not rebuild or substitute a different package.
6. The job exports the imported solution to temporary runner storage and verifies the agent, its single Gatekeeper tool, both inactive flows, rule table, and configuration definitions. It does not publish the verification export as an artifact. Temporary settings and the runner's PAC profile are cleared at the end.
7. Read the workflow result and import log. Complete the remaining setup below before enabling calendar processing. If a job fails, inspect its failed step; do not treat a successful build as a successful import.

Pull requests and pushes to main build and check the package automatically. **They never deploy.** Only an explicit Run workflow from main with deployment selected can enter the tenant job.

## Finish setup and enable processing

1. In the imported solution, open **Calendar Governance Rule** and its data. Check existing active rows before adding anything.
2. If the approved rule already exists, reuse it. Otherwise create one row, using **Protect board meetings** as the name and the exact rule text from [meeting-rule.json](../deployment/meeting-rule.json):

   > Board meetings are critical and cannot be moved. Any meeting that has "board meeting" in the subject is considered a board meeting.

3. Confirm the row is active and the Dataverse connection account can read it. Do not overwrite someone else's rules. An unsupported additional active rule deliberately blocks automatic resolution.
4. Check the test account's Outlook working days, opening and closing times, and time zone. Missing or invalid working hours stop a move; only weekdays are searched.
5. Save and publish the agent after checking its tool and authentication. Turn on **Check and move meeting**, then **Check new meeting**. Review any connection or permission prompts before proceeding.

Microsoft requires publishing an imported agent and configuring authentication in the target environment. See [agent solution import guidance](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-solutions-import-export).

## Test the installed solution

Use future temporary events without attendees, within the test account's working hours. Keep the starter off while preparing each set of existing events; enable it immediately before creating the new event that should trigger the test. Wait for processing before starting another scenario.

| Scenario | Expected calendar result | Expected notification |
| --- | --- | --- |
| New ordinary meeting with no overlap | Nothing moves; NoConflict | None |
| New ordinary meeting overlapping a board meeting, with free time available | Ordinary meeting moves; board meeting stays; duration preserved; Resolved | None |
| New board meeting overlapping an ordinary meeting, with free time available | Ordinary meeting moves; board meeting stays; Resolved | None |
| New board meeting overlapping another board meeting | Both remain unchanged; NeedsHelp | One notification attempt to the configured test assistant |
| Ordinary meeting conflict with no free interval in the search window | Nothing moves; NeedsHelp | One notification attempt |

Check actual Outlook times, the resolver's response, and the notification action, rather than just a green parent flow. For a successful send action, inspect Sent Items; it confirms submission, not recipient delivery. Preserve the result even when the test fails.

Record package version/checksum, target environment/tenant, date, configuration checks, each scenario's result, flow run IDs, and any screenshots with private data removed. Use [the acceptance record](../deployment/acceptance.md). This record establishes which installation and runtime checks were completed. Do not mark cross-tenant deployment as passed until the actual test completes.

## Stop or remove the POC

Turn off **Check new meeting** first, let active runs finish, then turn off the resolver. Remove temporary calendar events. An import rollback or uninstall does not reverse calendar changes or sent emails.

This is an **unmanaged** POC for inspection and modification. Deleting its solution container does not remove all underlying components. A disposable environment is the cleanest way to remove the entire trial. Do not delete connections shared with other solutions.

## Maintenance and boundaries

To change mailbox or recipient, stop processing, update environment-variable current values and connection bindings together, then save/re-enable the flows and repeat acceptance checks. Never use a secondary calendar ID with the current primary-calendar Graph path.

The Gatekeeper's policy checks, final reads, If-Match write protection, and outcome verification remain in place. Missing or malformed mailbox/assistant settings return UnableToCheck before calendar access. The trigger needs a valid Calendar ID to operate. No mailbox lock or duplicate-request ledger is added here; requests can overlap. Use sequential POC tests and keep production-readiness claims separate.

For maintainers, [script instructions](../scripts/README.md) cover local checks and package rebuilding. [Architecture](architecture.md), [security](security.md), and [test evidence](testing.md) explain the enforcement boundary and its limits.

## Alternative: manual import

If GitHub Actions is unavailable or the installer prefers a manual setup, download the same named solution ZIP and follow [manual installation](manual-install.md). This is an alternative route, not a requirement to repeat installation after a pipeline deployment. Both routes use the same Gatekeeper and finish with the same acceptance test.

## What has been verified

Local source checks, scheduling simulations, package packing/unpacking, workflow linting, and import-script tests establish the repository build path. A live federated GitHub deployment and independent calendar acceptance test require the receiving tenant's setup. Record those results in [the acceptance record](../deployment/acceptance.md); do not infer them from local tests.
