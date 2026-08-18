# Semantic Projection Core 0.11.1

Status: qualified candidate awaiting publication approval.

## Corrected

- Enforced the bounded Woofmapping profile's existing True Node preference.
- Excluded Mean Node derived descendants through owner closure.
- Excluded relationships touching policy-excluded endpoints.
- Reported deliberate policy exclusions separately from unsupported source
  scope in bounded audit coverage and diagnostics.
- Preserved AGF's canonical bounded calculated `Fortune` point; it is not the
  exact graph's duplicate legacy Fortune alias.

## Compatibility

The bounded request, output schema, profile, ontology, projected-term registry,
contexts, and accepted AGF wire contracts are unchanged. Distribution and engine
identity advance to 0.11.1 because executable semantic policy and its installed
fingerprints changed.

SPC 0.11.0 bounded artifacts may contain both True Node and Mean Node families
despite declaring the True Node preference. Regenerate those artifacts with
0.11.1 rather than deduplicating projected claims downstream.

## Qualification

- Complete source suite: 232 passed.
- Four-context plus exact/temporal focused regression: 22 passed.
- Two fixed-epoch wheel builds were byte-identical.
- The wheel installed non-editably under Linux/Python 3.11.
- Installed runtime smoke discovered all four profiles, seven commands, and 13
  contexts with matching 0.11.1 distribution/package/engine identity.
- All four bounded CLI contexts executed successfully from the installed wheel.

See [COMPATIBILITY.md](COMPATIBILITY.md) and
[CONSUMER INTEGRATION.md](CONSUMER%20INTEGRATION.md).
