# Install the POC in another tenant

This guide installs **Zava ExM Meeting Concierge 2.1.0.0** into a separate development or sandbox environment. Download the repository from the branch containing this release, or use `main` after its pull request is merged. Use the portable V2.1 package below, rather than the earlier lab exports.

This is a repository-authored unmanaged POC package. It has been packed, unpacked, and checked locally with the official Power Platform CLI. **A clean import into another environment is awaiting the owner's manual acceptance test.** Earlier live calendar tests establish Dev behavior, not cross-tenant deployment success.

## 1. Check the prerequisites

- A separate Power Platform environment with Dataverse and Copilot Studio available, with suitable licensing/capacity for the agent and flows. The ZIP does not provision a tenant, environment, mailbox, or licenses.
- An installer with permission to import solutions, configure connections and environment variables, publish the agent, and administer the custom rule table. Use an authorized environment administrator for the initial POC setup if needed; ordinary demo users do not need administrator access.
- An Exchange Online account with a primary calendar and valid Outlook working hours. Use an isolated test mailbox. This POC reads and updates the **connected account's primary calendar** through Graph `/me`; it does not support a delegated, shared, or secondary calendar.
- Tenant connector policies that allow Office 365 Outlook (including its HTTP request action), Microsoft Copilot Studio, and Microsoft Dataverse together. Confirm the agent's model and authentication are supported in the target environment.

## 2. Download and check the package

Download [the V2.1 unmanaged solution](../solution/exports/ZavaExMMeetingConcierge_2_1_0_0_unmanaged.zip), [its checksum](../solution/exports/SHA256SUMS.txt), and this guide. A GitHub source download also contains the settings template and optional scripts.

On Windows, verify the ZIP with:

```powershell
Get-FileHash ./solution/exports/ZavaExMMeetingConcierge_2_1_0_0_unmanaged.zip -Algorithm SHA256
```

Compare the result to `solution/exports/SHA256SUMS.txt`. Keep the original file intact. The package contains one agent, one agent tool, two flows, one rule table, three connection references, and three environment variable definitions. Account credentials and policy rows are not included.

## 3. Create the target connections

In the target environment, create or choose these connections:

| Connection label | Connector | Account and purpose |
| --- | --- | --- |
| Calendar connection | Office 365 Outlook | The test account whose primary calendar the POC may read and change; also sends assistant notifications |
| Agent connection | Microsoft Copilot Studio | An authorized target-tenant account that can invoke the imported agent |
| Meeting rules connection | Microsoft Dataverse | An authorized account in this environment with read access to active Calendar Governance Rule rows |

The flow uses saved owner connections. A caller does not supply a different mailbox or calendar. Restrict flow sharing and agent access to the intended POC users, and explicitly review run-only connection settings after import. Do not carry over assumptions about permissions from the original lab.

## 4. Gather the three settings

| Setting | What to enter |
| --- | --- |
| **Calendar mailbox** | Email address of the account used by Calendar connection |
| **Calendar ID** | Outlook ID of that same account's primary calendar |
| **Executive assistant email** | One test recipient who should receive unresolved-conflict notifications |

To find the Calendar ID, use a temporary instant flow in the target environment with Outlook **Get calendars (V2)**, using the same Calendar connection. Run it and inspect the returned calendar IDs. Select the account's primary calendar; display names can be localized. If needed, confirm the primary calendar ID using Microsoft Graph `GET /me/calendar` while signed into that same account. Remove the temporary helper afterward. Do not copy an event ID or an ID from another mailbox.

These settings have no lab defaults. They are configuration, not policy overrides. The mailbox setting supplies the working-hours lookup; calendar reads and writes still use the connected account. **The installer must verify that the account, mailbox setting, and primary Calendar ID agree.** Email syntax checks cannot establish that identity match.

## 5. Import and configure

1. Open Power Apps, select the target environment, then **Solutions > Import solution**. Select the V2.1 ZIP.
2. Map all three connection references to the target connections above. If the wizard does not show a connection step, open the imported solution's connection references and bind them before enabling anything.
3. Supply the three environment-variable current values. If the wizard does not request them, open each environment variable in the imported solution and set its current value.
4. Wait for import completion and check the import log. Both flows are packaged as **Off**. Verify that they remain off, especially if updating an existing installation: an import is not a guarantee that previously enabled flows become disabled. Pause an existing starter before an update.
5. Open the agent. Confirm **Check and move meeting** is its only tool, that the tool points to the imported flow, and that the starter's agent action points to the imported agent. Configure authentication and intended user access in this tenant; channel-specific settings may need to be configured again.

Optional CLI path, after signing into the intended tenant with the official Power Platform CLI:

```powershell
Copy-Item ./deployment/settings.example.json ./deployment/settings.local.json
# Fill in the three values and three target connection IDs in settings.local.json.
pac auth create --environment 'https://YOUR-ORG.crm.dynamics.com'
./scripts/import-solution.ps1 -EnvironmentUrl 'https://YOUR-ORG.crm.dynamics.com' -SettingsFile ./deployment/settings.local.json
```

The helper checks required settings, connection mappings, package checksum, and target environment access before import. It does not create OAuth connections, create the rule row, publish the agent, or enable the flows. Keep `settings.local.json` out of Git. A standard PAC deployment settings file can also be generated with `pac solution create-settings`; [Microsoft documents this mechanism](https://learn.microsoft.com/en-us/power-platform/alm/conn-ref-env-variables-build-tools).

## 6. Add the rule and publish

1. In the imported solution, open **Calendar Governance Rule** and its data. Check existing active rows before adding anything.
2. If the approved rule already exists, reuse it. Otherwise create one row, using **Protect board meetings** as the name and the exact rule text from [meeting-rule.json](../deployment/meeting-rule.json):

   > Board meetings are critical and cannot be moved. Any meeting that has "board meeting" in the subject is considered a board meeting.

3. Confirm the row is active and the Dataverse connection account can read it. Do not overwrite someone else's rules. An unsupported additional active rule deliberately blocks automatic resolution.
4. Check the test account's Outlook working days, opening and closing times, and time zone. Missing or invalid working hours stop a move; only weekdays are searched.
5. Save and publish the agent after checking its tool and authentication. Turn on **Check and move meeting**, then **Check new meeting**. Review any connection or permission prompts before proceeding.

Microsoft requires publishing an imported agent and configuring authentication in the target environment. See [agent solution import guidance](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-solutions-import-export).

## 7. Run the manual acceptance test

Use future temporary events without attendees, within the test account's working hours. Keep the starter off while preparing each set of existing events; enable it immediately before creating the new event that should trigger the test. Wait for processing before starting another scenario.

| Scenario | Expected calendar result | Expected notification |
| --- | --- | --- |
| New ordinary meeting with no overlap | Nothing moves; NoConflict | None |
| New ordinary meeting overlapping a board meeting, with free time available | Ordinary meeting moves; board meeting stays; duration preserved; Resolved | None |
| New board meeting overlapping an ordinary meeting, with free time available | Ordinary meeting moves; board meeting stays; Resolved | None |
| New board meeting overlapping another board meeting | Both remain unchanged; NeedsHelp | One notification attempt to the configured test assistant |
| Ordinary meeting conflict with no free interval in the search window | Nothing moves; NeedsHelp | One notification attempt |

Check actual Outlook times, the resolver's response, and the notification action, rather than just a green parent flow. For a successful send action, inspect Sent Items; it confirms submission, not recipient delivery. Preserve the result even when the test fails.

Record package version/checksum, target environment/tenant, date, configuration checks, each scenario's result, flow run IDs, and any screenshots with private data removed. Use [the acceptance record](../deployment/acceptance.md). This is the owner's independent proof of installation. Do not mark cross-tenant deployment as passed until the actual test completes.

## 8. Stop or remove the POC

Turn off **Check new meeting** first, let active runs finish, then turn off the resolver. Remove temporary calendar events. An import rollback or uninstall does not reverse calendar changes or sent emails.

This is an **unmanaged** POC for inspection and modification. Deleting its solution container does not remove all underlying components. A disposable environment is the cleanest way to remove the entire trial. Do not delete connections shared with other solutions.

## Maintenance and boundaries

To change mailbox or recipient, stop processing, update environment-variable current values and connection bindings together, then save/re-enable the flows and repeat acceptance checks. Never use a secondary calendar ID with the current primary-calendar Graph path.

The Gatekeeper's policy checks, final reads, If-Match write protection, and outcome verification remain in place. Missing or malformed mailbox/assistant settings return UnableToCheck before calendar access. The trigger needs a valid Calendar ID to operate. No mailbox lock or duplicate-request ledger is added here; requests can overlap. Use sequential POC tests and keep production-readiness claims separate.

For maintainers, [script instructions](../scripts/README.md) cover local checks and package rebuilding. [Architecture](architecture.md), [security](security.md), and [test evidence](testing.md) explain the enforcement boundary and its limits.
