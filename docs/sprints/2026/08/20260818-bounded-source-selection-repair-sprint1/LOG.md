# Bounded Source-Selection Repair Sprint 1 Log

Append-only chronological record. Commands, findings, decisions, changes,
verification, approvals, commits, release identities, and publication evidence
belong here as slices proceed.

## 2026-08-18 - Initial repository state and defect report

- Repository began clean on `main` at `da688c6` (`Document AGF 0.8.1 bounded
  compatibility`).
- A first downstream bounded authoring cycle produced both True Node and Mean
  Node claims. SBE QA correctly classified the resulting content as duplicate.
- Exact Woofmapped static projection already prefers True Node, excludes Mean
  Node through `excluded_by_source_selection_policy`, and excludes relationships
  touching the removed row. Existing regression coverage proves that behavior.
- The bounded profile declares `node_variant: true` and
  `fortune_variant: part_of_fortune`, but its object classifier currently checks
  only source shape and mapping availability. Both node variants therefore map
  to the same North Node semantic primitive under distinct source identities.
- The same implementation gap can affect the declared Fortune preference,
  derived rows owned by excluded aliases, dependent relationships, coverage,
  family accounting, registries, and all four contexts.
- No implementation change has begun. Candidate version 0.11.1 is a planning
  recommendation pending Slice 1 audit.

## 2026-08-18 - Planning gate

- Created the sprint plan, append-only log, and results index.
- Current gate is plan review. Implementation is not authorized.

## 2026-08-18 - Plan approval

- User approved the sprint plan and authorized commit, push, and Slice 1 work.
- Marked the sprint active and opened the reproduction/policy-closure audit.
