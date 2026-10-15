# Solution files

- `unpacked/` is the current V2 native source exported from the live Dev solution.
- `exports/ZavaExMMeetingConcierge_2_0_0_0_unmanaged.zip` is the current unmanaged import package.
- `provenance.json` records its version, origin, archive hash, and every native file hash.
- The `1_0_0_0` ZIP and `provenance-v1.json` preserve the original V1 evidence.

The unique solution name remains **ZavaCalendarGovernancePOC**. Platform schema names and component IDs are retained. Display names are **Check new meeting** and **Check and move meeting**.

A solution export does not contain account credentials, active Dataverse rule rows, calendar events, email, or flow run history. Review connection bindings, the fixed lab mailbox/calendar, and the assistant address before importing elsewhere. Publish the agent and verify both flows are active.

Read the [setup instructions](../docs/deployment.md) and [actual V2 test evidence](../docs/testing.md). This is a Dev pilot; no UAT or production deployment is claimed. The latest export contains only one agent tool; the seven retired tools have been removed. The calendar flow contains no AI Builder authorization action. The starter has no concurrency control configured.
