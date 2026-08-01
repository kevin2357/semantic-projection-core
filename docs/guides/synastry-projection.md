# Synastry projection

Synastry projection adds participant ownership and relationship roles to a canonical relationship graph, then delegates semantic mapping to the ordinary static compiler.

## Command-line route

Create a participant file:

```json
{
  "participants": [
    {"participant_id": "person-a", "role": "source"},
    {"participant_id": "person-b", "role": "target"}
  ]
}
```

Then run:

```powershell
python tools/project_synastry.py `
  --source path/to/synastry-package.json `
  --participants participants.json `
  --relationship-kind synastry `
  --profile orthodox `
  --context examples/contexts/orthodox_synastry_general_context.json `
  --out outputs/synastry.standard.json
```

Without `--participants`, the tool prompts for two or more participants. Optional `--structural-evidence`, `--source-identity`, `--options`, and `--request-out` flags expose the complete route.

## Preparation behavior

Objects receive participant ownership from explicit row fields, source identity, or resolvable object namespaces. Relationships receive source and target owner annotations, participant roles, `relationship_kind`, and an `inter_participant` flag.

An owner discovered on a source object but omitted from the supplied participant list is retained as an additional participant with role `unspecified`. Objects without resolvable ownership remain unowned; preparation does not invent identity merely to make the graph look tidier.

AGF/source registries are preserved in the normalized projection request. This is important for compact relationship packages whose semantics use registry references.

## Python route

```python
from semantic_projection import project_synastry
from semantic_projection.profiles import builtin_projection_registry

result = project_synastry(
    source_graph=graph,
    structural_evidence=evidence,
    source_identity=identity,
    source_registries=registries,
    participants=participants,
    relationship_kind="synastry",
    profile_id="orthodox_astrology.v1",
    profile_version="1.0.0",
    context=context,
    registry=builtin_projection_registry(),
)
```

The result exposes `request`, `artifact`, and `participant_index`.

Synastry is static relationship structure, not timing. Composite and Davison graphs represent relationship entities and retain their own source identities. None should be silently substituted for another.
