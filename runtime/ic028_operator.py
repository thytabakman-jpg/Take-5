"""IC-028 operator wrapper.

Curiosity-first inquiry and the complete execution path run under one controller
lease.  A bound entry contract is mandatory before substantive work.  The entry
mode controls legal stage ordering, so OBSERVE_DECOUPLED performs frozen
observation and observation reconciliation before goal-directed stages.
"""
from dataclasses import dataclass
from typing import Any, Callable
from controller_lease import ControllerLease, may_select_actions
from entry_contract import MODE_OBSERVE_DECOUPLED
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

GOAL_DIRECTED_STAGES=(
    "RECOVER_GOAL","CURIOSITY_PD","FORMALIZE","PLAN_ORDER","OBSERVE",
    "OBJECTIFY","GENERATE_WORK","SELECT","BIND","EXECUTE","ADMIT",
    "RECONCILE","PROPAGATE_AFFECTED_CONE","PERSIST","VERIFY","COMPLETE"
)

OBSERVER_FIRST_STAGES=(
    "OBSERVE","OBSERVE_RECONCILE","OBSERVE_TRC",
    "RECOVER_GOAL","CURIOSITY_PD","FORMALIZE","PLAN_ORDER",
    "OBJECTIFY","GENERATE_WORK","SELECT","BIND","EXECUTE","ADMIT",
    "RECONCILE","PROPAGATE_AFFECTED_CONE","PERSIST","VERIFY","COMPLETE"
)

def stages_for(entry_contract):
    if entry_contract.initial_mode==MODE_OBSERVE_DECOUPLED:
        return OBSERVER_FIRST_STAGES
    return GOAL_DIRECTED_STAGES

def run_ic028(lease:ControllerLease,state:Any,handlers:dict[str,Callable], *,
              entry_contract=None,jane_update:Callable|None=None,
              controller_decide:Callable|None=None,max_rounds:int=8):
    if entry_contract is None:
        return OperatorResult(state,[],False,"ENTRY_CONTRACT_REQUIRED")
    if lease.controller!=entry_contract.controller:
        return OperatorResult(state,[],False,"ENTRY_CONTROLLER_MISMATCH")
    if not getattr(entry_contract,"receipt",None):
        return OperatorResult(state,[],False,"ENTRY_CONTRACT_UNBOUND")
    if not may_select_actions(lease,"IC-028"):
        return OperatorResult(state,[],False,"LEASE_DENIED")

    stage_plan=stages_for(entry_contract)
    current=state
    if isinstance(current,dict):
        current={**current,"controller_mode":entry_contract.mode_profile.mode_id,"mode_profile":entry_contract.mode_profile}
    receipts=[OperatorReceipt("ENTRY_CONTRACT","BOUND",entry_contract)]
    for _ in range(max_rounds):
        material=False
        supervisory=False
        last_delta=None
        for stage in stage_plan:
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
                delta=out.get("delta")
                if delta is not None:
                    last_delta=delta
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
        if controller_decide is not None:
            decision=controller_decide(current,tuple(receipts))
            receipts.append(OperatorReceipt("CONTROLLER_DECISION","EXECUTED",decision))
            if isinstance(decision,dict) and decision.get("answer_sufficient"):
                return OperatorResult(current,receipts,True,None)
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
