"""K-F1 candidate legality membrane for the factored research foundation."""
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Attribution:
    behavior:str
    owner_before:str
    owner_after:str
    witness:str

@dataclass(frozen=True)
class RunPacket:
    referent:str
    protected_job:str
    family:str
    source_scope:str
    target_scope:str
    transition_kind:str
    breadth:str
    direction:str
    coupling:str
    provenance:str
    authority:str
    open_state:str="CLEAR"
    attribution:Optional[Attribution]=None

@dataclass(frozen=True)
class KernelVerdict:
    legal:bool
    reasons:tuple[str,...]

VALID_SCOPES={"SYSTEM","SUBSYSTEM","COMPONENT","INTERFACE","BOUNDARY_DECOMPOSITION","CROSS_LAYER"}
VALID_TRANSITIONS={"SELF","PROJECT","LIFT","RELATE","REDECOMPOSE","TRANSPORT"}
VALID_BREADTH={"EXPAND","CONTRACT"}
VALID_DIRECTION={"INWARD","OUTWARD"}
VALID_COUPLING={"ISOLATE","COUPLE"}
VALID_OPEN={"CLEAR","OPEN","BLOCKED","CONFLICT","INCOMPARABLE"}

def admit_run(p:RunPacket, reduction_or_transfer:bool=False)->KernelVerdict:
    reasons=[]
    if not p.referent or not p.protected_job: reasons.append("IDENTITY_MISSING")
    if p.source_scope not in VALID_SCOPES or p.target_scope not in VALID_SCOPES: reasons.append("SCOPE_INVALID")
    if p.transition_kind not in VALID_TRANSITIONS: reasons.append("TRANSITION_INVALID")
    if p.breadth not in VALID_BREADTH or p.direction not in VALID_DIRECTION or p.coupling not in VALID_COUPLING: reasons.append("MODE_INVALID")
    if not p.provenance: reasons.append("PROVENANCE_MISSING")
    if not p.authority: reasons.append("AUTHORITY_MISSING")
    if p.open_state not in VALID_OPEN: reasons.append("OPEN_STATE_INVALID")
    if reduction_or_transfer and p.attribution is None: reasons.append("ATTRIBUTION_REQUIRED")
    return KernelVerdict(not reasons,tuple(reasons))

def reentry_required(*,protected_delta=False,view_delta=False,candidate_delta=False,scope_delta=False,mode_delta=False,basis_delta=False,authority_delta=False,evidence_delta=False):
    return any((protected_delta,view_delta,candidate_delta,scope_delta,mode_delta,basis_delta,authority_delta,evidence_delta))
