import sys
sys.path.insert(0,"runtime")

from improvement_core import improve
from math_first_selector import select_min_cost_package

BASE={
    "identity":"x",
    "type":"system",
    "scope":"local",
    "job":"improve",
    "readings":[],
    "result_sensitive":[],
    "selectors":[],
    "authority":[],
    "local_authority":[],
    "provenance":[],
    "open":[],
}


def focus(_):
    return {"exact_discriminant":True,"independent_local":True}


def test_improvement_core_accepts_math_first_selector_without_outer_loop_rebuild():
    packet=dict(BASE)
    packet["obligations"]=["A","B"]
    packet["tool_contracts"]={
        "T1":{"cost":5.0},
        "T2":{"cost":1.0},
        "T3":{"cost":1.0},
    }

    def t1(state):
        out=dict(state)
        out["used"]=tuple(out.get("used",()))+("T1",)
        out["obligations"]=[]
        return out

    def t2(state):
        out=dict(state)
        out["used"]=tuple(out.get("used",()))+("T2",)
        out["obligations"]=[x for x in out["obligations"] if x!="A"]
        return out

    def t3(state):
        out=dict(state)
        out["used"]=tuple(out.get("used",()))+("T3",)
        out["obligations"]=[x for x in out["obligations"] if x!="B"]
        return out

    result=improve(
        packet,
        {"T1":["A","B"],"T2":["A"],"T3":["B"]},
        {"T1":t1,"T2":t2,"T3":t3},
        focus,
        package_selector=select_min_cost_package,
    )
    assert result.status=="CLOSED_RELATIVE"
    assert result.package==()
    assert result.final_packet["used"]==("T2","T3")
    assert all(pid!="T1" for pid,_ in result.results)
