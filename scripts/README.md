# Zava ExM Meeting Concierge maintenance scripts

Use an authenticated Microsoft Power Platform CLI installation. Export is read-only against the service but refreshes the local baseline. Review its resulting Git diff. Do not point it at another environment by accident.

```powershell
./scripts/export-solution.ps1 -EnvironmentUrl 'https://YOUR-DEV-ORG.crm.dynamics.com'
./scripts/pack-solution.ps1
python -m pip install PyYAML
python scripts/validate.py
```

Validation is static and makes no calendar writes. Pack output goes to ignored build/. Import is intentionally not automated: bind connections, review fixed values and dependencies, and seed rules as described in the implementation notes. The export script does not refresh provenance automatically; regenerate hashes and review the provenance record whenever replacing the baseline.
