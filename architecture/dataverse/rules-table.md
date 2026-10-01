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

[Native table XML](../../solution/unpacked/Entities/cr9b0_CalendarGovernanceRule/Entity.xml)
