# Slice 1 — Released Contract and Semantic Audit

```yaml
status: gate_candidate
date: 2026-08-13
implementation_changes: none
source_release: astrology-graph-foundry 0.8.0
current_spc_release: semantic-projection-core 0.10.0
candidate_spc_release: semantic-projection-core 0.11.0
```

## Outcome

AGF's bounded natal artifact is projectable, but it is not an alternate spelling
of the exact canonical graph. Safe support requires a separate atomic intake,
output contract, source-policy profile, evidence/provenance layer, family-aware
accounting, and installed route. Merely adding graph version 1.7.0 to SPC's
existing allowlist would accept an artifact whose semantic absences the current
engine misinterprets.

No release blocker prevents beginning the bounded intake slice. One upstream
evidence-vocabulary inconsistency requires preservation and explicit compatibility
handling; it does not require SPC to invent a resolution.

## Authoritative source baseline

The implementation will qualify against the immutable AGF baseline below:

| Identity | Qualified value |
| --- | --- |
| Distribution | `astrology-graph-foundry` 0.8.0 |
| Tag | `astrology-graph-foundry-v0.8.0` |
| Commit | `2e5feef35e6d7144c3e639ece0aba9ff587ea4e9` |
| Wheel SHA-256 | `f236de0bb7c254c4421f571e816f2314251636ebbed9aa3cb9cb2a09925c04ae` |
| Runtime manifest SHA-256 | `413c84728bc279bdfa67f892481ebe9837c0306093c2d28444caf239043ed5e2` |
| Package type/schema | `bounded_natal_dataset` / 1.0.0 |
| Canonical graph | `bounded_canonical_astrology_graph` / 1.7.0 |
| Evidence contract | `agf.bounded_uncertainty_evidence.v1.0.0` |
| Calculation profile | `agf.bounded_natal.calculation_profile.v1.12.0` |
| Interval proof | `agf.interval_proof.v1.0.0` |

The wheel hash is qualification evidence, not an SPC runtime dependency. AGF
0.8 deliberately emits projection-neutral wire artifacts and has no SPC runtime
or projection executor. SPC must preserve that separation.

## What the source artifact proves

AGF evaluates every valid minute in the normalized interval, inclusive of its
endpoints, and uses continuous envelopes where point samples alone cannot prove
the predicate. The bounded canonical graph contains only categorical objects and
relationships promoted as invariant under that proof policy. The surrounding
dataset retains conditional, variable, unavailable, or inconclusive evidence
needed to understand why other facts were not promoted.

The canonical graph is therefore an `bounded_invariant_subgraph`, not a most
likely chart, midpoint chart, probability distribution, rectification result,
or confidence-ranked list. Its topology is complete only for supported
invariant categorical facts. More rows do not mean greater truth, importance,
confidence, or authoring priority.

### Epistemic classifications

The released generalized classification vocabulary is:

- `invariant`;
- `conditional`;
- `variable`;
- `unavailable`; and
- `inconclusive`.

Projection may map the semantics of an invariant fact into the target domain.
It must preserve, rather than reinterpret, the epistemic classification and its
proof evidence. A context cannot turn conditional into invariant, variable into
stable, or unavailable into irrelevant.

### Precision and inference prohibitions

Canonical bounded objects prohibit `longitude`, `pretty`, and `sign_degree`.
Canonical bounded relationships prohibit `orb`, `distance`, `applying_delta`,
and `strength`. The graph declares no structural strength scores and no canonical
claims. SPC must not fill those absences using a midpoint, representative state,
default, profile salience, raw count, or exact-chart fallback.

## Source inventory

### Object families

| Source object type | Potential projected semantic material | Important qualifications |
| --- | --- | --- |
| `bounded_natal_body` | invariant body role with any separately proved sign, motion, house, dignity, or triplicity fields | A body can exist because only house is invariant; sign and motion are independently optional. |
| `bounded_antiscia_point` | derived coordinate-transform role | Must retain `owner_object_ref`, transform kind, evidence family, and non-independence. |
| `bounded_contra_antiscia_point` | derived coordinate-transform role | Same owner/family requirement as antiscia. |
| `bounded_harmonic_point` | harmonic transform role and harmonic number | Harmonic siblings cannot become independent support. |
| `bounded_house_cusp` | invariant cusp sign/ruler domain semantics | Contains no exact cusp degree. Ruler promotion depends on invariant sign prerequisites. |
| `bounded_angle` | invariant angle sign and optional invariant house | `Vertex` can appear through the angle family. No exact angle degree. |
| `bounded_sect_state` | invariant day/night sect state | A global categorical state, not an ordinary planet-like operator. |
| `bounded_calculated_point` | invariant sign/house for a branched calculated point | Multiple `possible_formula_ids` may remain; one invariant position does not imply one known formula branch. |

### Relationship families

| Source relationship type | Interpretation boundary |
| --- | --- |
| `BOUNDED_INVARIANT_ASPECT` | Invariant ordinary aspect type between emitted endpoints. |
| `BOUNDED_INVARIANT_DERIVED_ASPECT` | Invariant aspect involving derived coordinate material; preserve family lineage. |
| `BOUNDED_INVARIANT_DECLINATION_PARALLEL` | Invariant parallel relationship without longitude-aspect assumptions. |
| `BOUNDED_INVARIANT_DECLINATION_CONTRAPARALLEL` | Invariant contraparallel relationship without longitude-aspect assumptions. |
| `BOUNDED_INVARIANT_ANGLE_ASPECT` | Invariant relationship to an emitted angle. |
| `BOUNDED_INVARIANT_CALCULATED_POINT_ASPECT` | Invariant relationship involving a calculated point. |
| `BOUNDED_HAS_ANTISCIA_POINT` | Ownership/derivation topology, not an aspect or independent support event. |
| `BOUNDED_HAS_CONTRA_ANTISCIA_POINT` | Ownership/derivation topology. |
| `BOUNDED_HAS_HARMONIC_POINT` | Ownership/derivation topology. |

All relationships require emitted endpoints and direct uncertainty evidence.
Aspect-bearing types require an aspect label, but never an exact orb or strength.

### Capabilities and feature dispositions

The graph positively declares supported bounded categorical placements, ordinary
and derived aspects, body-coordinate evidence, declination evidence and
relationships, coordinate transforms, terrestrial-frame evidence, invariant
house membership, cusp semantics, angle aspects, sect, triplicity, and branched
calculated points.

It explicitly rejects exact longitudes, longitude-driven downstream activation,
house and angle transits, returns, and annual profections. Released artifacts
also record feature dispositions for unsupported or deliberately deferred
families. SPC must preserve the source capability map and dispositions rather
than derive capability from whichever rows happened to be emitted.

## Evidence and reference contract

Each emitted canonical row has an `uncertainty_evidence_ref` and
`evidence_metadata`. Some objects also have distinct house or triplicity evidence
references. Evidence records can include categorical possibilities, scalar or
circular/disjoint ranges, prerequisites, transition witnesses, counterexamples,
proof scope, availability, and a status reason.

SPC's bounded output will contain an artifact-scoped source-evidence registry:

1. include every evidence row referenced directly by emitted projected material;
2. recursively include prerequisite evidence when the prerequisite resolves to a
   registry entry under the released namespace rules;
3. retain non-registry prerequisite identifiers verbatim as opaque upstream
   feature/dependency references;
4. never rewrite an evidence row's classification, possibilities, ranges,
   witnesses, counterexamples, availability, reason, or proof scope according to
   projection context;
5. report missing direct references as fatal and unresolved prerequisites as
   explicit closure diagnostics according to the family policy frozen in Slice
   2; and
6. bind the subset to the source artifact's semantic hash and contract versions.

This avoids both evidence loss and unconditional duplication of source registries
that can exceed two thousand records.

### Qualified reference namespace

AGF canonical rows store raw IDs, while cross-section references can use
`canonical:object:<id>` and `canonical:relationship:<id>`. SPC will normalize
only these documented kind prefixes and will preserve the underlying ID exactly.
It will reject kind mismatches, ambiguous resolutions, and dangling direct refs.

## Evidence-family and coverage policy

AGF provides separate `record_independence_group`, `evidence_family_group`, and
`source_chart_family_group` concepts. The first identifies serialized records;
the second collapses root-owner/source constructions for anti-double-counting;
the third provides chart-scoped correspondence. The legacy `independence_group`
is a compatibility alias for the evidence family, not another vote.

The projected contract will preserve those identities verbatim in provenance and
add deterministic projected family indexes. Coverage will report at least:

- raw source/emitted record counts;
- eligible/mapped/unmapped record counts;
- distinct eligible/mapped/unmapped evidence-family counts; and
- explicit outside-scope/excluded counts.

Record coverage diagnoses mapping completeness. Family coverage diagnoses
semantic breadth. Neither becomes salience, confidence, relevance, or claim
weight. Ownership relationships are topology and do not receive aspect-style
relevance scores.

## Why the existing static route cannot be widened

The current static request accepts separately supplied `source_graph`,
`structural_evidence`, `source_identity`, and registries. For bounded projection,
these sections collectively establish the proof and can become inconsistent if
assembled independently. The bounded route will accept the full AGF dataset as
one atomic `source_artifact` and extract the sections itself.

Other incompatibilities include:

- current validation accepts only canonical graph version 1.3.0 and does not
  validate bounded package identity or evidence closure;
- exact Woofmapping accessors expect names plus exact-style sign/house fields,
  while bounded rows use `sign_index`, `house_number`, optional independent
  fields, and new object types;
- exact source selection does not classify bounded derived, sect, cusp, angle,
  and calculated-point families intentionally;
- current `_score` substitutes `1.0` when structural strength is absent, whereas
  bounded absence means strength is unavailable and must not be synthesized;
- relationship projection copies `orb` and produces relevance from that unsafe
  score fallback;
- current raw-record coverage would overstate semantic breadth for derived
  families; and
- current projected IDs include `context_id`, so they cannot alone establish
  correspondence across the four context artifacts.

The existing route will continue to reject bounded graphs.

## Selected additive public boundary

| Concern | Slice 1 decision |
| --- | --- |
| Request | `bounded_natal_projection_request.v1`; contains one full `source_artifact`, exact profile identity, context, and bounded options. |
| Output | `projected_bounded_semantic_graph.v1`; separate from and non-substitutable for `projected_semantic_graph.v1`. |
| CLI | `semantic-bounded-project`. |
| Profile | `woofmapped_bounded_astrology.v0` 0.1.0, with its own manifest, mapping namespace, source policy, and registry identity. |
| Target ontology | Reuse `woofmapped_astrology.v0`; boundedness changes source epistemics and contract, not the canine target domain. |
| Contexts | Reuse the four exact IDs/versions: handler, direct-to-dog, hybrid, and general. |
| Candidate release | SPC distribution and engine 0.11.0. |
| Runtime dependency | No AGF runtime dependency; consume the serialized contract. |
| Validation ownership | SPC-owned consumer schema plus semantic/reference validation for consumed fields; AGF retains full native-schema authority. |
| Evidence | Verbatim artifact-scoped direct-plus-resolvable-prerequisite closure. |
| Identity | Context-specific artifact IDs plus a context-independent correspondence key for parallel entities/relationships. |

A sibling profile avoids silently broadening the released
`woofmapped_astrology.v0` 0.1.0 source policy. Shared target definitions can be
factored internally, but installed manifests, mappings, and registries remain
independently fingerprintable semantic policy.

## Context invariance contract

Across handler, direct-to-dog, hybrid, and general outputs, the following must be
identical for corresponding material:

- source refs and source correspondence identity;
- epistemic classification;
- evidence records and evidence-family membership;
- proof scope and source limitations;
- capabilities and feature dispositions;
- mapping from source fact to target semantic primitive; and
- projected-term definition for the same semantic term.

Context can vary declared application relevance, target framing, audience
metadata, or context-owned semantic emphasis. Context-specific scores, if any,
must be clearly target relevance only and cannot be labelled certainty,
confidence, evidence strength, or source stability. Product audience and prose
voice remain downstream concerns despite suggestive context names.

## Upstream inconsistency and safe handling

The standalone AGF evidence schema enumerates six availability values. Released
code also emits `disabled`, `prerequisite_unavailable`,
`prerequisite_variable_or_unavailable`, and `unsupported_profile`. The package
schema leaves registry values structurally open, so package validation does not
reconcile this vocabulary. Specialized calculated-point evidence also does not
always use the generalized evidence envelope.

SPC will therefore:

- use `classification` as the epistemic state;
- preserve `availability` and `status_reason` as opaque upstream reason
  vocabulary;
- validate the family-specific fields it actually consumes;
- reject unknown classifications, but not invent equivalence among reason
  tokens; and
- record the mismatch as an AGF compatibility issue for future reconciliation.

This issue does not block Slice 2 because unavailable records are not promoted
as invariant projected claims, but it prevents SPC from asserting that every
registry value conforms to the standalone generalized evidence schema.

## Scale and determinism implications

AGF's qualified oracle produced approximately:

| Interval | Objects | Relationships | Evidence records | Artifact size |
| --- | ---: | ---: | ---: | ---: |
| 4 hours | 105 | 1,493 | 2,120 | 15.8 MB |
| 24 hours | 100 | 1,256 | 2,679 | 20.2 MB |
| 48 hours | 97 | 1,074 | 2,988 | 24.1 MB |

SPC must avoid repeated deep copies of the complete package in per-row mapping,
quadratic duplicate detection, and full-registry copying per context. Slice 7
will measure peak behavior and deterministic semantic identity while excluding
operational timestamps from semantic comparison according to an explicit hash
boundary.

## Unsupported cases for the first implementation

- bounded plus temporal activation;
- bounded synastry, composite, or Davison routes;
- representative/midpoint chart selection or rectification;
- probability or confidence derivation;
- exact orb, phase, distance, strength, return, or profection semantics;
- projecting non-invariant evidence as if it were a canonical target fact;
- automatic fallback to the exact Woofmapping profile;
- Orthodox or Cognitive bounded-profile qualification;
- downstream card selection, authorship, API behavior, or UI behavior; and
- assuming SBE accepts the new contract before a separate boundary test.

## Slice refinements

The approved nine-slice structure remains appropriate with these refinements:

- Slice 2 builds atomic package intake and source-section reconciliation, not a
  generic graph-version allowlist.
- Slice 3 owns evidence closure, context-independent correspondence IDs, and
  capability/feature-disposition preservation.
- Slice 5 reports both record and family coverage and forbids score fallback.
- Slice 6 compares epistemic subtrees byte-for-byte or by a defined semantic
  hash across all contexts.
- Slice 7 includes 15–25 MB source artifacts and verifies that artifact-scoped
  evidence materialization avoids unnecessary full-registry duplication.
- Slice 8 treats SBE support as an explicit acceptance boundary, not an assumed
  property of structurally valid output.

## Gate decision

Slice 1 is ready for review. Slice 2 may begin after approval with the identities
and policies above. The AGF availability-vocabulary mismatch should be reported
upstream, but it is a compatibility warning rather than a waived validation
failure or a blocker to implementing invariant-only intake.

