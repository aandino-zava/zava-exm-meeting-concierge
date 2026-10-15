# Test evidence

## Package and workflow checks

The solution package contains three connection references, three required environment variables without lab defaults, and inactive initial flow states. The official Power Platform CLI packed and unpacked it and generated deployment settings containing all three variables and connections.

The [GitHub Actions build](https://github.com/aandino-zava/zava-exm-meeting-concierge/actions/runs/38782964607) passed and saved the solution ZIP and checksum. Checks include:

- **27 scheduling simulations** against the workflow action definitions, using simulated calendar and policy services.
- **Six package checks** covering dependencies, configuration, inactive flows, package contents, and required README sections.
- **Six post-import verification tests** covering complete components and rejection of enabled flows, missing connections/configuration, incorrect tool bindings, and mismatched internal revisions.
- PowerShell import safeguards for missing settings, invalid targets, checksum mismatch, explicit target selection, and validation without tenant access.
- Source format, local link, archive integrity, fingerprint, credential-pattern, and single-agent-tool checks. Workflow linting also passed locally.

These checks do not authenticate runtime connectors or prove calendar behavior in a receiving tenant. The scheduling interpreter is a limited workflow-expression simulator, not the Microsoft runtime.

## Recorded Dev configuration

The authenticated **Zava PP Lab Dev** export dated October 15, 2026 contains one agent tool, **Check and move meeting**, two flows, and one governance table. Outlook and Dataverse use embedded flow connections. The starter has no concurrency control configured.

The live results below predate the portable configuration changes and the removal of the starter's sequential-run setting. They establish behavior for the tested Dev configuration, not a cross-tenant deployment or concurrency guarantee. The source packages and fingerprints preserve that distinction.

## Recorded live tests

Tests ran in Dev on October 15, 2026. Calendar times are Eastern.

| Scenario | Observed result | Evidence |
| --- | --- | --- |
| Agent call without conflict | NoConflict; no move, no email, no sign-in prompt | Copilot Studio test session |
| Automatic ordinary meeting versus board meeting | Planning moved from 10:00-10:30 to 11:00-11:30 on October 20. Board meeting stayed 10:00-11:00. Resolved; one move, no email. | Starter run `08584095458440334550013174027CU28` and independent Outlook read |
| Automatic two protected meetings | Both stayed unchanged. NeedsHelp; zero moves, notificationSent true. One new help email appeared in sent mail. | Starter run `08584095457683799364846773689CU01` and independent calendar/email reads |
| Direct calendar flow | Permitted moves and protected conflicts behaved as expected; working hours and Eastern time zone were checked | [Detailed Dev evidence](history/v2-build-record.md) |

All seven temporary events were removed. No attendees were invited. A successful notification action and sent-mail entry establish submission to Outlook, not recipient delivery.

The [archived test records](history/README.md) retain failed attempts, partial verification, and untested scenarios. Those results are not counted as passes.

## Target deployment acceptance

**Federated deployment and live acceptance in a receiving tenant have not been verified.** Complete [the acceptance record](../deployment/acceptance.md) after following the [deployment instructions and calendar scenarios](deployment.md#test-the-installed-solution).

The pipeline's deployment job imports the checked artifact and re-exports it to temporary runner storage. Its structural checks verify solution identity/revision, required components, one Gatekeeper tool, connection declarations, configuration definitions, and inactive flow states. They do not establish connection permissions, rule visibility, agent authentication/publication, or live calendar outcomes.

Verify actual calendar times, resolver responses, and notification action results. A successful parent flow or package build alone is insufficient evidence of a resolved meeting conflict.

## Run the local checks

From the repository root, follow [the script instructions](../scripts/README.md). Run `scripts/test_resolver.py`, `scripts/test_deployment.py`, and `scripts/test_verify_import.py`; PowerShell import safeguards are in `scripts/test-import.ps1`.

The scheduling cases cover ordinary and protected conflicts, no conflict, adjacent meetings, missing/unsupported rules, incomplete pages, changed events, a newly booked destination, write failures, no available slot, multiple conflicts, recurring/all-day events, missing events, fixed authorization, subject injection, weekends, daylight saving, and configured email values.
