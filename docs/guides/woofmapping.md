# Woofmapping

Woofmapped Astrology is a playful experimental reference profile that projects canonical astrology operators, modes, domains, interfaces, and relations into dog-centered behavioral semantics. It uses the same deterministic engine, audit, provenance, and materialization contracts as every other profile.

It is not veterinary advice, behavioral diagnosis, or an empirically validated model. It is, however, extremely serious about Doghouses.

## Natal

```powershell
python tools/woofmap_natal.py `
  --source path/to/natal-package.json `
  --out outputs/natal.woof.standard.json
```

This fixes the profile to `woofmapped_astrology.v0` 0.1.0 and defaults to `woofmapped_doghouse_general_context.json`. Supply `--context` to override the default. Other natal flags and output modes remain available.

## Transit

```powershell
python tools/woofmap_transit.py `
  --bundle path/to/temporal_projection_source_bundle.json `
  --audience handler `
  --out outputs/transit.woof.handler.standard.json
```

Audiences select a bundled context over the same primitive profile:

| Audience | Context | Intent |
|---|---|---|
| `handler` | `woofmapped.handler_guidance.v1` | Baseline-relative practical guidance framing |
| `dog` | `woofmapped.dog_direct.v1` | Direct dog-facing framing |
| `hybrid` | `woofmapped.hybrid_horoscope.v1` | Combined horoscope framing |

Handler is the default. Recommendation synthesis and final horoscope prose remain downstream.

## Synastry

```powershell
python tools/woofmap_synastry.py `
  --source path/to/synastry-package.json `
  --kind human-dog `
  --participant-a-id kevin `
  --participant-b-id bre `
  --out outputs/kevin-bre.woof.standard.json
```

Supported kinds are:

- `human-dog`: participant A defaults to handler/human and B to dog/canine.
- `dog-dog`: both participants default to dog/canine.

IDs are required; labels, roles, and species may be overridden. The tool selects the matching bundled context and preserves source registries.

Use `--request-out` when another pipeline needs the normalized request or participant annotations. All three tools support `--help` and can run entirely without prompts when required flags are supplied.
