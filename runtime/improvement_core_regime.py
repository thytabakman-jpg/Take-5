"""Current cumulative-autonomous ImprovementCore regime surface.

This is a composition surface, not a new controller ontology. It combines the
validated rich IC-028 stage manager with recursive child management and
basis-relative learning memory recovered as strict gains from the historical
ImprovementCore lineage.
"""
from dataclasses import dataclass
from typing import Any, Callable

from improvement_core_manager import (
    run_improvement_core_manager,
    ImprovementCoreManagerResult,
)
from improvement_core_recursive_manager import RecursiveImprovementCoreManager
from improvement_core_learning_memory import LearningMemory

@dataclass(frozen=True)
class ImprovementCoreRegime:
    stage_manager:str
    recursive_manager:str
    learning_memory:str
    controller:str="IC-028"

CURRENT_REGIME=ImprovementCoreRegime(
    stage_manager="runtime.improvement_core_manager.run_improvement_core_manager",
    recursive_manager="runtime.improvement_core_recursive_manager.RecursiveImprovementCoreManager",
    learning_memory="runtime.improvement_core_learning_memory.LearningMemory",
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
)->ImprovementCoreManagerResult:
    return run_improvement_core_manager(
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
