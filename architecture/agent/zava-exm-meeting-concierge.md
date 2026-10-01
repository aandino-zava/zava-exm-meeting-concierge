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

[Instructions](../../solution/unpacked/botcomponents/cr9b0_ZavaCalendarGovernanceAgent.gpt.default/data) · [Bot configuration](../../solution/unpacked/bots/cr9b0_ZavaCalendarGovernanceAgent/configuration.json)
