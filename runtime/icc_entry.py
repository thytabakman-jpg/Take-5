"""Canonical executable entry surface for ICC128.

The canonical ICC route binds the current ICC128 controller internally from typed
environment dependencies.  Arbitrary parent-controller injection is not part of
this surface.

Protected prefix:
    ASSERT(configured, wrapped, observer)
    -> GOAL(configured, wrapped, observer)
    -> protected Packetize
    -> current ICC128 controller episode

The historical generic injected-controller wrapper remains available only through
run_icc_debug_injected and is not a canonical ICC execution claim.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Mapping

from icc128_episode_adapter import ICC128EpisodeAdapter
from icc_entry_053_candidate import run_icc_053_candidate
from icc_bootstrap import run_icc_bootstrap
from math_first_wrapper import run_math_first_wrapper


@dataclass(frozen=True)
class ICC128RuntimeBindings:
    """Environment dependencies used to construct the canonical ICC128 episode."""

    generate_questions: Callable
    generate_work: Callable
    admit_results: Callable
    update_controller_state: Callable
    generic_execute: Callable | None = None
    delegated_controller_runners: Mapping[str, Callable] | None = None
    configured_tool_adapters: Mapping[str, Callable] | None = None
    durable_backend: Any = None
    discovery_closure: Callable | None = None
    state_from_packet: Callable | None = None
    memory_from_packet: Callable | None = None
    max_iterations: int = 32

    def build_adapter(self) -> ICC128EpisodeAdapter:
        return ICC128EpisodeAdapter(
            generate_questions=self.generate_questions,
            generate_work=self.generate_work,
            admit_results=self.admit_results,
            update_state=self.update_controller_state,
            generic_execute=self.generic_execute,
            delegated_controller_runners=self.delegated_controller_runners,
            configured_tool_adapters=self.configured_tool_adapters,
            durable_backend=self.durable_backend,
            discovery_closure=self.discovery_closure,
            state_from_packet=self.state_from_packet,
            memory_from_packet=self.memory_from_packet,
            max_iterations=int(self.max_iterations),
        )


def run_icc(
    binding,
    initial_state: Any,
    initial_jane_state: Any,
    *,
    controller_bindings: ICC128RuntimeBindings,
    assert_observer_fn: Callable,
    goal_observer_fn: Callable,
    observe_fn: Callable,
    formalize_fn: Callable,
    goal_project_fn: Callable,
    packetize_fn: Callable,
    closure_fn: Callable,
    update_fn: Callable,
    jane_update_fn: Callable | None,
    result_fn: Callable,
    reentry_fn: Callable | None = None,
    relevance_fn: Callable | None = None,
    result_equivalent_fn: Callable | None = None,
    max_rounds: int = 16,
):
    """Run the canonical ICC path with ICC128 bound as the substantive controller."""

    if not isinstance(controller_bindings, ICC128RuntimeBindings):
        raise TypeError("ICC128_RUNTIME_BINDINGS_REQUIRED")

    return run_icc_053_candidate(
        binding,
        initial_state,
        initial_jane_state,
        assert_observer_fn=assert_observer_fn,
        goal_observer_fn=goal_observer_fn,
        observe_fn=observe_fn,
        formalize_fn=formalize_fn,
        goal_project_fn=goal_project_fn,
        packetize_fn=packetize_fn,
        icc128_adapter=controller_bindings.build_adapter(),
        closure_fn=closure_fn,
        update_fn=update_fn,
        jane_update_fn=jane_update_fn,
        result_fn=result_fn,
        reentry_fn=reentry_fn,
        relevance_fn=relevance_fn,
        result_equivalent_fn=result_equivalent_fn,
        max_rounds=max_rounds,
    )


def run_icc_debug_injected(
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
    """Noncanonical debug/test surface retaining the former injectable wrapper.

    A result from this function is not sufficient evidence for a repository-backed
    ICC128 execution claim.
    """

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
