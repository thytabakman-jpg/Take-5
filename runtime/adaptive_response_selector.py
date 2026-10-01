"""Adaptive response selector derived from the ICC-128 select/update loop.

The selector treats user-visible format, identity, and exactness as hard
admissibility constraints. It then chooses the least extraneous admissible
response and carries rejection memory forward.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class ResponseCandidate:
    candidate_id: str
    artifact_id: str
    format_id: str
    exact: bool
    complete: bool
    unsupported_claims: int
    abstraction_drift: int
    extra_tokens: int
    affirmative_first: bool = True

@dataclass(frozen=True)
class ResponseState:
    requested_artifact_id: str
    requested_format_id: str
    rejected_candidate_ids: Tuple[str, ...] = ()
    rejected_format_ids: Tuple[str, ...] = ()

def admissible(c: ResponseCandidate, z: ResponseState) -> bool:
    return (
        c.artifact_id == z.requested_artifact_id
        and c.format_id == z.requested_format_id
        and c.exact
        and c.complete
        and c.unsupported_claims == 0
        and c.abstraction_drift == 0
        and c.affirmative_first
        and c.candidate_id not in z.rejected_candidate_ids
        and c.format_id not in z.rejected_format_ids
    )

def choose(candidates, state: ResponseState):
    live=tuple(c for c in candidates if admissible(c,state))
    if not live:
        return ()
    best=min(c.extra_tokens for c in live)
    return tuple(c for c in live if c.extra_tokens == best)

def update_rejection(state: ResponseState, *, candidate_id: str = "", format_id: str = "") -> ResponseState:
    rc=tuple(dict.fromkeys(state.rejected_candidate_ids + ((candidate_id,) if candidate_id else ())))
    rf=tuple(dict.fromkeys(state.rejected_format_ids + ((format_id,) if format_id else ())))
    return ResponseState(
        requested_artifact_id=state.requested_artifact_id,
        requested_format_id=state.requested_format_id,
        rejected_candidate_ids=rc,
        rejected_format_ids=rf,
    )
