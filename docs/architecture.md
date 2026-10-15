# How the solution works

The solution uses one agent and two flows. The agent hands the new meeting ID to **Check and move meeting**. The flow performs the scheduling work with fixed checks and returns the actual outcome. The agent explains that outcome.

## Agreed behavior

- Subjects containing **board meeting**, regardless of capitalization, are protected.
- Keep the meeting length.
- Look for the next free time after the original meeting ends, through the end of the second following business day. Read working hours and time zone from Outlook getSchedule for the configured mailbox; search weekdays that are also present in the returned working days. Earlier Dev tests used Monday-Friday, 8 AM-5 PM Eastern; each installation reads its own connected account settings. Holidays are not modeled.
- Keep a final authoritative calendar read before writing.
- Email the configured assistant only when a confirmed conflict remains unresolved.
- Keep one agent. Do not let AI authorize calendar changes or select replacement times.

The portable POC configures one connected account and its primary calendar per installation; multi-executive production use remains outside scope.

## The two flows

**Check new meeting** listens for newly created events and asks the agent to call the resolver once. It polls once per minute. Trigger concurrency control is not configured, so requests can overlap.

**Check and move meeting** accepts only the new event ID. It reads the actual event and overlapping events, checks active rules, selects eligible meetings, finds a free time, verifies the target and destination again, changes the calendar, and reads the result back. The caller cannot choose a different subject or supply an authorization decision.

If the new meeting is movable, move that meeting. If it is protected, move its eligible conflicting meetings. If two protected meetings conflict, neither moves. More than ten proposed moves, unsupported event types, missing data, and incomplete result pages require review. Recurring occurrences, series masters, and all-day meetings are deliberately left for manual review in this release.

## Fixed policy checks

The flow recognizes the approved board-protection text stored in the existing Dataverse table. It compares normalized policy text to the supported rule and checks the actual event subject using a case-insensitive containment test. It does not interpret arbitrary prose.

An empty rule set or a new unsupported active rule blocks automatic resolution. Editing policy text is not a way to grant new automatic permissions. A new rule needs a matching reviewed check and tests. The existing platform schema names and solution identity are retained.

## Finding a time

For each eligible meeting, read busy intervals for the bounded search window, sort them, and scan working days in order. Begin no earlier than the original meeting end, working-day opening, or the current time. Advance past any overlapping busy interval. Keep the first interval that fits the full meeting length before closing time.

This uses exact busy interval endpoints, not a model's estimate and not a fixed fifteen-minute grid. UTC calendar reads and explicit Outlook working-hour conversion handle daylight-saving changes. Touching endpoints do not overlap.

Before writing, reread the policy and target, require an unchanged nonempty ETag, and recheck the destination. PATCH uses If-Match and has no automatic retry. Read the changed event back, and finally check whether the original conflict is gone. An uncertain write is never reported as a confirmed resolution.

## Results and email

- **NoConflict:** no action was needed.
- **Resolved:** all selected moves were confirmed and the original conflict is gone. No email.
- **NeedsHelp:** a confirmed conflict remains unresolved. The flow attempts one assistant email.
- **UnableToCheck:** the checks did not establish an outcome. No successful resolution is claimed.

The response also includes the confirmed move count, whether help is needed, and whether the notification action succeeded. A successful email action establishes submission, not recipient delivery.

Only **Check and move meeting** remains as an agent tool. Outlook and Dataverse still operate inside that flow through saved connections. Removing an agent tool does not disable those flow connections.

## Why the reads remain

The flow reads the event rather than trusting AI-supplied event details. Its scheduling read supports candidate selection. Its final reads detect changed policy, stale targets, and new destination bookings. The post-write reads confirm the result. Each read has a distinct purpose; the agent no longer repeats those reads for the automatic path.

## Boundaries

The event ETag does not reserve the destination slot. An external user can book it after the last check. Final reconciliation detects an observed remaining conflict but does not eliminate this race.

Neither automatic nor direct requests have a durable mailbox lock. Simultaneous requests can compete for the same free interval. A durable request ledger, stronger identity restrictions, verified role assignments, multi-executive rule scope, and isolated UAT remain production work. This Dev implementation does not claim those controls are complete.

Local workflow simulations are separate from live platform tests. See the test evidence for exactly what was run.


## Why this is simpler

The flow searches for the time and enforces the supported board rule with fixed checks. One agent tool replaces separate reads, scheduling, and notification choices.

The agent remains to demonstrate Copilot Studio integration and explain results. This fixed process could also run without an agent; AI is not required to authorize a move.

See [Setup and maintenance](deployment.md) for native source locations and [Demo guide](demo.md) for the interview walkthrough.

## Portable POC configuration

The package declares all three required connection references, including Dataverse, and uses three required environment variables: Calendar mailbox, Calendar ID, and Executive assistant email. No lab values are supplied as defaults. Both flows are packaged off. A configuration check rejects missing or malformed mailbox/assistant email values before calendar access. The trigger uses the configured Calendar ID.

Graph reads and writes still use `/me`, so the configured mailbox and trigger Calendar ID must belong to the Outlook connection account's primary calendar. Configuration does not add support for shared or secondary calendars. The installer verifies this identity match. The agent cannot supply or override these settings. See [installation steps](deployment.md).

## Deployment boundary

GitHub Actions builds and checks the source without tenant access. Only an explicitly requested deployment from main can use the selected GitHub environment's federated identity and target settings. The receiving tenant authorizes that identity and its connections. Deployment imports a checked package and verifies components; it does not change the Gatekeeper's rules or grant the conversational agent new tools. Agent authentication/publication and calendar acceptance remain explicit setup steps.
