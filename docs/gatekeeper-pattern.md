# Zava ExM Meeting Concierge Gatekeeper pattern

The key decision in this implementation is simple: the component proposing a calendar change does not get to approve its own proposal. `ModifycalendarWithRuleCheck` independently evaluates the proposed move.

## Actual enforcement sequence

1. Accept the event ID, requested start, requested end, and informational reason.
2. GET the target event from Microsoft Graph using the supplied ID.
3. Query active Dataverse governance rules with `statecode eq 0`.
4. Read the target's current interval and filter other busy, non-cancelled events with strict overlap.
5. Use the Microsoft AI Classify template with `ALLOW,PROTECTED,DENY`. The prompt uses the actual event, current rules, and proposed timestamps. It does not include the caller reason as authorization.
6. Require ALLOW, nonempty rules, no remaining rule or conflict page, a real conflict, a non-cancelled event that is not a series master, and positive unchanged duration.
7. PATCH the event with UTC times and an If-Match ETag header only inside the permitted branch.
8. Return confirmed success, the protected rejection, or a generic no-success-confirmed result. Required upstream errors do not reach an authorized PATCH.

The response action runs after success, failure, skip, or timeout of the condition. This does not guarantee a business response for every possible service outage; it establishes the configured response path. No write is authorized by a missing classification.

## What this pattern demonstrates

External policy, authoritative resource retrieval, independent evaluation, and a constrained mutation path can be reused for other agent-initiated changes. The calendar subject and body are treated as untrusted data. The agent's explanation is informational only.

## Limits of this implementation

The rule interpretation is AI-based. There is no claim of deterministic policy semantics or formal prompt-injection resistance. The deterministic checks validate duration and the existence of a current conflict; they do not independently recheck the replacement slot, business hours, or the two-business-day search horizon. The flow appends Z to Graph times and relies on the current UTC serialization. This should be reviewed before extending timezone behavior.

If-Match is intended to prevent overwriting a changed event when a usable ETag is supplied; the flow does not explicitly check for a nonempty ETag before PATCH. The configured rejection says “Board meetings are protected and cannot be moved” even when a later natural-language rule protects a different category. These are implementation limitations, not hidden production guarantees.

See the [actual flow definition](../solution/unpacked/Workflows/ModifycalendarWithRuleCheck-80614549-FDBC-F111-AAAD-6045BD067E6D.json) and [flow contract](../architecture/flows/ModifycalendarWithRuleCheck.md).
