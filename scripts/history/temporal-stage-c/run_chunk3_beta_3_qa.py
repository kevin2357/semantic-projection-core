from __future__ import annotations
import hashlib, json, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; FIXTURES=ROOT/"outputs"/"fixture_test_files"; OUTPUTS=ROOT/"outputs"/"fixture_outputs"
CONTEXT=ROOT/"examples"/"contexts"/"cognitive_architecture_general_context.json"
def run(cmd,name,expected={0}):
    r=subprocess.run(cmd,cwd=ROOT,text=True,encoding="utf-8",errors="replace",capture_output=True)
    (OUTPUTS/name).write_text("$ "+" ".join(cmd)+"\n\nSTDOUT\n"+r.stdout+"\nSTDERR\n"+r.stderr+f"\nEXIT_CODE={r.returncode}\n",encoding="utf-8")
    if r.returncode not in expected: raise RuntimeError(f"Command failed ({r.returncode}): {' '.join(cmd)}")
    return r
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    OUTPUTS.mkdir(parents=True,exist_ok=True)
    for p in OUTPUTS.iterdir():
        if p.is_file(): p.unlink()
        else: shutil.rmtree(p)
    run([sys.executable,"-m","pytest","-q"],"pytest.log")
    from semantic_projection import identify_artifact
    inventory=[]; bundles=[]
    for p in sorted(FIXTURES.glob("*.json")):
        try:
            ident=identify_artifact(json.loads(p.read_text(encoding="utf-8")))
            inventory.append({"file":p.name,**ident.to_dict()})
            if ident.kind=="foundry_temporal_projection_source_bundle": bundles.append(p)
        except Exception as e: inventory.append({"file":p.name,"kind":"unreadable","error":str(e)})
    (OUTPUTS/"fixture_inventory.json").write_text(json.dumps(inventory,indent=2)+"\n",encoding="utf-8")
    if len(bundles)!=1: raise RuntimeError(f"Expected exactly one source bundle; found {len(bundles)}")
    bundle=bundles[0]; request=OUTPUTS/"temporal_request.json"; log=OUTPUTS/"semantic_projection.log"
    run([sys.executable,"-m","semantic_projection.temporal_cli","--bundle",str(bundle),"--projection-profile","cognitive_architecture_demo.v0","--projection-profile-version","0.2.0","--projection-context",str(CONTEXT),"--log-file",str(log),"--out",str(request)],"intake.log")
    a=OUTPUTS/"temporal_foundations_run1.json"; b=OUTPUTS/"temporal_foundations_run2.json"
    base=[sys.executable,"-m","semantic_projection.temporal_foundations_cli","--request",str(request),"--log-file",str(log)]
    run(base+["--out",str(a)],"foundations_run1.log"); run(base+["--out",str(b)],"foundations_run2.log")
    det={"byte_identical":a.read_bytes()==b.read_bytes(),"sha256_run1":sha(a),"sha256_run2":sha(b),"bytes":a.stat().st_size}
    (OUTPUTS/"determinism_result.json").write_text(json.dumps(det,indent=2)+"\n",encoding="utf-8")
    wrong=OUTPUTS/"wrong_input_should_not_exist.json"
    neg=run([sys.executable,"-m","semantic_projection.temporal_foundations_cli","--request",str(bundle),"--out",str(wrong),"--log-file",str(log)],"wrong_artifact.log",expected={2})
    result=json.loads(a.read_text(encoding="utf-8"))
    summary={"qa_contract":"chunk3.beta.3","pytest_passed":True,"fixture_inventory":inventory,"determinism":det,
             "wrong_artifact_rejected":neg.returncode==2 and not wrong.exists(),
             "static_projected_object_count":len(result["projected_target_graph"]["objects"]),
             "projected_activator_count":len(result["projected_activators"]),
             "unmapped_activator_count":result["coverage"]["unmapped_activator_count"],
             "passed":det["byte_identical"] and neg.returncode==2 and not wrong.exists()}
    (OUTPUTS/"qa_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(f"Chunk 3.beta.3 QA complete. Attach: {OUTPUTS}")
    return 0 if summary["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
