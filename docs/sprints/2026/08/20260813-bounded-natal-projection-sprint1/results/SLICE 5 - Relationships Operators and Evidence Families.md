# Slice 5 — Relationships, Operators, and Evidence Families

```yaml
status: gate_candidate
date: 2026-08-13
relationship_types_supported: 9
relevance_aggregation_unit: evidence_family_group
raw_record_counts_are_weights: false
```

## Outcome

SPC now projects every released bounded relationship family whose endpoints and
target semantic primitive are in declared Woofmapping scope. Aspect geometry,
declination geometry, and derivation topology receive different target treatment
rather than collapsing into one generic relationship. Evidence-family-aware
accounting prevents derived sibling multiplicity from manufacturing relevance or
apparent independent support.

`project_bounded_natal` is the complete in-process object-plus-relationship route.
The earlier `project_bounded_natal_objects` remains explicitly object-only and
continues to mark relationships deferred in its audit.

## Relationship mapping matrix

| Source relationship | Target treatment |
| --- | --- |
| `BOUNDED_INVARIANT_ASPECT` | Established Woofmapping relation for the invariant aspect. |
| `BOUNDED_INVARIANT_DERIVED_ASPECT` | Same aspect geometry mapping with derived source type and family preserved. |
| `BOUNDED_INVARIANT_ANGLE_ASPECT` | Same aspect geometry mapping between supported operator/interface endpoints. |
| `BOUNDED_INVARIANT_CALCULATED_POINT_ASPECT` | Same aspect geometry mapping involving a supported calculated point. |
| `BOUNDED_INVARIANT_DECLINATION_PARALLEL` | `subsystems_track_together` / `parallel_behavioral_expression`. |
| `BOUNDED_INVARIANT_DECLINATION_CONTRAPARALLEL` | `subsystems_counterbalance` / `counterparallel_behavioral_expression`. |
| `BOUNDED_HAS_ANTISCIA_POINT` | Unscored `coordinate_transform_of` lineage topology. |
| `BOUNDED_HAS_CONTRA_ANTISCIA_POINT` | Unscored `coordinate_transform_of` lineage topology. |
| `BOUNDED_HAS_HARMONIC_POINT` | Unscored `coordinate_transform_of` lineage topology. |

Declination relationships deliberately do not masquerade as longitude aspects.
Ownership relationships deliberately do not masquerade as behavioral
interactions.

## Preserved relationship structure

Every emitted relationship retains:

- exact canonical relationship ref;
- source relationship type;
- source aspect label where applicable;
- invariant classification;
- direct evidence refs and proof scope;
- evidence-family group;
- mapped endpoints;
- target relation, operators, and interaction mode;
- exact mapping-rule identity;
- context-specific row ID;
- context-independent correspondence ID; and
- operator-preservation provenance.

The output never contains source orb, distance, applying/separating delta,
structural strength, or other exact geometry prohibited by the bounded source
contract.

## Family-aware relevance

Semantic interactions have a profile relevance that belongs to an evidence
family, not independently to every serialized member. SPC calculates:

`member relevance = base profile relevance / scored family member count`

For example, the established square relation has base relevance 0.98:

| Serialized siblings in one family | Member relevance | Family total |
| ---: | ---: | ---: |
| 1 | 0.98 | 0.98 |
| 2 | 0.49 | 0.98 |

This policy does not claim probability, confidence, evidence strength, or source
importance. It only prevents target relevance from scaling with representational
multiplicity. The artifact records base relevance, family member count, member
allocation, and the non-weighting raw-count invariant on every scored relation.

Topology-only ownership relations have `null` base relevance, allocation, and
projected relevance.

## Coverage contract

Audit coverage separately reports:

- source, mapped, and outside-scope object records;
- source, mapped, and outside-scope relationship records;
- eligible and mapped object evidence families;
- eligible and mapped relationship evidence families;
- `raw_record_counts_are_weights: false`; and
- `relationship_relevance_aggregation_unit: evidence_family_group`.

Record coverage answers whether declared rows were handled. Family coverage
answers whether semantic constructions were handled. Neither is confidence,
salience, or an authoring priority.

## Projected terms

The bounded registry now defines:

- `coordinate_transform_of`;
- `derived_expression_lineage`;
- `subsystems_track_together`;
- `parallel_behavioral_expression`;
- `subsystems_counterbalance`; and
- `counterparallel_behavioral_expression`.

These terms join the established aspect relation and interaction-mode terms in
artifact-scoped used-term subsets. Every emitted relation and interaction mode
has a fully qualified resolvable definition.

## Unsupported and failure behavior

- Unknown aspect primitives are outside declared scope and appear in audit
  diagnostics/coverage.
- Relationships with an unsupported endpoint are outside declared scope.
- No placeholder endpoint or passthrough edge is created.
- An eligible source row that returns no mapping is fatal.
- An eligible source row whose projected endpoints cannot resolve is fatal.
- Non-invariant direct evidence is fatal before relationship emission.

## Verification

- Full SPC suite: 202 passed in 60.59 seconds.
- Bounded suite: 45 passed.
- Ruff: passed.
- All nine source relationship types have direct mapping-path coverage.
- Duplicate-family adversarial relevance allocation: passed.
- Raw-record versus family-coverage assertions: passed.
- Relationship evidence, endpoint, forbidden-field, deterministic replay, and
  input immutability checks: passed.
- Projected registry definitions and qualified refs: passed.
- Existing exact and temporal routes: passed unchanged.

## Gate decision

Slice 5 is ready for review. Slice 6 may exercise fully mapped artifacts through
all four contexts and prove structural correspondence plus certainty invariance.
No installed entry point, version bump, or release declaration has been added.

