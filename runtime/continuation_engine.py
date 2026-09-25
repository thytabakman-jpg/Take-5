"""Configured continuation engine: one mandatory composition path over Take-5 controls.

This facade is intentionally small. It prevents availability of separate modules from
being mistaken for realization of the whole continuation program.
"""
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class StepReceipt:
    step:str
    status:str
    value:Any=None

@dataclass
class ContinuationReceipt:
    receipts:list
    terminal:bool=False
    blocker:str|None=None

STEPS=("OBSERVE","OBJECTIFY","GENERATE_WORK","SELECT","BIND","EXECUTE","ADMIT",
       "PROPAGATE_AFFECTED_CONE","PERSIST","VERIFY","REENTER")

def run_continuation(handlers:dict[str,Callable], state:Any, *, max_rounds:int=8):
    receipts=[]
    current=state
    for _ in range(max_rounds):
        material=False
        for step in STEPS:
            fn=handlers.get(step)
            if fn is None:
                return ContinuationReceipt(receipts,False,f"UNBOUND:{step}")
            out=fn(current)
            if isinstance(out,dict) and out.get("blocked"):
                receipts.append(StepReceipt(step,"BLOCKED",out))
                return ContinuationReceipt(receipts,False,f"BLOCKED:{step}")
            status="EXECUTED"
            if isinstance(out,dict):
                material=material or bool(out.get("material_delta",False))
                current=out.get("state",current)
                if out.get("terminal"):
                    receipts.append(StepReceipt(step,status,out))
                    return ContinuationReceipt(receipts,True,None)
            elif out is not None:
                current=out
            receipts.append(StepReceipt(step,status,out))
        if not material:
            return ContinuationReceipt(receipts,True,None)
    return ContinuationReceipt(receipts,False,"OPEN:MAX_ROUNDS")
