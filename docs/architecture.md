# Zava ExM Meeting Concierge architecture

I separated calendar reasoning from calendar writes so the agent's decision is checked against current policy before it changes an event. The source is the actual October 1 export. Historical execution evidence comes from the September 30 implementation record.

## Runtime responsibilities

The trigger is a solution-aware cloud flow using `CalendarGetOnNewItemsV3`, a one-minute recurrence, and `splitOn` for returned events. It calls `ExecuteCopilotAsyncV2` and waits. A creation-only trigger avoids a move repeatedly triggering the same creation workflow.

The agent reads policy and calendar data, decides which event may move, and finds a replacement. If both events are movable, instructions select the newly created event; if both are protected, instructions leave both unchanged. Multiple conflicts require preserving every protected event and checking the proposed interval against returned busy events.

The Gatekeeper reads the actual event first, then the active rules, then the original interval's calendarView, then filters strict conflicts. AI Classify runs after those reads. A condition permits PATCH only when the independent classification and deterministic guards pass. This ordering is taken from the exported `runAfter` dependencies.

## Authority and identity

The boundary is architectural: enabled agent calendar reads are GET-only, while the single modification action calls the flow. It is not a tenant-wide permission boundary or an adversarial-security certification. Outlook connections still have their configured connector permissions. Governance table editors influence the policy and therefore require appropriate Dataverse access controls.

## Source map

- [Trigger JSON](../solution/unpacked/Workflows/ZavaCalendarGovernance-NewEvent-F5621481-00BD-F111-AAAD-6045BD06703E.json)
- [Gatekeeper JSON](../solution/unpacked/Workflows/ModifycalendarWithRuleCheck-80614549-FDBC-F111-AAAD-6045BD067E6D.json)
- [Agent instructions](../solution/unpacked/botcomponents/cr9b0_ZavaCalendarGovernanceAgent.gpt.default/data)
- [Connection reference metadata](../solution/unpacked/Other/Customizations.xml)
- [Rule table XML](../solution/unpacked/Entities/cr9b0_CalendarGovernanceRule/Entity.xml)
- [Standalone Mermaid](../architecture/architecture.mmd)

These are original platform definitions unpacked by PAC. The Markdown surrounding them is human-authored explanation.
