# Zava ExM Meeting Concierge testing

These results derive from my testing on what I derived to be a completed build, a good enough MVP. Each Evidence entry explains what was checked and what that check supports.
Two scenarios I had orriginally planned for were left untested.

## Normal meeting with no conflict

- **Purpose:** verify normal meeting with no conflict behavior.
- **Setup:** Create a normal event with only an adjacent, non-overlapping event.
- **Expected:** No search, move, or notification.
- **Observed:** The first automatic run moved the meeting unnecessarily. After correcting the overlap check, a direct flow test found no conflict and made no calendar update. We did not repeat the complete automatic process after that fix.
- **Status:** Partial — the corrected flow passed; the complete automatic process was not retested.
- **Components:** Agent, conflict filter, Gatekeeper.
- **Evidence:** The recorded flow run showed an empty conflict list and no calendar update. This supports the flow fix, but does not establish that the complete automatic process passed.


## Normal meeting conflicting with a board meeting

- **Purpose:** verify normal meeting conflicting with a board meeting behavior.
- **Setup:** A 30-minute normal event overlaps an existing protected board meeting.
- **Expected:** Move only the normal event and preserve duration.
- **Observed:** Live agent demonstration moved the normal event from 14:00–14:30 UTC to 14:30–15:00 UTC on October 1; Graph confirmed board unchanged.
- **Status:** Passed.
- **Components:** Agent, Graph, Gatekeeper.
- **Evidence:** During the live agent demonstration, a follow-up calendar read confirmed that the normal meeting had moved and the board meeting had stayed at its original time.


## New board meeting conflicting with normal meeting

- **Purpose:** verify new board meeting conflicting with normal meeting behavior.
- **Setup:** New protected board event overlaps a normal event at 11:00–11:30 AM EDT on October 1.
- **Expected:** Preserve board, move normal, send actual outcome notification.
- **Observed:** Final automatic run moved normal to 11:30 AM–12:00 PM EDT; board unchanged. Success message appeared in Sent Items at 3:30 PM September 30. Recipient delivery/read not verified.
- **Status:** Passed.
- **Components:** Trigger, agent, Gatekeeper, notification.
- **Evidence:** Both flows completed successfully. A refreshed calendar showed the normal meeting at its new time and the board meeting unchanged. Outlook Sent Items also showed the success notification with both meetings and the old and new times. We did not verify delivery to the recipient's inbox.


## Attempted protected board modification

- **Purpose:** verify attempted protected board modification behavior.
- **Setup:** Invoke enforcement against the protected target with proposed replacement timestamps.
- **Expected:** Reject and leave event unchanged.
- **Observed:** Returned Board meetings are protected and cannot be moved after independent reads; board unchanged.
- **Status:** Passed.
- **Components:** Gatekeeper, Graph, Dataverse, AI Classify.
- **Evidence:** The flow returned “Board meetings are protected and cannot be moved,” and the recorded check confirmed that the board meeting had not changed.


## Case insensitive protection

- **Purpose:** verify case insensitive protection behavior.
- **Setup:** Use uppercase, title-case, and lowercase board-meeting subjects.
- **Expected:** Interpret subject-based rule without case dependence.
- **Observed:** The uppercase example passed in a direct flow test. Title-case and lowercase examples passed during agent demonstrations. We did not test every possible spelling or capitalization.
- **Status:** Passed for observed cases.
- **Components:** Agent interpretation and Gatekeeper.
- **Evidence:** The build notes record protection working for “BOARD MEETING,” “Q4 Board Meeting,” and a lowercase “board meeting” subject. These were individual checks during the build, rather than a complete test of every variation.


## Two board meetings conflicting

- **Purpose:** verify two board meetings conflicting behavior.
- **Setup:** Two protected meetings overlap. Setup was not executed as a final scenario.
- **Expected:** Neither moves; qualifying new protected conflict is reported.
- **Observed:** Not tested. This scenario was left outside the final demonstration scope.
- **Status:** Not tested — removed from the remaining test scope by agreement.
- **Components:** Agent selection, Gatekeeper, notification.
- **Evidence:** This scenario was not run, so there is no observed result to support a pass or failure. The expected behavior above describes what the agent is instructed to do.


## No replacement slot

- **Purpose:** verify no replacement slot behavior.
- **Setup:** A movable conflicting event has no qualifying slot within two business days. Setup was not executed as a final scenario.
- **Expected:** Leave unchanged and report no-slot outcome; notify if qualifying.
- **Observed:** Not tested. This scenario was left outside the final demonstration scope.
- **Status:** Not tested — removed from the remaining test scope by agreement.
- **Components:** Agent search and notification.
- **Evidence:** We did not run a calendar example with every eligible replacement time unavailable. The no-slot behavior remains an instruction that still needs a dedicated test.


## Dynamic Dataverse rule modification

- **Purpose:** verify dynamic dataverse rule modification behavior.
- **Setup:** Temporarily change only the Dataverse rule to protect the normal test event.
- **Expected:** Agent and Gatekeeper independently apply new policy without instruction/flow edits.
- **Observed:** Agent read changed policy; flow denied the now-protected normal event and did not move it. Original rule restored. Further verification later waived.
- **Status:** Passed for completed demonstration.
- **Components:** Dataverse, agent lookup, independent flow lookup and classification.
- **Evidence:** After changing only the Dataverse rule, the agent recognized the normal meeting as protected and the flow refused to move it. The meeting remained unchanged, and the original rule was restored afterward. This demonstrated a policy change without editing the agent instructions or the flow.


## Protected event without a real conflict

- **Purpose:** verify protected event without a real conflict behavior.
- **Setup:** New protected event has only a touching endpoint with another event.
- **Expected:** No move and no notification.
- **Observed:** Recorded automatic run ignored adjacency and performed neither action.
- **Status:** Passed.
- **Components:** Trigger, agent strict overlap.
- **Evidence:** The recorded automatic run treated the back-to-back meetings as non-overlapping and took neither action: it did not move a meeting or send a notification.

## Corrections and evidence limits

Earlier runs exposed connection problems and a mix-up between the requested end time and the explanation for the move. The agent tool's input descriptions were corrected before the final successful run. Those earlier failures are not counted as passes.

These results describe the behavior observed during the build. They do not guarantee every possible calendar situation will work. Mailbox screenshots and raw service responses are not included because they contain account details of my demo tenant. The [solution instructions](../solution/README.md#what-was-checked) separately explain what was checked in the exported package.
