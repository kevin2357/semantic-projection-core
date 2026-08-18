# Downstream consumer contract

SPC artifacts are semantic interchange, not finished application products. Consumers may specialize them while preserving enough identity and provenance to audit the transformation.

## Stable assumptions

Consumers should rely on:

- explicit package and contract versions;
- exact profile and context identity;
- deterministic projected IDs for identical semantic inputs;
- `source_refs`, `mapping_rule_refs`, and provenance;
- profile-owned projected term definitions;
- explicit coverage, diagnostics, and limitation categories;
- canonical temporal facts remaining invariant across profiles and contexts;
- materialization mode being distinct from semantic projection.

Consumers should not rely on filenames, list insertion order beyond documented deterministic output, undocumented profile internals, or human-readable labels as identifiers.

## Consumer-owned semantics

A consumer may own a target-domain profile. Mythos, for example, projects Foundry facts through a Mythos-owned gameplay profile, then materializes SPC activations into game-owned runtime records. Numeric effects, stacking, scoring, and AI behavior remain outside SPC.

Similarly, AstroWoof authoring tools consume Woofmapped graphs and merge their used-term registries before selecting semantic bases for editorial work. Final card prose is downstream of projection.

AstroWoof's cross-system architecture and consumer obligations are maintained in
the separate
[astrowoof-project documentation](https://github.com/kevin2357/astrowoof-project/blob/main/docs/architecture/Semantic%20Projection%20Integration.md),
including its
[projected canine graph handoff](https://github.com/kevin2357/astrowoof-project/blob/main/docs/contracts/Projected%20Canine%20Graph%20Contract.md).
Those documents are authoritative for AstroWoof integration and product policy;
SPC's code, schemas, and documentation remain authoritative for projection
behavior. Product audience modes, authoring policy, cards, delivery, and UI must
not be inferred from similarly named SPC projection contexts.

These patterns are preferred: SPC acts as compiler/runtime, while the consumer owns application policy and its derived contracts.

## Registry aggregation

When combining artifacts from one profile version, consumers may union used-term subsets by stable key. Identical duplicate definitions are safe to deduplicate. Conflicting definitions under one registry ID/version must fail loudly.

## Temporal consumption

Treat `temporal_facts` as preserved upstream evidence. Application intensity, advice, forecast priority, or game magnitude may be derived from it, but should be stored in a consumer-owned namespace with links back to the projected activation.

Summary artifacts retain semantic hashes but omit rows. Consumers needing individual activations or source references must request standard, full, or forensic materialization.

## Compatibility discipline

Pin profile and contract versions in repeatable workflows. Validate artifacts at ingestion. Preserve route receipts where source-to-result traceability matters. When a consumer needs behavior not represented by the current contract, add a versioned consumer layer or propose an SPC contract evolution rather than overloading unrelated fields.

Production consumers must additionally pin the exact wheel SHA-256 and verify
the installed semantic-resource fingerprint. The supported 0.11.1 boundary and
consumer procedure are frozen in the
[release compatibility contract](../reference/release-compatibility.md) and
[release consumer handoff](release-consumer-handoff.md).
