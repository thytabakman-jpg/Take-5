"""Current cumulative-autonomous ImprovementCore regime surface.

Every governed ImprovementCore episode ends in a mandatory ImproveCoreAfterRun
self-improvement pass. The pass always records learning and updates the next
improvement frontier. Structural self-change remains strict-gain and
authority-gated rather than automatic mutation.
"""
from dataclasses import dataclass
from typing import Any, Callable

from improvement_core_manager import (
    run_improvement_core_manager,
    ImprovementCoreManagerResult,
)
from improvement_core_recursive_manager import RecursiveImprovementCoreManager
from improvement_core_learning_memory import LearningMemory
from improvement_core_afterrun import AfterRunReceipt, run_afterrun_improvement

REGIME_VERSION="093"

@dataclass(frozen=True)
class ImprovementCoreRegime:
    stage_manager:str
    recursive_manager:str
    learning_memory:str
    afterrun_tool:str
    response_bias_control:str
    object_lifecycle:str
    controller:str="IC-028"
    version:str=REGIME_VERSION

@dataclass(frozen=True)
class ImprovementCoreRegimeResult:
    manager_result:ImprovementCoreManagerResult
    recursive_result:dict|None
    learning_summary:tuple
    status:str
    blocker:str|None=None
    afterrun_receipt:AfterRunReceipt|None=None

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
    afterrun_tool="runtime.improvement_core_afterrun.run_afterrun_improvement",
    response_bias_control="runtime.improvement_core_response_bias",
    object_lifecycle="runtime.object_lifecycle",
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

def _finalize(*, manager_result, recursive_result, lm, basis, status, blocker,
              user_text, object_package_base,
              strict_gain_evaluator=None, authorized_applier=None):
    state=(
        recursive_result.get("state",manager_result.result.state)
        if isinstance(recursive_result,dict)
        else manager_result.result.state
    )
    after=run_afterrun_improvement(
        episode_id="improvement-core-manager",
        basis_id=str(basis),
        status=str(status),
        blocker=blocker,
        state=state,
        learning_memory=lm,
        recursive_result=recursive_result,
        strict_gain_evaluator=strict_gain_evaluator,
        authorized_applier=authorized_applier,
        user_text=user_text,
        object_package_base=object_package_base,
    )
    return ImprovementCoreRegimeResult(
        manager_result,
        recursive_result,
        tuple(lm.summary()),
        str(status),
        blocker,
        after,
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
    afterrun_strict_gain_evaluator:Callable|None=None,
    afterrun_authorized_applier:Callable|None=None,
    object_package_base:str|None="semantic_objects",
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
        return _finalize(
            manager_result=manager_result,recursive_result=None,lm=lm,basis=basis,
            status=status,blocker=manager_result.result.blocker,
            user_text=user_text,object_package_base=object_package_base,
            strict_gain_evaluator=afterrun_strict_gain_evaluator,
            authorized_applier=afterrun_authorized_applier,
        )

    required=("select_child_job","run_child","admit_child","update_parent")
    if recursive_handlers is None or any(k not in recursive_handlers for k in required):
        return _finalize(
            manager_result=manager_result,recursive_result=None,lm=lm,basis=basis,
            status="OPEN",blocker="RECURSIVE_MANAGER_HANDLERS_REQUIRED",
            user_text=user_text,object_package_base=object_package_base,
            strict_gain_evaluator=afterrun_strict_gain_evaluator,
            authorized_applier=afterrun_authorized_applier,
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
        return _finalize(
            manager_result=manager_result,recursive_result=None,lm=lm,basis=basis,
            status="OPEN",blocker=str(exc),
            user_text=user_text,object_package_base=object_package_base,
            strict_gain_evaluator=afterrun_strict_gain_evaluator,
            authorized_applier=afterrun_authorized_applier,
        )

    return _finalize(
        manager_result=manager_result,recursive_result=recursive_result,lm=lm,basis=basis,
        status=str(recursive_result.get("status","OPEN")),
        blocker=recursive_result.get("blocker"),
        user_text=user_text,object_package_base=object_package_base,
        strict_gain_evaluator=afterrun_strict_gain_evaluator,
        authorized_applier=afterrun_authorized_applier,
    )
