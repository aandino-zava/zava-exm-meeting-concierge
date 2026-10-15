# V1 component notes

Original specifications. Native source links below point to the V1 archive. For current behavior, read [How it works](../architecture.md).

---

Source: `architecture/agent/zava-exm-meeting-concierge.md`

# Zava ExM Meeting Concierge agent

The agent orchestrates one calendar-governance workflow. It is not a collection of independent agents. The instructions require runtime rules, authoritative event reads, strict conflict checks, duration preservation, and a search bounded to two business days.

Historical implementation notes recorded these four enabled tools:

| Tool | Responsibility |
| --- | --- |
| GetActiveCalendarGovernanceRules | Fixed current-environment active-rule query |
| ReadCalendarGraphViaOutlook | Graph event and calendarView GET |
| ModifycalendarWithRuleCheck | Independent calendar-write flow |
| NotifyExecutiveAssistant | Fixed-recipient outcome notification |

The export also includes duplicate Dataverse tools, a preauthorized Entra HTTP tool, and a getSchedule attempt. They were recorded as disabled during implementation. Their component XML uses ordinary active record states and does not clearly encode the UI disabled status. Do not interpret record state as proof of runtime tool enablement. Review these tools in Copilot Studio after import.

The exported instruction component records `modelNameHint: GPT56Chat`. The historical successful test notes recorded GPT5ReasoningPreview. No new functional run was performed for this export, and no cause is asserted for this difference. Confirm model selection and published behavior before reuse.

Web browsing is disabled. Configuration enables generative actions, model knowledge, file analysis, and semantic search, with content moderation recorded as Low and latest-model opt-in false. These are observed export settings, not general recommendations.

The fixed GET method constrains calendar writes, but the calendar URI scope is described in the tool instructions rather than enforced by a dedicated URI allowlist in the exported tool. Outlook permissions and governance access should be reviewed for production use.

[Instructions](../../solution/exports/ZavaExMMeetingConcierge_1_0_0_0_unmanaged.zip) · [Bot configuration](../../solution/exports/ZavaExMMeetingConcierge_1_0_0_0_unmanaged.zip)


---

Source: `architecture/dataverse/rules-table.md`

# Zava ExM Meeting Concierge governance rules

| Schema item | Exported value |
| --- | --- |
| Table schema | cr9b0_CalendarGovernanceRule |
| Logical name | cr9b0_calendargovernancerule |
| Entity set | cr9b0_calendargovernancerules |
| Primary ID | cr9b0_calendargovernanceruleid |
| Primary name | cr9b0_name, maximum 850 characters |
| Rule text | cr9b0_ruletext, multiline, maximum 10000 characters |
| Ownership | User owned |
| Active filter | statecode eq 0 |

The agent and Gatekeeper retrieve the name, rule text, and rule ID. Natural-language text supplies the policy semantics; there are no separately implemented protection keyword/category fields. The enforcement flow rejects empty or paginated rule results rather than treating an incomplete read as permission.

Create an active row named Initial Calendar Governance Rule after import, with this historical baseline text:

> Board meetings are critical and cannot be moved. Any meeting that has "board meeting" in the subject is considered a board meeting.

This is a documented seed value from the implementation record, not an exported Dataverse data row. Standard solution export carries schema, forms, views, and relationships, not the live policy record. Limit who can edit policy because the agent and flow interpret it as governance input.

[Native table XML](../../solution/exports/ZavaExMMeetingConcierge_1_0_0_0_unmanaged.zip)


---

Source: `architecture/flows/ModifycalendarWithRuleCheck.md`

# Zava ExM Meeting Concierge calendar modification contract

`ModifycalendarWithRuleCheck` is a Skills request flow and the agent's only configured calendar modification action.

| Request property | Meaning |
| --- | --- |
| `text` | eventId, authoritative Graph target ID |
| `text_1` | requestedStart, ISO8601 UTC ending Z |
| `text_2` | requestedEnd, ISO8601 UTC ending Z |
| `text_3` | reason, explanatory prose only |

All four inputs are required strings. The agent tool adds explicit descriptions for the last two properties; the flow trigger itself retains generic descriptions for those fields. These are distinct exported surfaces and have not been cosmetically rewritten.

The actions are authoritative event GET → List_rows → Read_current_conflicts → Filter_array → Run_a_prompt → Condition → Respond_to_Copilot. PATCH is nested inside the true condition branch. [Gatekeeper details](../../solution/exports/ZavaExMMeetingConcierge_1_0_0_0_unmanaged.zip) describe the precise guards and limits.

The output is a `result` string. Confirmed success includes the requested start and end. A PROTECTED classification returns the exact board-protection message. Other outcomes report that authorization or completion failed and that no successful modification was confirmed.

Outlook has `runtimeSource: invoker`; Dataverse has `runtimeSource: embedded`. The invoking agent's run context and connection configuration matter. Do not assume that every connection in the solution uses the same identity mode.

The exported workflow ID is `80614549-fdbc-f111-aaad-6045bd067e6d`. The bot action and workflow relationship both reference this ID. Historical Power Automate runtime URLs used a different flow identifier; the native exported ID is retained as the source-control reference.

[Actual JSON](../../solution/exports/ZavaExMMeetingConcierge_1_0_0_0_unmanaged.zip) · [Bot action](../../solution/exports/ZavaExMMeetingConcierge_1_0_0_0_unmanaged.zip)


---

Source: `architecture/flows/trigger-flow.md`

# Zava ExM Meeting Concierge trigger flow

**Purpose:** react to a newly created event and invoke the agent autonomously.

**Input:** Outlook CalendarGetOnNewItemsV3 results, split into individual events. The exported calendar value is a fixed lab calendar identifier. The recurrence is one minute.

**Action:** ExecuteCopilotAsyncV2 invokes the retained agent schema with the new event ID embedded in an explicit request to complete rule lookup, conflict handling, guarded modification, and qualifying notification.

**Output:** connector execution result from the agent. This flow has no custom response action or independent fallback notification branch.

**Dependencies:** embedded Outlook and Copilot Studio connection references, an available published agent, and a configured calendar. A connector or agent error can fail the invocation; do not infer successful mutation from trigger success alone.

**Export:** [native JSON](../../solution/exports/ZavaExMMeetingConcierge_1_0_0_0_unmanaged.zip). The export retains the original trigger flow display name and filename. Repository prose uses the canonical project name. The workflow ID is `f5621481-00bd-f111-aaad-6045bd06703e`.


---

Source: `architecture/tools/microsoft-graph.md`

# Zava ExM Meeting Concierge Microsoft Graph tools

| Operation | Use | Boundary |
| --- | --- | --- |
| GET /v1.0/me/events/{encodedEventId} | Authoritative target event | Agent reads and flow independently reads |
| GET /v1.0/me/calendar/calendarView | Expanded occurrences and busy intervals | Agent searches all pages; flow rejects incomplete current-conflict results |
| PATCH /v1.0/me/events/{encodedEventId} | Start and end update | Only inside Gatekeeper permitted branch |

The actual connector is Office 365 Outlook HttpRequest. The agent read action has Method fixed to GET. The Gatekeeper URL is assembled from the event ID, and its PATCH body sets start/end dateTime and timeZone UTC. Its header is `If-Match` with the authoritative event's `@odata.etag`.

Conflict means `other.start < target.end AND other.end > target.start`, with a different event ID, isCancelled false, and showAs not free. Touching endpoints do not overlap. Recurring occurrences are inspected through calendarView; series masters are not movable through the flow.

A fixed POST getSchedule setup tool is present but was recorded as disabled because its exposed file-body input was unsuitable. A preauthorized Entra GET tool is also retained from setup after unsuccessful reads. Neither is presented as a working-hours capability. The implemented fallback is Monday–Friday 09:00–17:00 in originalStartTimeZone.

[Read action](../../solution/exports/ZavaExMMeetingConcierge_1_0_0_0_unmanaged.zip) · [Notification action](../../solution/exports/ZavaExMMeetingConcierge_1_0_0_0_unmanaged.zip)
