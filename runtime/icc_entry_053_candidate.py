"""Guarded ICC128 entry substrate retained from the Kernel 053 candidate lineage.

The canonical caller constructs ICC128 internally. This substrate enforces the
ICC128 binding, anchors the operational goal to the admitted bootstrap GOAL
receipt, and guards Packetize against substantive selection.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from icc_bootstrap import run_icc_bootstrap
from math_first_wrapper import MathFirstResult, run_math_first_wrapper
from kernel053_packetize import PacketizeSelectionBlocked, validate_packetize_output


ICC128_CONTROLLER="ICC128"


def run_icc_053_candidate(
    binding,
    initial_state:Any,
    initial_jane_state:Any,
    *,
    assert_observer_fn:Callable,
    goal_observer_fn:Callable,
    observe_fn:Callable,
    formalize_fn:Callable,
    packetize_fn:Callable,
    icc128_adapter:Callable,
    closure_fn:Callable,
    update_fn:Callable,
    jane_update_fn:Callable|None,
    result_fn:Callable,
    reentry_fn:Callable|None=None,
    relevance_fn:Callable|None=None,
    result_equivalent_fn:Callable|None=None,
    max_rounds:int=16,
):
    controller=str(getattr(getattr(binding,"contract",None),"controller",""))
    lease_controller=str(getattr(getattr(binding,"lease",None),"controller",""))
    if controller!=ICC128_CONTROLLER or lease_controller!=ICC128_CONTROLLER:
        return MathFirstResult(
            initial_state,
            initial_jane_state,
            "BLOCKED",
            (),
            "ICC128_CONTROLLER_BINDING_REQUIRED",
        )

    governing_goal_holder={}

    def bootstrap_fn(state,bound):
        receipt=run_icc_bootstrap(
            deepcopy(state),
            bound,
            assert_observer_fn=assert_observer_fn,
            goal_observer_fn=goal_observer_fn,
        )
        governing_goal_holder["goal"]=deepcopy(receipt.goal_receipt.result)
        return receipt

    def project_governing_goal(math,bound):
        if "goal" not in governing_goal_holder:
            raise RuntimeError("GOVERNING_GOAL_BOOTSTRAP_REQUIRED")
        return {
            "governing_goal":deepcopy(governing_goal_holder["goal"]),
            "frozen_basis":deepcopy(math),
        }

    def guarded_packetize(math,goal,state,bound):
        try:
            packet=validate_packetize_output(
                packetize_fn(
                    deepcopy(math),
                    deepcopy(goal),
                    deepcopy(state),
                    bound,
                )
            )
        except PacketizeSelectionBlocked:
            raise
        packet["_kernel053_governed_state_snapshot"]=deepcopy(state)
        return packet

    kwargs=dict(
        bootstrap_fn=bootstrap_fn,
        observe_fn=observe_fn,
        formalize_fn=formalize_fn,
        goal_fn=project_governing_goal,
        architect_fn=guarded_packetize,
        ic_fn=icc128_adapter,
        closure_fn=closure_fn,
        update_fn=update_fn,
        jane_update_fn=jane_update_fn,
        result_fn=result_fn,
        reentry_fn=reentry_fn,
        result_equivalent_fn=result_equivalent_fn,
        max_rounds=max_rounds,
    )
    if relevance_fn is not None:
        kwargs["relevance_fn"]=relevance_fn

    return run_math_first_wrapper(
        binding,
        initial_state,
        initial_jane_state,
        **kwargs,
    )
