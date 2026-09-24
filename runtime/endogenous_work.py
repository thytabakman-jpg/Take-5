"""Endogenous Work Generator: system-level work discovery and closure.
Improvement Core is a policy/controller inside this lifecycle, not the lifecycle itself.
"""
from dataclasses import dataclass
from enum import Enum

class EntryMode(str,Enum):
    JOB_CONDITIONED="JOB_CONDITIONED"
    ZERO_REQUEST_DISCOVERY="ZERO_REQUEST_DISCOVERY"

class WorkStatus(str,Enum):
    ACTIVE="ACTIVE"
    CLOSED="CLOSED"
    PAUSED_OPEN="PAUSED_OPEN"
    BLOCKED="BLOCKED"

@dataclass(frozen=True)
class WorkItem:
    work_id:str
    obligation:str
    material:bool=True
    licensed:bool=True
    reachable:bool=True

@dataclass(frozen=True)
class WorkSelection:
    selected:tuple[WorkItem,...]
    incomparable:tuple[WorkItem,...]

def generate_obligations(state,job=None,discover=None):
    if job is not None:
        return tuple(state.get("obligations",()))
    if discover is None:
        return ()
    return tuple(discover(state))

def select_work(obligations):
    eligible=tuple(o for o in obligations if o.material and o.licensed and o.reachable)
    # No arbitrary collapse: absent a dominance relation, preserve plurality as incomparable.
    return WorkSelection(eligible,eligible if len(eligible)>1 else ())

def fresh_work(generated,discharged):
    done=set(discharged)
    return tuple(w for w in generated if w.work_id not in done)

def closure_status(generated,discharged,open_coordinates=(),blocked=False):
    if blocked:
        return WorkStatus.BLOCKED
    remaining=fresh_work(generated,discharged)
    if remaining:
        return WorkStatus.ACTIVE
    if open_coordinates:
        return WorkStatus.PAUSED_OPEN
    return WorkStatus.CLOSED
