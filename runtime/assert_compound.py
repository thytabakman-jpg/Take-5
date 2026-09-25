"""Executable orchestration shell for the compound ASSERT fixed-point engine.

This module binds the seven protected ASSERT stages and their reentry/closure
semantics without pretending that every stage's domain-specific semantics are
globally solved. Stage implementations are injected as typed callables.

Protected order:
ASSERT -> COMPARE -> RESOLVE -> HERE -> COMPARE -> INQUIRE -> REASSERT
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Callable, Mapping, Tuple

ASSERT_STAGE_ORDER: Tuple[str, ...] = (
    "ASSERT",
    "COMPARE_1",
    "RESOLVE",
    "HERE",
    "COMPARE_2",
    "INQUIRE",
    "REASSERT",
)

EPISTEMIC_STATUSES = ("TRUE", "FALSE", "UNKNOWN", "CONFLICT")
NON_SUCCESS_STATUSES = ("UNKNOWN", "OPEN", "BLOCKED", "CONFLICT")


@dataclass(frozen=True)
class AssertState:
    """Versionable state carried across ASSERT rounds.

    Payloads stay generic because ASSERT is a cross-domain orchestration tool.
    The orchestration layer preserves identity and stage order; domain-specific
    stage implementations own the internal schemas of each payload.
    """

    assertions: Any = ()
    comparisons: Any = ()
    resolutions: Any = ()
    here: Any = ()
    inquiries: Any = ()
    questions: Any = ()
    world: Any = ()
    discovery: Any = ()
    metadata: Mapping[str, Any] | None = None


Stage = Callable[[AssertState], AssertState]


@dataclass(frozen=True)
class AssertStages:
    assert_stage: Stage
    compare_stage: Stage
    resolve_stage: Stage
    here_stage: Stage
    inquire_stage: Stage
    reassert_stage: Stage


@dataclass(frozen=True)
class RoundResult:
    state: AssertState
    trace: Tuple[str, ...]


@dataclass(frozen=True)
class CompoundResult:
    state: AssertState
    rounds: int
    status: str
    traces: Tuple[Tuple[str, ...], ...]


def run_round(state: AssertState, stages: AssertStages) -> RoundResult:
    """Execute exactly one protected ASSERT round."""

    trace = []

    state = stages.assert_stage(state)
    trace.append("ASSERT")

    state = stages.compare_stage(state)
    trace.append("COMPARE_1")

    state = stages.resolve_stage(state)
    trace.append("RESOLVE")

    state = stages.here_stage(state)
    trace.append("HERE")

    # The second comparison is intentionally mandatory. HERE can recover new
    # objects/relations that invalidate the first comparison.
    state = stages.compare_stage(state)
    trace.append("COMPARE_2")

    state = stages.inquire_stage(state)
    trace.append("INQUIRE")

    state = stages.reassert_stage(state)
    trace.append("REASSERT")

    return RoundResult(state=state, trace=tuple(trace))


def discovery_signature(state: AssertState) -> tuple[Any, ...]:
    """Coordinates whose change forces ASSERT reentry under Contract 055."""

    return (
        state.assertions,
        state.comparisons,
        state.resolutions,
        state.here,
        state.inquiries,
        state.questions,
        state.world,
        state.discovery,
    )


def run_to_fixed_point(
    initial: AssertState,
    stages: AssertStages,
    *,
    max_rounds: int = 32,
    closure_gate: Callable[[AssertState], bool] | None = None,
) -> CompoundResult:
    """Reenter until discovery/world state stabilizes and closure is licensed.

    Equality is deliberately basis-relative to the explicit ASSERT state. A
    stronger caller may add a closure_gate that checks result-sensitive
    OPEN/BLOCKED/CONFLICT coordinates, verification, or domain obligations.
    """

    if max_rounds < 1:
        raise ValueError("max_rounds must be >= 1")

    current = initial
    previous_signature = None
    traces = []

    for round_no in range(1, max_rounds + 1):
        result = run_round(current, stages)
        current = result.state
        traces.append(result.trace)
        signature = discovery_signature(current)

        stable = previous_signature is not None and signature == previous_signature
        gate_ok = closure_gate(current) if closure_gate is not None else True

        if stable and gate_ok:
            return CompoundResult(
                state=current,
                rounds=round_no,
                status="CLOSED",
                traces=tuple(traces),
            )

        previous_signature = signature

    return CompoundResult(
        state=current,
        rounds=max_rounds,
        status="OPEN",
        traces=tuple(traces),
    )


def identity_stage(state: AssertState) -> AssertState:
    """Convenience stage for tests/adapters that intentionally make no change."""

    return replace(state)
