# Maintenance scripts

Use an authenticated official Power Platform CLI. Verify the target environment before exporting or importing.

```powershell
./scripts/export-solution.ps1 -EnvironmentUrl 'https://YOUR-DEV-ORG.crm.dynamics.com'
python scripts/record-provenance.py
python -m pip install PyYAML tzdata
python scripts/validate.py
python scripts/test_resolver.py
./scripts/pack-solution.ps1
```

Export refreshes the current V2 archive and unpacked source. Review the diff and regenerated provenance. The V1 archive remains unchanged. Pack writes to ignored `build/`.

When recording fingerprints, optionally pass `--pac-version` with the version actually used for export. If omitted, it is recorded as unknown. The export date is generated when the record is written.

`validate.py` checks file formats, local links, package integrity, current source hashes, original V1 archive hash, and common credential patterns. `test_resolver.py` executes the exported workflow action definitions against an in-memory calendar and policy service. It is a limited WDL interpreter, not Microsoft runtime validation. It never calls a live service. Keep live tests and their evidence separate.

Import is not automated. Bind reviewed connections, confirm the rule row and fixed mailbox/recipient, publish the agent, and verify actual calendar behavior before enabling automatic processing in another environment.
