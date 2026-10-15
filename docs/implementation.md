# Setup and maintenance

This release updates the existing unmanaged solution in Zava PP Lab Dev. Keep its unique name, component IDs, and schema names. Use the V2 archive, not the historical V1 archive.

1. Confirm the intended environment and export a backup. This prevents changing the wrong environment and provides a rollback source.
2. Import the unmanaged package, bind the existing Outlook, Copilot Studio, and Dataverse connections, and publish. For this approved single-calendar pilot, the resolver uses the existing lab owner Outlook connection rather than asking each caller to sign in. Review run-only sharing before enabling that choice in another environment. Credentials and active rule rows are not in a solution ZIP.
3. Confirm the active rule in the existing Calendar Governance Rule table: `Board meetings are critical and cannot be moved. Any meeting that has "board meeting" in the subject is considered a board meeting.` Unsupported additional active rules block resolution.
4. Review fixed mailbox, calendar trigger ID, and Nancy's email in the native flow definitions. They are scoped to this lab. A different mailbox needs a reviewed deployment change.
5. Check Outlook working hours. The resolver reads getSchedule for the configured mailbox and uses returned hours/time zone, on weekdays only. Missing/invalid settings stop the move.
6. Enable **Check and move meeting**, publish the agent, then enable **Check new meeting**. The automatic trigger runs one request at a time.
7. Use temporary events without attendees to test no conflict, a permitted move, two protected meetings, and an unavailable slot. Check actual calendar times and notification action status; a green parent flow alone is insufficient.
8. Remove temporary events, export the live solution, unpack it, update provenance, run source checks, and commit the reviewed changes.

For rollback, pause the automatic trigger and import the reviewed backup, restore connection bindings, republish the agent, and verify behavior before enabling the trigger. Rolling back a package does not reverse calendar changes or sent emails.

See [V2 design](v2-design.md), [test evidence](v2-testing.md), and [scripts](../scripts/README.md). No production deployment is claimed.
