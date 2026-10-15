# Solution files

## Portable POC package

- [V2.1 unmanaged ZIP](exports/ZavaExMMeetingConcierge_2_1_0_0_unmanaged.zip): repository-authored portable build for a new POC installation.
- [SHA-256 checksum](exports/SHA256SUMS.txt): verifies the download.
- `unpacked/`: current portable source, with the Dataverse connection dependency and three required environment variables.
- `provenance.json`: portable build origin, package hash, and native file fingerprints. This is not a fresh export from live Dev.

Follow [the installation guide](../docs/deployment.md). Both flows are packaged off. Supply target connections, Calendar mailbox, primary Calendar ID, and Executive assistant email, create or reuse the active rule, then configure and publish the agent before enabling processing.

The package has been locally packed, unpacked, and checked. A clean second-environment import is awaiting the owner's manual test. Credentials, active rule rows, calendar events, email, and flow run history are not included.

## Preserved evidence

The V1 ZIP and `provenance-v1.json` preserve original evidence. The V2.0 ZIP and `provenance-v2-dev.json` preserve the owner-reviewed live Dev export before portability changes. Use V2.1 for a new installation; do not edit the earlier archives.

Platform schema names and component IDs remain stable. One agent tool, **Check and move meeting**, owns the configured calendar change path. No AI classification authorizes writes. The starter has no concurrency control configured; this is a primary-calendar Dev POC rather than a production deployment.
