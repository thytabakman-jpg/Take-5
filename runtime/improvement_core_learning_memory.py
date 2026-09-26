"""ImprovementCore basis-relative learning memory.

Certified negative route evidence is durable across fresh processes. Unchanged
no-gain/rejected/failed/cycle routes are removed from admission until a relevant
dependency coordinate or another explicit retry condition changes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from improvement_core_progress_relation import retry_licensed


VALID_DISPOSITIONS={
    "GAIN","NO_GAIN","REJECTED","FAILED","OPEN","BLOCKED","CONFLICT",
    "CYCLE_NO_GAIN",
}
DURABLE_BLOCKING_DISPOSITIONS={"NO_GAIN","REJECTED","FAILED","CYCLE_NO_GAIN"}

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_DURABLE_LEARNING_PATH=ROOT/"integration"/"IMPROVEMENT_CORE_DURABLE_LEARNING_110.json"


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
    durable_path:Path|None=None
    autosave:bool=False

    @classmethod
    def from_durable(
        cls,
        path:Path|str=DEFAULT_DURABLE_LEARNING_PATH,
        *,
        autosave:bool=True,
    )->"LearningMemory":
        p=Path(path)
        records:list[RouteEvidence]=[]
        if p.exists():
            payload=json.loads(p.read_text(encoding="utf-8"))
            if payload.get("status")!="CURRENT":
                raise ValueError("IC_LEARNING_DURABLE_LEDGER_NOT_CURRENT")
            for row in payload.get("records",()):
                disposition=str(row.get("disposition",""))
                if disposition not in VALID_DISPOSITIONS:
                    raise ValueError("IC_LEARNING_INVALID_DURABLE_DISPOSITION")
                records.append(RouteEvidence(
                    route_id=str(row["route_id"]),
                    basis_id=str(row["basis_id"]),
                    disposition=disposition,
                    dependency_footprint=frozenset(
                        str(x) for x in row.get("dependency_footprint",())
                    ),
                    evidence=dict(row.get("evidence",{})),
                ))
        return cls(records=records,durable_path=p,autosave=autosave)

    @staticmethod
    def _same(a:RouteEvidence,b:RouteEvidence)->bool:
        return (
            a.route_id==b.route_id
            and a.basis_id==b.basis_id
            and a.disposition==b.disposition
            and a.dependency_footprint==b.dependency_footprint
            and a.evidence==b.evidence
        )

    def record(
        self,
        route_id:str,
        basis_id:str,
        disposition:str,
        dependency_footprint:set[str]|frozenset[str],
        evidence:dict[str,Any]|None=None,
    )->None:
        if disposition not in VALID_DISPOSITIONS:
            raise ValueError("IC_LEARNING_INVALID_DISPOSITION")
        row=RouteEvidence(
            route_id=str(route_id),
            basis_id=str(basis_id),
            disposition=disposition,
            dependency_footprint=frozenset(str(x) for x in dependency_footprint),
            evidence=dict(evidence or {}),
        )
        if any(self._same(row,existing) for existing in self.records):
            return
        self.records.append(row)
        if (
            self.autosave
            and self.durable_path is not None
            and disposition in DURABLE_BLOCKING_DISPOSITIONS
        ):
            self.persist()

    def persist(self)->None:
        if self.durable_path is None:
            raise ValueError("IC_LEARNING_DURABLE_PATH_REQUIRED")
        durable=[
            {
                "route_id":r.route_id,
                "basis_id":r.basis_id,
                "disposition":r.disposition,
                "dependency_footprint":sorted(r.dependency_footprint),
                "evidence":r.evidence,
            }
            for r in self.records
            if r.disposition in DURABLE_BLOCKING_DISPOSITIONS
        ]
        payload={
            "schema_version":1,
            "object_id":"TAKE5_IMPROVEMENT_CORE_DURABLE_LEARNING_110",
            "date":"2026-09-26",
            "status":"CURRENT",
            "regime_version":"090",
            "purpose":"Durable basis-relative negative-route memory.",
            "records":durable,
        }
        self.durable_path.parent.mkdir(parents=True,exist_ok=True)
        tmp=self.durable_path.with_suffix(self.durable_path.suffix+".tmp")
        tmp.write_text(
            json.dumps(payload,indent=2,sort_keys=False,default=str)+"\n",
            encoding="utf-8",
        )
        tmp.replace(self.durable_path)

    def unchanged_rerun_blocked(
        self,
        route_id:str,
        basis_id:str,
        changed_coordinates:set[str]|None=None,
        *,
        failure_signature_defeated:bool=False,
        representation_changed:bool=False,
        executability_changed:bool=False,
        new_interaction_package:bool=False,
    )->bool:
        prior=[
            r for r in self.records
            if r.route_id==route_id and r.basis_id==basis_id
        ]
        if not prior:
            return False
        last=prior[-1]
        if last.disposition not in DURABLE_BLOCKING_DISPOSITIONS:
            return False
        return not retry_licensed(
            last.dependency_footprint,
            frozenset(str(x) for x in (changed_coordinates or set())),
            failure_signature_defeated=failure_signature_defeated,
            representation_changed=representation_changed,
            executability_changed=executability_changed,
            new_interaction_package=new_interaction_package,
        )

    def invalidated_routes(self,changed_coordinates:set[str])->set[str]:
        changed=set(str(x) for x in changed_coordinates)
        return {
            r.route_id for r in self.records
            if changed & set(r.dependency_footprint)
        }

    def summary(self)->list[dict[str,Any]]:
        return [
            {
                "route_id":r.route_id,
                "basis_id":r.basis_id,
                "disposition":r.disposition,
                "dependency_footprint":sorted(r.dependency_footprint),
                "evidence":dict(r.evidence),
            }
            for r in self.records
        ]
