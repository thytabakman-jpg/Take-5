"""Currentness Audit: compare built components to latest admitted basis."""
from dataclasses import dataclass
from enum import Enum

class Currentness(str,Enum):
    CURRENT="CURRENT"; PATCH="PATCH"; REPLACE="REPLACE"; OPEN="OPEN"; SUPERSEDED="SUPERSEDED"

@dataclass(frozen=True)
class CurrentnessReceipt:
    component:str
    built_basis:str
    latest_basis:str
    protected:tuple[str,...]
    delta:tuple[str,...]
    status:Currentness
    action:str
    evidence:tuple[str,...]=()
    obligations:tuple[str,...]=()
    dependents:tuple[str,...]=()
    reverified:bool=False

def assess(*,component,built_basis,latest_basis,protected=(),delta=(),behavior_preserved=True,
           local_patch_available=True,evidence=(),obligations=(),dependents=(),reverified=False):
    delta=tuple(delta)
    if not delta:
        status=Currentness.CURRENT; action="KEEP"
    elif behavior_preserved and local_patch_available:
        status=Currentness.PATCH; action="PATCH_IN_PLACE"
    elif not behavior_preserved:
        status=Currentness.REPLACE; action="REPLACE_MINIMAL_LOAD_BEARING_COMPONENT"
    else:
        status=Currentness.OPEN; action="PRESERVE_AND_INVESTIGATE"
    return CurrentnessReceipt(component,built_basis,latest_basis,tuple(protected),delta,status,action,tuple(evidence),tuple(obligations),tuple(dependents),reverified)

def audit_complete(receipts):
    rs=tuple(receipts)
    return bool(rs) and all((r.status in {Currentness.CURRENT,Currentness.SUPERSEDED}) or (r.status==Currentness.PATCH and r.reverified) for r in rs)
