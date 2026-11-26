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

# I. Stage and result contracts.
# Compatibility candidate (retained pending external consumer verification):
# TERMINAL_NON_SUCCESS has no local consumer.
TERMINAL_NON_SUCCESS={"OPEN","BLOCKED","CONFLICT"}
# Native result carriers use these basis-relative success dispositions.
SEMANTIC_STAGE_SUCCESS={"CLOSED","CLOSED_RELATIVE","RELATIVE_CLOSE","ACCEPT"}

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

@dataclass(frozen=True)
class MTReturnResult:
    state:Any
    mt_result:Any
    semantic_receipts:tuple[StageReceipt,...]
    open_objects:tuple[str,...]
    rounds:int
    status:str

# II. One semantic resolution pass.
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
            if material is not True and material is not False:
                receipts.append(StageReceipt(object_id,stage.tool_id,"INVALID_MATERIAL_EVIDENCE",False))
                object_open=True
                break
            receipts.append(StageReceipt(object_id,stage.tool_id,status,material))
            if material:
                current=next_state
                any_material=True
            if status not in SEMANTIC_STAGE_SUCCESS:
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

# III. MT re-entry and return boundary.
# Compatibility candidate: result_equivalent is retained in the public signature
# pending caller verification; it is not an admission or closure witness.
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
    revisited on a later MT encounter. The result_equivalent argument is kept
    for caller compatibility; prior-result equivalence cannot certify a newly
    changed semantic state.
    """
    if max_rounds < 1:
        raise ValueError("max_rounds must be >= 1")

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
        last_result=mt_result

    return MTReturnResult(state,last_result,tuple(all_receipts),open_objects,max_rounds,"OPEN")
