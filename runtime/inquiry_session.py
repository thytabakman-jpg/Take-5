"""Executable facade for the current Big Equation.

Semantic form:
    e0 = PEC(u,Z0)
    Z0+ = P_e0(Z0)
    Run_Q = HF001_session^TRC[U_Q o C_Q o E_Q o G_Q](Z0+)

The facade does not implement domain questions itself. It enforces entry preparation,
observer-first ordering when selected, closure before state admission, and recursive
HF-style reentry through the existing recursive_episode runtime.
"""
from dataclasses import dataclass
from typing import Any, Callable

from entry_contract import EntryBinding, MODE_OBSERVE_DECOUPLED, entry_is_bound
from recursive_episode import (
    ClosureResult,
    RecursiveReceipt,
    RoundResult,
    Terminal,
    run_recursive_episode,
)

@dataclass(frozen=True)
class SessionResult:
    state:Any
    receipt:RecursiveReceipt
    entry_receipt:str
    observer_used:bool
    observer_closure_status:str|None=None

def _terminal_from_closure(status):
    if status=="OPEN":
        return Terminal.OPEN
    if status=="BLOCKED":
        return Terminal.BLOCKED
    return None

def run_inquiry_session(
    binding:EntryBinding,
    initial_state:Any,
    *,
    round_fn:Callable[[Any],RoundResult],
    closure_fn:Callable[[Any,RoundResult],ClosureResult],
    update_fn:Callable[[Any,RoundResult,ClosureResult],Any],
    terminal_fn:Callable[[Any,RoundResult,ClosureResult],Terminal],
    observer_fn:Callable[[Any],RoundResult]|None=None,
    observer_reconcile_fn:Callable[[Any,RoundResult],RoundResult]|None=None,
    observer_closure_fn:Callable[[Any,RoundResult],ClosureResult]|None=None,
    challenge_fn:Callable[[Any],RoundResult]|None=None,
    max_rounds:int=64,
)->SessionResult:
    """Run the current entry-prepared, TRC-interleaved HF1 inquiry session."""
    if not entry_is_bound(binding):
        raise RuntimeError("ENTRY_CONTRACT_REQUIRED")

    state=initial_state
    observer_used=False
    observer_status=None

    if binding.contract.initial_mode==MODE_OBSERVE_DECOUPLED:
        observer_used=True
        if observer_fn is None or observer_reconcile_fn is None or observer_closure_fn is None:
            raise RuntimeError("OBSERVER_PIPELINE_UNBOUND")

        observed=observer_fn(state)
        reconciled=observer_reconcile_fn(state,observed)
        observer_closure=observer_closure_fn(state,reconciled)
        observer_status=observer_closure.status

        terminal=_terminal_from_closure(observer_closure.status)
        if terminal is not None:
            if observer_closure.admit_on_terminal:
                state=update_fn(state,reconciled,observer_closure)
            receipt=RecursiveReceipt(terminal=terminal)
            receipt.rounds.append({
                "round":"observer_preparation",
                "result_delta":reconciled.result_delta,
                "search_delta":reconciled.search_delta,
                "closure_status":observer_closure.status,
            })
            return SessionResult(
                state,receipt,binding.contract.receipt,True,observer_status
            )

        state=update_fn(state,reconciled,observer_closure)

    state,receipt=run_recursive_episode(
        state,
        round_fn=round_fn,
        closure_fn=closure_fn,
        update_fn=update_fn,
        terminal_fn=terminal_fn,
        challenge_fn=challenge_fn,
        max_rounds=max_rounds,
    )
    return SessionResult(
        state,receipt,binding.contract.receipt,observer_used,observer_status
    )
