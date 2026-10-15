> Archived Dev verification dated October 15, 2026. The tested starter used sequential processing; the current source does not configure that control. See [current test evidence](../testing.md).

# V2 verification

Tests are against Zava PP Lab Dev on October 15, 2026 unless marked as local simulation. Temporary events have no attendees or reminders. Times below are Eastern.

## Live results recorded so far

| Test | Observed result | Evidence |
|---|---|---|
| Direct resolver: new ordinary meeting conflicts with board meeting | Planning moved from 10:00-10:30 to 11:00-11:30 on October 19; board stayed 10:00-11:00. Resolution confirmed; notification action skipped. | Resolver run `08584095694758977058626530539CU28`; independent Outlook calendar read |
| Initial automatic test: second protected meeting | Parent trigger completed, but agent reported UnableToCheck and did not invoke resolver. This is a failed end-to-end test, not a successful resolution. | Trigger run `08584095692014001008919513827CU10`; Copilot Studio activity trace |
| Outlook configuration | Actual mailbox setting is Monday-Friday 08:00-17:00, Eastern Standard Time. This corrected an earlier 09:00 assumption. | Mailbox settings read; final workflow reads getSchedule |

The first resolver move predates the working-hours update. The updated flow was then checked directly:

| Test | Observed result | Evidence |
|---|---|---|
| Two protected meetings | Both stayed at their original times. The help email appeared in Outlook sent mail. | Resolver run `08584095684687595328803362507CU20`; independent calendar and email reads |
| Updated working-hours path | The new ordinary test meeting moved from 10:00-10:30 to 11:30-12:00, after the other bookings. Its Eastern time zone and 30-minute length were preserved. | Resolver run `08584095684424503411317845998CU01`; independent Outlook read |
| Agent tool format | Copilot Studio recognizes the flow and its eventId input after canonical YAML formatting. The agent selected it, then requested the caller's Outlook connection. | Copilot Studio test trace |

## Automatic tests using embedded connections

The tested flow and native export use embedded Outlook and Dataverse connections. The agent was published and both flows were enabled for the recorded tests.

- A fresh agent test returned NoConflict without a sign-in prompt, with no move and no email.
- Automatic trigger run `08584095458440334550013174027CU28` completed successfully. Its agent response was Resolved with one confirmed move and no email. An independent Outlook read confirmed that Planning moved from 10:00-10:30 to 11:00-11:30 on October 20, while BOARD MEETING stayed at 10:00-11:00.
- Automatic trigger run `08584095457683799364846773689CU01` returned NeedsHelp, zero confirmed moves, and notificationSent true. Independent Outlook reads confirmed both protected meetings remained at their original times and one new help email appeared in sent mail for this test.

The calendar trigger polls once per minute. The automatic run appeared after polling; a temporarily empty run list was not treated as success or failure.

## Local simulation

Run `python scripts/test_resolver.py`. The interpreter executes the exported action definitions against an in-memory calendar and policy service. It does not call Microsoft services or prove connector authentication.

The 22 cases cover a normal move, new protected meeting, two protected meetings, no conflict, touching endpoints, missing/unsupported/extra rules, incomplete pages, stale target, destination race, write failure, unavailable slot, multiple conflicts, recurrence, all-day events, missing event, fixed authorization, nesting limit, subject injection, weekend search, and daylight saving. Working-hour/time-zone behavior uses the verified 08:00-17:00 Eastern setting in the service mock.

## Limits

A successful notification action establishes submission to Outlook, not recipient delivery. Automatic requests run sequentially, but duplicate requests and parallel direct calls have no durable request ledger. A final slot read cannot reserve a destination against an external calendar user. No multi-executive, production role, or isolated UAT claim is made.

All four temporary calendar events were removed after the direct tests. No attendees were invited. The help email remains as test evidence. The final direct move returned status Resolved, movedCount 1, needsHelp false, and notificationSent false.

The three automatic-test events were also removed, and an independent calendar read confirmed the test date was empty. At the end of the test session, both flows were active and the agent was published. All seven temporary events from the direct and automatic tests have been removed.
