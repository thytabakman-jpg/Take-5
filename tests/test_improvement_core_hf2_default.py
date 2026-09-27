import sys
sys.path.insert(0,"runtime")

from improvement_core_dispatch import dispatch_improvement_core
from improvement_core_regime import run_improvement_core_regime
from ic028_operator import GOAL_DIRECTED_STAGES


def _return_done(state,memory,context):
    status=str(context.get("candidate_status","OPEN"))
    return {
        "disposition":"RETURN",
        "terminal":status,
        "goal_closed":status=="COMPLETE",
        "owned_work_remaining":False,
        "consequence_closed":True,
        "blocker":context.get("candidate_blocker"),
        "evidence":["test:whole-job-post-hf2"],
    }


def _fresh_stable(state,memory,context):
    return {
        "status":"NO_GAIN",
        "owned_work_remaining":False,
        "evidence":[f"test:fresh:{context['challenge_index']}"],
        "challenge_id":f"test-fresh-{context['challenge_index']}",
    }



def _handlers(counter, *, reenter_upstream=False, material=True):
    handlers={}

    def passthrough(stage):
        def fn(state):
            return {
                "state":{**state,"last_stage":stage},
                "material_delta":False,
            }
        return fn

    for stage in GOAL_DIRECTED_STAGES:
        handlers[stage]=passthrough(stage)

    def execute(state):
        counter["execute"]+=1
        if state.get("repair_applied"):
            return {
                "state":state,
                "material_delta":material,
            }
        return {
            "state":{
                **state,
                "repair_applied":True,
                "semantic_value":1,
            },
            "material_delta":material,
            "delta":{"material_result_delta":material},
        }

    def admit(state):
        out={**state}
        if reenter_upstream:
            out["hf1_disposition"]="REENTER"
            out["hf1_targets"]=["UPSTREAM_BASIS"]
        return {"state":out,"material_delta":False}

    def complete(state):
        return {"state":state,"terminal":True,"material_delta":False}

    handlers["EXECUTE"]=execute
    handlers["ADMIT"]=admit
    handlers["COMPLETE"]=complete
    handlers["REENTER"]=lambda state: {"state":state,"terminal":True}
    return handlers


def test_bare_improvementcore_reapplies_under_hf2_until_second_pass_has_no_new_semantic_delta(tmp_path):
    calls={"execute":0}
    resolution,out=dispatch_improvement_core(
        "ImproveCore, solve this",
        target="problem",
        job="solve",
        basis="current",
        state={},
        handlers=_handlers(calls),
        return_verifier=_return_done,
        fresh_reobserve=_fresh_stable,
    )
    assert resolution.entrypoint.endswith("run_improvement_core_with_hf2")
    assert out.status=="COMPLETE"
    assert out.hf2_status=="RELATIVE_CLOSE"
    assert calls["execute"]==2
    assert [row["disposition"] for row in out.hf2_trace]==[
        "REAPPLY_C","RELATIVE_CLOSE"
    ]
    assert out.result.state["semantic_value"]==1


def test_hf2_requires_material_witness_not_state_change_alone():
    calls={"execute":0}
    _,out=dispatch_improvement_core(
        "ImproveCore, inspect this",
        target="problem",
        job="inspect",
        basis="current",
        state={},
        handlers=_handlers(calls,material=False),
        return_verifier=_return_done,
        fresh_reobserve=_fresh_stable,
    )
    assert out.status=="COMPLETE"
    assert out.hf2_status=="RELATIVE_CLOSE"
    assert calls["execute"]==1
    assert len(out.hf2_trace)==1


def test_hf1_upstream_reentry_escapes_local_hf2_and_returns_parent_open():
    calls={"execute":0}
    _,out=dispatch_improvement_core(
        "ImproveCore, solve this",
        target="problem",
        job="solve",
        basis="current",
        state={},
        handlers=_handlers(calls,reenter_upstream=True),
        return_verifier=_return_done,
        fresh_reobserve=_fresh_stable,
    )
    assert out.status=="OPEN"
    assert out.blocker=="HF002_RETURN_REENTER"
    assert out.hf2_status=="RETURN_REENTER"
    assert calls["execute"]==1


def test_debug_surface_can_disable_default_hf2():
    calls={"execute":0}
    _,out=dispatch_improvement_core(
        "ImproveCore, one pass only for debugging",
        target="problem",
        job="debug",
        basis="current",
        state={},
        handlers=_handlers(calls),
        hf2_enabled=False,
        allow_ungated_debug=True,
    )
    assert out.status=="COMPLETE"
    assert out.hf2_status=="DISABLED"
    assert out.hf2_trace==()
    assert calls["execute"]==1


def test_direct_regime_remains_one_pass_low_level_surface():
    calls={"execute":0}
    out=run_improvement_core_regime(
        "ImproveCore low-level",
        target="problem",
        job="debug",
        basis="current",
        state={},
        handlers=_handlers(calls),
    )
    assert out.status=="COMPLETE"
    assert out.hf2_status is None
    assert calls["execute"]==1



def test_parent_return_gate_reenters_full_improvementcore_after_meaningful_step():
    calls={"execute":0,"gate":0}

    def verify_return(state,memory,context):
        calls["gate"]+=1
        if calls["gate"]==1:
            return {
                "disposition":"CONTINUE",
                "owned_work_remaining":True,
                "consequence_closed":True,
                "goal_closed":False,
                "state_patch":{"parent_phase":1},
                "evidence":["test:first-step-not-parent-complete"],
                "reason":"another owned job remains",
            }
        return {
            "disposition":"RETURN",
            "terminal":"COMPLETE",
            "goal_closed":True,
            "owned_work_remaining":False,
            "consequence_closed":True,
            "evidence":["test:governing-job-closed"],
        }

    _,out=dispatch_improvement_core(
        "ImproveCore, finish the whole job",
        target="problem",
        job="finish all owned work",
        basis="current",
        state={},
        handlers=_handlers(calls),
        return_verifier=verify_return,
        fresh_reobserve=_fresh_stable,
        parent_max_rounds=4,
    )

    assert out.status=="COMPLETE"
    assert calls["gate"]==2
    assert calls["execute"]==3
    assert len(out.parent_return_trace)==2
    assert out.parent_return_trace[0]["disposition"]=="CONTINUE"
    assert out.parent_return_trace[0]["hf2_status"]=="RELATIVE_CLOSE"
    assert out.parent_return_trace[1]["disposition"]=="RETURN"
    assert out.parent_return_trace[1]["hf2_status"]=="RELATIVE_CLOSE"


def test_user_facing_improvementcore_without_parent_return_verifier_fails_open():
    calls={"execute":0}
    _,out=dispatch_improvement_core(
        "ImproveCore, solve this fully",
        target="problem",
        job="solve",
        basis="current",
        state={},
        handlers=_handlers(calls),
        fresh_reobserve=_fresh_stable,
    )
    assert out.status=="OPEN"
    assert out.blocker=="PARENT_RETURN_GATE_REQUIRED"
    assert len(out.parent_return_trace)==1


def test_user_facing_improvementcore_without_fresh_reobserver_fails_open_before_complete():
    calls={"execute":0}
    _,out=dispatch_improvement_core(
        "ImproveCore, solve this fully",
        target="problem",
        job="solve",
        basis="current",
        state={},
        handlers=_handlers(calls),
        return_verifier=_return_done,
    )
    assert out.status=="OPEN"
    assert out.blocker=="FRESH_WHOLE_JOB_REOBSERVATION_REQUIRED"
