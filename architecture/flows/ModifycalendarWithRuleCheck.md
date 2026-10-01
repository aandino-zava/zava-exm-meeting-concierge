# Zava ExM Meeting Concierge calendar modification contract

`ModifycalendarWithRuleCheck` is a Skills request flow and the agent's only configured calendar modification action.

| Request property | Meaning |
| --- | --- |
| `text` | eventId, authoritative Graph target ID |
| `text_1` | requestedStart, ISO8601 UTC ending Z |
| `text_2` | requestedEnd, ISO8601 UTC ending Z |
| `text_3` | reason, explanatory prose only |

All four inputs are required strings. The agent tool adds explicit descriptions for the last two properties; the flow trigger itself retains generic descriptions for those fields. These are distinct exported surfaces and have not been cosmetically rewritten.

The actions are authoritative event GET → List_rows → Read_current_conflicts → Filter_array → Run_a_prompt → Condition → Respond_to_Copilot. PATCH is nested inside the true condition branch. [Gatekeeper details](../../docs/gatekeeper-pattern.md) describe the precise guards and limits.

The output is a `result` string. Confirmed success includes the requested start and end. A PROTECTED classification returns the exact board-protection message. Other outcomes report that authorization or completion failed and that no successful modification was confirmed.

Outlook has `runtimeSource: invoker`; Dataverse has `runtimeSource: embedded`. The invoking agent's run context and connection configuration matter. Do not assume that every connection in the solution uses the same identity mode.

The exported workflow ID is `80614549-fdbc-f111-aaad-6045bd067e6d`. The bot action and workflow relationship both reference this ID. Historical Power Automate runtime URLs used a different flow identifier; the native exported ID is retained as the source-control reference.

[Actual JSON](../../solution/unpacked/Workflows/ModifycalendarWithRuleCheck-80614549-FDBC-F111-AAAD-6045BD067E6D.json) · [Bot action](../../solution/unpacked/botcomponents/cr9b0_ZavaCalendarGovernanceAgent.action.ModifycalendarWithRuleCheck/data)
