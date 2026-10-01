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
    assert out["post_mutation_clean_pass"] is True
    assert [r["disposition"] for r in out["trace"]]==[
        "REAPPLY_CLEAN_VERIFY","RELATIVE_CLOSE"
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
    assert out["open"]==["FIXED_POINT_NOT_REACHED_WITHIN_MAX_ROUNDS"]


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
