# Zava ExM Meeting Concierge repository validation

Validation date: October 1, 2026. This is source/package validation, not a repeat of the historical functional tests.

| Check | Result |
| --- | --- |
| Authenticated source environment | PAC confirmed Zava PP Lab Dev and the existing solution display name |
| Supported export and unpack | PAC unmanaged export and unpack succeeded |
| Package reconstruction | PAC unmanaged pack succeeded without custom component export errors |
| Component inventory | 1 bot, 22 bot components, 2 flows, 1 table, 5 connection references, 1 AI Skill Config |
| Native fidelity | SHA256 manifest covers original ZIP and every unpacked file |
| Structured content | Native JSON, XML, and bot YAML parsed successfully |
| Documentation | Local relative links checked; current export differences and historical test limits recorded |
| Mermaid | Standalone source and README diagram both parsed successfully with Mermaid and match |
| Secret review | Candidate files and original archive members scanned; no credential signatures found |
| Authentication state | No cache, profile, credential, or .env file included |
| Naming | No obsolete spaced project title in repository-authored prose; native legacy references retained |
| Destination | aandino-zava/zava-exm-meeting-concierge, private, main |
| Import into another environment | Not performed |
| New functional calendar testing | Not performed |

The original ZIP is retained alongside the unpacked baseline. Successful repacking is not proof of a successful import: AI Classify remains an external Microsoft dependency, connection bindings and fixed configuration need review, and the governance data row must be seeded separately.

The sensitive-data scan reports address occurrences in the unchanged native assets. Two are the configured recipient and mailbox description; Dataverse output metadata also includes schema-related address-pattern text. Those findings were reviewed rather than deleted from the original export. The private baseline is not suitable for an unreviewed public visibility change.

Use `python scripts/validate.py` with PyYAML installed to repeat the static scan and syntax/hash/link checks. The scan does not detect every possible secret format and is not a production security audit.

The complete staged file set and diff were reviewed, including native component definitions, fixed configuration, dependency metadata, and authored documentation. Git whitespace validation passed with CRLF treated as the native Windows line ending. Authentication caches and local QA tools are outside the repository.
