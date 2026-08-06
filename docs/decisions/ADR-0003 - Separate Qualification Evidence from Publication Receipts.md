# ADR-0003 — Separate Qualification Evidence from Publication Receipts

```yaml
status: accepted
date: 2026-08-05
owner: semantic-projection-core
scope: release evidence
```

## Context

The external release manifest must be hashed and qualified before publication,
but publication IDs, timestamps, remote tag objects, and authenticated download
results do not exist until afterward. Updating the uploaded manifest to include
those facts would change an asset after its qualification hash was recorded and
create a circular publication process.

## Decision

The uploaded release manifest is an immutable qualification-time snapshot.
Post-publication facts are recorded in a separate publication-verification
artifact committed after remote tag and asset verification.

The publication receipt must state the remote tag target, release identity,
asset IDs, sizes and hashes, authenticated download comparison, and any
platform immutability or signature limitations.

## Consequences

- A published qualification manifest may retain a pre-publication status such
  as `qualified_awaiting_publication`; this describes when its bytes were
  frozen, not the current GitHub release state.
- Publication evidence can be extended without replacing already verified
  release assets.
- Consumers verify artifact bytes from the published checksums and use the
  publication receipt to verify remote delivery state.
- Signed tags or platform-enforced immutable releases remain separate controls
  and must not be implied when absent.
