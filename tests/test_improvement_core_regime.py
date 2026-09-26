import sys
sys.path.insert(0,"runtime")

from improvement_core_learning_memory import LearningMemory
from improvement_core_recursive_manager import RecursiveImprovementCoreManager,ChildReturn
from improvement_core_regime import CURRENT_REGIME,run_improvement_core_regime
from ic028_operator import GOAL_DIRECTED_STAGES

def _stage_handlers(live=False):
    handlers={}
    for stage in GOAL_DIRECTED_STAGES:
        def fn(state,stage=stage):
            if stage=="COMPLETE" and live:
                return {
                    "state":{
                        **state,
                        "live_continuation":True,
                        "terminal":"CONTINUE",
                        "step":0,
                        "basis_id":"b0",
                    },
                    "terminal":True,
                }
            return {
                "state":{**state,stage:True},
                "material_delta":stage=="EXECUTE",
                "supervisory_relevant":False,
            }
        handlers[stage]=fn
    handlers["REENTER"]=lambda state: {"state":state,"terminal":True}
    return handlers

def _recursive_handlers():
    def select(z,m):
        if z.get("step",0)==0:
            return {
                "id":"j1",
                "route_id":"route-j1",
                "task":"verify",
                "basis_id":z.get("basis_id","b0"),
                "dependency_footprint":["evidence"],
            }
        return None
    def child(job):
        return ChildReturn(
            child_id=job.id,
            job_id=job.job["id"],
            execution_truth="FULL_MATCH",
            result={"task":job.job["task"]},
            basis_id=job.basis_id,
        )
    def admit(ret,z,m):
        return "ADMIT",{"material_result_delta":True,"finding":"verified"}
    def update(z,m,a,d):
        z=dict(z);m=dict(m)
        z["step"]=z.get("step",0)+1
        z["live_continuation"]=False
        z["terminal"]="COMPLETE"
        return z,m
    return {
        "select_child_job":select,
        "run_child":child,
        "admit_child":admit,
        "update_parent":update,
    }

def test_learning_memory_blocks_unchanged_no_gain_and_reopens_on_dependency_delta():
    m=LearningMemory()
    m.record("broad_sweep","basis0","NO_GAIN",{"representation","evidence"},{"why":"same residual"})
    assert m.unchanged_rerun_blocked("broad_sweep","basis0",set())
    assert m.unchanged_rerun_blocked("broad_sweep","basis0",{"authority"})
    assert not m.unchanged_rerun_blocked("broad_sweep","basis0",{"representation"})

def test_recursive_manager_keeps_parent_control_across_children():
    def select(z,m):
        if z["step"]==0:return {"id":"j1","task":"diagnose","basis_id":"b0"}
        if z["step"]==1:return {"id":"j2","task":"verify","basis_id":"b1"}
        return None
    def child(job):
        return ChildReturn(
            child_id=job.id,
            job_id=job.job["id"],
            execution_truth="FULL_MATCH",
            result={"task":job.job["task"]},
            basis_id=job.basis_id,
        )
    def admit(ret,z,m):
        return "ADMIT",{"material_result_delta":True,"finding":ret.result["task"]}
    def update(z,m,a,d):
        z=dict(z);m=dict(m);z["step"]+=1;m[f"d{z['step']}"]=d
        if z["step"]>=2:
            z["terminal"]="COMPLETE";z["live_continuation"]=False
        else:
            z["basis_id"]="b1";z["live_continuation"]=True
        return z,m

    mgr=RecursiveImprovementCoreManager(select,child,admit,update)
    out=mgr.run({"step":0,"terminal":"CONTINUE","live_continuation":True,"basis_id":"b0"},{})
    assert out["status"]=="COMPLETE"
    assert [x["selected_job"]["id"] for x in out["traces"]]==["j1","j2"]

def test_recursive_manager_fails_if_host_stops_while_continuation_is_live():
    def child(job):
        raise AssertionError("child should not run")
    mgr=RecursiveImprovementCoreManager(
        lambda z,m:None,
        child,
        lambda *args:("OPEN",{}),
        lambda z,m,a,d:(z,m),
    )
    try:
        mgr.run({"terminal":"CONTINUE","live_continuation":True},{})
    except RuntimeError as exc:
        assert "LIVENESS_FAILURE" in str(exc)
    else:
        raise AssertionError("expected liveness failure")

def test_regime_activates_recursive_manager_when_stage_result_has_live_continuation():
    out=run_improvement_core_regime(
        "ImproveCore, solve this",
        target="problem",
        job="solve",
        basis="current",
        state={},
        handlers=_stage_handlers(live=True),
        recursive_handlers=_recursive_handlers(),
    )
    assert out.status=="COMPLETE"
    assert out.recursive_result is not None
    assert out.recursive_result["status"]=="COMPLETE"
    assert out.recursive_result["traces"][0]["selected_job"]["id"]=="j1"
    assert any(x["route_id"]=="route-j1" and x["disposition"]=="GAIN" for x in out.learning_summary)

def test_regime_fails_open_when_live_continuation_has_no_recursive_bindings():
    out=run_improvement_core_regime(
        "ImproveCore, solve this",
        target="problem",
        job="solve",
        basis="current",
        state={},
        handlers=_stage_handlers(live=True),
    )
    assert out.status=="OPEN"
    assert out.blocker=="RECURSIVE_MANAGER_HANDLERS_REQUIRED"

def test_regime_learning_memory_blocks_unchanged_no_gain_route():
    memory=LearningMemory()
    memory.record("route-j1","b0","NO_GAIN",{"evidence"},{"prior":"no gain"})
    out=run_improvement_core_regime(
        "ImproveCore, solve this",
        target="problem",
        job="solve",
        basis="current",
        state={},
        handlers=_stage_handlers(live=True),
        recursive_handlers=_recursive_handlers(),
        learning_memory=memory,
    )
    assert out.status=="OPEN"
    assert out.recursive_result is not None
    assert out.recursive_result["blocker"]=="IC_MANAGER_LEARNING_BLOCKED_UNCHANGED_ROUTE"

def test_current_regime_is_versioned_and_exposes_active_components():
    assert CURRENT_REGIME.controller=="IC-028"
    assert CURRENT_REGIME.version=="085"
    assert "improvement_core_manager" in CURRENT_REGIME.stage_manager
    assert "recursive_manager" in CURRENT_REGIME.recursive_manager
    assert "learning_memory" in CURRENT_REGIME.learning_memory


def test_recursive_manager_preserves_plural_nondominated_frontier():
    def select(z,m):
        return [
            {"id":"a","basis_id":"b0","goal_gain":3,"information_gain":1,"cost":2},
            {"id":"b","basis_id":"b0","goal_gain":1,"information_gain":4,"cost":1},
        ]
    def child(job):
        raise AssertionError("plural frontier must not be arbitrarily collapsed")
    mgr=RecursiveImprovementCoreManager(
        select,
        child,
        lambda *args:("OPEN",{}),
        lambda z,m,a,d:(z,m),
    )
    out=mgr.run({"terminal":"CONTINUE","live_continuation":True,"basis_id":"b0"},{})
    assert out["status"]=="OPEN"
    assert out["blocker"]=="IC_MANAGER_PLURAL_NONDOMINATED_CHILD_FRONTIER"
    assert set(out["frontier"]["nondominated"])=={"a","b"}


def test_recursive_manager_filters_protected_regression_before_choice():
    def select(z,m):
        return [
            {"id":"unsafe","basis_id":"b0","goal_gain":999,"preserves_protected":False},
            {"id":"safe","basis_id":"b0","goal_gain":1},
        ]
    def child(job):
        return ChildReturn(
            child_id=job.id,
            job_id=job.job["id"],
            execution_truth="FULL_MATCH",
            result={"ok":True},
            basis_id=job.basis_id,
        )
    def admit(ret,z,m):
        return "ADMIT",{"material_result_delta":True}
    def update(z,m,a,d):
        z=dict(z);z["terminal"]="COMPLETE";z["live_continuation"]=False
        return z,m
    mgr=RecursiveImprovementCoreManager(select,child,admit,update)
    out=mgr.run({"terminal":"CONTINUE","live_continuation":True,"basis_id":"b0"},{})
    assert out["status"]=="COMPLETE"
    assert out["traces"][0]["selected_job"]["id"]=="safe"
