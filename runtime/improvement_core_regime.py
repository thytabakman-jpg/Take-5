"""Current cumulative-autonomous ImprovementCore regime surface.

The regime preserves canonical zero-request entry at the dispatch boundary, basis-relative route calibration and relation admission in upstream discovery, and a first-class external-acquisition preflight.  When outside
evidence or an outside capability has material expected value, ImprovementCore
uses a bound host adapter before expensive internal reconstruction.  When the
outside capability is unavailable, the regime preserves a typed OPEN gap
instead of pretending internal work closed it.
"""
from dataclasses import dataclass
from typing import Any, Callable

from improvement_core_manager import (
    run_improvement_core_manager,
    ImprovementCoreManagerResult,
)
from improvement_core_recursive_manager import RecursiveImprovementCoreManager
from improvement_core_learning_memory import LearningMemory
from improvement_core_external_acquisition import (
    ExternalAcquisitionReceipt,
    ExternalDisposition,
    acquire_external,
    merge_external_outputs,
)

REGIME_VERSION="090"

@dataclass(frozen=True)
class ImprovementCoreRegime:
    stage_manager:str
    recursive_manager:str
    learning_memory:str
    external_acquisition:str
    configured_tool_bridge:str
    controller:str="IC-028"
    version:str=REGIME_VERSION

@dataclass(frozen=True)
class ImprovementCoreRegimeResult:
    manager_result:ImprovementCoreManagerResult
    recursive_result:dict|None
    learning_summary:tuple
    status:str
    blocker:str|None=None
    external_receipt:ExternalAcquisitionReceipt|None=None

    @property
    def receipt(self):
        return self.manager_result.receipt

    @property
    def result(self):
        return self.manager_result.result

CURRENT_REGIME=ImprovementCoreRegime(
    stage_manager="runtime.improvement_core_manager.run_improvement_core_manager",
    recursive_manager="runtime.improvement_core_recursive_manager.RecursiveImprovementCoreManager",
    learning_memory="runtime.improvement_core_learning_memory.LearningMemory",
    external_acquisition="runtime.improvement_core_external_acquisition.acquire_external",
    configured_tool_bridge="runtime.improvement_core_tool_bridge.execute_bound_tools",
)

def _record_stage_learning(state,learning_memory):
    if not isinstance(state,dict):
        return
    events=state.get("learning_events",())
    for event in events:
        if not isinstance(event,dict):
            continue
        required={"route_id","basis_id","disposition"}
        if not required<=set(event):
            continue
        learning_memory.record(
            str(event["route_id"]),
            str(event["basis_id"]),
            str(event["disposition"]),
            set(event.get("dependency_footprint",())),
            dict(event.get("evidence",{})),
        )

def run_improvement_core_regime(
    user_text:str,
    *,
    target:str,
    job:str,
    basis:str,
    state:Any,
    handlers:dict[str,Callable],
    authority=frozenset(),
    boundary=None,
    explicit_mode=None,
    observer_risk=None,
    jane_update:Callable|None=None,
    controller_decide:Callable|None=None,
    max_rounds:int=8,
    recursive_handlers:dict[str,Callable]|None=None,
    learning_memory:LearningMemory|None=None,
    external_adapters:dict[str,Callable]|None=None,
    force_external:bool=False,
    allow_external_gap:bool=True,
    configured_tool_adapters:dict[str,Callable]|None=None,
)->ImprovementCoreRegimeResult:
    lm=learning_memory or LearningMemory()

    external_receipt=acquire_external(
        state,
        external_adapters,
        force_external=force_external,
        allow_gap=allow_external_gap,
    )
    prepared_state=merge_external_outputs(state,external_receipt)
    external_gap=(
        external_receipt.decision.disposition==ExternalDisposition.OPEN_GAP
    )

    manager_result=run_improvement_core_manager(
        user_text,
        target=target,
        job=job,
        basis=basis,
        state=prepared_state,
        handlers=handlers,
        authority=authority,
        boundary=boundary,
        explicit_mode=explicit_mode,
        observer_risk=observer_risk,
        jane_update=jane_update,
        controller_decide=controller_decide,
        max_rounds=max_rounds,
        configured_tool_adapters=configured_tool_adapters,
    )
    current=manager_result.result.state
    _record_stage_learning(current,lm)

    live=isinstance(current,dict) and bool(current.get("live_continuation"))
    if not live:
        if external_gap:
            return ImprovementCoreRegimeResult(
                manager_result,None,tuple(lm.summary()),"OPEN",
                "EXTERNAL_ACQUISITION_GAP",external_receipt
            )
        status="COMPLETE" if manager_result.result.terminal else "OPEN"
        blocker=None if manager_result.result.terminal else manager_result.result.blocker
        return ImprovementCoreRegimeResult(
            manager_result,None,tuple(lm.summary()),status,blocker,external_receipt
        )

    required=("select_child_job","run_child","admit_child","update_parent")
    if recursive_handlers is None or any(k not in recursive_handlers for k in required):
        return ImprovementCoreRegimeResult(
            manager_result,
            None,
            tuple(lm.summary()),
            "OPEN",
            "RECURSIVE_MANAGER_HANDLERS_REQUIRED",
            external_receipt,
        )

    recursive=RecursiveImprovementCoreManager(
        select_child_job=recursive_handlers["select_child_job"],
        run_child=recursive_handlers["run_child"],
        admit_child=recursive_handlers["admit_child"],
        update_parent=recursive_handlers["update_parent"],
        max_iterations=int(recursive_handlers.get("max_iterations",32)),
        learning_memory=lm,
    )
    try:
        recursive_result=recursive.run(
            dict(current),
            dict(recursive_handlers.get("memory",{})),
        )
    except RuntimeError as exc:
        return ImprovementCoreRegimeResult(
            manager_result,
            None,
            tuple(lm.summary()),
            "OPEN",
            str(exc),
            external_receipt,
        )

    status=str(recursive_result.get("status","OPEN"))
    blocker=recursive_result.get("blocker")
    if external_gap and status in {"COMPLETE","RELATIVE_CLOSE","CLOSED_RELATIVE"}:
        status="OPEN"
        blocker="EXTERNAL_ACQUISITION_GAP"

    return ImprovementCoreRegimeResult(
        manager_result,
        recursive_result,
        tuple(lm.summary()),
        status,
        blocker,
        external_receipt,
    )
