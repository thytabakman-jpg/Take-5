"""Generic Tool Run Closure runtime.

This realizes the current TRC orchestration contract without owning domain-specific
harvesting or mutation semantics. Callers provide the harvest/disposition/realize/
verify/consume functions; this module guarantees recursive consequence closure,
exact consequence identity, induced-consequence reharvest, typed terminal
dispositions, and a closure certificate.

Global harvest completeness is intentionally not claimed.
"""
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Iterable

# I. Consequence and certificate contracts.
class Disposition(str, Enum):
    REALIZE = "REALIZE"
    CERTIFIED_NO_EFFECT = "CERTIFIED_NO_EFFECT"
    OPEN = "OPEN"
    BLOCKED = "BLOCKED"
    PENDING_AUTHORIZATION = "PENDING_AUTHORIZATION"

class ConsumerState(str, Enum):
    CONSUMED = "CONSUMED"
    CERTIFIED_NO_EFFECT = "CERTIFIED_NO_EFFECT"
    OPEN = "OPEN"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"

@dataclass(frozen=True)
class Consequence:
    referent:str
    effect_class:str
    target_state:str
    authority_scope:str
    source_version:str
    protected_class:str
    payload:Any=None

    @property
    def cid(self):
        return (
            self.referent,
            self.effect_class,
            self.target_state,
            self.authority_scope,
            self.source_version,
            self.protected_class,
        )

@dataclass(frozen=True)
class StageResult:
    state:Any
    status:str="OK"
    induced:tuple[Consequence,...]=()
    evidence:tuple[str,...]=()
    resume_condition:str|None=None

@dataclass(frozen=True)
class ConsequenceRecord:
    cid:tuple
    disposition:str
    realization_state:str
    verification_state:str
    consumer_state:str
    evidence:tuple[str,...]=()
    resume_condition:str|None=None

@dataclass(frozen=True)
class SubsumptionRecord:
    cid:tuple
    witness:str
    basis:str
    invalidation_trigger:str

@dataclass(frozen=True)
class ClosureCertificate:
    status:str
    harvest_count:int
    accounted_count:int
    settled_count:int
    records:tuple[ConsequenceRecord,...]
    duplicate_subsumptions:tuple[SubsumptionRecord,...]
    open_coordinates:tuple[str,...]
    blocker_coordinates:tuple[str,...]
    pending_coordinates:tuple[str,...]
    harvest_basis:str
    harvest_complete:bool=False

@dataclass(frozen=True)
class ToolRunClosureResult:
    state:Any
    certificate:ClosureCertificate

# II. Stage and queue utilities.
def _coordinate(cid):
    return ":".join(map(str,cid))


def _stage(value, fallback_state):
    if isinstance(value, StageResult):
        return value
    if value is None:
        return StageResult(fallback_state)
    return StageResult(value)

def _enqueue(queue, items):
    for item in items or ():
        if not isinstance(item, Consequence):
            raise TypeError("induced consequences must be Consequence objects")
        queue.append(item)

# III. Certificate assembly (relative to the supplied harvest basis).
# Pending review: a CLOSED certificate and harvest_complete=False are distinct
# coordinates; consumer contracts must not treat relative closure as global harvest.
# Pending review: CERTIFIED_NO_EFFECT currently records no separate witness;
# evidence-bearing disposition design requires callback-consumer comparison.
def _closure_certificate(initial,records,subsumptions,open_coords,blocked_coords,pending_coords,harvest_basis,harvest_complete):
    accounted=len(records)
    settled=sum(
        r.consumer_state in {
            ConsumerState.CONSUMED.value,
            ConsumerState.CERTIFIED_NO_EFFECT.value,
        }
        for r in records
    )

    if blocked_coords:
        status="BLOCKED"
    elif open_coords or pending_coords:
        status="OPEN"
    else:
        status="CLOSED"

    return ClosureCertificate(
        status=status,
        harvest_count=len(initial),
        accounted_count=accounted,
        settled_count=settled,
        records=tuple(records),
        duplicate_subsumptions=tuple(subsumptions),
        open_coordinates=tuple(dict.fromkeys(open_coords)),
        blocker_coordinates=tuple(dict.fromkeys(blocked_coords)),
        pending_coordinates=tuple(dict.fromkeys(pending_coords)),
        harvest_basis=harvest_basis,
        harvest_complete=harvest_complete is True,
    )


# IV. Recursive consequence realization, verification and consumption.
# Domain-specific discovery and mutation remain with caller-provided handlers.
def run_tool_run_closure(
    *,
    tool_result:Any,
    pre_state:Any,
    post_state:Any,
    harvest_fn:Callable[[Any,Any,Any],Iterable[Consequence]],
    disposition_fn:Callable[[Consequence,Any],Disposition|str],
    realize_fn:Callable[[Consequence,Any],StageResult|Any],
    verify_fn:Callable[[Consequence,Any],StageResult|Any],
    consume_fn:Callable[[Consequence,Any],StageResult|Any],
    harvest_basis:str="DECLARED",
    harvest_complete:bool=False,
    max_consequences:int=1024,
)->ToolRunClosureResult:
    """Close all harvested and induced consequences relative to supplied handlers."""
    state=post_state
    initial=tuple(harvest_fn(tool_result,pre_state,post_state))
    queue=deque(initial)
    seen=set()
    records=[]
    subsumptions=[]
    open_coords=[]
    blocked_coords=[]
    pending_coords=[]
    steps=0

    while queue:
        steps+=1
        if steps>max_consequences:
            open_coords.append("TRC:MAX_CONSEQUENCES")
            # Preserve the identities of the unprocessed obligations so the
            # resource stop does not erase the remaining consequence frontier.
            for remaining in queue:
                if not isinstance(remaining,Consequence):
                    raise TypeError("harvest_fn must return Consequence objects")
                if remaining.cid not in seen:
                    open_coords.append(_coordinate(remaining.cid))
            break

        q=queue.popleft()
        if not isinstance(q,Consequence):
            raise TypeError("harvest_fn must return Consequence objects")

        cid=q.cid
        if cid in seen:
            subsumptions.append(SubsumptionRecord(
                cid=cid,
                witness="EXACT_CID_EQUIVALENCE",
                basis=harvest_basis,
                invalidation_trigger="ANY_CID_COORDINATE_CHANGES",
            ))
            continue
        seen.add(cid)

        raw_disp=disposition_fn(q,state)
        disp=raw_disp.value if isinstance(raw_disp,Disposition) else str(raw_disp)
        evidence=[]

        if disp==Disposition.CERTIFIED_NO_EFFECT.value:
            records.append(ConsequenceRecord(
                cid,disp,"NOT_REQUIRED","NOT_REQUIRED",
                ConsumerState.CERTIFIED_NO_EFFECT.value,
            ))
            continue

        if disp==Disposition.OPEN.value:
            key=_coordinate(cid)
            open_coords.append(key)
            records.append(ConsequenceRecord(
                cid,disp,"NOT_STARTED","OPEN",ConsumerState.OPEN.value,
            ))
            continue

        if disp==Disposition.BLOCKED.value:
            key=_coordinate(cid)
            blocked_coords.append(key)
            records.append(ConsequenceRecord(
                cid,disp,"NOT_STARTED","BLOCKED",ConsumerState.BLOCKED.value,
            ))
            continue

        if disp==Disposition.PENDING_AUTHORIZATION.value:
            key=_coordinate(cid)
            pending_coords.append(key)
            records.append(ConsequenceRecord(
                cid,disp,"NOT_STARTED","PENDING_AUTHORIZATION",ConsumerState.OPEN.value,
                resume_condition="AUTHORITY_GRANTED",
            ))
            continue

        if disp!=Disposition.REALIZE.value:
            raise ValueError(f"unsupported consequence disposition: {disp}")

        realized=_stage(realize_fn(q,state),state)
        state=realized.state
        evidence.extend(realized.evidence)
        _enqueue(queue,realized.induced)
        # Preserve existing explicit realization successes; other dispositions
        # cannot license verification or consumption.
        if realized.status not in {"OK","REALIZED","COMPLETED_UNVERIFIED"}:
            target=blocked_coords if realized.status=="BLOCKED" else open_coords
            key=_coordinate(cid)
            target.append(key)
            records.append(ConsequenceRecord(
                cid,disp,realized.status,"NOT_RUN",
                ConsumerState.BLOCKED.value if realized.status=="BLOCKED" else ConsumerState.OPEN.value,
                tuple(evidence),realized.resume_condition or f"REALIZATION_NOT_CERTIFIED:{realized.status}",
            ))
            continue

        verified=_stage(verify_fn(q,state),state)
        state=verified.state
        evidence.extend(verified.evidence)
        _enqueue(queue,verified.induced)
        # Only an actual VERIFIED receipt can authorize consumption. An
        # implicit OK, FAILED or arbitrary string was never proof of a check.
        if verified.status!="VERIFIED":
            verify_status=(verified.status if verified.status in {"OPEN","BLOCKED"} else "OPEN")
            target=open_coords if verify_status=="OPEN" else blocked_coords
            key=_coordinate(cid)
            target.append(key)
            records.append(ConsequenceRecord(
                cid,disp,realized.status,verified.status,
                ConsumerState.OPEN.value if verify_status=="OPEN" else ConsumerState.BLOCKED.value,
                tuple(evidence),verified.resume_condition or f"VERIFICATION_NOT_CERTIFIED:{verified.status}",
            ))
            continue

        consumed=_stage(consume_fn(q,state),state)
        state=consumed.state
        evidence.extend(consumed.evidence)
        _enqueue(queue,consumed.induced)
        consumer=consumed.status
        if consumer not in {
            ConsumerState.CONSUMED.value,
            ConsumerState.CERTIFIED_NO_EFFECT.value,
            ConsumerState.OPEN.value,
            ConsumerState.BLOCKED.value,
        }:
            consumer=ConsumerState.UNKNOWN.value

        key=_coordinate(cid)
        if consumer==ConsumerState.OPEN.value or consumer==ConsumerState.UNKNOWN.value:
            open_coords.append(key)
        elif consumer==ConsumerState.BLOCKED.value:
            blocked_coords.append(key)

        records.append(ConsequenceRecord(
            cid,disp,realized.status,verified.status,consumer,
            tuple(evidence),consumed.resume_condition,
        ))

    certificate=_closure_certificate(initial,records,subsumptions,open_coords,blocked_coords,pending_coords,harvest_basis,harvest_complete)
    return ToolRunClosureResult(state,certificate)
