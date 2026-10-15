# Portable package checks and live evidence

## Package checks

The solution package includes the Dataverse connection reference, three required environment variables without lab defaults, and inactive initial flow states. The official Power Platform CLI packed/unpacked it and generated a settings file containing all three variables and all three connections. All three variable definitions are present in the ZIP, survive unpacking, and are recognized by create-settings. This is not a successful target import claim.

All **27 scheduling simulations** and **six deployment checks** pass locally. New cases exercise a different mailbox, the configured assistant recipient, and invalid/missing settings stopping before service access. These are simulated services and static package checks, not Microsoft runtime tests.

**Independent target deployment: not yet run.** The owner will test the installation guide in a separate environment and record results in [the acceptance record](../deployment/acceptance.md). The portable package has not been deployed to live Dev as part of this repository change.

## Earlier Dev evidence

The following evidence describes earlier implementation snapshots and must not be used as proof of a cross-tenant import.

### Recorded Dev snapshot

On October 15, 2026, the owner removed the seven retired tools and reported satisfactory manual testing. A fresh authenticated export from **Zava PP Lab Dev** confirms:

- One agent tool remains: **Check and move meeting**.
- There are two flows and one governance table.
- The calendar-flow definition is unchanged from the version used in the recorded automatic tests below.
- The starter no longer has concurrency control configured. This snapshot does not promise one-at-a-time processing.
- Outlook and Dataverse remain embedded flow connections.

All 22 local workflow checks, source/link/fingerprint checks, and the official PAC package rebuild passed against this refreshed snapshot. Both original PDF reports were verified byte-for-byte unchanged.

No new run IDs were supplied for the owner's manual tests. No new live calendar tests were performed for this repository-only refresh.

### Recorded live tests

These tests ran in Dev on October 15, before the latest tool removal and starter-setting change. Times are Eastern.

| Scenario | Observed result | Evidence |
| --- | --- | --- |
| Fresh agent call without conflict | NoConflict; no move, no email, no sign-in prompt | Copilot Studio test session |
| Automatic ordinary meeting versus board meeting | Planning moved from 10:00-10:30 to 11:00-11:30 on October 20. Board meeting stayed 10:00-11:00. Resolved; one move, no email. | Starter run `08584095458440334550013174027CU28` and independent Outlook read |
| Automatic two protected meetings | Both stayed unchanged. NeedsHelp; zero moves, notificationSent true. One new help email appeared in sent mail. | Starter run `08584095457683799364846773689CU01` and independent calendar/email reads |
| Direct calendar flow | Permitted moves and protected conflicts behaved as expected; working hours and Eastern time zone were checked | [Detailed Dev evidence](history/v2-build-record.md) |

All seven temporary events were removed. No attendees were invited. A successful notification action and sent-mail entry establish submission to Outlook, not recipient delivery.

## Running current local checks

Run `python scripts/test_resolver.py` and `python scripts/test_deployment.py` from the repository root. The 27 cases execute the current calendar-flow definitions against in-memory services. They cover ordinary and protected conflicts, no conflict, adjacent meetings, missing/unsupported rules, incomplete pages, changed events, a newly booked destination, write failures, no available slot, multiple conflicts, recurring/all-day events, missing events, fixed authorization, nesting, subject injection, weekends, and daylight saving.

This limited workflow-expression interpreter does not authenticate connectors, execute the starter, test parallel requests, or replace live platform tests. Source checks also validate file formats, links, archive integrity, fingerprints, credential patterns, and the single agent tool.

Follow the [demo guide](demo.md) to repeat live checks. Verify actual calendar times and the returned outcome as well as a green run indicator. [Earlier evidence](history/README.md) retains waived tests and failed attempts as recorded.

## GitHub Actions deployment checks

The workflow runs source validation, scheduling simulations, package checks, and PowerShell import safeguards before saving the build artifact. It passes workflow linting locally. Tenant deployment uses only that run's artifact and explicitly supplied target settings; pull requests and normal pushes cannot enter the deployment job. Deployment is restricted to main, uses GitHub federation, and serializes runs for the selected GitHub environment.

After import, the workflow re-exports the solution to temporary runner storage and checks the internal solution identity/revision, required components, one agent tool, connection declarations, configuration definitions, and inactive flow states. These structural checks do not prove connection permissions, rule visibility, agent publication, or live calendar behavior. No live federated deployment has been verified yet. Complete [the acceptance record](../deployment/acceptance.md) after the independent tenant test.
