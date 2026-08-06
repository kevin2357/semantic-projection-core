# ADR-0002 — Require Invariant Full Schema Validation at Runtime

```yaml
status: accepted
date: 2026-08-05
owner: semantic-projection-core
scope: contract validation
```

## Context

Before release qualification, `jsonschema` was optional and dev-only. When it
was absent, `validate_contract()` performed only shallow required-field checks.
The same invalid document could therefore be accepted or rejected depending on
ambient packages unrelated to the declared SPC runtime.

That behavior made the public contract environment-dependent and prevented a
wheel-only consumer from knowing which validation boundary it had installed.

## Decision

Full Draft 2020-12 JSON Schema validation is required runtime behavior.
`jsonschema>=4,<5` is a mandatory distribution dependency, and SPC does not
silently fall back to shallow validation.

Specialized deterministic and referential-integrity validators continue to
enforce constraints that JSON Schema alone cannot express.

## Consequences

- Source checkouts and installed wheels enforce the same schema depth.
- A missing validation dependency is an installation failure, not a reduced
  operating mode.
- Consumer environments must install declared dependencies rather than relying
  on SPC's historical zero-dependency assumption.
- Schema-version and validation-behavior changes belong in compatibility and
  release qualification.
