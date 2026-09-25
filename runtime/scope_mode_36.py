"""Canonical 36-cell ImproveCore controller coverage lattice: Scope x ModeFace."""
from dataclasses import dataclass
from scope_ontology import Scope
from run_geometry import ModeFace,Mode

DISPOSITIONS={"GENERATED_AND_DISPOSITIONED","NOT_APPLICABLE","BLOCKED","OPEN","DEFERRED_NONRESULTSENSITIVE"}

@dataclass(frozen=True)
class CoverageCell:
    scope:Scope
    face:ModeFace
    disposition:str
    reason:str=""

    def __post_init__(self):
        if self.disposition not in DISPOSITIONS:
            raise ValueError("invalid disposition")
        if self.disposition!="GENERATED_AND_DISPOSITIONED" and not self.reason:
            raise ValueError("non-generated disposition requires reason")

def cells36():
    return tuple((s,f) for s in Scope for f in ModeFace)

def active_cells(scope:Scope,mode:Mode):
    return tuple((scope,f) for f in mode.faces())

def closure_legal(applicable,ledger):
    for cell in applicable:
        rec=ledger.get(cell)
        if rec is None:
            return False
        if rec.disposition in {"OPEN","BLOCKED"}:
            return False
    return True
