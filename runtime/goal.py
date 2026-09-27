"""Recovered native GOAL semantic runtime.

GOAL recovers a versioned target/completion contract from a typed current-state
packet. Open-ended semantic reconstruction is an explicit host binding; missing
or malformed bindings fail closed rather than falling back to generic analysis.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Callable,Mapping

INPUT_KEYS=("X","S","J0","K","E","A","B")
OUTPUT_KEYS=("GT","Succ","Inv","Scope","Auth","Reopen","Open","Witness")

@dataclass(frozen=True)
class GoalResult:
    status:str
    goal:dict[str,Any]|None
    blocker:str|None=None

def recover_goal(packet:Mapping[str,Any],*,goal_reconstructor:Callable|None)->GoalResult:
    missing=tuple(k for k in INPUT_KEYS if k not in packet)
    if missing:
        return GoalResult("OPEN",None,"GOAL_INPUT_MISSING:"+",".join(missing))
    if not callable(goal_reconstructor):
        return GoalResult("OPEN",None,"GOAL_RECONSTRUCTOR_REQUIRED")

    request={
        "job":"recover_target_and_completion_contract",
        "input":{k:packet[k] for k in INPUT_KEYS},
        "procedure_independence":True,
        "required_output":OUTPUT_KEYS,
        "protected_witnesses":(
            "target_before_plan","target_not_method","success_not_milestone",
            "versioned_referent","protected_invariants","authority_boundary",
            "reopen_conditions","OPEN_preservation","material_goal_change_reentry",
        ),
    }
    raw=goal_reconstructor(request)
    if not isinstance(raw,Mapping):
        return GoalResult("BLOCKED",None,"GOAL_RECONSTRUCTOR_INVALID_RETURN")
    missing_out=tuple(k for k in OUTPUT_KEYS if k not in raw)
    if missing_out:
        return GoalResult("OPEN",None,"GOAL_OUTPUT_MISSING:"+",".join(missing_out))

    goal={k:raw[k] for k in OUTPUT_KEYS}
    if not goal["GT"] or not goal["Succ"] or not goal["Scope"]:
        return GoalResult("OPEN",goal,"GOAL_CORE_COORDINATE_EMPTY")
    if goal["Open"] is None:
        return GoalResult("OPEN",goal,"GOAL_OPEN_COORDINATE_UNTYPED")

    status="OPEN" if bool(goal["Open"]) else "RELATIVE_CLOSE"
    return GoalResult(status,goal,None)
