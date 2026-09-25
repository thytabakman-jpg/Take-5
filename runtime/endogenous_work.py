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
    return WorkItem(**{**work.__dict__,"status":WorkStatus.ACTIVE})

def generate_obligations(state,job=None,discover=None):
    if job is not None:
        return tuple(state.get("obligations",()))
    if discover is None:
        return ()
    return tuple(discover(state))

def select_work(obligations):
    eligible=tuple(o for o in obligations if o.material and o.licensed and o.reachable and o.status not in {WorkStatus.CLOSED,WorkStatus.BLOCKED})
    return WorkSelection(eligible,eligible if len(eligible)>1 else ())

def fresh_work(generated,discharged):
    done=set(discharged)
    return tuple(w for w in generated if w.work_id not in done and w.status!=WorkStatus.CLOSED)

def closure_status(generated,discharged,open_coordinates=(),blocked=False):
    if blocked:
        return WorkStatus.BLOCKED
    remaining=fresh_work(generated,discharged)
    if remaining:
        return WorkStatus.ACTIVE
    if open_coordinates:
        return WorkStatus.PAUSED_OPEN
    return WorkStatus.CLOSED
