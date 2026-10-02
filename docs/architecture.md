# Zava ExM Meeting Concierge architecture

I built this around one simple idea: let the agent work out a scheduling problem, then check its proposed change before touching the calendar.

Zava ExM Meeting Concierge looks for conflicts, reads the current meeting rules, and finds a replacement time. A separate flow, called the Gatekeeper, decides whether the move is allowed.

## What happens when a meeting is created

1. **Outlook starts the process.** A flow checks for newly created events every minute and passes each event to the agent. Moving an existing meeting does not start that same creation process again.
2. **The agent reads the rules and calendar.** The rules live in Dataverse, outside the agent's instructions. The agent checks which meetings actually overlap; back-to-back meetings do not count as a conflict.
3. **The agent proposes a solution.** It preserves protected meetings and looks for another time for a meeting that can move. Its instructions say to move the new meeting if both are movable, and leave both alone if both are protected.
4. **The Gatekeeper checks the proposal.** It retrieves the meeting directly from Microsoft Graph, reads the rules again, and confirms there is a conflict. It uses AI to interpret the rules and also checks conditions such as preserving the meeting's duration. Only an allowed proposal reaches the calendar update.
5. **The agent reports the outcome.** When a newly created protected meeting has a conflict, the executive assistant receives the confirmed outcome, including a failure or an inability to find a new time.

## Why the second check matters

The agent's explanation is not permission to move a meeting. The Gatekeeper makes its own check against the actual event and current rules. That separation is the main point of this proof of concept.

There are limits. AI still interprets the policy, and the agent is responsible for checking the replacement time. The Gatekeeper does not repeat the entire scheduling search. Also, this design controls how this agent changes the calendar; it does not remove calendar permissions from other applications or users. Anyone allowed to edit the Dataverse rules can influence the decision, so that access matters too.

## Where to find the details

The [architecture diagram](../README.md#architecture) shows the complete path. For a closer look, see the [trigger flow](../architecture/flows/trigger-flow.md), [Gatekeeper](gatekeeper-pattern.md), [agent](../architecture/agent/zava-exm-meeting-concierge.md), and [rule table](../architecture/dataverse/rules-table.md).

The [exported solution](../solution/README.md) contains the actual platform files from October 1, 2026. These explanations describe that implementation; the [test results](testing.md) record what was observed during the September 30 build.
