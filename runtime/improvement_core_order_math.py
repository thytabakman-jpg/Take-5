"""Indexed preorder mathematics for ImprovementCore strict gain.

Candidate successor to the transition-local progress predicate.
Research branch only until repository validation and promotion.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import FrozenSet, Iterable, Mapping, Tuple


class ExecutionLevel(IntEnum):
    NOT_EXECUTED = 0
    SELECTED = 1
    BOUND = 2
    EXECUTED = 3
    CONSUMED = 4
    VERIFIED = 5


@dataclass(frozen=True)
class Basis:
    basis_id: str
    vocabulary: FrozenSet[str] = frozenset()
    authority: FrozenSet[str] = frozenset()
    protected: FrozenSet[str] = frozenset()


@dataclass(frozen=True)
class SystemState:
    state_id: str
    basis_id: str
    protected_capabilities: FrozenSet[str] = frozenset()
    admissible_models: FrozenSet[str] = frozenset()
    satisfied_goals: FrozenSet[str] = frozenset()
    verified_contributions: FrozenSet[str] = frozenset()
    execution_level: ExecutionLevel = ExecutionLevel.NOT_EXECUTED
    burden: float = 0.0


@dataclass(frozen=True)
class TransportCertificate:
    source_basis: str
    target_basis: str
    common_basis: str
    source_map: Mapping[str, str]
    target_map: Mapping[str, str]
    preserves_protected: bool = True
    preserves_authority: bool = True
    path_coherent: bool = True
    evidence: Tuple[str, ...] = ()

    @property
    def valid(self) -> bool:
        return bool(
            self.common_basis
            and self.preserves_protected
            and self.preserves_authority
            and self.path_coherent
            and self.evidence
        )


@dataclass(frozen=True)
class ComparisonFrame:
    """One declared comparison basis for a whole improvement episode.

    A frame assigns every participating basis exactly one admitted transport into
    the same common basis. This prevents pairwise comparisons from silently
    changing comparison frames and makes chain transitivity testable.
    """
    frame_id: str
    common_basis: str
    transports: Mapping[str, Mapping[str, str]]
    preserves_protected: bool = True
    preserves_authority: bool = True
    evidence: Tuple[str, ...] = ()

    @property
    def valid(self) -> bool:
        return bool(
            self.frame_id
            and self.common_basis
            and self.preserves_protected
            and self.preserves_authority
            and self.evidence
        )

    def transport(self, state: SystemState) -> SystemState | None:
        if not self.valid:
            return None
        if state.basis_id == self.common_basis:
            mapping: Mapping[str, str] = {}
        else:
            mapping = self.transports.get(state.basis_id)
            if mapping is None:
                return None
        return transport_state(
            state,
            common_basis=self.common_basis,
            mapping=mapping,
        )


@dataclass(frozen=True)
class Comparison:
    left: SystemState
    right: SystemState
    comparable: bool
    non_regressive: bool
    strict_coordinates: Tuple[str, ...]
    equivalent: bool
    reason: str


def _transport_id(value: str, mapping: Mapping[str, str]) -> str:
    return str(mapping.get(value, value))


def _transport_set(values: FrozenSet[str], mapping: Mapping[str, str]) -> FrozenSet[str]:
    return frozenset(_transport_id(v, mapping) for v in values)


def transport_state(
    state: SystemState,
    *,
    common_basis: str,
    mapping: Mapping[str, str],
) -> SystemState:
    return SystemState(
        state_id=state.state_id,
        basis_id=common_basis,
        protected_capabilities=_transport_set(state.protected_capabilities, mapping),
        admissible_models=_transport_set(state.admissible_models, mapping),
        satisfied_goals=_transport_set(state.satisfied_goals, mapping),
        verified_contributions=_transport_set(state.verified_contributions, mapping),
        execution_level=state.execution_level,
        burden=state.burden,
    )


def common_basis_states(
    left: SystemState,
    right: SystemState,
    certificate: TransportCertificate | None = None,
) -> tuple[SystemState, SystemState] | None:
    if left.basis_id == right.basis_id:
        return left, right
    if certificate is None or not certificate.valid:
        return None
    if certificate.source_basis != left.basis_id or certificate.target_basis != right.basis_id:
        return None
    return (
        transport_state(left, common_basis=certificate.common_basis, mapping=certificate.source_map),
        transport_state(right, common_basis=certificate.common_basis, mapping=certificate.target_map),
    )


def information_refines(left: SystemState, right: SystemState) -> bool:
    """Right is at least as informative when it rules out no fewer admissible models.

    Empty model sets are not treated as automatically better; they are reserved for
    explicit inconsistency handling outside this preorder.
    """
    if not left.admissible_models or not right.admissible_models:
        return left.admissible_models == right.admissible_models
    return right.admissible_models <= left.admissible_models


def _semantic_weak(left: SystemState, right: SystemState) -> bool:
    return bool(
        left.protected_capabilities <= right.protected_capabilities
        and information_refines(left, right)
        and left.satisfied_goals <= right.satisfied_goals
        and left.verified_contributions <= right.verified_contributions
        and left.execution_level <= right.execution_level
    )


def _semantic_strict_coordinates(left: SystemState, right: SystemState) -> tuple[str, ...]:
    strict = []
    if left.protected_capabilities < right.protected_capabilities:
        strict.append("protected_capabilities")
    if information_refines(left, right) and left.admissible_models != right.admissible_models:
        strict.append("information")
    if left.satisfied_goals < right.satisfied_goals:
        strict.append("satisfied_goals")
    if left.verified_contributions < right.verified_contributions:
        strict.append("verified_contributions")
    if left.execution_level < right.execution_level:
        strict.append("execution_truth")
    return tuple(strict)


def compare_states(
    left: SystemState,
    right: SystemState,
    *,
    certificate: TransportCertificate | None = None,
) -> Comparison:
    pair = common_basis_states(left, right, certificate)
    if pair is None:
        return Comparison(left, right, False, False, (), False, "BASIS_TRANSPORT_REQUIRED")

    l, r = pair
    semantic_weak = _semantic_weak(l, r)
    semantic_strict = _semantic_strict_coordinates(l, r)
    semantic_equivalent = semantic_weak and _semantic_weak(r, l)

    # Burden is a strict-gain coordinate only inside semantic equivalence.
    # It does not veto a genuine semantic gain merely because that gain costs more.
    burden_strict = semantic_equivalent and r.burden < l.burden
    strict = semantic_strict + (("burden",) if burden_strict else ())

    non_regressive = semantic_weak or (
        semantic_equivalent and r.burden <= l.burden
    )
    equivalent = semantic_equivalent and r.burden == l.burden

    return Comparison(
        left,
        right,
        True,
        non_regressive,
        strict,
        equivalent,
        "OK" if non_regressive else "REGRESSION_OR_INCOMPARABLE_SEMANTIC_COORDINATE",
    )


def weak_improvement(
    left: SystemState,
    right: SystemState,
    *,
    certificate: TransportCertificate | None = None,
) -> bool:
    c = compare_states(left, right, certificate=certificate)
    return c.comparable and c.non_regressive


def strict_improvement(
    left: SystemState,
    right: SystemState,
    *,
    certificate: TransportCertificate | None = None,
) -> bool:
    c = compare_states(left, right, certificate=certificate)
    return c.comparable and c.non_regressive and bool(c.strict_coordinates)


def equivalent_state(
    left: SystemState,
    right: SystemState,
    *,
    certificate: TransportCertificate | None = None,
) -> bool:
    pair = common_basis_states(left, right, certificate)
    if pair is None:
        return False
    l, r = pair
    return _semantic_weak(l, r) and _semantic_weak(r, l) and l.burden == r.burden


def compare_in_frame(
    left: SystemState,
    right: SystemState,
    frame: ComparisonFrame,
) -> Comparison:
    """Compare two states after transport into one episode-wide basis."""
    l = frame.transport(left)
    r = frame.transport(right)
    if l is None or r is None:
        return Comparison(left, right, False, False, (), False, "COMPARISON_FRAME_INCOMPLETE")
    return compare_states(l, r)


def weak_improvement_in_frame(
    left: SystemState,
    right: SystemState,
    frame: ComparisonFrame,
) -> bool:
    cmp = compare_in_frame(left, right, frame)
    return cmp.comparable and cmp.non_regressive


def strict_improvement_in_frame(
    left: SystemState,
    right: SystemState,
    frame: ComparisonFrame,
) -> bool:
    cmp = compare_in_frame(left, right, frame)
    return cmp.comparable and cmp.non_regressive and bool(cmp.strict_coordinates)


def frame_chain_strict(
    states: Iterable[SystemState],
    frame: ComparisonFrame,
) -> bool:
    """Finite witness that every adjacent edge and the end-to-end edge are strict.

    Because every state is transported by the same frame into one preorder fiber,
    this checks the concrete condition needed for a multi-basis improvement chain.
    """
    xs = tuple(states)
    if len(xs) < 2:
        return False
    if not all(strict_improvement_in_frame(a, b, frame) for a, b in zip(xs, xs[1:])):
        return False
    return strict_improvement_in_frame(xs[0], xs[-1], frame)


@dataclass(frozen=True)
class StepReceipt:
    route_id: str
    execution_level: ExecutionLevel
    boundary_verified: bool
    obligations_terminal: bool
    evidence: Tuple[str, ...] = ()


@dataclass(frozen=True)
class StepDisposition:
    status: str
    comparison: Comparison


def classify_step(
    left: SystemState,
    right: SystemState,
    receipt: StepReceipt,
    *,
    certificate: TransportCertificate | None = None,
) -> StepDisposition:
    cmp = compare_states(left, right, certificate=certificate)
    if receipt.execution_level < ExecutionLevel.CONSUMED:
        return StepDisposition("OPEN_EXECUTION", cmp)
    if not receipt.boundary_verified:
        return StepDisposition("OPEN_BOUNDARY", cmp)
    if not receipt.obligations_terminal:
        return StepDisposition("OPEN_OBLIGATIONS", cmp)
    if not receipt.evidence:
        return StepDisposition("OPEN_EVIDENCE", cmp)
    if not cmp.comparable:
        return StepDisposition("OPEN_COMPARISON", cmp)
    if not cmp.non_regressive:
        return StepDisposition("REGRESSION", cmp)
    if cmp.strict_coordinates:
        return StepDisposition("STRICT_GAIN", cmp)
    if equivalent_state(left, right, certificate=certificate):
        return StepDisposition("NO_GAIN", cmp)
    return StepDisposition("INCOMPARABLE", cmp)


@dataclass(frozen=True)
class NoGainRecord:
    route_id: str
    basis_id: str
    semantic_class: str
    dependency_footprint: FrozenSet[str]
    evidence: Tuple[str, ...] = ()


def retry_licensed(
    record: NoGainRecord,
    *,
    current_basis_id: str,
    current_semantic_class: str,
    changed_coordinates: FrozenSet[str] = frozenset(),
    failure_signature_defeated: bool = False,
    new_interaction: bool = False,
) -> bool:
    if current_basis_id != record.basis_id:
        return True
    if current_semantic_class != record.semantic_class:
        return True
    return bool(
        set(record.dependency_footprint) & set(changed_coordinates)
        or failure_signature_defeated
        or new_interaction
    )


def cycle_no_gain(
    semantic_classes: Iterable[str],
    strict_gain_flags: Iterable[bool],
) -> bool:
    classes = tuple(semantic_classes)
    gains = tuple(strict_gain_flags)
    if len(classes) < 2 or len(gains) != len(classes) - 1:
        return False
    current = classes[-1]
    for i in range(len(classes) - 2, -1, -1):
        if classes[i] == current:
            return not any(gains[i:])
    return False


@dataclass(frozen=True)
class ClosureState:
    goal_gap_zero: bool
    live_frontier: FrozenSet[str]
    open_obligations: FrozenSet[str] = frozenset()
    blocked_obligations: FrozenSet[str] = frozenset()
    conflicts: FrozenSet[str] = frozenset()
    coverage_current: bool = False
    basis_current: bool = True
    protected_preserved: bool = True


def closure_disposition(state: ClosureState) -> str:
    if state.conflicts:
        return "CONFLICT"
    if state.blocked_obligations:
        return "BLOCKED"
    if state.open_obligations:
        return "OPEN"
    if not state.basis_current or not state.coverage_current:
        return "RETURN_REENTER"
    if not state.protected_preserved:
        return "REGRESSION"
    if state.live_frontier:
        return "CONTINUE"
    if not state.goal_gap_zero:
        return "OPEN"
    return "RELATIVE_CLOSE"


def finite_fixed_basis_execution_bound(
    quotient_state_count: int,
    route_count: int,
) -> int:
    """Upper bound when each state-route pair is tested at most once under a fixed basis."""
    if quotient_state_count < 1 or route_count < 0:
        raise ValueError("invalid finite basis cardinalities")
    return quotient_state_count * route_count
