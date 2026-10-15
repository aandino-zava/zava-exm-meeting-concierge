# Check new meeting

The display name is **Check new meeting**. Its existing workflow identity is retained.

The [native workflow](../../solution/unpacked/Workflows/Checknewmeeting-F5621481-00BD-F111-AAAD-6045BD06703E.json) listens for a created event in the configured lab calendar. It passes that exact ID to the agent, asks for one resolver call, and serializes automatic requests.

The creation trigger is paused pending approval for the flow to use the lab owner's existing Outlook connection and final automatic acceptance testing. A green parent run alone does not prove that the agent called the resolver; inspect the returned outcome and the calendar.
