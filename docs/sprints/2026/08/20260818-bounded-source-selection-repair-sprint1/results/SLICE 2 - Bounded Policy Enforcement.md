# Slice 2 - Bounded Policy Enforcement

## Outcome

The Woofmapped bounded route now enforces its declared True Node preference as
a closed source-selection policy. Mean Node is excluded before mapping, and the
exclusion follows its derived objects and every relationship touching an
excluded endpoint.

The implementation does not alter the existing bounded output schema. It uses
the schema's extensible audit object to distinguish deliberate policy exclusion
from unsupported source scope.

## Implemented boundary

- `bounded_natal_body` named `Mean Node` is
  `excluded_by_source_selection_policy`.
- Name normalization accepts AGF's canonical spaced form and underscore-form
  compatibility fixtures.
- True Node remains eligible.
- Derived objects inherit exclusion through `owner_object_ref`.
- Relationships inherit exclusion when either endpoint is excluded.
- Mean Node is not promoted when True Node is absent.
- AGF bounded `bounded_calculated_point` named `Fortune` remains eligible. This
  is the one canonical bounded calculated point, not the exact graph's duplicate
  legacy Lot-of-Fortune alias that exact source selection removes.

## Audit behavior

The bounded audit now records deterministic object and relationship policy
exclusion counts and ID lists separately from `outside_declared_scope`. An
informational `bounded.source_selection.exclusions` diagnostic repeats the
excluded IDs for operational discovery.

Projected-term materialization remains based only on emitted entities. Excluded
Mean Node records therefore cannot enlarge the artifact-scoped used-term subset.

## Focused verification

The checkout was mounted read-only into the existing Linux Python 3.11 QA image.
An ephemeral pytest installation ran:

```text
tests/bounded/test_bounded_source_selection.py
tests/bounded/test_bounded_object_projection.py
tests/bounded/test_bounded_relationship_projection.py
```

Result: **21 passed** in 33.12 seconds. The only warning was pytest's expected
failure to create `.pytest_cache` on the read-only mount.

Machine-readable evidence is in
[`bounded-source-selection-verification.json`](bounded-source-selection-verification.json).

## Gate disposition

Slice 2 is ready for review. This slice intentionally does not change package or
engine versions, profile manifests, runtime fingerprints, release notes, or
downstream fixtures; those remain within subsequent sprint slices.
