# Zava ExM Meeting Concierge solution assets

This folder contains the actual solution exported from Zava PP Lab Dev on October 1, 2026.

- **`exports/`** contains the original unmanaged ZIP—the Power Platform package used for import.
- **`unpacked/`** contains the same solution separated into files by Microsoft's Power Platform CLI, so changes to the flows, agent, and table can be reviewed in Git.
- **`provenance.json`** records the export version, component counts, and file fingerprints. Those fingerprints help detect whether the saved export has changed.

The platform-generated names and references are preserved so the files stay consistent with the deployed solution.

## What was checked

The export completed successfully, and Microsoft's tooling was able to rebuild the source files into a solution ZIP. The saved files also passed format checks.

That gives another developer a usable starting package and source files that can be rebuilt. It does **not** prove the solution has been deployed successfully in another environment. That still requires the right connections, settings, and a separate test.

Calendar behavior was checked during the build. See the [test results](../docs/testing.md) for what worked, what needed a fix, and what was not tested.

## What is included

The package contains one agent, two flows, the governance table, five connection references, 22 agent components, a generated AI Skill Config, and the supporting platform definitions.

## What needs configuration after import

The package does not carry account sign-ins, the active rule stored in Dataverse, calendar meetings, emails, or run history. Add the starting rule and connect the intended accounts.

The calendar and assistant recipient are fixed to the lab's values. Review them before enabling the automation. Also check the model and enabled tools: earlier setup tools remain in the export, and the files do not clearly show which were disabled in the editor.

## Required Microsoft component

The Gatekeeper uses Microsoft's AI Classify component. It must be available in the destination environment. The exact dependency is recorded in `unpacked/Other/Solution.xml` as PowerAI / msdyn_AISolutionDefaultTemplates, version 202608.1.4.1.

Follow the [setup instructions](../docs/implementation.md) before turning on the imported solution.
