# Zava ExM Meeting Concierge solution assets

`exports/ZavaExMMeetingConcierge_1_0_0_0_unmanaged.zip` is the original unmanaged PAC export from Zava PP Lab Dev. `unpacked/` is PAC's native unpacked representation; files were not manually reconstructed or renamed. `provenance.json` records hashes and component counts.

Exported on October 1, 2026 using PAC 2.12.2. The source environment was confirmed through `pac auth list`, `pac org list`, `pac org who --environment`, and `pac solution list --environment` before export. The display name was already correct. The retained internal unique name is used only where the tooling requires it.

PAC successfully repacked the unpacked tree into an unmanaged ZIP. That validates local packaging, not import or runtime behavior in a second environment. The repacked QA file is not committed; recreate it with the pack script.

## Included

Agent and bot configuration, 22 bot components, two workflow definitions and metadata, the rule table with forms/views/relationships, five connection references, generated AI Skill Config, and solution metadata.

## Not carried by this export

OAuth connection credentials, active governance data row, calendar fixtures, email messages, run history, and a formal evaluation set. No environment-variable definitions were present. Tool enablement needs review after import because retained setup tools do not have an unambiguous disabled marker in this export.

## Dependency

Solution.xml declares AI Classify from Microsoft PowerAI / msdyn_AISolutionDefaultTemplates, version 202608.1.4.1. This Microsoft template is an external dependency, not a missing custom artifact manually recreated here. Ensure it is available in the destination.

See [implementation and import notes](../docs/implementation.md) before enabling the imported automation. Fixed lab configuration remains in the private baseline.
