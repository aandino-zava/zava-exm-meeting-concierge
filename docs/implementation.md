# Zava ExM Meeting Concierge implementation

## Source and configuration

PAC 2.12.2 exported the existing unmanaged version 1.0.0.0 from Zava PP Lab Dev on October 1, 2026. The source solution and agent display names are Zava ExM Meeting Concierge. No live configuration was changed for the repository work.

## Connections

| Reference role | Exported connector | Observed use |
| --- | --- | --- |
| Trigger agent execution | shared_microsoftcopilotstudio | Embedded connection in trigger |
| Trigger and guarded event operations | shared_office365 | Embedded trigger; invoker in Gatekeeper |
| Agent Dataverse lookup and AI classification | shared_commondataserviceforapps | Maker agent tool; embedded flow |
| Agent calendar reads and notification | shared_office365 | Maker tools |
| Earlier Entra HTTP setup | shared_webcontents | Retained reference for setup tool |

Five connection references are included. OAuth credentials and authenticated connections are not exported with the solution. The importer must supply valid connections and review the invoker/maker contexts.

## Environment variables

There are no environment-variable definitions in this export. The trigger calendar identifier and notification recipient are fixed in the assets. The rule lookup uses the current environment. These settings require explicit review after import; there is no implemented environment-variable abstraction to claim here.

## Deployment checklist

1. Prepare a separate Dataverse development environment with Copilot Studio, Office 365 Outlook, and AI Builder capabilities and appropriate licensing.
2. Make the Microsoft AI Classify dependency available. Solution.xml declares the PowerAI / msdyn_AISolutionDefaultTemplates dependency, version 202608.1.4.1.
3. Import the original or PAC-repacked unmanaged ZIP. Resolve connection references using the intended owner/invoker accounts.
4. Choose the correct Outlook calendar and replace the fixed lab recipient in the target environment before enabling unattended execution.
5. Seed the documented active rule row. Restrict rule-edit access appropriately.
6. Review the four intended tools and the retained setup tools; the export does not clearly preserve the UI enablement distinction. Confirm model selection.
7. Publish the agent and enable the two flows only after reviewing the target configuration. Run controlled acceptance checks before operational use.

The export/pack validation does not prove import portability or runtime success in another environment. This task did not import into another environment or rerun calendar scenarios.

## Retained internal naming

Native files retain the solution unique name, bot schema prefix, trigger workflow name/filename, generated connection-reference display names, and related component paths from initial development. These belong to the unchanged export. They are not the repository's product name. Removing them cosmetically would make this baseline diverge from the actual deployment and could break references.

## Known differences from the prior report

The October 1 export records GPT56Chat as the model hint, while September 30 test notes recorded a reasoning-preview selection. The native enforcement workflow ID is 80614549-fdbc-f111-aaad-6045bd067e6d and is used by both its bot action and relationship; historical runtime URL identifiers differ. The source files take precedence for current exported configuration; the earlier observations remain historical evidence only.
