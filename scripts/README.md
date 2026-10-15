# Build and deployment scripts

Use Python 3.11+ and an official Power Platform CLI. Local checks and packaging do not require signing into a tenant.

```powershell
python -m pip install PyYAML tzdata
python scripts/test_resolver.py
python scripts/test_deployment.py
./scripts/pack-solution.ps1
python scripts/validate.py
```

Pack writes a versioned ZIP under ignored `build/`. The repository also includes the ready-to-import V2.1 ZIP and its SHA-256 checksum under `solution/exports/`.

For an authorized import, follow [the installation guide](../docs/deployment.md), create the target connections, copy `deployment/settings.example.json` to ignored `deployment/settings.local.json`, and fill the settings and connection IDs. Then use `import-solution.ps1 -EnvironmentUrl <target-url> -SettingsFile <local-settings-file>`. It checks inputs and package checksum before calling PAC. It does not sign users into connectors, seed rules, publish the agent, or enable processing.

## Preparing a new package version

Update the solution version and reviewed source, then run the tests above. Build the distributable and record its origin:

```powershell
./scripts/pack-solution.ps1 -OutputPath ./solution/exports/ZavaExMMeetingConcierge_2_1_0_0_unmanaged.zip
python scripts/record-provenance.py --pac-version '<actual CLI version>'
python scripts/validate.py
```

Use the filename matching the new version when preparing another release. Do not overwrite V1 or V2.0 evidence. Record-provenance identifies a repository build; it does not imply a live export or a successful import. The validator checks formats, local links, current package/source fingerprints, preserved archive hashes, and common credential patterns.

`test_resolver.py` runs the current workflow action definitions against simulated calendar and policy services. `test_deployment.py` checks required connections, configuration, initial flow state, and preserved README sections. Neither is Microsoft runtime validation.

## Reviewing future live changes

After verifying the intended environment, `export-solution.ps1 -EnvironmentUrl <source-url>` stages an authenticated live ZIP and unpacked source under `build/live-export/`. It deliberately does not overwrite portable source or historical packages. Review the staged diff before reconciling a live change into the next portable version. Keep live test evidence separate from simulations and package checks.
