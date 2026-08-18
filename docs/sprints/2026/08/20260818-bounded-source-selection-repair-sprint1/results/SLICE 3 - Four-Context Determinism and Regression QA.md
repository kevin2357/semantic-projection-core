# Slice 3 - Four-Context Determinism and Regression QA

## Outcome

The bounded source-selection repair is deterministic and context-invariant
across all four supported Woofmapping contexts. The complete SPC source suite
passes with the candidate installed editably in a writable ephemeral Linux
environment, and focused exact-static and temporal regressions confirm the
repair did not disturb their established source-selection behavior.

## Four-context guarantees exercised

For general, handler, direct-to-dog, and hybrid:

- True Node and its eligible derived family are retained;
- Mean Node and its derived family are excluded by policy;
- every relationship touching the excluded family is excluded;
- exclusion counts and ordered source-ID ledgers are identical;
- projected artifacts remain structurally and epistemically parallel;
- no context receives canonical or epistemic priority; and
- repeated execution of each request produces equal contract objects.

The fixture follows AGF 0.8.1 bounded object types, names, owner references,
evidence metadata, and relationship shapes. It intentionally uses both canonical
spaced and normalized underscore spelling to keep compatibility normalization
under test.

## Regression qualification

The final corrected source harness:

1. mounted the checkout read-only;
2. copied only the source-suite-required repository material into ephemeral
   writable container storage;
3. removed the image's released SPC 0.11.0 wheel;
4. installed the copied candidate editably with development dependencies; and
5. ran from the copied repository root under Python 3.11.

Results:

- complete SPC source suite: **232 passed** in 56.08 seconds;
- focused four-context, bounded selection, exact static node/Fortune, and
  temporal Mean Node tests: **22 passed** in 119.57 seconds;
- focused Ruff over all sprint-changed Python files: **passed**.

The focused exact and temporal cases retain their existing expected behavior:
exact projection removes Mean Node and the legacy Fortune alias in favor of True
Node and Part of Fortune, while temporal activator classification continues to
report Mean Node as policy-excluded.

## Harness findings

The initial read-only in-place run was not a valid full source-suite harness:
two CLIs use a default repository-relative log path, and release-identity tests
correctly distinguish an installed wheel from an editable checkout. Those four
failures disappeared when the candidate was installed editably from writable
ephemeral storage. Intermediate minimal-copy failures were likewise caused by
omitted repository tools and durable fixtures, not executable behavior.

Whole-tree Ruff was inspected but is not claimed as clean. The current Windows
mount presents Python files to Linux as executable, producing widespread
`EXE002`, and unrelated historical files retain existing lint debt. The bounded
implementation and tests touched by this sprint pass focused Ruff with only that
filesystem-mode artifact excluded.

## Evidence and gate disposition

Compact machine-readable evidence is in
[`four-context-regression-verification.json`](four-context-regression-verification.json).

Slice 3 is ready for review. Release identity, installed-wheel qualification,
compatibility guidance, reproducible build evidence, and downstream handoff
remain Slice 4 work.
