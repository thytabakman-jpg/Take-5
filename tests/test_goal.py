import sys
sys.path.insert(0,"runtime")
from goal import recover_goal

PACKET={"X":"system","S":{"state":"current"},"J0":"make it durable","K":"basis","E":["evidence"],"A":"observer","B":[]}

def recon(req):
    assert req["procedure_independence"] is True
    return {"GT":"goal-v1","Succ":"all actionable obligations closed","Inv":["execution_truth"],"Scope":"system","Auth":"observer","Reopen":["material currentness change"],"Open":[],"Witness":["evidence"]}

def test_goal_native_relative_close():
    out=recover_goal(PACKET,goal_reconstructor=recon)
    assert out.status=="RELATIVE_CLOSE"
    assert out.goal["GT"]=="goal-v1"

def test_goal_requires_semantic_binding():
    out=recover_goal(PACKET,goal_reconstructor=None)
    assert out.status=="OPEN"
    assert out.blocker=="GOAL_RECONSTRUCTOR_REQUIRED"

def test_goal_preserves_open():
    def r(req):
        x=recon(req); x["Open"]=["target scope ambiguity"]; return x
    out=recover_goal(PACKET,goal_reconstructor=r)
    assert out.status=="OPEN"
    assert out.goal["Open"]==["target scope ambiguity"]
