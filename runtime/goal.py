"""Native GOAL semantic core.

GOAL recovers the governing goal from candidate control evidence.  It keeps the
goal object G=<X,T,I,Sigma> distinct from protected constraints and fails OPEN
when the admitted evidence does not determine one governing goal.

This module does not manufacture candidate goals from arbitrary prose.  Candidate
generation/evidence extraction is a host semantic responsibility and remains an
explicit environment input.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


TERMINAL={"CLOSED_RELATIVE","OPEN","CONFLICT"}


@dataclass(frozen=True)
class GoalObject:
    """The recovered governing goal G=<X,T,I,Sigma>."""

    X:str
    T:str
    I:str
    Sigma:str


@dataclass(frozen=True)
class GoalCandidate:
    candidate_id:str
    goal:GoalObject
    constraints:tuple[str,...]=()
    evidence:tuple[str,...]=()
    grounded:bool=False
    authority_typed:bool=False
    determinate_enough:bool=False


@dataclass(frozen=True)
class GoalRecoveryResult:
    status:str
    active_goal:GoalObject|None
    active_candidate_ids:tuple[str,...]
    constraint_sets:tuple[tuple[str,...],...]
    admitted_candidate_ids:tuple[str,...]
    rejected_candidate_ids:tuple[str,...]
    blocker:str|None
    evidence:tuple[str,...]


def _candidate_signature(candidate:GoalCandidate)->tuple:
    return (
        candidate.goal,
        tuple(candidate.constraints),
        tuple(candidate.evidence),
        bool(candidate.grounded),
        bool(candidate.authority_typed),
        bool(candidate.determinate_enough),
    )


def _admissible(candidate:GoalCandidate)->bool:
    return bool(
        candidate.candidate_id
        and candidate.evidence
        and candidate.grounded
        and candidate.authority_typed
        and candidate.determinate_enough
        and candidate.goal.X
        and candidate.goal.T
        and candidate.goal.I
        and candidate.goal.Sigma
    )


def recover_goal(candidates:Iterable[GoalCandidate])->GoalRecoveryResult:
    """Recover one governing goal or preserve typed non-closure.

    Admission corresponds to the current Goal-Math predicate:
      Grounded(g,E) and AuthorityTyped(g) and DeterminateEnough_J(g).

    Distinct admissible GoalObject values are never silently ranked.  Multiple
    evidence-bearing candidates may support the same GoalObject; their constraint
    sets and evidence remain separately preserved.
    """
    rows=tuple(candidates)
    seen={}
    for candidate in rows:
        if not isinstance(candidate,GoalCandidate):
            raise TypeError("GOAL_CANDIDATE_REQUIRED")
        prior=seen.get(candidate.candidate_id)
        if prior is not None and _candidate_signature(prior)!=_candidate_signature(candidate):
            return GoalRecoveryResult(
                "CONFLICT",None,(),(),(),(),
                f"GOAL_CANDIDATE_ID_CONFLICT:{candidate.candidate_id}",(),
            )
        seen[candidate.candidate_id]=candidate

    unique=tuple(seen.values())
    admitted=tuple(c for c in unique if _admissible(c))
    rejected=tuple(c for c in unique if not _admissible(c))

    if not admitted:
        return GoalRecoveryResult(
            "OPEN",None,(),(),
            (),tuple(c.candidate_id for c in rejected),
            "NO_ADMISSIBLE_GOVERNING_GOAL",(),
        )

    by_goal={}
    for candidate in admitted:
        by_goal.setdefault(candidate.goal,[]).append(candidate)

    if len(by_goal)>1:
        return GoalRecoveryResult(
            "OPEN",None,(),(),
            tuple(c.candidate_id for c in admitted),
            tuple(c.candidate_id for c in rejected),
            "PLURAL_GOVERNING_GOALS",
            tuple(dict.fromkeys(
                ev for c in admitted for ev in c.evidence
            )),
        )

    goal, supporters=next(iter(by_goal.items()))
    return GoalRecoveryResult(
        "CLOSED_RELATIVE",
        goal,
        tuple(c.candidate_id for c in supporters),
        tuple(tuple(c.constraints) for c in supporters),
        tuple(c.candidate_id for c in admitted),
        tuple(c.candidate_id for c in rejected),
        None,
        tuple(dict.fromkeys(ev for c in supporters for ev in c.evidence)),
    )
