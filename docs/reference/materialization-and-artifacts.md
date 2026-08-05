# Materialization and artifact identity

Projection execution creates a full semantic artifact. Materialization selects a consumer view without rerunning or changing the semantic mapping.

## Modes

| Mode | Graph rows | Audit/diagnostics | Intended use |
|---|---|---|---|
| `full` | Complete | Complete | Development, detailed analysis, reusable source artifact |
| `standard` | Complete | Compact audit and diagnostic summaries, with errors/warnings | Ordinary interchange and downstream consumption |
| `summary` | Omitted | Coverage and diagnostic summaries | Indexes, catalogs, routing, lightweight comparison |
| `forensic` | Complete | Complete plus integrity hashes and counts | Reproducibility, debugging, artifact audits |

Temporal standard materialization also compacts the embedded static target graph. Temporal summaries retain semantic hashes for activators, activations, sequences, states, and preserved temporal facts even though graph rows are omitted.

All materializations preserve the compact runtime identity. Materialization
never substitutes a new runtime, profile, context, or policy fingerprint.

Static audit and diagnostics can also be emitted as a separate deterministic `projection_forensic_audit` artifact.

## Materialization is not projection

Changing `full` to `summary` changes payload shape, not target-domain meaning. A consumer needing another profile or context must run another projection. A consumer needing fewer rows or more audit detail should select another materialization.

## Artifact identification

`identify_artifact()` recognizes supported artifacts from contract metadata rather than filenames. Current temporal routing uses this distinction to separate source bundles, normalized requests, projected graphs, and route receipts.

Consumers should inspect `package_type`, contract/version metadata, profile and context identity, and materialization mode. Filenames are convenient labels, not contracts.

For release traceability, also inspect `metadata.runtime_identity` and compare
its installed runtime/resource fingerprints with the qualified release
manifest. The original wheel SHA-256 remains external because it cannot be
reconstructed from an extracted installation.
