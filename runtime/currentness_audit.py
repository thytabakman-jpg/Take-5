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

def _nonempty_identity(value):
    return isinstance(value,str) and bool(value.strip())

def assess(*,component,built_basis,latest_basis,object_identity="",built_generation="",
           latest_generation="",identity_verified=False,protected=(),delta=(),
           behavior_preserved=True,local_patch_available=True,evidence=(),obligations=(),
           dependents=(),reverified=False):
    delta=tuple(delta)
    identity_ready=bool(
        _nonempty_identity(object_identity)
        and _nonempty_identity(built_generation)
        and _nonempty_identity(latest_generation)
        and identity_verified is True
    )
    if not identity_ready:
        status=Currentness.OPEN
        action="RESOLVE_IMMUTABLE_IDENTITY"
    elif built_generation != latest_generation and not delta:
        # The caller cannot prove "no change" when exact generations disagree.
        # Preserve OPEN rather than letting an omitted delta manufacture CURRENT.
        status=Currentness.OPEN
        action="RECONCILE_GENERATION_DELTA"
    elif built_basis != latest_basis and not delta:
        status=Currentness.OPEN
        action="RECONCILE_BASIS_DELTA"
    elif not delta:
        status=Currentness.CURRENT
        action="KEEP"
    elif behavior_preserved is True and local_patch_available is True:
        status=Currentness.PATCH
        action="PATCH_IN_PLACE"
    elif behavior_preserved is False:
        status=Currentness.REPLACE
        action="REPLACE_MINIMAL_LOAD_BEARING_COMPONENT"
    else:
        status=Currentness.OPEN
        action="PRESERVE_AND_INVESTIGATE"
    return CurrentnessReceipt(
        component=component,
        object_identity=object_identity if _nonempty_identity(object_identity) else "",
        built_generation=built_generation if _nonempty_identity(built_generation) else "",
        latest_generation=latest_generation if _nonempty_identity(latest_generation) else "",
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
        identity_verified=identity_verified is True,
    )

def audit_complete(receipts):
    rs=tuple(receipts)
    return bool(rs) and all(
        r.identity_verified is True
        and _nonempty_identity(r.object_identity)
        and _nonempty_identity(r.built_generation)
        and _nonempty_identity(r.latest_generation)
        and (
            (
                r.status==Currentness.CURRENT
                and r.built_generation==r.latest_generation
                and r.built_basis==r.latest_basis
                and not r.delta
            )
            or r.status==Currentness.SUPERSEDED
            or (r.status==Currentness.PATCH and r.reverified is True)
        )
        for r in rs
    )
