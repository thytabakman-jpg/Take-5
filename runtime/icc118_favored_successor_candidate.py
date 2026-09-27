"""Project-local candidate for the favored ICC118 behavioral successor.

Not a promoted configured tool. The candidate reconstructs the high-value behavior
that was repeatedly attached to the "118" label across historically colliding usages.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Tuple

@dataclass(frozen=True)
class Reality:
    semantic_available: bool
    runtime_available: bool
    authority_available: bool

@dataclass(frozen=True)
class Residual:
    residual_id: str
    resolved: bool = False
    candidate_actions: Tuple[str,...] = ()
    boundary_class: str | None = None
    coverage_adequate: bool = False
    reopen_conditions: Tuple[str,...] = ()

@dataclass(frozen=True)
class Action:
    action_id: str
    expected_gain: float
    dependency_leverage: float
    continuation_value: float
    cost: float
    preserves: bool = True

def reality_status(r: Reality) -> str:
    if not r.semantic_available:
        return "SEMANTIC_UNAVAILABLE"
    if not r.runtime_available:
        return "RUNTIME_BLOCKED"
    if not r.authority_available:
        return "AUTHORITY_BLOCKED"
    return "EXECUTABLE"

def _dominates(a: Action, b: Action) -> bool:
    no_worse=(
        a.expected_gain >= b.expected_gain and
        a.dependency_leverage >= b.dependency_leverage and
        a.continuation_value >= b.continuation_value and
        a.cost <= b.cost
    )
    strict=(
        a.expected_gain > b.expected_gain or
        a.dependency_leverage > b.dependency_leverage or
        a.continuation_value > b.continuation_value or
        a.cost < b.cost
    )
    return no_worse and strict

def nondominated(actions: Iterable[Action]) -> tuple[Action,...]:
    pool=tuple(a for a in actions if a.preserves)
    return tuple(a for a in pool if not any(_dominates(b,a) for b in pool if b!=a))

def live(residual: Residual) -> bool:
    if residual.resolved:
        return False
    if residual.candidate_actions:
        return True
    return not (
        residual.boundary_class in {
            "EXTERNAL_CONTROL","USER_AUTHORITY","EVIDENCE_EXHAUSTED",
            "HISTORICAL_EVIDENCE_EXHAUSTED","CONFLICT_TERMINAL"
        }
        and residual.coverage_adequate
        and bool(residual.reopen_conditions)
    )

def completion(parent_goal_satisfied: bool, residuals: Iterable[Residual]) -> bool:
    return bool(parent_goal_satisfied and not any(live(r) for r in residuals))

PROTECTED_BEHAVIORS=(
    "REALITY_TRIAD_SEPARATION",
    "STATE_RELATIVE_WORK_SELECTION",
    "NONDOMINATED_PLURALITY",
    "CHEAP_DIRECT_PATH_WHEN_DOMINATING",
    "STRUCTURAL_STEWARDSHIP_AND_OWNER_SEPARATION",
    "PARENT_GOAL_CONTINUITY",
    "NO_PREMATURE_UNRESOLVED_RELEASE",
    "EXECUTION_TRUTH",
    "RESULT_SENSITIVE_REENTRY",
    "USER_DOES_NOT_SCRIPT_INTERNAL_TOOL_SEQUENCE",
)
