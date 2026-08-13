# Slice 4 — Woofmapping Bounded Object Projection

```yaml
status: gate_candidate
date: 2026-08-13
profile_id: woofmapped_bounded_astrology.v0
profile_version: 0.1.0
target_ontology: woofmapped_astrology.v0
relationship_projection: deferred
```

## Outcome

SPC now projects the deliberately supported invariant bounded object families
into the Woofmapping target ontology. The new profile has independent executable
policy identity while reusing established canine primitive meanings. It produces
the separate projected-bounded contract and preserves every qualifier's evidence
without inventing exact position, structural strength, or unsupported target
semantics.

Relationship projection remains absent by design until Slice 5.

## Profile ownership

`woofmapped_bounded_astrology.v0` 0.1.0 owns:

- bounded package and graph source selection;
- invariant-only epistemic policy;
- object-family eligibility;
- exact target primitive selection;
- sign-index to canine-mode composition;
- invariant-house to Doghouse-domain composition;
- coordinate-transform semantic treatment;
- unsupported object policy;
- bounded mapping rule IDs and versions; and
- a separately identified projected-term registry.

It targets `woofmapped_astrology.v0` because boundedness changes source
epistemics, supported composition, and output contract—not the meaning of
`pack_role_identity`, `behavioral_doorway`, or a Doghouse domain.

## Supported object mappings

| Bounded source family | Target treatment |
| --- | --- |
| Known `bounded_natal_body` | Established canine operator/orientation with independently proved mode and domain composition. |
| Known `bounded_angle` | Established canine interface with independently proved mode/domain composition. |
| Known `bounded_calculated_point` | Established target orientation/interface, including `Fortune` and `Vertex` aliases. |
| `bounded_house_cusp` | Corresponding Doghouse domain with source sign and ruler facts preserved. |
| `bounded_antiscia_point` | Root owner's target operator re-expressed through an antiscia coordinate transform. |
| `bounded_contra_antiscia_point` | Root owner's target operator re-expressed through a contra-antiscia transform. |
| `bounded_harmonic_point` | Root owner's target operator re-expressed through the numbered harmonic transform. |

Derived objects retain owner identity and evidence-family grouping. Their
semantic key includes the transform kind and qualifier, so they remain distinct
from both the root object and sibling transforms without being interpreted as
independent evidence or additional salience.

## Explicit unsupported behavior

The first object slice does not map:

- `bounded_sect_state`; or
- calculated points without an established Woofmapping primitive.

These rows appear in `outside_declared_scope_ids` with deterministic coverage
counts. They are not silently passed through, assigned generic dog labels, or
treated as mapping failures. Supporting them later requires an explicit ontology
decision and profile version.

Malformed nominally supported objects are distinguishable from deliberately
outside-scope objects. An eligible object that produces no mapping is fatal.

## Composition rules

The object mapping composes only independently promoted source facts:

- `sign_index` resolves to one established Woofmapping mode;
- `house_number` resolves to one Doghouse domain;
- missing sign or house produces `null`, not a default;
- motion, dignity, triplicity ruler, and possible formula IDs remain labelled
  source attributes;
- derived transforms add `reexpress_through_coordinate_transform`; and
- every projected object carries invariant classification, direct evidence refs,
  family groups, and proof scope.

Projection relevance is intentionally `null` in this slice. Structural strength
is prohibited. Source counts and object multiplicity are not target weights.

## Evidence hardening

Mapping exposed a source-proof requirement not fully enforced in Slice 2:
promoted house and triplicity qualifiers may rely on evidence distinct from the
object's primary coordinate evidence.

Intake now requires:

- `house_uncertainty_evidence_ref` whenever a non-cusp object has
  `house_number`; and
- `triplicity_uncertainty_evidence_ref` whenever an object has
  `triplicity_ruler`.

Both must resolve, are included in the projected row's epistemic basis, and join
the artifact evidence closure. A cusp's house number identifies which cusp the
row represents and is not itself promoted house-membership evidence.

## Projected terms

The profile carries a bounded registry identity:

`woofmapped_bounded_astrology.projected_terms` 0.1.0.

Artifacts materialize only definitions used by emitted operators, modes, and
domains. Each corresponding object attribute receives a fully qualified term
reference. The definitions retain the established target meanings, while the
registry ID prevents consumers from mistaking a bounded policy artifact for one
produced by the released exact profile.

## Packaging and release boundary

The profile's manifest, ontology, registry, and Python policy are package
resources under the existing package-data boundary. Runtime identity discovers
them as a bundled, content-addressed profile resource set.

The profile is intentionally not yet advertised through installed entry points
or 0.10.0 release compatibility. Installed exposure before relationships,
four-context QA, and release qualification would turn an internal candidate into
a false supported-release claim. That boundary is retained for Slices 8 and 9.

## Verification

- Bounded suite: 34 passed.
- Full SPC suite: 191 passed in 61.04 seconds.
- Ruff on all bounded intake, object execution, profile, and focused test code:
  passed.
- Profile manifest schema: passed.
- Projected-term registry semantic validation: passed.
- Runtime profile resource-set identity is bundled and SHA-256 addressed.
- Deterministic repeat projection and input immutability: passed.
- Unsupported context, wrong house policy, and non-invariant direct evidence
  rejection: passed.
- Existing exact and temporal suites: passed unchanged.

## Gate decision

Slice 4 is ready for review. Slice 5 may add relationship/operator projection,
ownership topology, family-aware coverage, and anti-inflation policy against the
now-qualified object endpoints. No relationship mapping has been implemented
early.

