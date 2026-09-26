"""Canonical ImprovementCore progress relation.

Promoted into regime 090 as the recurrence, no-gain, and anti-cycle
mathematics. Progress claims are target-, basis-, and boundary-indexed.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Mapping, Sequence, Tuple


class EvaluationTarget(str, Enum):
    ARTIFACT = "ARTIFACT"
    METHOD = "METHOD"
    INTERACTION = "INTERACTION"
    REDUCTION = "REDUCTION"
    ACTIVATION = "ACTIVATION"
    HOST_BOUNDARY = "HOST_BOUNDARY"
    CONTROLLER = "CONTROLLER"


class EffectKind(str, Enum):
    ACTION_CHANGED = "ACTION_CHANGED"
    PROTECTED_FAILURE_PREVENTED = "PROTECTED_FAILURE_PREVENTED"
    LOWER_BURDEN_EQUIVALENT = "LOWER_BURDEN_EQUIVALENT"
    NEW_REACHABLE_WORK = "NEW_REACHABLE_WORK"
    NEGATIVE_ROUTE_CLOSED = "NEGATIVE_ROUTE_CLOSED"
    GOAL_GAP_REDUCED = "GOAL_GAP_REDUCED"
    MATERIAL_DISTINCTION_DISCOVERED = "MATERIAL_DISTINCTION_DISCOVERED"
    MATERIAL_RELATION_DISCOVERED = "MATERIAL_RELATION_DISCOVERED"
    COVERAGE_STRENGTHENED = "COVERAGE_STRENGTHENED"
    EXECUTION_TRUTH_STRENGTHENED = "EXECUTION_TRUTH_STRENGTHENED"
    OPEN_RESOLVED = "OPEN_RESOLVED"
    BLOCKED_RESOLVED = "BLOCKED_RESOLVED"
    CONFLICT_RESOLVED = "CONFLICT_RESOLVED"


TERMINAL_OBLIGATION_STATES = frozenset(
    {"CLOSED", "OPEN", "BLOCKED", "CONFLICT", "NOT_APPLICABLE"}
)


@dataclass(frozen=True)
class ClaimScope:
    target: EvaluationTarget
    job_id: str
    basis_id: str
    representation_id: str
    boundary: str
    benchmark_id: str | None = None


@dataclass(frozen=True)
class EffectWitness:
    kind: EffectKind
    target: EvaluationTarget
    basis_id: str
    boundary: str
    evidence: Mapping[str, object]
    route_id: str | None = None
    benchmark_id: str | None = None

    def valid_for(self, scope: ClaimScope) -> bool:
        if not self.evidence:
            return False
        if self.target != scope.target:
            return False
        if self.boundary != scope.boundary:
            return False
        if self.basis_id != scope.basis_id:
            return False
        if scope.benchmark_id is not None and self.benchmark_id != scope.benchmark_id:
            return False
        return True


@dataclass(frozen=True)
class TransitionComparison:
    scope: ClaimScope
    pre_semantic_class: str
    post_semantic_class: str
    pre_basis_id: str
    post_basis_id: str
    protected_before: FrozenSet[str] = frozenset()
    protected_after: FrozenSet[str] = frozenset()
    explicitly_disposed_losses: FrozenSet[str] = frozenset()
    effects: Tuple[EffectWitness, ...] = ()
    obligation_states: Tuple[str, ...] = ()
    boundary_verified: bool = False
    basis_reconciled: bool = False


@dataclass(frozen=True)
class SemanticStep:
    semantic_class: str
    basis_id: str
    effects: Tuple[str, ...] = ()
    resolved_unresolved_state: bool = False


def silent_regressions(cmp: TransitionComparison) -> frozenset[str]:
    lost = set(cmp.protected_before) - set(cmp.protected_after)
    lost -= set(cmp.explicitly_disposed_losses)
    return frozenset(lost)


def obligations_typed(cmp: TransitionComparison) -> bool:
    return all(state in TERMINAL_OBLIGATION_STATES for state in cmp.obligation_states)


def comparison_basis_valid(cmp: TransitionComparison) -> bool:
    if cmp.pre_basis_id == cmp.post_basis_id == cmp.scope.basis_id:
        return True
    return cmp.basis_reconciled


def valid_effects(cmp: TransitionComparison) -> tuple[EffectWitness, ...]:
    return tuple(effect for effect in cmp.effects if effect.valid_for(cmp.scope))


def strict_progress(cmp: TransitionComparison) -> bool:
    """Canonical partial strict-gain witness.

    A transition is a strict gain for the stated scope only when no protected
    regression is hidden, at least one causal effect witnesses the exact
    evaluation target/boundary/basis, obligations are typed, and the claimed
    boundary has actually been verified.
    """
    return bool(
        not silent_regressions(cmp)
        and valid_effects(cmp)
        and obligations_typed(cmp)
        and comparison_basis_valid(cmp)
        and cmp.boundary_verified
    )


def certified_no_gain(cmp: TransitionComparison) -> bool:
    """Witness a genuinely tested continuation-equivalent no-gain transition."""
    return bool(
        cmp.pre_semantic_class == cmp.post_semantic_class
        and cmp.pre_basis_id == cmp.post_basis_id == cmp.scope.basis_id
        and not valid_effects(cmp)
        and not silent_regressions(cmp)
        and obligations_typed(cmp)
        and cmp.boundary_verified
    )


def cycle_no_gain(history: Sequence[SemanticStep]) -> bool:
    """Detect a repeated semantic class under the same basis with no net effect.

    This deliberately ignores raw artifact/state IDs. The final semantic class
    must have appeared earlier under the same basis and all intervening steps
    must be effect-free and must not resolve an OPEN/BLOCKED/CONFLICT state.
    """
    if len(history) < 2:
        return False

    current = history[-1]
    for i in range(len(history) - 2, -1, -1):
        prior = history[i]
        if (
            prior.semantic_class == current.semantic_class
            and prior.basis_id == current.basis_id
        ):
            intervening = history[i + 1 :]
            return all(
                not step.effects and not step.resolved_unresolved_state
                for step in intervening
            )
    return False


def retry_licensed(
    dependency_footprint: frozenset[str],
    changed_coordinates: frozenset[str],
    *,
    failure_signature_defeated: bool = False,
    representation_changed: bool = False,
    executability_changed: bool = False,
    new_interaction_package: bool = False,
) -> bool:
    return bool(
        set(dependency_footprint) & set(changed_coordinates)
        or failure_signature_defeated
        or representation_changed
        or executability_changed
        or new_interaction_package
    )
