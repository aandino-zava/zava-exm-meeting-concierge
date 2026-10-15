# Fixed calendar checks

The calendar change flow accepts only `eventId` (the trigger's `text` field). The caller cannot pass a proposed time, subject, duration, or permission decision.

The flow reads the current event, detects strict overlaps, checks the active rule, selects movable events, and searches the actual calendar. Before PATCH it rereads rules and the target, requires an unchanged ETag, and rereads the destination. PATCH uses If-Match with no automatic retry. It reads back the changed event and checks that the original conflict is gone.

A missing or unsupported active rule blocks resolution. No AI Builder prompt grants permission. [Read the complete design](v2-design.md).
