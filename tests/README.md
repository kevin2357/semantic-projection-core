# Test suite

The test suite is organized by public capability rather than implementation
phase. Tests should describe behavior that users and maintainers can rely on;
historical development-stage labels belong in Git history, not test names.

## Layout

- `contracts/`: public API, schema, validation, identity, and property tests
- `engine/`: projection orchestration, diagnostics, audit, logging, and I/O
- `profiles/`: profile-specific behavior and vocabulary coverage
- `rendering/`: deterministic rendering behavior
- `materialization/`: static artifact materialization
- `synastry/`: relationship and directional projection behavior
- `temporal/`: temporal intake, contracts, projection, materialization, and pipeline
- `cli/`: installed entry points, convenience tools, and QA runner behavior
- `integration/`: package boundaries, discovery, and realistic end-to-end fixtures
- `fixtures/`: compact, representative source artifacts used by integration tests

Shared request construction and projection helpers live in `factories.py`.
Repository-relative test paths live in `paths.py`.

## Running tests

Run the entire suite:

```powershell
python scripts/run_qa.py
```

Run it with the enforced branch-aware coverage threshold:

```powershell
python scripts/run_qa.py --coverage
```

Run a capability-focused suite:

```powershell
python scripts/run_qa.py --suite temporal
python scripts/run_qa.py --suite woofmapped
python scripts/run_qa.py --suite cli
```

The supported suite names are `all`, `static`, `temporal`, `woofmapped`,
`cli`, and `integration`. Direct `pytest` invocation remains available for
individual files and tests.

## Test design conventions

- Prefer public entry points over private implementation details.
- Name tests after durable behavior, not roadmap phases or work chunks.
- Use compact realistic fixtures for cross-module integration behavior.
- Keep focused unit inputs inline when a fixture would obscure the behavior.
- Mark subprocess-heavy tests with `subprocess` and broader package-boundary
  tests with `integration`.
- Add regression coverage with every defect fix.
- Keep tests deterministic; projection IDs and rendered artifacts must not
  depend on process order, locale, or platform-default text encoding.

Coverage is configured in `pyproject.toml`. The suite currently enforces an
85% total branch-aware floor; the floor is a backstop, not a substitute for
testing important behavior and failure modes.

## Historical QA scripts

Development-stage runners from the temporal Stage C work are retained under
`scripts/history/temporal-stage-c/` for archaeology. They are not supported
entry points. Use `scripts/run_qa.py` for current validation.
