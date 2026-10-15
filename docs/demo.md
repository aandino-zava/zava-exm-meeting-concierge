# Demo guide

Open the configured test Outlook calendar, Copilot Studio Activity, and the two Power Automate flows. Use temporary meetings without attendees on a clear future weekday. The trigger polls once per minute; allow processing time.

## Explain the design

> I kept one agent and one scheduling tool. The flow checks the rules, finds a time, makes the change, and verifies the result. The agent explains it. The executive assistant is contacted only when a confirmed conflict still needs help.

Show **Check and move meeting**, then open that flow's Outlook and Dataverse actions. Those connections work inside the flow; the agent no longer needs separate tools for the same work.

## 1. No conflict

Create `Demo - BOARD MEETING`, 10:00-11:00, with no overlapping busy event. Wait for processing. Confirm NoConflict, no move, and no email. Protecting a meeting does not mean emailing about it every time.

## 2. Automatic resolution

Create `Demo - Planning`, 10:00-10:30. If 11:00-11:30 is free and within working hours, expect Planning to move there. The board meeting must stay put. Show the calendar and Resolved outcome; confirm the 30-minute length and no help email.

Explain that the flow chooses and verifies the time; the model does not authorize the move.

## 3. Human help

Create `Demo - Second board meeting`, 10:15-10:45. Expect both protected meetings to stay put, NeedsHelp, zero moves, and the help email to the configured assistant address. Check notificationSent and sent mail before claiming submission.

Explain that the automation stops where its rules stop. Remove the temporary meetings afterward. A green parent run alone is insufficient evidence.

## Questions to prepare for

**Could this run without an agent?** Yes. The fixed process could run in Power Automate. The retained agent demonstrates Copilot Studio integration and explains results.

**Can an admin add any rule as prose?** No. The flow supports the approved board-protection rule. New or unsupported active text blocks resolution until reviewed checks and tests are added.

**Why reread before a move?** A person may edit the meeting or book the destination during the search. Final reads catch changes observed then; they do not reserve the slot.

**Is it production ready?** This is a single-calendar Dev pilot. It does not establish all attendees' availability or support every event type. The current starter permits overlapping runs. A durable lock, duplicate-request tracking, stronger caller restrictions, verified roles, and isolated UAT remain production work.

See [How it works](architecture.md), [Security](security.md), and [Test evidence](testing.md).

## Demo in another tenant

Install using [the POC guide](deployment.md), supply the target primary calendar and assistant settings, and complete [the acceptance record](../deployment/acceptance.md). Use the actual configured assistant and working hours in your walkthrough. Retain the distinction between earlier Dev evidence and the new installation's results; a package check alone does not establish a successful import.
