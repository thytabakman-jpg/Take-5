"""Canonical Improvement Core manager entry.

This is the explicit user-invocation path for the rich IC-028 controller.
It binds the entry contract before substantive work and delegates the governed
episode to runtime/ic028_operator.py.

The narrower runtime/improvement_core.py remains available as a subordinate
obligation/package capability; it is not the manager identity.
"""
from dataclasses import dataclass
from typing import Any, Callable

from entry_contract import bind_entry_contract, MODE_GOAL_DIRECTED, MODE_OBSERVE_DECOUPLED
from ic028_operator import run_ic028, OperatorResult

@dataclass(frozen=True)
class ImprovementCoreManagerReceipt:
    controller:str
    initial_mode:str
    entry_receipt:str
    terminal:bool
    blocker:str|None
    stages:tuple[str,...]

@dataclass(frozen=True)
class ImprovementCoreManagerResult:
    result:OperatorResult
    receipt:ImprovementCoreManagerReceipt

def run_improvement_core_manager(
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
    configured_tool_adapters:dict[str,Callable]|None=None,
)->ImprovementCoreManagerResult:
    binding=bind_entry_contract(
        user_text,
        target=target,
        job=job,
        basis=basis,
        authority=frozenset(authority),
        boundary=boundary,
        explicit_mode=explicit_mode,
        observer_risk=observer_risk,
        episode_id="improvement-core-manager",
    )
    out=run_ic028(
        binding.lease,
        state,
        handlers,
        entry_contract=binding.contract,
        jane_update=jane_update,
        controller_decide=controller_decide,
        max_rounds=max_rounds,
        configured_tool_adapters=configured_tool_adapters,
    )
    receipt=ImprovementCoreManagerReceipt(
        controller=binding.contract.controller,
        initial_mode=binding.contract.initial_mode,
        entry_receipt=binding.contract.receipt,
        terminal=out.terminal,
        blocker=out.blocker,
        stages=tuple(r.stage for r in out.receipts),
    )
    return ImprovementCoreManagerResult(out,receipt)

def manager_mode_name(mode:str)->str:
    if mode==MODE_OBSERVE_DECOUPLED:
        return "OBSERVER_FIRST"
    if mode==MODE_GOAL_DIRECTED:
        return "GOAL_DIRECTED"
    return "UNKNOWN"
