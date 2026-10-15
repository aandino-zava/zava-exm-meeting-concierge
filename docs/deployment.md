# Setup and maintenance

This release updates the existing unmanaged solution in Zava PP Lab Dev. Keep its unique name, component IDs, and schema names. Use the V2 archive, not the historical V1 archive.

1. Confirm the intended environment and export a backup. This prevents changing the wrong environment and provides a rollback source.
2. Import the unmanaged package, bind the existing Outlook, Copilot Studio, and Dataverse connections, and publish. For this approved single-calendar pilot, the resolver uses the existing lab owner Outlook connection rather than asking each caller to sign in. Review run-only sharing before enabling that choice in another environment. Credentials and active rule rows are not in a solution ZIP.
3. Confirm the active rule in the existing Calendar Governance Rule table: `Board meetings are critical and cannot be moved. Any meeting that has "board meeting" in the subject is considered a board meeting.` Unsupported additional active rules block resolution.
4. Review fixed mailbox, calendar trigger ID, and Nancy's email in the native flow definitions. They are scoped to this lab. A different mailbox needs a reviewed deployment change.
5. Check Outlook working hours. The resolver reads getSchedule for the configured mailbox and uses returned hours/time zone, on weekdays only. Missing/invalid settings stop the move.
6. Enable **Check and move meeting**, publish the agent, then enable **Check new meeting**. The current starter has no concurrency control configured; do not assume requests run one at a time.
7. Use temporary events without attendees to test no conflict, a permitted move, two protected meetings, and an unavailable slot. Check actual calendar times and notification action status; a green parent flow alone is insufficient.
8. Remove temporary events, export the live solution, unpack it, update provenance, run source checks, and commit the reviewed changes.

For rollback, pause the automatic trigger and import the reviewed backup, restore connection bindings, republish the agent, and verify behavior before enabling the trigger. Rolling back a package does not reverse calendar changes or sent emails.

See [How it works](architecture.md), [test evidence](testing.md), and [scripts](../scripts/README.md). No production deployment is claimed.

## Native source

| Item | Source |
| --- | --- |
| Check new meeting | [Starter flow](../solution/unpacked/Workflows/Checknewmeeting-F5621481-00BD-F111-AAAD-6045BD06703E.json) |
| Check and move meeting | [Calendar flow](../solution/unpacked/Workflows/Checkandmovemeeting-80614549-FDBC-F111-AAAD-6045BD067E6D.json) |
| Agent instructions | [Instruction component](../solution/unpacked/botcomponents/cr9b0_ZavaCalendarGovernanceAgent.gpt.default/data) |
| Agent tool | [Single flow tool](../solution/unpacked/botcomponents/cr9b0_ZavaCalendarGovernanceAgent.action.ModifycalendarWithRuleCheck/data) |
| Meeting rule table | [Table definition](../solution/unpacked/Entities/cr9b0_CalendarGovernanceRule/Entity.xml) |

User-facing names remain easy to follow. Native solution identifiers and schema names are retained so existing platform references stay consistent.

The table is user owned. Rule text is `cr9b0_ruletext`, the display name is `cr9b0_name`, and the flow reads active rows from `cr9b0_calendargovernancerules`. A solution export contains the table definition, not the rule rows.
