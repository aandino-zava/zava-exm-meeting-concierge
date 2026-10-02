# Zava ExM Meeting Concierge implementation

This repository contains the solution I built in Zava PP Lab Dev. It was exported on October 1, 2026 using Microsoft's Power Platform CLI. Nothing in the live implementation was changed to create the repository.

## What connects it together

Outlook provides the calendar and sends the notification. Copilot Studio runs the agent. Dataverse stores the rules, and AI Builder helps the Gatekeeper interpret them.

The export includes five connection references, which tell the components which service connections to use. It does not include the sign-ins needed to use those services. When importing the solution elsewhere, connect it to the intended accounts. Some actions use a configured account, while others depend on the account used to call the flow. The [flow specification](../architecture/flows/ModifycalendarWithRuleCheck.md) records that distinction.

The calendar and assistant recipient are fixed to the lab's settings. They are not automatically replaced during import. Review both before turning on the automation.

## Start with a Dev environment

I use Dev as the editable home for this solution. I can build and test there, then prepare a reviewed release for UAT and, eventually, Prod. This project has not gone through those later stages.

If you need to build a similar lab first, follow my [Power Platform ALM lab setup guide](https://github.com/aandino-zava/zava-power-platform-lab/blob/main/docs/deployment-runbook.md). It covers the environment structure and deployment setup. The steps below cover this solution's own connections, rules, and settings.

## Setting it up in another environment

1. **Prepare a development environment.** It needs Dataverse, Copilot Studio, Outlook, and AI Builder access, with the required licensing. The Microsoft AI Classify component must also be available.
2. **Import the solution and connect the accounts.** Use the exported ZIP or one rebuilt from the source files. Choose the calendar and notification recipient for the new environment.
3. **Add the governance rule.** The export includes the table, but not the live rule stored in it. Add the [documented starting rule](../architecture/dataverse/rules-table.md) and decide who can edit it.
4. **Review the agent's tools and model.** The export still contains earlier setup tools that were disabled during the build. Check that only the intended tools are enabled; the exported files do not clearly preserve that distinction.
5. **Publish and enable.** Publish the agent, turn on the two flows, and check the behavior with controlled calendar examples before relying on it.

The solution was successfully exported, unpacked, and rebuilt into an import package. It has not been imported into a second environment, so those packaging checks do not establish that another deployment will work without configuration.

## A few details worth keeping clear

**Some internal names are older than the project name.** The project is Zava ExM Meeting Concierge. Earlier names remain inside platform files because changing them could break references. They were preserved in the export.

**The model setting differs from the earlier test notes.** The October 1 export records `GPT56Chat`; the September 30 notes recorded a reasoning-preview model. I have not established why they differ. Review the selected model before reusing the solution. Earlier test results describe the earlier runs.

For package versions, service dependencies, and the original files, see the [solution notes](../solution/README.md) and [export record](../solution/provenance.json). The [test results](testing.md) explain what was demonstrated and what was left untested.
