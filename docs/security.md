# Security and governance

The fixed workflow is the only configured calendar write path. It reads event details itself and recognizes only the supported board-protection rule. Meeting text and model output cannot grant permission. Active rules are checked again before every move.

Calendar PATCH uses a fresh ETag with If-Match. Automatic write retries are disabled. A destination read reduces scheduling races; it cannot reserve the slot. A post-write read checks the actual outcome. Uncertain results are left for review.

Connections remain scoped to the existing lab account. This release does not change permissions or prove least-privilege role assignments. Protect connection ownership and restrict who can edit the agent, flows, and rules. Flow run history can contain calendar data; review retention and access before wider use.

The automatic trigger is serialized. Direct parallel calls still lack a durable mailbox lock and request ledger. Caller identity binding, duplicate notification prevention across repeated requests, role verification, environment separation, and release approvals remain production work. Do not present this single-calendar Dev pilot as production-ready.

See the [V2 design](v2-design.md) for supported behavior and limits.

The resolver originally required the callers own Outlook connection. Changing it to use the lab owner connection lets existing run-only callers reach that mailbox through this fixed flow. That change needs explicit approval and a review of existing flow sharing; it is not merely a sign-in refresh.
