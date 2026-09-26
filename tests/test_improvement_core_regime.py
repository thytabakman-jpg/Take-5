import sys
sys.path.insert(0,"runtime")

from improvement_core_learning_memory import LearningMemory
from improvement_core_recursive_manager import RecursiveImprovementCoreManager,ChildReturn
from improvement_core_regime import CURRENT_REGIME

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

def test_current_regime_exposes_rich_manager_recursive_manager_and_memory():
    assert CURRENT_REGIME.controller=="IC-028"
    assert "improvement_core_manager" in CURRENT_REGIME.stage_manager
    assert "recursive_manager" in CURRENT_REGIME.recursive_manager
    assert "learning_memory" in CURRENT_REGIME.learning_memory
