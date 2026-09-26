"""Configured program: What Is the Solution to My Problem?

Candidates may propose attacks/effects. They cannot self-establish execution,
effect, preservation, verification, or closure. Those facts must arrive through
separate evidence receipts.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple


@dataclass(frozen=True)
class Problem:
    observed: Tuple[str, ...]
    generators: Tuple[str, ...]
    required_effects: Tuple[str, ...]
    protected: Tuple[str, ...]
    constraints: Tuple[str, ...] = ()
    evidence: Tuple[str, ...] = ()


@dataclass(frozen=True)
class Candidate:
    id: str
    proposed_attacks: Tuple[str, ...] = ()
    proposed_effects: Tuple[str, ...] = ()
    proposed_preservations: Tuple[str, ...] = ()
    cost: float = 0.0


@dataclass(frozen=True)
class SolutionReceipt:
    candidate_id: str
    source: str
    execution_stage: str
    observed_attacks: Tuple[str, ...] = ()
    observed_effects: Tuple[str, ...] = ()
    observed_preservations: Tuple[str, ...] = ()
    observed_violations: Tuple[str, ...] = ()
    verification_status: str = "OPEN"
    closure_status: str = "OPEN"
    evidence: Tuple[str, ...] = ()


@dataclass(frozen=True)
class SolutionResult:
    status: str
    selected: Tuple[str, ...]
    rejected: Tuple[str, ...]
    residual: Tuple[str, ...]
    verification_required: Tuple[str, ...]


def _covers(required: Iterable[str], supplied: Iterable[str]) -> bool:
    return set(required) <= set(supplied)


def _receipt_valid_for(problem: Problem, candidate: Candidate, receipt: SolutionReceipt) -> bool:
    return (
        receipt.candidate_id == candidate.id
        and bool(receipt.source)
        and receipt.execution_stage == "CONSUMED"
        and _covers(problem.generators, receipt.observed_attacks)
        and _covers(problem.required_effects, receipt.observed_effects)
        and _covers(problem.protected, receipt.observed_preservations)
        and not receipt.observed_violations
        and receipt.verification_status == "PASS"
        and receipt.closure_status == "CLOSED"
        and bool(receipt.evidence)
    )


def _proposal_relevant(problem: Problem, candidate: Candidate) -> bool:
    return (
        _covers(problem.generators, candidate.proposed_attacks)
        and _covers(problem.required_effects, candidate.proposed_effects)
        and _covers(problem.protected, candidate.proposed_preservations)
    )


def _dominates(a: Candidate, b: Candidate) -> bool:
    no_worse = (
        set(b.proposed_attacks) <= set(a.proposed_attacks)
        and set(b.proposed_effects) <= set(a.proposed_effects)
        and set(b.proposed_preservations) <= set(a.proposed_preservations)
        and a.cost <= b.cost
    )
    strict = (
        set(b.proposed_attacks) < set(a.proposed_attacks)
        or set(b.proposed_effects) < set(a.proposed_effects)
        or set(b.proposed_preservations) < set(a.proposed_preservations)
        or a.cost < b.cost
    )
    return no_worse and strict


def solve(
    problem: Problem,
    candidates: Iterable[Candidate],
    receipts: Iterable[SolutionReceipt] = (),
) -> SolutionResult:
    candidates = tuple(candidates)
    receipts = tuple(receipts)

    if not problem.generators:
        return SolutionResult(
            status="OPEN",
            selected=(),
            rejected=tuple(c.id for c in candidates),
            residual=("DIAGNOSED_GENERATOR_MISSING",),
            verification_required=(),
        )

    relevant = tuple(c for c in candidates if _proposal_relevant(problem, c))
    rejected = tuple(c.id for c in candidates if c not in relevant)

    if not relevant:
        return SolutionResult(
            status="OPEN",
            selected=(),
            rejected=rejected,
            residual=tuple(sorted(set(problem.generators) | set(problem.required_effects))),
            verification_required=(),
        )

    frontier = tuple(
        c for c in relevant
        if not any(_dominates(other, c) for other in relevant if other is not c)
    )

    valid_receipts = {
        c.id: tuple(r for r in receipts if _receipt_valid_for(problem, c, r))
        for c in frontier
    }
    solved = tuple(c for c in frontier if valid_receipts[c.id])

    if solved:
        return SolutionResult(
            status="SOLVED",
            selected=tuple(sorted(c.id for c in solved)),
            rejected=rejected,
            residual=(),
            verification_required=(),
        )

    return SolutionResult(
        status="VERIFY_REQUIRED",
        selected=tuple(sorted(c.id for c in frontier)),
        rejected=rejected,
        residual=("EXTERNAL_EXECUTION_EFFECT_PRESERVATION_VERIFICATION_CLOSURE_RECEIPT_REQUIRED",),
        verification_required=tuple(sorted(c.id for c in frontier)),
    )
