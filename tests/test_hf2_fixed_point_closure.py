import sys
sys.path.insert(0,"runtime")

from configured_hf2_execution import execute_configured_with_hf2
from global_tool_execution import build_tool_execution_plan
from hf002_recursive_continuation import HF002RecursiveContinuation
from tool_run_registry import CONFIGURED_RUNS


def _engine(run_capability, *, max_rounds=8):
    holder={"raw":{}}

    def wrapped(state,memory):
        raw=run_capability(state,memory)
        holder["raw"]=raw
        return raw

    def normalize(raw,current,memory):
        return raw.get("state",current), {
            "material_result_delta":bool(raw.get("material_delta",False)),
            "affected_frontier":raw.get("hf2_affected_frontier"),
            "scope_deltas":raw.get("hf2_scope_deltas"),
            "route_equivalence":"test-route",
        }

    def trc(before,after,delta):
        return {"terminal":True}

    def hf1(before,after,delta):
        return {"disposition":"STABLE"}

    def live(state,memory):
        return bool(holder["raw"].get("hf2_live_local",False))

    def close(state,memory):
        return bool(holder["raw"].get("hf2_local_close",True))

    return HF002RecursiveContinuation(
        run_capability=wrapped,
        admit_normalize=normalize,
        trc_verify=trc,
        hf1_classify=hf1,
        live_local=live,
        local_close=close,
        max_rounds=max_rounds,
    )


def test_material_round_forces_internal_clean_verification_pass():
    calls=[]

    def run(state,memory):
        n=len(calls)+1
        calls.append(n)
        return {
            "execution_truth":"SEMANTICALLY_APPLIED",
            "state":{"version":1},
            "material_delta":n==1,
            "hf2_live_local":False,
            "hf2_local_close":True,
        }

    out=_engine(run).run({"version":0},{})
    assert out["status"]=="RELATIVE_CLOSE"
    assert calls==[1,2]
    assert [r["disposition"] for r in out["trace"]]==[
        "REAPPLY_C","RELATIVE_CLOSE"
    ]


def test_repeated_material_delta_never_false_closes():
    calls=[]

    def run(state,memory):
        calls.append(True)
        return {
            "execution_truth":"SEMANTICALLY_APPLIED",
            "state":{"version":len(calls)},
            "material_delta":True,
            "hf2_live_local":False,
            "hf2_local_close":True,
        }

    out=_engine(run,max_rounds=3).run({"version":0},{})
    assert out["status"]=="RESOURCE_STOP"
    assert len(calls)==3
    assert [r["disposition"] for r in out["trace"]]==["REAPPLY_C"]*3
    assert all(r["disposition"]!="RELATIVE_CLOSE" for r in out["trace"])


def test_affected_frontier_blocks_close_even_on_clean_round():
    def run(state,memory):
        return {
            "execution_truth":"SEMANTICALLY_APPLIED",
            "material_delta":False,
            "hf2_live_local":False,
            "hf2_local_close":True,
            "hf2_affected_frontier":("section",),
        }

    out=_engine(run).run({}, {})
    assert out["status"]=="OPEN"
    assert out["open"]==["AFFECTED_FRONTIER_NOT_CLOSED"]


def test_scope_delta_blocks_close_even_when_local_adapter_says_closed():
    def run(state,memory):
        return {
            "execution_truth":"SEMANTICALLY_APPLIED",
            "material_delta":False,
            "hf2_live_local":False,
            "hf2_local_close":True,
            "hf2_scope_deltas":{"paragraph":False,"section":True},
        }

    out=_engine(run).run({}, {})
    assert out["status"]=="OPEN"
    assert out["open"]==["AFFECTED_FRONTIER_NOT_CLOSED"]


def test_configured_wrapper_propagates_affected_scope_contract():
    plan=build_tool_execution_plan(CONFIGURED_RUNS["MT"])

    def adapter(state,plan):
        return {
            "status":"EXECUTED",
            "execution_truth":"SEMANTICALLY_APPLIED",
            "material_delta":False,
            "hf2_live_local":False,
            "hf2_local_close":True,
            "hf2_scope_deltas":{"claim":False,"paragraph":True},
        }

    out=execute_configured_with_hf2(
        tool_id="MT",plan=plan,state={},adapter=adapter,max_rounds=4
    )
    assert out.status=="OPEN"
    assert out.call_count==1


def test_reusing_hf2_engine_does_not_reuse_previous_episode_receipts():
    def run(state,memory):
        return {"execution_truth":"SEMANTICALLY_APPLIED","state":state,
                "material_delta":False}
    engine=_engine(run)
    first=engine.run({"version":1},{})
    second=engine.run({"version":2},{})
    assert len(first["trace"])==len(second["trace"])==1
    assert second["trace"][0]["state_before"]=={"version":2}


def test_non_success_attempt_is_recorded_in_trace():
    for status in ("OPEN","BLOCKED","CONFLICT"):
        out = _engine(lambda *_:{"execution_truth":status}).run({}, {})
        assert out["status"] == status
        assert len(out["trace"]) == 1
        assert out["trace"][0]["disposition"] == status


def test_nonterminal_trc_attempt_is_recorded_without_admitting_state():
    engine = _engine(lambda *_:{"execution_truth":"IMPLEMENTATION_EXECUTED","state":{"new":True}})
    engine.trc_verify = lambda *_:{"terminal":False}
    out = engine.run({}, {})
    assert out["status"] == "OPEN" and out["state"] == {}
    assert out["trace"][0]["disposition"] == "OPEN"


def test_hf2_round_receipts_freeze_nested_state_at_each_round():
    calls=[]
    def run(state,memory):
        calls.append(True)
        if len(calls)==1:
            state["nested"]["version"]=1
        else:
            state["nested"]["version"]=2
        return {"execution_truth":"SEMANTICALLY_APPLIED","state":state,
                "material_delta":len(calls)==1}
    out=_engine(run).run({"nested":{"version":0}}, {})
    assert out["status"]=="RELATIVE_CLOSE"
    assert out["trace"][0]["state_before"]["nested"]["version"]==0
    assert out["trace"][0]["state_after"]["nested"]["version"]==1
    assert out["trace"][1]["state_before"]["nested"]["version"]==1
    assert out["trace"][1]["state_after"]["nested"]["version"]==2


def test_hf2_rejects_unverified_nested_mutations_and_textual_terminal():
    initial={"nested":{"version":0}}
    def run(state,memory):
        state["nested"]["version"]=1
        return {"execution_truth":"IMPLEMENTATION_EXECUTED","state":state}
    engine=_engine(run)
    engine.trc_verify=lambda *_:{"terminal":"false"}
    out=engine.run(initial,{})
    assert out["status"]=="OPEN"
    assert out["state"]=={"nested":{"version":0}}
    assert initial=={"nested":{"version":0}}
    assert out["trace"][0]["state_after"]==out["state"]


def test_hf2_non_success_does_not_admit_in_place_mutation():
    initial={"nested":{"version":0}}
    def run(state,memory):
        state["nested"]["version"]=1
        return {"execution_truth":"BLOCKED"}
    out=_engine(run).run(initial,{})
    assert out["status"]=="BLOCKED"
    assert out["state"]==initial=={"nested":{"version":0}}



def test_shared_material_vocabulary_across_compiler_wrapper_and_engine():
    from configured_hf2_execution import _delta_from_raw
    from hf002_recursive_continuation import MATERIAL_DELTA_KEYS, material_delta_present
    from recursive_compiler import hf2_fixed_point_witness
    for key in MATERIAL_DELTA_KEYS:
        delta=_delta_from_raw("MT",{"hf2_delta":{key:True},"material_delta":False})
        assert material_delta_present(delta)
        assert HF002RecursiveContinuation._material(delta)
        assert not hf2_fixed_point_witness([{"disposition":"RELATIVE_CLOSE","delta":delta}])
        assert "material_result_delta" not in delta or key=="material_result_delta"


def test_status_only_configured_success_cannot_close():
    from configured_hf2_execution import SUCCESS_STATUSES
    plan=build_tool_execution_plan(CONFIGURED_RUNS["MT"])
    for status in SUCCESS_STATUSES:
        out=execute_configured_with_hf2(tool_id="MT",plan=plan,state={},
            adapter=lambda *_:{"status":status,"hf2_local_close":True})
        assert out.status=="OPEN"
        assert "WITHOUT_EXECUTION_WITNESS" in out.last_raw["blocker"]


def test_unknown_hf1_disposition_blocks_without_admitting_successor():
    plan=build_tool_execution_plan(CONFIGURED_RUNS["MT"])
    for invalid in ("UNKNOWN",None,False,""):
        out=execute_configured_with_hf2(tool_id="MT",plan=plan,state={"n":0},
            adapter=lambda *_:{"status":"EXECUTED","state":{"n":1},
                              "hf1_disposition":invalid})
        assert out.status=="BLOCKED"
        assert out.state=={"n":0}
        assert out.trace[-1]["disposition"]=="BLOCKED"


def test_in_place_successor_is_verified_against_frozen_predecessor():
    observed=[]
    def run(state,memory):
        state["nested"]["version"]=1
        return {"execution_truth":"SEMANTICALLY_APPLIED","state":state}
    def trc(before,after,delta):
        observed.append(("trc",before["nested"]["version"],after["nested"]["version"]))
        before["nested"]["version"]=99
        return {"terminal":True}
    def hf1(before,after,delta):
        observed.append(("hf1",before["nested"]["version"],after["nested"]["version"]))
        return {"disposition":"STABLE"}
    engine=_engine(run)
    engine.trc_verify=trc
    engine.hf1_classify=hf1
    initial={"nested":{"version":0}}
    out=engine.run(initial,{})
    assert observed==[("trc",0,1),("hf1",0,1)]
    assert initial==out["trace"][0]["state_before"]=={"nested":{"version":0}}



def test_compiler_rejects_incomplete_or_contradictory_native_fixed_point():
    from copy import deepcopy
    from recursive_compiler import hf2_fixed_point_witness
    out=_engine(lambda state,memory:{"execution_truth":"IMPLEMENTATION_EXECUTED","state":state}).run({}, {})
    trace=out["trace"]
    assert hf2_fixed_point_witness(trace)
    assert not hf2_fixed_point_witness([{"disposition":"RELATIVE_CLOSE","delta":{}}])
    for key,value in (("trc",{"terminal":False}),("live_local",True),("local_close",False),
                      ("delta",{"affected_frontier":["section"]}),("delta",{"scope_deltas":{"p":True}})):
        altered=deepcopy(trace)
        altered[-1][key]=value
        assert not hf2_fixed_point_witness(altered)


def test_self_recurrence_cannot_close_with_unresolved_frontier():
    plan=build_tool_execution_plan(CONFIGURED_RUNS["HF002"])
    for hints in ({"hf2_live_local":True},{"hf2_local_close":False},
                  {"hf2_affected_frontier":["section"]},{"hf2_scope_deltas":{"p":True}},
                  {"trc_terminal":False}):
        out=execute_configured_with_hf2(tool_id="HF002",plan=plan,state={},
            adapter=lambda *_:{"status":"EXECUTED","result":True,**hints})
        assert out.status=="OPEN" and out.call_count==1
    for status in ("OPEN","BLOCKED","CONFLICT","RETURN_REENTER","RESOURCE_STOP"):
        out=execute_configured_with_hf2(tool_id="HF002",plan=plan,state={},
            adapter=lambda *_:{"status":"EXECUTED","result":{"status":status}})
        assert out.status==status and out.call_count==1
    out=execute_configured_with_hf2(tool_id="HF002",plan=plan,state={},
        adapter=lambda *_:{"status":"EXECUTED","result":{"status":"RELATIVE_CLOSE","trace":[]}})
    assert out.status=="OPEN"
    clean=execute_configured_with_hf2(tool_id="HF002",plan=plan,state={},
        adapter=lambda *_:{"status":"EXECUTED","result":True,"hf2_live_local":False})
    assert clean.status=="SELF_CLOSE" and clean.call_count==1


def test_affected_scope_cannot_disappear_between_rounds_without_clearance():
    plan=build_tool_execution_plan(CONFIGURED_RUNS["MT"])
    for second,expected in (({},"OPEN"),({"hf2_scope_deltas":{"other":False}},"OPEN"),
                            ({"hf2_scope_deltas":{"section":False}},"RELATIVE_CLOSE"),
                            ({"hf2_scope_deltas":{}},"RELATIVE_CLOSE")):
        calls=[]
        def adapter(*_):
            calls.append(1)
            return {"status":"EXECUTED","result":True,"material_delta":len(calls)==1,
                    **({"hf2_scope_deltas":{"section":True}} if len(calls)==1 else second)}
        out=execute_configured_with_hf2(tool_id="MT",plan=plan,state={},adapter=adapter)
        assert out.status==expected and out.call_count==2
        if expected=="OPEN":
            assert out.trace[-1]["delta"]["scope_deltas"]["section"] is True


def test_changed_native_receipts_force_clean_successor_pass():
    plan=build_tool_execution_plan(CONFIGURED_RUNS["MT"])
    for key in ("native_receipts","cell_receipts","question_receipts","cognitive_receipts"):
        calls=[]
        def adapter(*_):
            calls.append(1)
            return {"status":"EXECUTED","result":True,"material_delta":len(calls)==1,
                    key:["first" if len(calls)==1 else "new"]}
        out=execute_configured_with_hf2(tool_id="MT",plan=plan,state={},adapter=adapter)
        assert out.status=="RELATIVE_CLOSE" and out.call_count==3
        assert [r["disposition"] for r in out.trace]==["REAPPLY_C","REAPPLY_C","RELATIVE_CLOSE"]

def test_configured_and_self_routes_reject_nonboolean_control_flags():
    for tool in ("MT","HF002"):
        plan=build_tool_execution_plan(CONFIGURED_RUNS[tool])
        for key in ("material_delta","hf2_local_close","hf2_live_local","trc_terminal"):
            for flag in ("false",1,0,None):
                out=execute_configured_with_hf2(tool_id=tool,plan=plan,state={"v":0},
                    adapter=lambda *_:{"status":"EXECUTED","result":True,
                        "state":{"v":1},key:flag})
                assert out.status=="OPEN" and out.state=={"v":0}
                assert out.last_raw["blocker"]==f"CONFIGURED_HF2_INVALID_BOOLEAN:{key}"


def test_self_recurrence_does_not_mutate_or_admit_failed_successor():
    plan=build_tool_execution_plan(CONFIGURED_RUNS["HF002"])
    state={"nested":{"v":0}}
    def adapter(current,_):
        current["nested"]["v"]=1
        return {"status":"BLOCKED","state":current,"material_delta":True}
    out=execute_configured_with_hf2(tool_id="HF002",plan=plan,state=state,adapter=adapter)
    assert out.state==state=={"nested":{"v":0}}
    assert not out.admitted_material_delta


def test_native_hf2_needs_explicit_boolean_closure_and_live_frontier():
    for flag in ("false",1,0,None):
        engine=_engine(lambda state,memory:{"execution_truth":"IMPLEMENTATION_EXECUTED","state":state})
        engine.local_close=lambda *_:flag
        assert engine.run({}, {})["status"]=="OPEN"
        engine.local_close=lambda *_:True
        engine.live_local=lambda *_:flag
        assert engine.run({}, {})["status"]=="OPEN"


def test_malformed_control_evidence_does_not_downgrade_blocked_or_conflicting_status():
    from configured_hf2_execution import _raw_mapping
    for status in ("BLOCKED","CONFLICT"):
        out=_raw_mapping({"status":status,"result":True,"hf2_local_close":"false"})
        assert out["status"]==out["execution_truth"]==status
