"""Durable material-knowledge ledger for ImprovementCore.

Purpose:
    No admitted material knowledge event is allowed to disappear merely because
    an ImprovementCore episode ends, a process restarts, or a later
    architecture compresses the system.

This ledger is not an authority engine. Capture != acceptance. Every node keeps
provenance, basis, dependency links, related objects, evidence references, and a
typed disposition. Supersession/rejection changes current disposition without
deleting historical capture.

The repository can only capture events that cross this governed path. It does
not claim access to unseen chats or external sources that were never supplied.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_KNOWLEDGE_LEDGER_PATH=ROOT/"integration"/"IMPROVEMENT_CORE_KNOWLEDGE_LEDGER_113.json"

VALID_KINDS={
    "IDEA","DISTINCTION","RELATION","INVARIANT","PROBLEM","SOLUTION",
    "EVIDENCE","OPEN_QUESTION","REPRESENTATION","CAPABILITY",
    "MATERIAL_TRANSITION","MATERIAL_DELTA","OTHER",
}
VALID_DISPOSITIONS={
    "CAPTURED","OPEN","ADMITTED","CURRENT","REJECTED","SUPERSEDED",
    "BLOCKED","CONFLICT",
}

MATERIAL_KEYS=(
    "material_result_delta",
    "material_search_delta",
    "material_relation_delta",
    "open_refinement",
    "changed_representation",
    "goal_gap_reduced",
    "execution_truth_strengthened",
    "resolved_open",
    "resolved_blocked",
    "resolved_conflict",
    "negative_evidence",
)


def _canon(value:Any)->str:
    return json.dumps(value,sort_keys=True,separators=(",",":"),default=str)


def _stable_id(kind:str,statement:str,basis_id:str)->str:
    raw=_canon({
        "kind":str(kind),
        "statement":str(statement).strip(),
        "basis_id":str(basis_id),
    })
    return "K-"+hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


@dataclass
class KnowledgeNode:
    knowledge_id:str
    kind:str
    statement:str
    basis_id:str
    disposition:str
    related_objects:list[str]=field(default_factory=list)
    dependency_footprint:list[str]=field(default_factory=list)
    evidence_refs:list[str]=field(default_factory=list)
    provenance:list[dict[str,Any]]=field(default_factory=list)
    metadata:dict[str,Any]=field(default_factory=dict)


@dataclass
class KnowledgeHistoryEvent:
    sequence:int
    knowledge_id:str
    action:str
    disposition:str
    source_episode:str
    source_route:str
    evidence_refs:list[str]
    metadata:dict[str,Any]=field(default_factory=dict)


@dataclass
class KnowledgeLedger:
    nodes:dict[str,KnowledgeNode]=field(default_factory=dict)
    history:list[KnowledgeHistoryEvent]=field(default_factory=list)
    durable_path:Path|None=None
    autosave:bool=False

    @classmethod
    def from_durable(
        cls,
        path:Path|str=DEFAULT_KNOWLEDGE_LEDGER_PATH,
        *,
        autosave:bool=True,
    )->"KnowledgeLedger":
        p=Path(path)
        ledger=cls(durable_path=p,autosave=autosave)
        if not p.exists():
            return ledger
        payload=json.loads(p.read_text(encoding="utf-8"))
        if payload.get("status")!="CURRENT":
            raise ValueError("IC_KNOWLEDGE_LEDGER_NOT_CURRENT")
        for row in payload.get("nodes",()):
            node=KnowledgeNode(
                knowledge_id=str(row["knowledge_id"]),
                kind=str(row["kind"]),
                statement=str(row["statement"]),
                basis_id=str(row["basis_id"]),
                disposition=str(row["disposition"]),
                related_objects=[str(x) for x in row.get("related_objects",())],
                dependency_footprint=[str(x) for x in row.get("dependency_footprint",())],
                evidence_refs=[str(x) for x in row.get("evidence_refs",())],
                provenance=[dict(x) for x in row.get("provenance",())],
                metadata=dict(row.get("metadata",{})),
            )
            ledger.nodes[node.knowledge_id]=node
        for row in payload.get("history",()):
            ledger.history.append(KnowledgeHistoryEvent(
                sequence=int(row["sequence"]),
                knowledge_id=str(row["knowledge_id"]),
                action=str(row["action"]),
                disposition=str(row["disposition"]),
                source_episode=str(row.get("source_episode","")),
                source_route=str(row.get("source_route","")),
                evidence_refs=[str(x) for x in row.get("evidence_refs",())],
                metadata=dict(row.get("metadata",{})),
            ))
        return ledger

    def _append_history(
        self,
        knowledge_id:str,
        *,
        action:str,
        disposition:str,
        source_episode:str,
        source_route:str,
        evidence_refs:list[str],
        metadata:dict[str,Any]|None=None,
    )->None:
        self.history.append(KnowledgeHistoryEvent(
            sequence=len(self.history)+1,
            knowledge_id=knowledge_id,
            action=action,
            disposition=disposition,
            source_episode=source_episode,
            source_route=source_route,
            evidence_refs=list(evidence_refs),
            metadata=dict(metadata or {}),
        ))

    def record(
        self,
        *,
        kind:str,
        statement:str,
        basis_id:str,
        source_episode:str,
        source_route:str="",
        disposition:str="CAPTURED",
        related_objects=(),
        dependency_footprint=(),
        evidence_refs=(),
        metadata:Mapping[str,Any]|None=None,
        knowledge_id:str|None=None,
    )->KnowledgeNode:
        kind=str(kind).upper()
        disposition=str(disposition).upper()
        statement=str(statement).strip()
        if kind not in VALID_KINDS:
            raise ValueError("IC_KNOWLEDGE_INVALID_KIND")
        if disposition not in VALID_DISPOSITIONS:
            raise ValueError("IC_KNOWLEDGE_INVALID_DISPOSITION")
        if not statement:
            raise ValueError("IC_KNOWLEDGE_EMPTY_STATEMENT")
        basis_id=str(basis_id or "UNSPECIFIED")
        kid=str(knowledge_id or _stable_id(kind,statement,basis_id))
        prov={
            "source_episode":str(source_episode),
            "source_route":str(source_route),
        }
        refs=[str(x) for x in evidence_refs if str(x)]
        related=[str(x) for x in related_objects if str(x)]
        deps=[str(x) for x in dependency_footprint if str(x)]

        existing=self.nodes.get(kid)
        if existing is None:
            node=KnowledgeNode(
                knowledge_id=kid,
                kind=kind,
                statement=statement,
                basis_id=basis_id,
                disposition=disposition,
                related_objects=sorted(set(related)),
                dependency_footprint=sorted(set(deps)),
                evidence_refs=sorted(set(refs)),
                provenance=[prov],
                metadata=dict(metadata or {}),
            )
            self.nodes[kid]=node
            self._append_history(
                kid,action="CAPTURE",disposition=disposition,
                source_episode=str(source_episode),source_route=str(source_route),
                evidence_refs=refs,metadata=dict(metadata or {}),
            )
        else:
            if (
                existing.kind!=kind
                or existing.statement!=statement
                or existing.basis_id!=basis_id
            ):
                raise ValueError("IC_KNOWLEDGE_ID_COLLISION")
            changed=False
            for value in related:
                if value not in existing.related_objects:
                    existing.related_objects.append(value); changed=True
            for value in deps:
                if value not in existing.dependency_footprint:
                    existing.dependency_footprint.append(value); changed=True
            for value in refs:
                if value not in existing.evidence_refs:
                    existing.evidence_refs.append(value); changed=True
            if prov not in existing.provenance:
                existing.provenance.append(prov); changed=True
            if disposition!=existing.disposition:
                existing.disposition=disposition; changed=True
            if metadata:
                for k,v in dict(metadata).items():
                    if existing.metadata.get(k)!=v:
                        existing.metadata[k]=v; changed=True
            existing.related_objects.sort()
            existing.dependency_footprint.sort()
            existing.evidence_refs.sort()
            node=existing
            if changed:
                self._append_history(
                    kid,action="INTEGRATE",disposition=disposition,
                    source_episode=str(source_episode),source_route=str(source_route),
                    evidence_refs=refs,metadata=dict(metadata or {}),
                )

        if self.autosave and self.durable_path is not None:
            self.persist()
        return node

    def record_explicit_event(
        self,
        event:Mapping[str,Any],
        *,
        fallback_basis:str,
        source_episode:str,
    )->KnowledgeNode:
        return self.record(
            kind=str(event.get("kind","IDEA")),
            statement=str(event.get("statement") or event.get("idea") or event.get("content") or ""),
            basis_id=str(event.get("basis_id") or fallback_basis),
            source_episode=str(event.get("source_episode") or source_episode),
            source_route=str(event.get("source_route") or event.get("route_id") or ""),
            disposition=str(event.get("disposition","CAPTURED")),
            related_objects=event.get("related_objects",()),
            dependency_footprint=event.get("dependency_footprint",()),
            evidence_refs=event.get("evidence_refs",()),
            metadata=dict(event.get("metadata",{})),
            knowledge_id=event.get("knowledge_id"),
        )

    def capture_material_trace(
        self,
        trace:Mapping[str,Any],
        *,
        fallback_basis:str,
        source_episode:str,
    )->KnowledgeNode|None:
        delta=trace.get("delta",{})
        if not isinstance(delta,Mapping):
            return None
        selected=trace.get("selected_job",{})
        if not isinstance(selected,Mapping):
            selected={}
        material={k:delta.get(k) for k in MATERIAL_KEYS if delta.get(k)}
        progress=tuple(str(x) for x in trace.get("progress_effects",()) if str(x))
        if not material and not progress:
            return None
        route_id=str(
            selected.get("route_id")
            or selected.get("id")
            or trace.get("iteration","")
        )
        basis=str(selected.get("basis_id") or fallback_basis)
        statement=_canon({
            "route_id":route_id,
            "material":material,
            "progress_effects":progress,
        })
        return self.record(
            kind="MATERIAL_TRANSITION",
            statement=statement,
            basis_id=basis,
            source_episode=source_episode,
            source_route=route_id,
            disposition="CAPTURED",
            related_objects=(str(selected.get("id","")),),
            dependency_footprint=selected.get("dependency_footprint",()),
            evidence_refs=tuple(
                str(x) for x in delta.get("evidence_refs",()) if str(x)
            ),
            metadata={"delta":dict(delta),"progress_effects":progress},
        )

    def persist(self)->None:
        if self.durable_path is None:
            raise ValueError("IC_KNOWLEDGE_DURABLE_PATH_REQUIRED")
        payload={
            "schema_version":1,
            "object_id":"TAKE5_IMPROVEMENT_CORE_KNOWLEDGE_LEDGER_113",
            "date":"2026-09-26",
            "status":"CURRENT",
            "regime_version":"090",
            "purpose":"Durable capture and integration of admitted material knowledge events. Capture is not authority.",
            "nodes":[asdict(self.nodes[k]) for k in sorted(self.nodes)],
            "history":[asdict(x) for x in self.history],
        }
        self.durable_path.parent.mkdir(parents=True,exist_ok=True)
        tmp=self.durable_path.with_suffix(self.durable_path.suffix+".tmp")
        tmp.write_text(json.dumps(payload,indent=2,sort_keys=False,default=str)+"\n",encoding="utf-8")
        tmp.replace(self.durable_path)

    def unresolved(self)->tuple[str,...]:
        return tuple(sorted(
            k for k,v in self.nodes.items()
            if v.disposition in {"CAPTURED","OPEN","BLOCKED","CONFLICT"}
        ))

    def summary(self)->list[dict[str,Any]]:
        return [
            {
                "knowledge_id":node.knowledge_id,
                "kind":node.kind,
                "statement":node.statement,
                "basis_id":node.basis_id,
                "disposition":node.disposition,
                "related_objects":tuple(node.related_objects),
                "dependency_footprint":tuple(node.dependency_footprint),
                "evidence_refs":tuple(node.evidence_refs),
                "provenance_count":len(node.provenance),
            }
            for node in (self.nodes[k] for k in sorted(self.nodes))
        ]
