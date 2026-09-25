"""6x6x6 run geometry: directed six-scope transitions crossed with six mode faces."""
from dataclasses import dataclass
from enum import Enum
from scope_ontology import Scope,required_handoff

class ModeFace(str,Enum):
    EXPAND="EXPAND"
    CONTRACT="CONTRACT"
    INWARD="INWARD"
    OUTWARD="OUTWARD"
    ISOLATE="ISOLATE"
    COUPLE="COUPLE"

@dataclass(frozen=True)
class Mode:
    breadth:str
    direction:str
    coupling:str

    def __post_init__(self):
        if self.breadth not in {"EXPAND","CONTRACT"}: raise ValueError("breadth")
        if self.direction not in {"INWARD","OUTWARD"}: raise ValueError("direction")
        if self.coupling not in {"ISOLATE","COUPLE"}: raise ValueError("coupling")

    def faces(self):
        return {ModeFace(self.breadth),ModeFace(self.direction),ModeFace(self.coupling)}

@dataclass(frozen=True)
class RunCoordinate:
    family:str
    source_scope:Scope
    target_scope:Scope
    mode:Mode

    @property
    def transition_kind(self):
        return required_handoff(self.source_scope,self.target_scope)

def scope_edges():
    return tuple((a,b) for a in Scope for b in Scope)

def face_cells():
    return tuple((a,b,f) for a in Scope for b in Scope for f in ModeFace)

def full_mode_cells():
    modes=tuple(Mode(b,d,c) for b in ("EXPAND","CONTRACT")
                         for d in ("INWARD","OUTWARD")
                         for c in ("ISOLATE","COUPLE"))
    return tuple((a,b,m) for a in Scope for b in Scope for m in modes)
