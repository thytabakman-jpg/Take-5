from endogenous_work import WorkItem,WorkStatus
from system_loop import run_system

BASE={"identity":"x","type":"system","scope":"local","job":"repair","readings":[],"result_sensitive":[],"selectors":[],"authority":["observe"],"local_authority":["observe"],"provenance":[],"open":[]}

def focus(_): return {"exact_discriminant":True,"independent_local":True}

def test_system_not_ic_owns_regeneration_and_closure():
    s=dict(BASE); s["obligations"]=[WorkItem("w1","CHECK")]
    def worker(x):
        y=dict(x); y["obligations"]=[]; y["fixed"]=True; return y
    r=run_system(s,"repair",None,{"C02":["CHECK"]},{"C02":worker},focus)
    assert r.status==WorkStatus.CLOSED
    assert r.state["fixed"] is True
    assert "w1" in r.discharged

def test_unreachable_work_cannot_be_called_closed():
    s=dict(BASE); s["obligations"]=[WorkItem("w1","CHECK",reachable=False)]
    r=run_system(s,"repair",None,{}, {},focus)
    assert r.status==WorkStatus.BLOCKED

def test_missing_capability_preserves_open():
    s=dict(BASE); s["obligations"]=[WorkItem("w1","UNKNOWN")]
    r=run_system(s,"repair",None,{}, {},focus)
    assert r.status==WorkStatus.PAUSED_OPEN
    assert "w1" in r.open_coordinates
