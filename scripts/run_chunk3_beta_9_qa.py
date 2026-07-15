from __future__ import annotations
import hashlib, json, shutil, subprocess, sys, traceback
from pathlib import Path
from typing import Any
from semantic_projection import ProjectionContext, project_foundry_temporal_bundle
from semantic_projection.artifact_identity import identify_artifact
ROOT=Path(__file__).resolve().parents[1]; FIXTURES=ROOT/"outputs"/"fixture_test_files"; OUTPUTS=ROOT/"outputs"/"fixture_outputs"
def write_json(path:Path,value:Any): path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
def sha(path:Path): return hashlib.sha256(path.read_bytes()).hexdigest()
def context(name:str): return ProjectionContext.from_dict(json.loads((ROOT/"examples"/"contexts"/name).read_text(encoding="utf-8")))
def main():
 shutil.rmtree(OUTPUTS,ignore_errors=True); OUTPUTS.mkdir(parents=True,exist_ok=True); summary={"pass":"3.beta.9","status":"failed"}
 try:
  r=subprocess.run([sys.executable,"-m","pytest","-q"],cwd=ROOT,text=True,capture_output=True,encoding="utf-8"); (OUTPUTS/"pytest.log").write_text(r.stdout+r.stderr+f"\nEXIT_CODE={r.returncode}\n",encoding="utf-8"); summary["pytest"]={"passed":r.returncode==0,"exit_code":r.returncode}
  if r.returncode: raise RuntimeError("pytest failed")
  rows=[]; found=[]
  for p in sorted(FIXTURES.glob("*.json")):
   payload=json.loads(p.read_text(encoding="utf-8")); ident=identify_artifact(payload); rows.append({"path":str(p.relative_to(ROOT)),**ident.to_dict()});
   if ident.kind=="foundry_temporal_projection_source_bundle": found.append(p)
  write_json(OUTPUTS/"fixture_inventory.json",{"artifacts":rows})
  if len(found)!=1: raise RuntimeError(f"Expected exactly one Foundry bundle; found {len(found)}")
  bundle=json.loads(found[0].read_text(encoding="utf-8")); reports={}
  for stem,ctxname in (("woofmapped_handler","woofmapped_handler_guidance_context.json"),("woofmapped_dog_direct","woofmapped_dog_direct_context.json")):
   a=project_foundry_temporal_bundle(bundle,profile_id="woofmapped_astrology.v0",profile_version="0.1.0",context=context(ctxname),output_mode="standard").artifact
   b=project_foundry_temporal_bundle(bundle,profile_id="woofmapped_astrology.v0",profile_version="0.1.0",context=context(ctxname),output_mode="standard").artifact
   p1=OUTPUTS/f"{stem}.standard.json"; p2=OUTPUTS/f"{stem}.standard.run2.json"; write_json(p1,a); write_json(p2,b)
   reports[stem]={"context_id":a["metadata"]["context_id"],"determinism_repeat_executed":True,"byte_identical":p1.read_bytes()==p2.read_bytes(),"sha256_run1":sha(p1),"sha256_run2":sha(p2),"projected_activators":len(a["projected_activators"]),"projected_activations":len(a["projected_activations"]),"capability_status":a["metadata"].get("capability_status"),"contract_generation":a["metadata"].get("contract_generation")}
  if not all(x["byte_identical"] for x in reports.values()): raise RuntimeError("Determinism repeat failed")
  summary.update({"status":"passed","fixture":str(found[0].relative_to(ROOT)),"contexts":reports,"all_executed_determinism_checks_passed":True,"all_routes_determinism_tested":True})
  write_json(OUTPUTS/"qa_summary.json",summary); return 0
 except Exception as e:
  summary["error"]=str(e); summary["traceback"]=traceback.format_exc(); write_json(OUTPUTS/"qa_summary.json",summary); print(summary["traceback"],file=sys.stderr); return 1
if __name__=="__main__": raise SystemExit(main())
