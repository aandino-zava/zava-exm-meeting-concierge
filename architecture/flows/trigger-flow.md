# Zava ExM Meeting Concierge trigger flow

**Purpose:** react to a newly created event and invoke the agent autonomously.

**Input:** Outlook CalendarGetOnNewItemsV3 results, split into individual events. The exported calendar value is a fixed lab calendar identifier. The recurrence is one minute.

**Action:** ExecuteCopilotAsyncV2 invokes the retained agent schema with the new event ID embedded in an explicit request to complete rule lookup, conflict handling, guarded modification, and qualifying notification.

**Output:** connector execution result from the agent. This flow has no custom response action or independent fallback notification branch.

**Dependencies:** embedded Outlook and Copilot Studio connection references, an available published agent, and a configured calendar. A connector or agent error can fail the invocation; do not infer successful mutation from trigger success alone.

**Export:** [native JSON](../../solution/unpacked/Workflows/ZavaCalendarGovernance-NewEvent-F5621481-00BD-F111-AAAD-6045BD06703E.json). The export retains the original trigger flow display name and filename. Repository prose uses the canonical project name. The workflow ID is `f5621481-00bd-f111-aaad-6045bd06703e`.
