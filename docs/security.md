# Security and governance

The fixed workflow is the only configured calendar write path. It reads event details itself and recognizes only the supported board-protection rule. Meeting text and model output cannot grant permission. Active rules are checked again before every move.

Calendar PATCH uses a fresh ETag with If-Match. Automatic write retries are disabled. A destination read reduces scheduling races; it cannot reserve the slot. A post-write read checks the actual outcome. Uncertain results are left for review.

Each installation binds its own target-tenant connections. Recorded Dev tests used the configured lab account; those results do not establish least-privilege role assignments. Protect connection ownership and restrict who can edit the agent, flows, and rules. Flow run history can contain calendar data; review retention and access before wider use.

The current starter has no concurrency control configured. Parallel automatic or direct calls lack a durable mailbox lock and request ledger. Caller identity binding, duplicate notification prevention across repeated requests, role verification, environment separation, and release approvals remain production work. Do not present this single-calendar Dev pilot as production-ready.

See the [architecture](architecture.md) for supported behavior and limits.

The resolver uses embedded Outlook and Dataverse connections. Authorized run-only callers can reach the configured calendar through that flow path. Review connection permissions and flow sharing before a wider rollout. This is a single-calendar service identity design; production identity isolation has not been verified.

## Portable installation

The solution ships no mailbox, calendar ID, assistant recipient, or connection credentials in current flow settings. Required environment variables and connection mappings select the target configuration. They are administered by the installer, not supplied by the agent. Both flows are packaged off; verify their state when updating an existing installation. Missing or malformed email configuration stops processing before calendar access.

The installer must verify that the Outlook connection account, configured mailbox, and primary Calendar ID agree. This is not enforced by an identity comparison in the flow. Keep agent access and run-only sharing limited to intended POC users, configure authentication after import, and avoid anonymous/public exposure. Environment variable values are configuration rather than secret storage. The distributed package contains no lab mailbox, calendar ID, or notification recipient defaults.

## GitHub deployment identity

The receiving tenant authorizes a dedicated Dataverse application user and a GitHub environment federated credential. The deployment job alone has `id-token: write`; build jobs have no tenant credentials. Deployment is manual, restricted to main, and uses the checked build artifact. Configure the GitHub environment's main-only branch policy as documented, plus approvals where supported. Pinning action commits limits unexpected upstream action changes.

No client secret or user password is stored for workflow sign-in. Target settings are an environment secret, are written only to temporary runner storage, and are not uploaded with build artifacts. PAC profiles and the temporary settings file are cleared after a deployment attempt. The application user's deployment role and connection access remain the receiving administrator's responsibility; broad POC administrator access is not a least-privilege production design.
