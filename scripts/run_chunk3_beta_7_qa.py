from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Any

from semantic_projection import ProjectionContext, project_foundry_temporal_bundle
from semantic_projection.artifact_identity import identify_artifact

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "outputs" / "fixture_test_files"
OUTPUTS = ROOT / "outputs" / "fixture_outputs"
CONTEXT = ROOT / "examples" / "contexts" / "cognitive_architecture_general_context.json"


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_pytest() -> dict[str, Any]:
    result = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT, text=True, capture_output=True, encoding="utf-8")
    (OUTPUTS / "pytest.log").write_text(result.stdout + result.stderr + f"\nEXIT_CODE={result.returncode}\n", encoding="utf-8")
    return {"exit_code": result.returncode, "passed": result.returncode == 0}


def find_bundles() -> list[Path]:
    rows=[]; found=[]
    for path in sorted(FIXTURES.glob("*.json")):
        payload=json.loads(path.read_text(encoding="utf-8"))
        identity=identify_artifact(payload)
        rows.append({"path":str(path.relative_to(ROOT)), **identity.to_dict()})
        if identity.kind == "foundry_temporal_projection_source_bundle":
            found.append(path)
    write_json(OUTPUTS / "fixture_inventory.json", {"artifacts": rows})
    if not found:
        raise RuntimeError("Expected at least one Foundry temporal source bundle.")
    return found


def main() -> int:
    shutil.rmtree(OUTPUTS, ignore_errors=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    summary={"stage":"C7","status":"failed"}
    try:
        summary["pytest"]=run_pytest()
        if not summary["pytest"]["passed"]:
            raise RuntimeError("pytest failed")
        context=ProjectionContext.from_dict(json.loads(CONTEXT.read_text(encoding="utf-8")))
        bundles=find_bundles()
        routes=[]
        for index,path in enumerate(bundles, start=1):
            bundle=json.loads(path.read_text(encoding="utf-8"))
            stem=f"route_{index}_{path.stem}"
            first=project_foundry_temporal_bundle(bundle, profile_id="cognitive_architecture_demo.v0", profile_version="0.2.0", context=context, output_mode="standard")
            second=project_foundry_temporal_bundle(bundle, profile_id="cognitive_architecture_demo.v0", profile_version="0.2.0", context=context, output_mode="standard")
            out1=OUTPUTS/f"{stem}.standard.json"; out2=OUTPUTS/f"{stem}.standard.run2.json"
            write_json(out1, first.artifact); write_json(out2, second.artifact)
            write_json(OUTPUTS/f"{stem}.request.json", first.request)
            write_json(OUTPUTS/f"{stem}.receipt.json", first.receipt)
            same=out1.read_bytes()==out2.read_bytes()
            route={
                "fixture":str(path.relative_to(ROOT)),
                "target_family":first.receipt["metadata"]["target_family"],
                "request_id":first.receipt["metadata"]["request_id"],
                "projected_graph_id":first.receipt["metadata"]["projected_graph_id"],
                "route_hash":first.receipt["metadata"]["route_hash"],
                "byte_identical":same,
                "sha256_run1":sha256(out1),
                "sha256_run2":sha256(out2),
                "size_bytes":out1.stat().st_size,
            }
            if not same:
                raise RuntimeError(f"Non-deterministic production route for {path.name}")
            routes.append(route)
        write_json(OUTPUTS/"production_routes.json", {"routes":routes})
        summary.update({"status":"passed","fixture_count":len(bundles),"routes":routes,"all_deterministic":all(r["byte_identical"] for r in routes)})
        write_json(OUTPUTS/"qa_summary.json", summary)
        return 0
    except Exception as exc:
        summary["error"]=str(exc); summary["traceback"]=traceback.format_exc()
        write_json(OUTPUTS/"qa_summary.json", summary)
        print(summary["traceback"], file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
