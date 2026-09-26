from dataclasses import dataclass
from typing import Any,Mapping

@dataclass(frozen=True)
class Preservation:
    capability_id:str
    status:str
    missing:tuple[str,...]

REQUIRED=("identity","semantics","reachability","selection","execution","effect","consumer","recovery")

def capability_preservation(capability_id:str,witness:Mapping[str,Any])->Preservation:
    missing=tuple(k for k in REQUIRED if not witness.get(k))
    return Preservation(capability_id,"PRESERVED" if not missing else "OPEN",missing)

@dataclass(frozen=True)
class KernelChange:
    consequential:bool
    observed:bool
    typed:bool
    authorized:bool
    transition:bool
    verified:bool
    open_preserved:bool

def legal_change(c:KernelChange)->bool:
    if not c.consequential:
        return True
    return all((c.observed,c.typed,c.authorized,c.transition,c.verified,c.open_preserved))

def reentry_required(*deltas:bool)->bool:
    return any(deltas)
