# Zava ExM Meeting Concierge testing

These are historical observations from the September 30 build, not tests newly executed against the October 1 export. No results were fabricated or inferred from repacking. “Blocked — waived” marks an unexecuted scenario that the user removed from the remaining test scope; it is not a platform failure. The full final no-conflict E2E remains incomplete.

## Normal meeting with no conflict

- **Purpose:** verify normal meeting with no conflict behavior.
- **Setup:** Create a normal event with only an adjacent, non-overlapping event.
- **Expected:** No search, move, or notification.
- **Observed:** Initial autonomous run moved unnecessarily. Strict overlap gating was corrected; a later flow regression returned an empty conflict filter and did not PATCH. Final autonomous scenario was not repeated.
- **Status:** Blocked for full final E2E; flow regression Passed.
- **Components:** Agent, conflict filter, Gatekeeper.
- **Evidence:** 08584108114374449731697095118CU25.


## Normal meeting conflicting with a board meeting

- **Purpose:** verify normal meeting conflicting with a board meeting behavior.
- **Setup:** A 30-minute normal event overlaps an existing protected board meeting.
- **Expected:** Move only the normal event and preserve duration.
- **Observed:** Live agent demonstration moved the normal event from 14:00–14:30 UTC to 14:30–15:00 UTC on October 1; Graph confirmed board unchanged.
- **Status:** Passed.
- **Components:** Agent, Graph, Gatekeeper.
- **Evidence:** Live agent session; no durable run ID recorded in the available summary.


## New board meeting conflicting with normal meeting

- **Purpose:** verify new board meeting conflicting with normal meeting behavior.
- **Setup:** New protected board event overlaps a normal event at 11:00–11:30 AM EDT on October 1.
- **Expected:** Preserve board, move normal, send actual outcome notification.
- **Observed:** Final automatic run moved normal to 11:30 AM–12:00 PM EDT; board unchanged. Success message appeared in Sent Items at 3:30 PM September 30. Recipient delivery/read not verified.
- **Status:** Passed.
- **Components:** Trigger, agent, Gatekeeper, notification.
- **Evidence:** Trigger 08584108103541098475962594378CU18; Gatekeeper 08584108102580689374781356824CU28.


## Attempted protected board modification

- **Purpose:** verify attempted protected board modification behavior.
- **Setup:** Invoke enforcement against the protected target with proposed replacement timestamps.
- **Expected:** Reject and leave event unchanged.
- **Observed:** Returned Board meetings are protected and cannot be moved after independent reads; board unchanged.
- **Status:** Passed.
- **Components:** Gatekeeper, Graph, Dataverse, AI Classify.
- **Evidence:** 08584108118253875832227990286CU11.


## Case insensitive protection

- **Purpose:** verify case insensitive protection behavior.
- **Setup:** Use uppercase, title-case, and lowercase board-meeting subjects.
- **Expected:** Interpret subject-based rule without case dependence.
- **Observed:** Uppercase passed at flow level; title-case and lowercase passed in agent demonstrations. Not a complete parameterized suite.
- **Status:** Passed for observed cases.
- **Components:** Agent interpretation and Gatekeeper.
- **Evidence:** Historical implementation observation; no complete run set retained.


## Two board meetings conflicting

- **Purpose:** verify two board meetings conflicting behavior.
- **Setup:** Two protected meetings overlap. Setup was not executed as a final scenario.
- **Expected:** Neither moves; qualifying new protected conflict is reported.
- **Observed:** Not tested. User waived the remaining scenario.
- **Status:** Blocked — waived, not a technical blocker.
- **Components:** Agent selection, Gatekeeper, notification.
- **Evidence:** None.


## No replacement slot

- **Purpose:** verify no replacement slot behavior.
- **Setup:** A movable conflicting event has no qualifying slot within two business days. Setup was not executed as a final scenario.
- **Expected:** Leave unchanged and report no-slot outcome; notify if qualifying.
- **Observed:** Not tested. User waived the remaining scenario.
- **Status:** Blocked — waived, not a technical blocker.
- **Components:** Agent search and notification.
- **Evidence:** None.


## Dynamic Dataverse rule modification

- **Purpose:** verify dynamic dataverse rule modification behavior.
- **Setup:** Temporarily change only the Dataverse rule to protect the normal test event.
- **Expected:** Agent and Gatekeeper independently apply new policy without instruction/flow edits.
- **Observed:** Agent read changed policy; flow denied the now-protected normal event and did not move it. Original rule restored. Further verification later waived.
- **Status:** Passed for completed demonstration.
- **Components:** Dataverse, agent lookup, independent flow lookup and classification.
- **Evidence:** 08584108117138635358821195306CU23.


## Protected event without a real conflict

- **Purpose:** verify protected event without a real conflict behavior.
- **Setup:** New protected event has only a touching endpoint with another event.
- **Expected:** No move and no notification.
- **Observed:** Recorded automatic run ignored adjacency and performed neither action.
- **Status:** Passed.
- **Components:** Trigger, agent strict overlap.
- **Evidence:** 08584108116049867791990576046CU05.

## Corrections and evidence limits

Earlier connection/query failures and a start/end/reason mapping problem preceded the final successful run. The last two input descriptions were corrected in the agent tool. Those failures are not counted as passes. There was no new E2E run after the display-name publication, and none during this repository task.

The [sanitized evidence register](../tests/evidence/README.md) retains run references and specific observations. Raw run payloads, screenshots of mailbox pages, and the prior Word report are excluded because they include unnecessary identity and environment context. The register is a human-authored record, not an exported run log. Source-control validation is reported separately in [validation](validation.md).
