import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"take6-bootstrap/migration"))
sys.path.insert(0,str(ROOT/"runtime"))
from build_tool_capsules import compile_tool_capsules,verify_tool_capsule_index,cid
from tool_run_registry import CONFIGURED_RUNS
from tool_manifest import manifest_for
from portable_tool_conductor import compilation_witness

def test_take6_tool_capsules_cover_current_repertoire_without_silent_open():
    out=compile_tool_capsules(source_basis="changed-state-campaign-current")
    assert verify_tool_capsule_index(out)
    assert out["tool_count"]==len(CONFIGURED_RUNS)
    assert {x["tool_id"] for x in out["capsules"]}==set(CONFIGURED_RUNS)
    assert all(not x["open_coordinates"] for x in out["capsules"])
    assert all(x["runtime_cid"] for x in out["capsules"])
    for cap in out["capsules"]:
        manifest=manifest_for(cap["tool_id"])
        spec=CONFIGURED_RUNS[cap["tool_id"]]
        witness=compilation_witness(cap["tool_id"])
        expected=set(manifest.behavior_ids())|set(spec.protected_behaviors)
        assert set(cap["protected_behaviors"])==expected
        assert cap["environment_contract"]["required_environment"]==list(witness.required_environment)
        assert cap["spec_cid"] in out["object_store"]
        assert cap["runtime_cid"] in out["object_store"]

def test_take6_tool_capsule_compilation_is_deterministic():
    a=compile_tool_capsules(source_basis="same")
    b=compile_tool_capsules(source_basis="same")
    assert a==b
    assert a["index_cid"]==b["index_cid"]

def test_take6_capsule_hash_tamper_fails():
    out=compile_tool_capsules(source_basis="same")
    key=next(iter(out["object_store"]))
    out["object_store"][key]={"tampered":True}
    try:
        verify_tool_capsule_index(out)
    except RuntimeError as exc:
        assert "HASH_MISMATCH" in str(exc)
    else:
        raise AssertionError("tampered capsule object passed")
