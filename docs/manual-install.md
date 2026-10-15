# Manual installation

Use this route if you prefer to import a downloaded ZIP or cannot use GitHub Actions. **You do not need to do both routes.** GitHub Actions is the [main deployment path](deployment.md).

The receiving tenant's administrator still authorizes the account connections and supplies the target settings. A manual import does not require creating the GitHub deployment application or its federated trust.

## Download the solution

Download [ZavaExMMeetingConcierge.zip](../solution/exports/ZavaExMMeetingConcierge.zip) and [SHA256SUMS.txt](../solution/exports/SHA256SUMS.txt). Alternatively, download the **ZavaExMMeetingConcierge** artifact from a successful **Meeting Concierge** workflow run and extract it to obtain the solution ZIP and checksum. Import the inner solution ZIP, not GitHub's outer artifact archive or the repository source ZIP.

Check the downloaded solution:

```powershell
Get-FileHash ./solution/exports/ZavaExMMeetingConcierge.zip -Algorithm SHA256
```

Use the actual downloaded file path if different, and compare the result with `SHA256SUMS.txt`.

## Import into the target environment

1. Follow the [prerequisites, account connections, and calendar settings](deployment.md) sections of the deployment guide. Check that the Outlook account, configured mailbox, and primary Calendar ID agree.
2. If updating an existing installation, stop both flows and review a backup before importing.
3. In Power Apps, select the intended target environment, then **Solutions > Import solution** and choose `ZavaExMMeetingConcierge.zip`.
4. Map the three connection references to target connections and set Calendar mailbox, Calendar ID, and Executive assistant email. If the wizard skips these prompts, open the imported solution and set the connection bindings and environment-variable current values before enabling anything.
5. Wait for import completion and check the log. Verify both flows remain off. Inspect the agent's one tool and the starter's agent binding.
6. Follow **Finish setup and enable processing** and **Test the installed solution** in [the deployment guide](deployment.md): create/reuse the approved rule, configure agent authentication/access, publish the agent, enable the flows, and complete the calendar scenarios.

## Optional local CLI import

With the repository checkout, official Power Platform CLI, and target connections ready:

```powershell
Copy-Item ./deployment/settings.example.json ./deployment/settings.local.json
# Fill in the three settings and three target connection IDs.
pac auth create --environment 'https://YOUR-ORG.crm.dynamics.com'
./scripts/import-solution.ps1 -EnvironmentUrl 'https://YOUR-ORG.crm.dynamics.com' -SettingsFile ./deployment/settings.local.json
```

The helper validates inputs and checksum, verifies target access, and imports. It does not create connections, add rule data, publish the agent, or enable processing. Never commit the completed settings. Complete the same setup and acceptance steps as a UI import.
