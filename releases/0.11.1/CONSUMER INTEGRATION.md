# Consumer Integration - Semantic Projection Core 0.11.1

Install only the immutable release wheel and verify its exact SHA-256:

```text
semantic-projection-core @ https://github.com/kevin2357/semantic-projection-core/releases/download/semantic-projection-core-v0.11.1/semantic_projection_core-0.11.1-py3-none-any.whl \
    --hash=sha256:dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612
```

Then require a non-editable 0.11.1 runtime:

```text
semantic-runtime-smoke --require-installed --json
```

For bounded natal, invoke `semantic-bounded-project` once for each exact context
ID/version. Preserve the native outputs, runtime receipt, AGF runtime receipt,
source hash, registry, audit, evidence closure, and correspondence IDs.

Do not repair 0.11.0 output in SBE. Regenerate it with 0.11.1 so source-selection
closure occurs before projected identity, evidence, registry, and relevance are
created.

See the complete
[`release-consumer-handoff.md`](../../docs/integration/release-consumer-handoff.md).
