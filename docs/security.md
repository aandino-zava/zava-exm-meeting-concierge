# Security and governance

The fixed workflow is the only configured calendar write path. It reads event details itself and recognizes only the supported board-protection rule. Meeting text and model output cannot grant permission. Active rules are checked again before every move.

Calendar PATCH uses a fresh ETag with If-Match. Automatic write retries are disabled. A destination read reduces scheduling races; it cannot reserve the slot. A post-write read checks the actual outcome. Uncertain results are left for review.

Portable installations bind their own target-tenant connections. Earlier Dev evidence used the approved lab account. This repository refresh does not change live permissions or prove least-privilege role assignments. Protect connection ownership and restrict who can edit the agent, flows, and rules. Flow run history can contain calendar data; review retention and access before wider use.

The current starter has no concurrency control configured. Parallel automatic or direct calls lack a durable mailbox lock and request ledger. Caller identity binding, duplicate notification prevention across repeated requests, role verification, environment separation, and release approvals remain production work. Do not present this single-calendar Dev pilot as production-ready.

See the [architecture](architecture.md) for supported behavior and limits.

The user approved the existing lab owner Outlook connection for automatic requests on October 15, 2026. The saved resolver now uses that embedded connection, as does Dataverse. Existing run-only callers can reach the lab mailbox only through the configured flow path; flow sharing was not expanded. Review these callers before a wider rollout. This is a single-calendar service identity choice, not verified production identity isolation.

## Portable installation

V2.1 ships no mailbox, calendar ID, assistant recipient, or connection credentials in current flow settings. Required environment variables and connection mappings select the target configuration. They are administered by the installer, not supplied by the agent. Both flows are packaged off; verify their state when updating an existing installation. Missing or malformed email configuration stops processing before calendar access.

The installer must verify that the Outlook connection account, configured mailbox, and primary Calendar ID agree. This is not enforced by an identity comparison in the flow. Keep agent access and run-only sharing limited to intended POC users, configure authentication after import, and avoid anonymous/public exposure. Environment variable values are configuration rather than secret storage. The historical exports retain lab configuration as evidence; the portable package does not use those values.
