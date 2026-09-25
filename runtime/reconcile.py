"""Reconcile admitted results into coherent current state.

Admission and reconciliation are distinct: admission licenses a result to enter;
reconciliation determines its joint consequences with already admitted state.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class ReconcileResult:
    state:object
    conflicts:tuple=()
    subsumptions:tuple=()
    revisions:tuple=()
    new_relations:tuple=()
    open_coordinates:tuple=()

def reconcile(state, admitted_results, resolver):
    return resolver(state, tuple(admitted_results))
