"""ImprovementCore basis-relative learning memory.

Preserves no-gain, rejected, failed and other route outcomes relative to the
basis and dependency footprint that produced them. Unchanged failed/no-gain
routes remain blocked until a result-sensitive dependency coordinate changes.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Any

VALID_DISPOSITIONS={"GAIN","NO_GAIN","REJECTED","FAILED","OPEN","BLOCKED","CONFLICT"}

@dataclass(frozen=True)
class RouteEvidence:
    route_id:str
    basis_id:str
    disposition:str
    dependency_footprint:frozenset[str]
    evidence:dict[str,Any]

@dataclass
class LearningMemory:
    records:list[RouteEvidence]=field(default_factory=list)

    def record(self,route_id:str,basis_id:str,disposition:str,
               dependency_footprint:set[str]|frozenset[str],
               evidence:dict[str,Any]|None=None)->None:
        if disposition not in VALID_DISPOSITIONS:
            raise ValueError("IC_LEARNING_INVALID_DISPOSITION")
        self.records.append(RouteEvidence(
            route_id=route_id,
            basis_id=basis_id,
            disposition=disposition,
            dependency_footprint=frozenset(dependency_footprint),
            evidence=evidence or {},
        ))

    def unchanged_rerun_blocked(self,route_id:str,basis_id:str,
                                changed_coordinates:set[str]|None=None)->bool:
        changed=set(changed_coordinates or set())
        prior=[r for r in self.records if r.route_id==route_id and r.basis_id==basis_id]
        if not prior:
            return False
        last=prior[-1]
        if last.disposition not in {"NO_GAIN","REJECTED","FAILED"}:
            return False
        if changed & set(last.dependency_footprint):
            return False
        return True

    def invalidated_routes(self,changed_coordinates:set[str])->set[str]:
        changed=set(changed_coordinates)
        return {
            r.route_id for r in self.records
            if changed & set(r.dependency_footprint)
        }

    def summary(self)->list[dict[str,Any]]:
        return [asdict(r) for r in self.records]
