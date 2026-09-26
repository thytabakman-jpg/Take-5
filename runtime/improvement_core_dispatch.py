"""User-invocation dispatch for Improvement Core.

Ordinary user phrases that name ImproveCore/Improvement Core resolve to the
canonical rich manager entry. This prevents the host from silently selecting
the narrower obligation/package runtime as the user-facing controller.

This module only resolves and dispatches the controller path. It does not
manufacture stage handlers or authority.
"""
from dataclasses import dataclass
from typing import Any, Callable

from entry_contract import resolve_controller
from improvement_core_manager import run_improvement_core_manager

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
        entrypoint="runtime.improvement_core_manager.run_improvement_core_manager",
    )

def dispatch_improvement_core(
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
):
    resolution=resolve_improvement_core_invocation(user_text)
    result=run_improvement_core_manager(
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
    return resolution,result
