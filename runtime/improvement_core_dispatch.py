"""User-invocation dispatch for Improvement Core.

Ordinary user phrases that name ImproveCore/Improvement Core resolve to the
current cumulative-autonomous ImprovementCore regime. When the host supplies no
substantive target/job/basis, the dispatcher can first run governed zero-request
observation over an addressable corpus and create only a discovery seed. The
normal controller then owns substantive work generation.

Recursive-management and learning-memory inputs remain preserved across the
dispatch boundary.
"""
from dataclasses import dataclass
from typing import Any, Callable, Iterable

from entry_contract import resolve_controller
from improvement_core_regime import run_improvement_core_regime
from improvement_core_learning_memory import LearningMemory
from improvement_core_upstream import discover_upstream_seed

IMPROVEMENT_CORE_CONTROLLER="IC-028"

@dataclass(frozen=True)
class InvocationResolution:
    controller:str
    entrypoint:str

def resolve_improvement_core_invocation(user_text:str)->InvocationResolution:
    controller=resolve_controller(user_text)
    if controller!=IMPROVEMENT_CORE_CONTROLLER:
        raise RuntimeError(f"IMPROVEMENT_CORE_CONTROLLER_UNRESOLVED:{controller}")
    return InvocationResolution(
        controller=controller,
        entrypoint="runtime.improvement_core_regime.run_improvement_core_regime",
    )

def dispatch_improvement_core(
    user_text:str,
    *,
    state:Any,
    handlers:dict[str,Callable],
    target:str|None=None,
    job:str|None=None,
    basis:str|None=None,
    corpus:Iterable[Any]|None=None,
    authority=frozenset(),
    boundary=None,
    explicit_mode=None,
    observer_risk=None,
    jane_update:Callable|None=None,
    controller_decide:Callable|None=None,
    max_rounds:int=8,
    recursive_handlers:dict[str,Callable]|None=None,
    learning_memory:LearningMemory|None=None,
):
    resolution=resolve_improvement_core_invocation(user_text)

    supplied=(target is not None,job is not None,basis is not None)
    if any(supplied) and not all(supplied):
        raise RuntimeError("IMPROVEMENT_CORE_PARTIAL_ENTRY_COORDINATES")

    if not any(supplied):
        if corpus is None:
            raise RuntimeError("IMPROVEMENT_CORE_CORPUS_REQUIRED_FOR_UPSTREAM_DISCOVERY")
        seed=discover_upstream_seed(corpus)
        target,job,basis=seed.target,seed.job,seed.basis
        if state is None:
            state={}
        if not isinstance(state,dict):
            raise RuntimeError("IMPROVEMENT_CORE_UPSTREAM_STATE_REQUIRES_MAPPING")
        state={**state,**seed.state_delta}

    result=run_improvement_core_regime(
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
        recursive_handlers=recursive_handlers,
        learning_memory=learning_memory,
    )
    return resolution,result
