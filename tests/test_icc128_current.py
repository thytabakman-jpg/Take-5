from icc128_autonomous_controller import ICC128Controller
from rho128_policy import Package, choose, needs_reselection
from tool_run_registry import CONFIGURED_RUNS

def test_icc128_is_current_registered_tool():
    s=CONFIGURED_RUNS["ICC128"]
    assert s.complete()
    assert s.geometry=="D36_C"
    assert s.wrapper_required
    assert s.recurrence_engine=="HF002"

def test_icc128_endogenous_loop_reenters_until_complete():
    def gq(z,m):
        return [] if z["step"]>=2 else [{"id":f"q{z['step']}"}]
    def gw(q,z,m):
        return [{"id":"w:"+x["id"]} for x in q]
    def select(q,w,z,m):
        return w[:1]
    def execute(sel,z,m):
        return [{"id":x["id"],"finding":"x"} for x in sel]
    def admit(results,z,m):
        return {"material_result_delta":bool(results),"results":results}
    def update(z,m,d):
        z=dict(z); m=dict(m)
        z["step"]+=1
        if z["step"]>=2:
            z["terminal"]="COMPLETE"; z["admitted_continuation"]=False
        else:
            z["terminal"]="CONTINUE"; z["admitted_continuation"]=True
        m[f"step{z['step']}"]=d
        return z,m

    out=ICC128Controller(gq,gw,select,execute,admit,update).run(
        {"step":0,"terminal":"CONTINUE","admitted_continuation":True},{}
    )
    assert out["status"]=="COMPLETE"
    assert len(out["traces"])==2

def test_state_relative_selector_prefers_minimum_burden_when_cheap():
    state={
        "task_and_job_well_typed":True,
        "one_validated_capability_clearly_fits":True,
        "consequence_bounded":True,
        "no_material_rival_exposed":True,
    }
    ps=[
        Package("heavy",frozenset({"recover"}),burden=5,info_gain=1),
        Package("light",frozenset({"recover"}),burden=1,info_gain=1),
    ]
    out=choose(state,ps,{"recover"})
    assert out["mode"]=="CHEAP_DIRECT"
    assert out["selected"]==["light"]

def test_material_failure_forces_reselection():
    assert needs_reselection({"failed_route":True})
