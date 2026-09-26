"""Current cumulative-autonomous ImprovementCore regime surface.

This composition makes the rich IC-028 stage manager the first governed pass,
then activates recursive parent/child management when the resulting state still
has live continuation. Basis-relative learning memory participates in recursive
route selection and can also receive typed learning events from the stage state.

Regime 084 is entered by a dispatcher that can now generate a governed
zero-request observation seed before this stage manager runs.
"""
from dataclasses import dataclass
from typing import Any, Callable

from improvement_core_manager import (
    run_improvement_core_manager,
    ImprovementCoreManagerResult,
)
from improvement_core_recursive_manager import RecursiveImprovementCoreManager
from improvement_core_learning_memory import LearningMemory

REGIME_VERSION="086"

@dataclass(frozen=True)
class ImprovementCoreRegime:
    stage_manager:str
    recursive_manager:str
    learning_memory:str
    controller:str="IC-028"
    version:str=REGIME_VERSION

@dataclass(frozen=True)
class ImprovementCoreRegimeResult:
    manager_result:ImprovementCoreManagerResult
    recursive_result:dict|None
    learning_summary:tuple
    status:str
    blocker:str|None=None

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
)->ImprovementCoreRegimeResult:
    lm=learning_memory or LearningMemory()
    manager_result=run_improvement_core_manager(
        user_text,
        target=target,
        job=job,
        basis=basis,
        state=state,
        handlers=handlers,
        authority=authority,
        boundary=boundary,
        explicit_mode=explicit_mode,
        observer_risk=observer_risk,
        jane_update=jane_update,
        controller_decide=controller_decide,
        max_rounds=max_rounds,
    )
    current=manager_result.result.state
    _record_stage_learning(current,lm)

    live=isinstance(current,dict) and bool(current.get("live_continuation"))
    if not live:
        status="COMPLETE" if manager_result.result.terminal else "OPEN"
        return ImprovementCoreRegimeResult(
            manager_result,None,tuple(lm.summary()),status,None
        )

    required=("select_child_job","run_child","admit_child","update_parent")
    if recursive_handlers is None or any(k not in recursive_handlers for k in required):
        return ImprovementCoreRegimeResult(
            manager_result,
            None,
            tuple(lm.summary()),
            "OPEN",
            "RECURSIVE_MANAGER_HANDLERS_REQUIRED",
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
        )

    return ImprovementCoreRegimeResult(
        manager_result,
        recursive_result,
        tuple(lm.summary()),
        str(recursive_result.get("status","OPEN")),
        recursive_result.get("blocker"),
    )
