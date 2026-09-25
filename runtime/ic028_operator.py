"""IC-028 operator wrapper.

Curiosity-first inquiry and the complete execution path run under one controller
lease. Concrete project/tool functions are injected as handlers.
"""
from dataclasses import dataclass
from typing import Any, Callable
from controller_lease import ControllerLease, may_select_actions
from jane_sync import jane_sync

@dataclass
class OperatorReceipt:
    stage:str
    status:str
    value:Any=None

@dataclass
class OperatorResult:
    state:Any
    receipts:list
    terminal:bool
    blocker:str|None=None

STAGES=("RECOVER_GOAL","CURIOSITY_PD","FORMALIZE","PLAN_ORDER","OBSERVE",
        "OBJECTIFY","GENERATE_WORK","SELECT","BIND","EXECUTE","ADMIT",
        "RECONCILE","PROPAGATE_AFFECTED_CONE","PERSIST","VERIFY","COMPLETE")

def run_ic028(lease:ControllerLease,state:Any,handlers:dict[str,Callable], *,
              jane_update:Callable|None=None,max_rounds:int=8):
    if not may_select_actions(lease,"IC-028"):
        return OperatorResult(state,[],False,"LEASE_DENIED")
    current=state
    receipts=[]
    for _ in range(max_rounds):
        material=False
        supervisory=False
        last_delta=None
        for stage in STAGES:
            fn=handlers.get(stage)
            if fn is None:
                return OperatorResult(current,receipts,False,f"UNBOUND:{stage}")
            out=fn(current)
            if isinstance(out,dict) and out.get("blocked"):
                receipts.append(OperatorReceipt(stage,"BLOCKED",out))
                return OperatorResult(current,receipts,False,f"BLOCKED:{stage}")
            if isinstance(out,dict):
                current=out.get("state",current)
                material=material or bool(out.get("material_delta"))
                supervisory=supervisory or bool(out.get("supervisory_relevant"))
                last_delta=out.get("delta",last_delta)
                if stage=="COMPLETE" and out.get("terminal"):
                    receipts.append(OperatorReceipt(stage,"EXECUTED",out))
                    return OperatorResult(current,receipts,True,None)
            elif out is not None:
                current=out
            receipts.append(OperatorReceipt(stage,"EXECUTED",out))
        if material and jane_update is not None:
            js=jane_sync(material=True,supervisory_relevant=supervisory,
                         update=jane_update,delta=last_delta)
            receipts.append(OperatorReceipt("JANE_SYNC","EXECUTED",js))
        reenter=handlers.get("REENTER")
        if reenter is None:
            return OperatorResult(current,receipts,False,"UNBOUND:REENTER")
        nxt=reenter(current)
        receipts.append(OperatorReceipt("REENTER","EXECUTED",nxt))
        if isinstance(nxt,dict):
            current=nxt.get("state",current)
            if nxt.get("terminal"):
                return OperatorResult(current,receipts,True,None)
            if not material and not nxt.get("continue",False):
                return OperatorResult(current,receipts,True,None)
        elif not material:
            return OperatorResult(current,receipts,True,None)
    return OperatorResult(current,receipts,False,"OPEN:MAX_ROUNDS")
