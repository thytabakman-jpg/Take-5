"""Configured program: What Is the Solution to My Problem?

The program evaluates candidate interventions against a diagnosed problem object.
It preserves OPEN when no candidate attacks the diagnosed generator, closes all
required effects, preserves protected behavior, and has executable/verification
evidence.
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
    attacks: Tuple[str, ...] = ()
    resolves: Tuple[str, ...] = ()
    preserves: Tuple[str, ...] = ()
    violates: Tuple[str, ...] = ()
    executable: bool = False
    verified: bool = False
    cost: float = 0.0


@dataclass(frozen=True)
class SolutionResult:
    status: str
    selected: Tuple[str, ...]
    rejected: Tuple[str, ...]
    residual: Tuple[str, ...]
    verification_required: Tuple[str, ...]


def _covers(required: Iterable[str], supplied: Iterable[str]) -> bool:
    return set(required) <= set(supplied)


def admissible(problem: Problem, candidate: Candidate) -> bool:
    return (
        _covers(problem.generators, candidate.attacks)
        and _covers(problem.required_effects, candidate.resolves)
        and _covers(problem.protected, candidate.preserves)
        and not candidate.violates
        and candidate.executable
    )


def _dominates(a: Candidate, b: Candidate) -> bool:
    no_worse = (
        set(b.attacks) <= set(a.attacks)
        and set(b.resolves) <= set(a.resolves)
        and set(b.preserves) <= set(a.preserves)
        and a.cost <= b.cost
    )
    strict = (
        set(b.attacks) < set(a.attacks)
        or set(b.resolves) < set(a.resolves)
        or set(b.preserves) < set(a.preserves)
        or a.cost < b.cost
    )
    return no_worse and strict


def solve(problem: Problem, candidates: Iterable[Candidate]) -> SolutionResult:
    candidates = tuple(candidates)

    if not problem.generators:
        return SolutionResult(
            status="OPEN",
            selected=(),
            rejected=tuple(c.id for c in candidates),
            residual=("DIAGNOSED_GENERATOR_MISSING",),
            verification_required=(),
        )

    admitted = tuple(c for c in candidates if admissible(problem, c))
    rejected = tuple(c.id for c in candidates if c not in admitted)

    if not admitted:
        return SolutionResult(
            status="OPEN",
            selected=(),
            rejected=rejected,
            residual=tuple(sorted(set(problem.generators) | set(problem.required_effects))),
            verification_required=(),
        )

    frontier = tuple(
        c for c in admitted
        if not any(_dominates(other, c) for other in admitted if other is not c)
    )

    verified = tuple(c for c in frontier if c.verified)
    if verified:
        return SolutionResult(
            status="SOLVED",
            selected=tuple(sorted(c.id for c in verified)),
            rejected=rejected,
            residual=(),
            verification_required=(),
        )

    return SolutionResult(
        status="VERIFY_REQUIRED",
        selected=tuple(sorted(c.id for c in frontier)),
        rejected=rejected,
        residual=(),
        verification_required=tuple(sorted(c.id for c in frontier)),
    )
