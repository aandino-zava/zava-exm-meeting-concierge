# Solution files

- [ZavaExMMeetingConcierge.zip](exports/ZavaExMMeetingConcierge.zip): unmanaged solution for a POC installation.
- [SHA-256 checksum](exports/SHA256SUMS.txt): verifies the download.
- `unpacked/`: native solution source, including required connection references and configuration definitions.
- `provenance.json`: package origin, hash, internal solution revision, and source fingerprints.

Follow [GitHub Actions deployment](../docs/deployment.md) for the main path, or [manual installation](../docs/manual-install.md) to import the downloaded ZIP. GitHub Actions builds the same source and saves the named ZIP and checksum as a workflow artifact.

Both flows are packaged off. The receiving tenant supplies its connections, Calendar mailbox, primary Calendar ID, Executive assistant email, and active rule data. Configure agent authentication/access and publish it before enabling processing. Credentials, calendar events, email, and flow run history are not included.

The Gatekeeper remains the only agent calendar-write path. Native component identities and the internal platform revision are retained for upgrades; reader-facing product and package names remain stable. The current package and its fingerprints are the installation and source-verification baseline.

Local packaging and tests do not establish a successful target deployment. Record the independent installation and calendar test in [the acceptance record](../deployment/acceptance.md).
