"""Concurrency preflight for ImprovementCore workstreams.

This module is intentionally non-authoritative. It does not select the current
ImprovementCore controller and does not promote architecture. It answers one
narrow question before a repository-mutating ImproveCore episode starts:

Can this proposed workstream proceed without invalidating or overwriting an
already-active workstream's declared dependency footprint?

Conflict relation for proposed workstream i against active workstream j:

    Conf(i,j) iff
      W_i ∩ (R_j ∪ W_j) != ∅
      or
      W_j ∩ (R_i ∪ W_i) != ∅

where R is the declared read set and W is the intended write set.

The relation is symmetric at the footprint level. Unknown registry completeness
fails closed because an undisclosed active writer cannot be proven disjoint.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

ACTIVE_STATUSES={
    "ACTIVE","RUNNING","CONTINUE","ACTIVE_RECONCILIATION","MERGE_REQUIRED",
    "OPEN","IN_PROGRESS"
}

@dataclass(frozen=True)
class WorkstreamClaim:
    workstream_id:str
    base_commit:str
    read_set:frozenset[str]
    write_set:frozenset[str]
    status:str="ACTIVE"

@dataclass(frozen=True)
class PeerConflict:
    peer_id:str
    proposed_writes_peer_reads:frozenset[str]
    write_write:frozenset[str]
    peer_writes_proposed_reads:frozenset[str]

    @property
    def paths(self)->frozenset[str]:
        return (
            self.proposed_writes_peer_reads
            | self.write_write
            | self.peer_writes_proposed_reads
        )

@dataclass(frozen=True)
class ConcurrencyDecision:
    disposition:str
    conflicts:tuple[PeerConflict,...]
    blocker:str|None=None

    @property
    def can_start(self)->bool:
        return self.disposition=="ALLOW"

def _active(claim:WorkstreamClaim)->bool:
    return claim.status.upper() in ACTIVE_STATUSES

def compare_claims(proposed:WorkstreamClaim, peer:WorkstreamClaim)->PeerConflict|None:
    if not _active(peer):
        return None
    wi=set(proposed.write_set)
    ri=set(proposed.read_set)
    wj=set(peer.write_set)
    rj=set(peer.read_set)

    a=frozenset(wi & rj)
    b=frozenset(wi & wj)
    c=frozenset(wj & ri)
    if not (a or b or c):
        return None
    return PeerConflict(peer.workstream_id,a,b,c)

def preflight(
    proposed:WorkstreamClaim,
    peers:Iterable[WorkstreamClaim],
    *,
    registry_complete:bool,
    current_base_commit:str|None=None,
)->ConcurrencyDecision:
    """Return a fail-closed launch decision.

    BASE_STALE blocks a workstream whose frozen base no longer equals the caller's
    current base snapshot. ACTIVE_FOOTPRINT_CONFLICT blocks any symmetric
    read/write or write/write collision. REGISTRY_INCOMPLETE blocks when the
    caller cannot establish that all active workstreams were considered.
    """
    if not registry_complete:
        return ConcurrencyDecision("BLOCK",(),"REGISTRY_INCOMPLETE")

    if current_base_commit is not None and proposed.base_commit!=current_base_commit:
        return ConcurrencyDecision("BLOCK",(),"BASE_STALE")

    conflicts=tuple(
        c for c in (compare_claims(proposed,p) for p in peers)
        if c is not None
    )
    if conflicts:
        return ConcurrencyDecision("RECONCILE_REQUIRED",conflicts,"ACTIVE_FOOTPRINT_CONFLICT")

    return ConcurrencyDecision("ALLOW",())
