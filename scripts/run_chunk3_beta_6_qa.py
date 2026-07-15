from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Any

from semantic_projection import (
    ProjectionContext,
    adapt_foundry_temporal_source_bundle,
    canonical_temporal_fact_view,
    materialize_projected_temporal_graph,
    project_temporal,
)
from semantic_projection.artifact_identity import identify_artifact
from semantic_projection.ids import stable_hash
from semantic_projection.logging_config import configure_logging, log_event

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "outputs" / "fixture_test_files"
OUTPUTS = ROOT / "outputs" / "fixture_outputs"

CASES = {
    "orthodox_general": {
        "profile_id": "orthodox_astrology.v1",
        "profile_version": "1.0.0",
        "context": "orthodox_general_context.json",
    },
    "orthodox_professional": {
        "profile_id": "orthodox_astrology.v1",
        "profile_version": "1.0.0",
        "context": "orthodox_relationship_professional_context.json",
    },
    "cognitive": {
        "profile_id": "cognitive_architecture_demo.v0",
        "profile_version": "0.2.0",
        "context": "cognitive_architecture_general_context.json",
    },
    "woofmapped": {
        "profile_id": "woofmapped_astrology.v0",
        "profile_version": "0.1.0",
        "context": "woofmapped_doghouse_general_context.json",
    },
}


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_pytest() -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    (OUTPUTS / "pytest.log").write_text(
        result.stdout + result.stderr + f"\nEXIT_CODE={result.returncode}\n",
        encoding="utf-8",
    )
    return {"exit_code": result.returncode, "passed": result.returncode == 0}


def find_bundle() -> Path:
    candidates = []
    inventory = []
    for path in sorted(FIXTURES.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        identity = identify_artifact(payload)
        inventory.append({
            "path": str(path.relative_to(ROOT)),
            "kind": identity.kind,
            "package_type": identity.package_type,
            "contract_version": identity.contract_version,
        })
        if identity.kind == "foundry_temporal_projection_source_bundle":
            candidates.append(path)
    write_json(OUTPUTS / "fixture_inventory.json", {"artifacts": inventory})
    if len(candidates) != 1:
        raise RuntimeError(f"Expected exactly one Foundry temporal source bundle; found {len(candidates)}.")
    return candidates[0]


def temporal_facts_by_source(graph: dict[str, Any]) -> dict[str, Any]:
    return {
        row["source_activation_ref"]: canonical_temporal_fact_view(row["temporal_facts"])
        for row in graph.get("projected_activations") or []
    }


def semantics_by_source(graph: dict[str, Any]) -> dict[str, Any]:
    activators = {
        row["id"]: row for row in graph.get("projected_activators") or []
    }
    return {
        row["source_activation_ref"]: {
            "projected_relationship_type": row["projected_relationship_type"],
            "projected_activator_ref": row["projected_activator_ref"],
            "projected_activator_operator": (
                activators.get(row["projected_activator_ref"]) or {}
            ).get("projected_operator_ref"),
            "projected_target_ref": row["projected_target_ref"],
            "projected_activation_domain_ref": row.get("projected_activation_domain_ref"),
        }
        for row in graph.get("projected_activations") or []
    }


def main() -> int:
    shutil.rmtree(OUTPUTS, ignore_errors=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    logger = configure_logging(log_path=OUTPUTS / "semantic_projection.log")
    summary: dict[str, Any] = {"stage": "C6", "status": "failed"}
    try:
        summary["pytest"] = run_pytest()
        if not summary["pytest"]["passed"]:
            raise RuntimeError("pytest failed")

        bundle_path = find_bundle()
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        results: dict[str, dict[str, Any]] = {}

        for name, spec in CASES.items():
            context_payload = json.loads(
                (ROOT / "examples" / "contexts" / spec["context"]).read_text(encoding="utf-8")
            )
            request = adapt_foundry_temporal_source_bundle(
                bundle,
                profile_id=spec["profile_id"],
                profile_version=spec["profile_version"],
                context=ProjectionContext.from_dict(context_payload),
            )
            full = project_temporal(request)
            standard = materialize_projected_temporal_graph(full, mode="standard")
            summary_view = materialize_projected_temporal_graph(full, mode="summary")
            write_json(OUTPUTS / f"{name}.standard.json", standard)
            write_json(OUTPUTS / f"{name}.summary.json", summary_view)
            results[name] = full
            coverage = full["summary"]["coverage"]
            log_event(
                logger,
                "c6_profile_projection_completed",
                case=name,
                profile_id=spec["profile_id"],
                context_id=context_payload["context_id"],
                projected_activators=len(full["projected_activators"]),
                projected_activations=len(full["projected_activations"]),
                projected_sequences=len(full["projected_sequences"]),
                target_eligible_but_unmapped=coverage["activations"]["target_eligible_but_unmapped_count"],
            )

        # Determinism: regenerate Cognitive standard independently.
        cog_spec = CASES["cognitive"]
        cog_context = ProjectionContext.from_dict(json.loads(
            (ROOT / "examples" / "contexts" / cog_spec["context"]).read_text(encoding="utf-8")
        ))
        cog_request2 = adapt_foundry_temporal_source_bundle(
            bundle,
            profile_id=cog_spec["profile_id"],
            profile_version=cog_spec["profile_version"],
            context=cog_context,
        )
        cog_standard2 = materialize_projected_temporal_graph(
            project_temporal(cog_request2), mode="standard"
        )
        run2 = OUTPUTS / "cognitive.standard.run2.json"
        write_json(run2, cog_standard2)
        run1 = OUTPUTS / "cognitive.standard.json"
        determinism = {
            "byte_identical": run1.read_bytes() == run2.read_bytes(),
            "bytes_run1": run1.stat().st_size,
            "bytes_run2": run2.stat().st_size,
            "sha256_run1": sha256(run1),
            "sha256_run2": sha256(run2),
        }
        write_json(OUTPUTS / "determinism_result.json", determinism)

        # Cross-profile invariant comparison on source arcs common to all three ontologies.
        core_names = ["orthodox_general", "cognitive", "woofmapped"]
        fact_maps = {name: temporal_facts_by_source(results[name]) for name in core_names}
        common = sorted(set.intersection(*(set(value) for value in fact_maps.values())))
        fact_mismatches = []
        for source_ref in common:
            hashes = {name: stable_hash(fact_maps[name][source_ref]) for name in core_names}
            if len(set(hashes.values())) != 1:
                fact_mismatches.append({"source_activation_ref": source_ref, "hashes": hashes})

        semantic_maps = {name: semantics_by_source(results[name]) for name in core_names}
        distinct_semantic_examples = []
        for source_ref in common:
            values = {name: semantic_maps[name][source_ref] for name in core_names}
            signature = {
                name: (
                    row["projected_relationship_type"],
                    row["projected_activator_operator"],
                    row["projected_activation_domain_ref"],
                )
                for name, row in values.items()
            }
            if len(set(signature.values())) > 1:
                distinct_semantic_examples.append({
                    "source_activation_ref": source_ref,
                    "semantics": values,
                })
            if len(distinct_semantic_examples) >= 10:
                break

        # Orthodox context comparison: same temporal facts and source arc set, context-specific semantics.
        general = results["orthodox_general"]
        professional = results["orthodox_professional"]
        general_facts = temporal_facts_by_source(general)
        professional_facts = temporal_facts_by_source(professional)
        context_common = sorted(set(general_facts) & set(professional_facts))
        context_fact_mismatches = [
            ref for ref in context_common
            if stable_hash(general_facts[ref]) != stable_hash(professional_facts[ref])
        ]
        general_sem = semantics_by_source(general)
        professional_sem = semantics_by_source(professional)
        context_semantic_changes = [
            {
                "source_activation_ref": ref,
                "general": general_sem[ref],
                "professional": professional_sem[ref],
            }
            for ref in context_common
            if general_sem[ref] != professional_sem[ref]
        ]

        comparison = {
            "profile_counts": {
                name: {
                    "profile_id": results[name]["metadata"]["profile_id"],
                    "context_id": results[name]["metadata"]["context_id"],
                    "projected_activator_count": len(results[name]["projected_activators"]),
                    "projected_activation_count": len(results[name]["projected_activations"]),
                    "projected_sequence_count": len(results[name]["projected_sequences"]),
                    "projected_state_count": results[name]["summary"]["projected_observation_state_count"],
                    "coverage": results[name]["summary"]["coverage"],
                }
                for name in results
            },
            "cross_profile_common_activation_count": len(common),
            "cross_profile_temporal_fact_mismatches": fact_mismatches,
            "cross_profile_temporal_facts_preserved": not fact_mismatches,
            "distinct_semantic_examples": distinct_semantic_examples,
            "orthodox_context_common_activation_count": len(context_common),
            "orthodox_context_temporal_fact_mismatches": context_fact_mismatches,
            "orthodox_context_temporal_facts_preserved": not context_fact_mismatches,
            "orthodox_context_semantic_change_count": len(context_semantic_changes),
            "orthodox_context_semantic_change_examples": context_semantic_changes[:10],
            "cognitive_spirit_status": {
                "eligible_but_unmapped": results["cognitive"]["summary"]["coverage"]["activations"]["target_eligible_but_unmapped_count"],
                "profile_scope_excluded": results["cognitive"]["summary"]["coverage"]["activations"]["target_excluded_by_profile_scope_count"],
            },
            "summary_semantic_hashes_present": all(
                "semantic_hashes" in json.loads(
                    (OUTPUTS / f"{name}.summary.json").read_text(encoding="utf-8")
                )
                for name in results
            ),
            "upstream_limitations_annotated": all(
                all(isinstance(row, dict) and row.get("status") for row in result["upstream_source_limitations"])
                for result in results.values()
            ),
        }
        write_json(OUTPUTS / "cross_profile_comparison.json", comparison)

        summary.update({
            "status": "passed",
            "fixture": str(bundle_path.relative_to(ROOT)),
            "case_count": len(results),
            "determinism": determinism,
            "cross_profile_temporal_facts_preserved": comparison["cross_profile_temporal_facts_preserved"],
            "orthodox_context_temporal_facts_preserved": comparison["orthodox_context_temporal_facts_preserved"],
            "orthodox_context_semantic_change_count": comparison["orthodox_context_semantic_change_count"],
            "summary_semantic_hashes_present": comparison["summary_semantic_hashes_present"],
            "upstream_limitations_annotated": comparison["upstream_limitations_annotated"],
        })
        write_json(OUTPUTS / "qa_summary.json", summary)
        print(f"Chunk 3.beta.6 QA passed. Outputs: {OUTPUTS}")
        return 0
    except Exception as exc:
        summary["error"] = str(exc)
        summary["traceback"] = traceback.format_exc()
        write_json(OUTPUTS / "qa_summary.json", summary)
        (OUTPUTS / "qa_runner.log").write_text(summary["traceback"], encoding="utf-8")
        print(f"Chunk 3.beta.6 QA failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
