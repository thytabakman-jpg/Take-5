"""Migration queue semantics as typed views over work objects, not five primitive stores."""
from dataclasses import dataclass
from enum import Enum

class WorkClass(str,Enum):
    BACKLOG="BACKLOG"
    DEBT="DEBT"
    ACTIVE="ACTIVE"
    SORT_LATER="SORT_LATER"
    TRANSFER="TRANSFER"

@dataclass(frozen=True)
class MigratedWork:
    work_id:str
    work_class:WorkClass
    active:bool
    authoritative:bool
    priority:int|None
    provenance:tuple[str,...]
    blocked:bool=False

def validate_work(w):
    if w.work_class in {WorkClass.BACKLOG,WorkClass.SORT_LATER,WorkClass.TRANSFER} and w.authoritative:
        return False
    if w.work_class==WorkClass.BACKLOG and w.active:
        return False
    return bool(w.work_id and w.provenance)

def queue_view(items,kind):
    return tuple(w for w in items if w.work_class==kind)

def activation_allowed(w,licensed):
    return validate_work(w) and licensed and not w.blocked
