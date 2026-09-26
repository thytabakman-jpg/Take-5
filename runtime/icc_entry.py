"""Canonical executable entry surface for ICC.

Every ICC run enters here or through another surface that preserves the same
bootstrap invariant enforced again by math_first_wrapper.

Protected prefix:
    ASSERT(configured, wrapped, observer)
    -> GOAL(configured, wrapped, observer)
    -> ICC wrapper

The bootstrap is deliberately fail-closed.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from icc_bootstrap import run_icc_bootstrap
from math_first_wrapper import run_math_first_wrapper


def run_icc(
    binding,
    initial_state: Any,
    initial_jane_state: Any,
    *,
    assert_observer_fn: Callable,
    goal_observer_fn: Callable,
    observe_fn: Callable,
    formalize_fn: Callable,
    goal_fn: Callable,
    architect_fn: Callable,
    ic_fn: Callable,
    closure_fn: Callable,
    update_fn: Callable,
    jane_update_fn: Callable | None,
    result_fn: Callable,
    reentry_fn: Callable | None = None,
    relevance_fn: Callable | None = None,
    result_equivalent_fn: Callable | None = None,
    max_rounds: int = 16,
):
    """Run ICC only after the protected observer bootstrap is certified."""

    def bootstrap_fn(state, bound):
        return run_icc_bootstrap(
            deepcopy(state),
            bound,
            assert_observer_fn=assert_observer_fn,
            goal_observer_fn=goal_observer_fn,
        )

    kwargs = dict(
        bootstrap_fn=bootstrap_fn,
        observe_fn=observe_fn,
        formalize_fn=formalize_fn,
        goal_fn=goal_fn,
        architect_fn=architect_fn,
        ic_fn=ic_fn,
        closure_fn=closure_fn,
        update_fn=update_fn,
        jane_update_fn=jane_update_fn,
        result_fn=result_fn,
        reentry_fn=reentry_fn,
        result_equivalent_fn=result_equivalent_fn,
        max_rounds=max_rounds,
    )
    if relevance_fn is not None:
        kwargs["relevance_fn"] = relevance_fn

    return run_math_first_wrapper(
        binding,
        initial_state,
        initial_jane_state,
        **kwargs,
    )
