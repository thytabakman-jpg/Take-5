"""Currentness Audit: resolve immutable identity before comparing admitted bases."""
from dataclasses import dataclass
from enum import Enum

class Currentness(str,Enum):
    CURRENT="CURRENT"; PATCH="PATCH"; REPLACE="REPLACE"; OPEN="OPEN"; SUPERSEDED="SUPERSEDED"

@dataclass(frozen=True)
class CurrentnessReceipt:
    component:str
    object_identity:str
    built_generation:str
    latest_generation:str
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
    identity_verified:bool=False

def assess(*,component,built_basis,latest_basis,object_identity="",built_generation="",
           latest_generation="",identity_verified=False,protected=(),delta=(),
           behavior_preserved=True,local_patch_available=True,evidence=(),obligations=(),
           dependents=(),reverified=False):
    delta=tuple(delta)
    identity_ready=bool(
        str(object_identity).strip()
        and str(built_generation).strip()
        and str(latest_generation).strip()
        and identity_verified
    )
    if not identity_ready:
        status=Currentness.OPEN
        action="RESOLVE_IMMUTABLE_IDENTITY"
    elif not delta:
        status=Currentness.CURRENT
        action="KEEP"
    elif behavior_preserved and local_patch_available:
        status=Currentness.PATCH
        action="PATCH_IN_PLACE"
    elif not behavior_preserved:
        status=Currentness.REPLACE
        action="REPLACE_MINIMAL_LOAD_BEARING_COMPONENT"
    else:
        status=Currentness.OPEN
        action="PRESERVE_AND_INVESTIGATE"
    return CurrentnessReceipt(
        component=component,
        object_identity=str(object_identity),
        built_generation=str(built_generation),
        latest_generation=str(latest_generation),
        built_basis=built_basis,
        latest_basis=latest_basis,
        protected=tuple(protected),
        delta=delta,
        status=status,
        action=action,
        evidence=tuple(evidence),
        obligations=tuple(obligations),
        dependents=tuple(dependents),
        reverified=reverified,
        identity_verified=bool(identity_verified),
    )

def audit_complete(receipts):
    rs=tuple(receipts)
    return bool(rs) and all(
        r.identity_verified
        and bool(r.object_identity)
        and bool(r.built_generation)
        and bool(r.latest_generation)
        and (
            r.status in {Currentness.CURRENT,Currentness.SUPERSEDED}
            or (r.status==Currentness.PATCH and r.reverified)
        )
        for r in rs
    )
