"""Generic recursive episode wrapper for Take-5 nonproduction research.

Implements the current semantic pattern:
round -> Tool Run Closure -> admitted update -> HF-style reentry.
A stronger terminal claim may require an external challenger.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

class Terminal(str, Enum):
    CONTINUE = "CONTINUE"
    RELATIVE_CLOSE = "RELATIVE_CLOSE"
    OPEN = "OPEN"
    BLOCKED = "BLOCKED"

@dataclass(frozen=True)
class RoundResult:
    value: Any
    result_delta: bool = False
    search_delta: bool = False
    open_coordinates: tuple[str, ...] = ()

@dataclass(frozen=True)
class ClosureResult:
    status: str
    value: Any = None
    open_coordinates: tuple[str, ...] = ()

@dataclass
class RecursiveReceipt:
    rounds: list[dict[str, Any]] = field(default_factory=list)
    terminal: Terminal = Terminal.CONTINUE
    external_challenge_used: bool = False

def run_recursive_episode(
    initial_state: Any,
    *,
    round_fn: Callable[[Any], RoundResult],
    closure_fn: Callable[[Any, RoundResult], ClosureResult],
    update_fn: Callable[[Any, RoundResult, ClosureResult], Any],
    terminal_fn: Callable[[Any, RoundResult, ClosureResult], Terminal],
    challenge_fn: Callable[[Any], RoundResult] | None = None,
    max_rounds: int = 64,
):
    """Run interleaved recursive closure.

    Every round crosses closure_fn before state can be re-entered.
    A relative-close decision is challenged once when challenge_fn is supplied.
    """
    state = initial_state
    receipt = RecursiveReceipt()

    for index in range(1, max_rounds + 1):
        rr = round_fn(state)
        cr = closure_fn(state, rr)
        receipt.rounds.append({
            "round": index,
            "result_delta": rr.result_delta,
            "search_delta": rr.search_delta,
            "closure_status": cr.status,
        })

        if cr.status == "OPEN":
            receipt.terminal = Terminal.OPEN
            return state, receipt
        if cr.status == "BLOCKED":
            receipt.terminal = Terminal.BLOCKED
            return state, receipt

        state = update_fn(state, rr, cr)
        decision = terminal_fn(state, rr, cr)

        if decision == Terminal.RELATIVE_CLOSE and challenge_fn is not None and not receipt.external_challenge_used:
            receipt.external_challenge_used = True
            challenge = challenge_fn(state)
            challenge_closure = closure_fn(state, challenge)
            receipt.rounds.append({
                "round": f"{index}:external_challenge",
                "result_delta": challenge.result_delta,
                "search_delta": challenge.search_delta,
                "closure_status": challenge_closure.status,
            })
            if challenge_closure.status == "OPEN":
                receipt.terminal = Terminal.OPEN
                return state, receipt
            if challenge_closure.status == "BLOCKED":
                receipt.terminal = Terminal.BLOCKED
                return state, receipt
            state = update_fn(state, challenge, challenge_closure)
            if challenge.result_delta or challenge.search_delta:
                continue

        if decision != Terminal.CONTINUE:
            receipt.terminal = decision
            return state, receipt

        if not (rr.result_delta or rr.search_delta):
            receipt.terminal = Terminal.OPEN
            return state, receipt

    receipt.terminal = Terminal.OPEN
    return state, receipt
