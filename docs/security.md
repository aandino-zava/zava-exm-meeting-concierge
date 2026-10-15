# Security and governance

The fixed workflow is the only configured calendar write path. It reads event details itself and recognizes only the supported board-protection rule. Meeting text and model output cannot grant permission. Active rules are checked again before every move.

Calendar PATCH uses a fresh ETag with If-Match. Automatic write retries are disabled. A destination read reduces scheduling races; it cannot reserve the slot. A post-write read checks the actual outcome. Uncertain results are left for review.

Connections remain scoped to the existing lab account. This repository refresh does not change live permissions or prove least-privilege role assignments. Protect connection ownership and restrict who can edit the agent, flows, and rules. Flow run history can contain calendar data; review retention and access before wider use.

The current starter has no concurrency control configured. Parallel automatic or direct calls lack a durable mailbox lock and request ledger. Caller identity binding, duplicate notification prevention across repeated requests, role verification, environment separation, and release approvals remain production work. Do not present this single-calendar Dev pilot as production-ready.

See the [architecture](architecture.md) for supported behavior and limits.

The user approved the existing lab owner Outlook connection for automatic requests on October 15, 2026. The saved resolver now uses that embedded connection, as does Dataverse. Existing run-only callers can reach the lab mailbox only through the configured flow path; flow sharing was not expanded. Review these callers before a wider rollout. This is a single-calendar service identity choice, not verified production identity isolation.
