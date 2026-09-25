import sys
sys.path.insert(0,"runtime")
from inquiry_compiler import compile_question
from controller_lease import ControllerLease
from ic028_operator import run_ic028

def test_inquiry_pd_precedes_math():
    calls=[]
    def pd(q): calls.append("PD"); return q+"?"
    def math(q): calls.append("MATH"); return __import__("inquiry_compiler").FormalQuestion(q,"x",("a",))
    q,probes=compile_question("curious",pd,math)
    assert calls==["PD","MATH"]
    assert len(probes)==36

def test_operator_runs_and_reenters():
    lease=ControllerLease("e","IC-028","j","b")
    stages=("RECOVER_GOAL","CURIOSITY_PD","FORMALIZE","PLAN_ORDER","EXECUTE","ADMIT","RECONCILE","PERSIST","VERIFY")
    def mk(stage):
        return lambda s: {"state":{**s,stage:True},"material_delta":stage=="EXECUTE","supervisory_relevant":stage=="EXECUTE","delta":"d"}
    handlers={s:mk(s) for s in stages}
    handlers["REENTER"]=lambda s: {"state":s,"terminal":True}
    seen=[]
    out=run_ic028(lease,{},handlers,jane_update=lambda d:seen.append(d))
    assert out.terminal
    assert seen==["d"]
    assert any(r.stage=="JANE_SYNC" for r in out.receipts)
