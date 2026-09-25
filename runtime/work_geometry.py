"""Typed placement of Work in the canonical Scope x ModeFace controller lattice."""
from dataclasses import dataclass
from endogenous_work import WorkItem
from scope_mode_36 import Scope,ModeFace,CoverageCell

@dataclass(frozen=True)
class RoutedWork:
    work:WorkItem
    scope:Scope
    active_modes:frozenset[ModeFace]

    def coverage_cells(self):
        return tuple(CoverageCell(self.scope,m) for m in sorted(self.active_modes,key=lambda x:x.value))

def place_work(work,scope,active_modes):
    modes=frozenset(active_modes)
    if not modes:
        raise ValueError("work placement requires at least one controller mode face")
    return RoutedWork(work,Scope(scope),frozenset(ModeFace(x) for x in modes))
