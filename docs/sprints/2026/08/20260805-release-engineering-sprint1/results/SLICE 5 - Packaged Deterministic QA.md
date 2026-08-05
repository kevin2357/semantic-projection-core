# Slice 5 - Packaged Deterministic QA

## Result

Status: **gate passed**

The `semantic-projection-core` 0.10.0 candidate wheel was installed into a
fresh Python 3.12 environment outside the repository. The qualification
harness ran from a copied script and copied fixtures with `PYTHONPATH` cleared.
The imported `semantic_projection` module resolved from that environment's
`site-packages`, not from the checkout.

Compact machine-readable evidence is in
[deterministic-fixture-summary.json](deterministic-fixture-summary.json).

## Durable QA boundary

Added `scripts/qualify_installed_runtime.py` as a repeatable installed-wheel QA
harness. It intentionally imports neither `tests` nor repository helpers. Given
two AGF boundary fixtures, it:

- projects a natal graph through every bundled profile;
- projects Woofmapping through general, handler, direct-to-dog, and hybrid;
- validates every static artifact against the native output schema;
- proves canonical-byte repeatability for every static case;
- checks projected-term subset identity and reference closure;
- proves all four Woofmapping artifacts preserve the same source topology;
- strictly merges their artifact-scoped registries and rejects conflicting
  definitions;
- runs and validates a full temporal route twice, including its receipt;
- records artifact, registry, resource-set, fixture, and topology hashes; and
- exercises unsupported versions, missing logical and physical resources,
  registry conflict, and malformed-output failures.

The strict registry merge in this harness models the documented downstream
consumer rule. It is a QA assertion, not a newly promoted SPC runtime API.

## Installed candidate identity

- wheel: `semantic_projection_core-0.10.0-py3-none-any.whl`
- wheel bytes: `129379`
- wheel SHA-256:
  `0c4b64932a1a5b717b108e1637ecde9222ddd017f31c4fd9647ff6adc3715bf2`
- installed runtime package set:
  `a3408e8032d6a65d74716ba5e1e2fd7baa7c47aebfdbe7b196e9c3b17cd4ae48`
- semantic resource set:
  `2262689d70b38e3319a7f19a6431462a863acbb68bc8f1da31550c0a9fc72773`

This is the Slice 5 candidate identity, not the final release checksum. Slice 7
will rebuild twice under the reproducibility control and establish the final
artifact identity.

## Static and context results

Six repeated static cases passed: Orthodox, cognitive demonstration, and four
Woofmapping contexts. The Orthodox fixture produced 8 objects and 7
relationships. Cognitive and each Woofmapping context produced 7 objects and 6
relationships.

All four Woofmapping context artifacts had source-topology hash
`8ce9d2c7d42e8c7112e10e4977d439526e23bf8e16ea4f77e3dab33ea205a27a`.
Their artifact hashes differ, as required by context-bound artifact identity,
while their projected registry subsets are identical at 28 terms with registry
hash `968c459ab84631f7f81438ce3691e29c28beef0ed5536c6f23e18887a47e5005`.

## Temporal and failure results

The tiny AGF temporal source bundle passed the installed Woofmapping handler
route with one activator and one activation. Both the full temporal artifact and
route receipt were canonically byte-identical across repeated executions and
passed their native validators.

The installed runtime rejected all six negative cases:

1. canonical graph version `9.9.9`;
2. Woofmapping profile version `9.9.9`;
3. an unavailable exact context version;
4. the exact handler context after its JSON file was removed from a temporary
   shadow copy of the installed package;
5. a conflicting definition under an existing projected-term key; and
6. a projected static artifact missing required metadata.

The temporary shadow package was scoped to the harness process and removed
automatically.

## Console, discovery, and repository QA

All six installed commands passed a safe installed invocation. The five data
commands passed `--help`; `semantic-runtime-smoke` completed successfully and
wrote the installed release manifest. Installed entry-point discovery returned
the three declared bundled profiles.

The initial clean-environment repository run exposed one obsolete test
allowance that removed `semantic-runtime-smoke` from the expected command set.
The new editable installation correctly included the command, so the test was
corrected to require exact equality. The corrected full suite passed: 157 tests.

## Boundary and deferral

The fixtures are SPC's checked-in AGF 1.3.0 natal boundary fixture and Foundry
temporal bundle 1.0.0 fixture, both identified by hashes in the JSON evidence.
They establish the installed AGF-to-SPC contract boundary without importing
AGF or using an editable SPC checkout.

Slice 6 remains responsible for the controlled real AGF runtime to installed
SPC wheel to SBE acceptance proof, including Ella if compatible. No SBE claim
is made by this slice.
