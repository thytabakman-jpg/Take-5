"""Endogenous typed work generator and queue-view semantics."""
from dataclasses import dataclass
from enum import Enum

class EntryMode(str,Enum):
    JOB_CONDITIONED="JOB_CONDITIONED"
    ZERO_REQUEST_DISCOVERY="ZERO_REQUEST_DISCOVERY"

class WorkStatus(str,Enum):
    CANDIDATE="CANDIDATE"
    ACTIVE="ACTIVE"
    CLOSED="CLOSED"
    PAUSED_OPEN="PAUSED_OPEN"
    BLOCKED="BLOCKED"

class WorkKind(str,Enum):
    CANDIDATE="CANDIDATE"
    DEBT="DEBT"
    ACTIVE_WORKSTREAM="ACTIVE_WORKSTREAM"
    UNRESOLVED_ROUTING="UNRESOLVED_ROUTING"
    TRANSFER="TRANSFER"

@dataclass(frozen=True)
class WorkItem:
    work_id:str
    obligation:str
    material:bool=True
    licensed:bool=True
    reachable:bool=True
    kind:WorkKind=WorkKind.CANDIDATE
    status:WorkStatus=WorkStatus.CANDIDATE
    provenance:tuple=()
    authority:tuple=()
    cost:float|None=None
    risk:float|None=None
    target:str|None=None
    relations:tuple=()

@dataclass(frozen=True)
class WorkSelection:
    selected:tuple[WorkItem,...]
    incomparable:tuple[WorkItem,...]

def activate(work:WorkItem,authority_token:str):
    if not work.licensed or authority_token not in set(work.authority):
        raise PermissionError("activation requires licensed authority")
    if not work.material or not work.reachable:
        raise PermissionError("activation requires material, reachable work")
    if work.status not in {WorkStatus.CANDIDATE, WorkStatus.ACTIVE}:
        raise PermissionError("activation cannot bypass blocked, paused, or closed state")
    return WorkItem(**{**work.__dict__,"status":WorkStatus.ACTIVE})

def generate_obligations(state,job=None,discover=None):
    if job is not None:
        return tuple(state.get("obligations",()))
    if discover is None:
        return ()
    return tuple(discover(state))

def select_work(obligations):
    eligible=tuple(o for o in obligations if o.material and o.licensed and o.reachable and o.status in {WorkStatus.CANDIDATE,WorkStatus.ACTIVE})
    return WorkSelection(eligible,eligible if len(eligible)>1 else ())

def fresh_work(generated,discharged):
    done=set(discharged)
    return tuple(w for w in generated if w.work_id not in done and w.status!=WorkStatus.CLOSED)

def closure_status(generated,discharged,open_coordinates=(),blocked=False):
    if blocked:
        return WorkStatus.BLOCKED
    remaining=fresh_work(generated,discharged)
    # A stored but non-runnable obligation prevents closure, yet is not ACTIVE.
    if any(w.status in {WorkStatus.CANDIDATE, WorkStatus.ACTIVE} for w in remaining):
        return WorkStatus.ACTIVE
    if any(w.status == WorkStatus.BLOCKED for w in remaining):
        return WorkStatus.BLOCKED
    if remaining or open_coordinates:
        return WorkStatus.PAUSED_OPEN
    return WorkStatus.CLOSED
