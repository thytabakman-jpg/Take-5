"""Synchronous before-return semantic gate for configured MT.

A black box does not have to be fully solved. The gate performs one finite
configured resolution pass, admits any material progress, re-runs MT when that
progress can change MT's result, and preserves unresolved residue as OPEN for
future encounters.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable

from semantic_resolution_pipeline import plan_black_box_resolution

TERMINAL_NON_SUCCESS={"OPEN","BLOCKED"}

@dataclass(frozen=True)
class StageReceipt:
    object_id:str
    tool_id:str
    status:str
    material:bool

@dataclass(frozen=True)
class SemanticGateResult:
    state:Any
    receipts:tuple[StageReceipt,...]
    open_objects:tuple[str,...]
    material:bool
    stop_reason:str

def run_semantic_pass(
    state:Any,
    black_box_ids:Iterable[str],
    *,
    execute_stage:Callable[[str,str,Any],tuple[Any,str,bool]],
)->SemanticGateResult:
    current=state
    receipts=[]
    open_objects=[]
    any_material=False

    for object_id in tuple(dict.fromkeys(str(x) for x in black_box_ids)):
        plan=plan_black_box_resolution(object_id)
        object_open=False
        for stage in plan.stages:
            next_state,status,material=execute_stage(stage.tool_id,object_id,current)
            status=str(status)
            material=bool(material)
            receipts.append(StageReceipt(object_id,stage.tool_id,status,material))
            if material:
                current=next_state
                any_material=True
            if status in TERMINAL_NON_SUCCESS:
                object_open=True
                break
        if object_open:
            open_objects.append(object_id)

    return SemanticGateResult(
        current,
        tuple(receipts),
        tuple(dict.fromkeys(open_objects)),
        any_material,
        "MATERIAL_PROGRESS" if any_material else ("OPEN_PRESERVED" if open_objects else "NO_MATERIAL_DELTA"),
    )

@dataclass(frozen=True)
class MTReturnResult:
    state:Any
    mt_result:Any
    semantic_receipts:tuple[StageReceipt,...]
    open_objects:tuple[str,...]
    rounds:int
    status:str

def run_mt_with_before_return_gate(
    initial_state:Any,
    *,
    run_mt:Callable[[Any],tuple[Any,Any]],
    detect_black_boxes:Callable[[Any,Any],Iterable[str]],
    execute_stage:Callable[[str,str,Any],tuple[Any,str,bool]],
    result_equivalent:Callable[[Any,Any],bool]=lambda a,b:a==b,
    max_rounds:int=4,
)->MTReturnResult:
    """Run MT, enrich black boxes synchronously, and re-run MT on material deltas.

    This does not require semantic closure. OPEN residue is returned and may be
    revisited on a later MT encounter.
    """
    state=initial_state
    all_receipts=[]
    last_result=None
    open_objects=()

    for round_index in range(1,max_rounds+1):
        mt_state,mt_result=run_mt(state)
        boxes=tuple(dict.fromkeys(str(x) for x in detect_black_boxes(mt_state,mt_result)))
        if not boxes:
            return MTReturnResult(mt_state,mt_result,tuple(all_receipts),(),round_index,"CLOSED_RELATIVE")

        semantic=run_semantic_pass(mt_state,boxes,execute_stage=execute_stage)
        all_receipts.extend(semantic.receipts)
        open_objects=semantic.open_objects

        if not semantic.material:
            return MTReturnResult(
                semantic.state,mt_result,tuple(all_receipts),open_objects,round_index,
                "OPEN" if open_objects else "CLOSED_RELATIVE"
            )

        state=semantic.state
        if last_result is not None and result_equivalent(last_result,mt_result):
            # Semantic state improved, but the protected MT result has stabilized.
            return MTReturnResult(
                state,mt_result,tuple(all_receipts),open_objects,round_index,
                "OPEN" if open_objects else "CLOSED_RELATIVE"
            )
        last_result=mt_result

    return MTReturnResult(state,last_result,tuple(all_receipts),open_objects,max_rounds,"OPEN")
