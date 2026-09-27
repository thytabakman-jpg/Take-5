"""Deterministic Take-6 tool-capsule compiler from current Take-5 authority."""
from __future__ import annotations
from dataclasses import asdict
import hashlib,json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"runtime"))

from portable_tool_conductor import compilation_witness
from tool_manifest import manifest_for
from tool_run_registry import CONFIGURED_RUNS

def _canon(v):
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,default=str).encode("utf-8")

def cid(v):
    return "sha256:"+hashlib.sha256(_canon(v)).hexdigest()

def _put(store,payload):
    key=cid(payload)
    prior=store.get(key)
    if prior is not None and prior!=payload:
        raise RuntimeError("TAKE6_CAPSULE_CID_COLLISION")
    store[key]=payload
    return key

def compile_tool_capsules(*,source_basis):
    store={}
    capsules=[]
    for tool_id in sorted(CONFIGURED_RUNS):
        spec=CONFIGURED_RUNS[tool_id]
        manifest=manifest_for(tool_id)
        witness=compilation_witness(tool_id)

        spec_payload={
            "kind":"TAKE5_CONFIGURED_TOOL_SPEC",
            "tool_id":tool_id,
            "configured_run":asdict(spec),
            "manifest":asdict(manifest),
        }
        spec_cid=_put(store,spec_payload)

        runtime_payload={
            "kind":"TAKE5_NATIVE_RUNTIME_WITNESS",
            "tool_id":tool_id,
            "witness":witness.payload(),
        }
        runtime_cid=_put(store,runtime_payload) if witness.entrypoint else None

        dependency_cids=[]
        for binding in manifest.bindings:
            dep={
                "kind":"TAKE5_PROTECTED_BINDING",
                "tool_id":tool_id,
                "binding":asdict(binding),
            }
            dependency_cids.append(_put(store,dep))

        protected=sorted(set(manifest.behavior_ids())|set(spec.protected_behaviors))
        tests=sorted(set(b.witness for b in manifest.bindings))
        open_coordinates=[]
        if not spec.complete():
            open_coordinates.append("CONFIGURED_RUN_INCOMPLETE")
        if not manifest.complete():
            open_coordinates.append("MANIFEST_INCOMPLETE")
        if witness.entrypoint is None:
            open_coordinates.append("NATIVE_RUNTIME_UNRECOVERED")

        capsule={
            "tool_id":tool_id,
            "spec_cid":spec_cid,
            "runtime_cid":runtime_cid,
            "dependency_cids":sorted(set(dependency_cids)),
            "protected_behaviors":protected,
            "equivalence_tests":tests,
            "environment_contract":{
                "required_environment":list(witness.required_environment),
                "self_contained":bool(witness.self_contained),
                "execution_status":witness.status,
            },
            "open_coordinates":sorted(set(open_coordinates)),
        }
        capsule_cid=_put(store,{"kind":"TAKE6_TOOL_CAPSULE","capsule":capsule})
        capsules.append({"capsule_cid":capsule_cid,**capsule})

    body={
        "schema_version":"0.1",
        "object_id":"TAKE6:TOOL-CAPSULE-INDEX:001",
        "source_basis":str(source_basis),
        "tool_count":len(capsules),
        "capsules":capsules,
        "object_store":store,
    }
    body["index_cid"]=cid(body)
    return body

def verify_tool_capsule_index(index):
    if index.get("tool_count")!=len(index.get("capsules",())):
        raise RuntimeError("TAKE6_TOOL_CAPSULE_COUNT_MISMATCH")
    store=index.get("object_store",{})
    for key,payload in store.items():
        if cid(payload)!=key:
            raise RuntimeError("TAKE6_TOOL_CAPSULE_OBJECT_HASH_MISMATCH:"+key)
    ids=[]
    for cap in index.get("capsules",()):
        ids.append(cap["tool_id"])
        for key in ("spec_cid","runtime_cid"):
            value=cap.get(key)
            if value and value not in store:
                raise RuntimeError("TAKE6_TOOL_CAPSULE_MISSING_OBJECT:"+str(value))
        for value in cap["dependency_cids"]:
            if value not in store:
                raise RuntimeError("TAKE6_TOOL_CAPSULE_MISSING_DEPENDENCY:"+value)
        if not cap["protected_behaviors"]:
            raise RuntimeError("TAKE6_TOOL_CAPSULE_PROTECTED_BEHAVIOR_EMPTY:"+cap["tool_id"])
        if cap["open_coordinates"]:
            raise RuntimeError("TAKE6_TOOL_CAPSULE_OPEN:"+cap["tool_id"]+":"+",".join(cap["open_coordinates"]))
    if len(ids)!=len(set(ids)):
        raise RuntimeError("TAKE6_TOOL_CAPSULE_DUPLICATE_TOOL_ID")
    expected=set(CONFIGURED_RUNS)
    if set(ids)!=expected:
        raise RuntimeError("TAKE6_TOOL_CAPSULE_REPERTOIRE_MISMATCH")
    expected_cid=index.get("index_cid")
    body={k:v for k,v in index.items() if k!="index_cid"}
    if cid(body)!=expected_cid:
        raise RuntimeError("TAKE6_TOOL_CAPSULE_INDEX_HASH_MISMATCH")
    return True

if __name__=="__main__":
    source=sys.argv[1] if len(sys.argv)>1 else "TAKE5_CURRENT_CAMPAIGN"
    out=compile_tool_capsules(source_basis=source)
    verify_tool_capsule_index(out)
    print(json.dumps(out,sort_keys=True,separators=(",",":")))
