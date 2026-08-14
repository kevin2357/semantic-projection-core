# 0.11.0 consumer integration

This candidate is not active until the annotated tag and published assets have
been verified. Once published, install the private wheel using the exact URL
and SHA-256 in [requirements-production.txt](requirements-production.txt), then
run:

```powershell
semantic-runtime-smoke --require-installed --json
```

For bounded natal input, invoke `semantic-bounded-project` once for each exact
supported context. Preserve the native artifact, projected-term registry,
source evidence, capabilities, limitations, family and correspondence IDs,
and complete runtime provenance. Reject version drift and missing resources.

Do not pass bounded output to an exact-only authoring policy or fill `null`
scores with defaults. See the full
[consumer handoff](../../docs/integration/release-consumer-handoff.md).
