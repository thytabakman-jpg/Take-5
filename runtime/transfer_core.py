"""TransferCore runtime for Take-5.

TransferCore discovers bounded plausible targets, types source->target relations,
checks provenance/applicability/bridge license/target effect/duplication, emits a
typed handoff, and never launders target mutation authority.

It is an analytic + handoff tool.  Target mutation remains a separate authorized
transition followed by verification and feedback.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Callable
import hashlib
import json

class TransferStatus(str,Enum):
    ADMITTED="ADMITTED"
    REJECTED="REJECTED"
    PARKED="PARKED"
    NO_EFFECT="NO_EFFECT"
    OPEN="OPEN"
    BLOCKED="BLOCKED"
    CONFLICT="CONFLICT"

@dataclass(frozen=True)
class TransferSource:
    source_id:str
    source_project:str
    source_result_ref:str
    source_refs:tuple[str,...]
    object_type:str
    payload:Any
    provenance:dict[str,Any]

@dataclass(frozen=True)
class TransferTarget:
    target_id:str
    target_project:str
    target_job:str
    target_type:str
    metadata:dict[str,Any]

@dataclass(frozen=True)
class TransferRelation:
    source_id:str
    target_id:str
    status:TransferStatus
    relation_statement:str
    applicability:bool|None
    bridge_license:str
    target_effect:str
    material_effect:bool|None
    duplication_status:str
    authority_state:str
    evidence:dict[str,Any]
    open:tuple[str,...]=()

@dataclass(frozen=True)
class TransferHandoff:
    handoff_id:str
    source_result_ref:str
    source_project:str
    source_refs:tuple[str,...]
    relation_status:str
    relation_statement:str
    candidate_targets:tuple[str,...]
    target_effect:str
    bridge_license:str
    duplication_status:str
    authority_state:str
    review_trigger:str
    target_mutated:bool=False

@dataclass(frozen=True)
class TransferCoreResult:
    status:str
    source:TransferSource
    targets:tuple[TransferTarget,...]
    relations:tuple[TransferRelation,...]
    handoffs:tuple[TransferHandoff,...]
    selected_targets:tuple[str,...]
    open:tuple[str,...]
    execution_truth:str="IMPLEMENTATION_EXECUTED"

def _hid(source_id:str,target_id:str)->str:
    raw=f"{source_id}|{target_id}".encode()
    return "XFER:"+hashlib.sha256(raw).hexdigest()[:16]

def _target_from(value:Any)->TransferTarget:
    if isinstance(value,TransferTarget):
        return value
    if not isinstance(value,dict):
        raise TypeError("TRANSFERCORE_TARGET_MUST_BE_MAPPING")
    required=("target_id","target_project","target_job","target_type")
    missing=[x for x in required if not value.get(x)]
    if missing:
        raise ValueError("TRANSFERCORE_TARGET_MISSING:"+",".join(missing))
    return TransferTarget(
        str(value["target_id"]),str(value["target_project"]),
        str(value["target_job"]),str(value["target_type"]),
        dict(value.get("metadata",{})),
    )

def _relation_from(source:TransferSource,target:TransferTarget,value:Any)->TransferRelation:
    if isinstance(value,TransferRelation):
        return value
    if not isinstance(value,dict):
        raise TypeError("TRANSFERCORE_RELATION_MUST_BE_MAPPING")

    applicability=value.get("applicability")
    material=value.get("material_effect")
    bridge=str(value.get("bridge_license","OPEN"))
    duplication=str(value.get("duplication_status","OPEN"))
    authority=str(value.get("authority_state","target mutation not authorized"))
    statement=str(value.get("relation_statement","")).strip()
    effect=str(value.get("target_effect","")).strip()
    open_items=list(value.get("open",()) or ())

    if not statement:
        open_items.append("RELATION_STATEMENT_MISSING")
    if not effect:
        open_items.append("TARGET_EFFECT_MISSING")

    explicit=value.get("status")
    if explicit is not None:
        status=TransferStatus(str(explicit))
    elif open_items or applicability is None or material is None or bridge=="OPEN" or duplication=="OPEN":
        status=TransferStatus.OPEN
    elif applicability is False:
        status=TransferStatus.REJECTED
    elif bridge.upper() in {"REJECTED","UNLICENSED","NO_LICENSE"}:
        status=TransferStatus.REJECTED
    elif duplication.upper() in {"FULL_DUPLICATE","ALREADY_OWNED","NO_NEW_EFFECT"}:
        status=TransferStatus.NO_EFFECT
    elif material is False:
        status=TransferStatus.NO_EFFECT
    else:
        status=TransferStatus.ADMITTED

    return TransferRelation(
        source.source_id,target.target_id,status,statement,applicability,bridge,
        effect,material,duplication,authority,dict(value.get("evidence",{})),
        tuple(dict.fromkeys(str(x) for x in open_items)),
    )

def relation_to_handoff(source:TransferSource,target:TransferTarget,
                        rel:TransferRelation)->TransferHandoff|None:
    if rel.status in {TransferStatus.REJECTED,TransferStatus.NO_EFFECT}:
        return None
    review_trigger=(
        "target_authority_review"
        if rel.status==TransferStatus.ADMITTED
        else "resolve_transfer_open_or_blocker"
    )
    return TransferHandoff(
        handoff_id=_hid(source.source_id,target.target_id),
        source_result_ref=source.source_result_ref,
        source_project=source.source_project,
        source_refs=source.source_refs,
        relation_status=rel.status.value,
        relation_statement=rel.relation_statement or "OPEN relation",
        candidate_targets=(target.target_id,),
        target_effect=rel.target_effect or "OPEN",
        bridge_license=rel.bridge_license,
        duplication_status=rel.duplication_status,
        authority_state=rel.authority_state,
        review_trigger=review_trigger,
        target_mutated=False,
    )

def run_transfer_core(
    source:TransferSource,
    *,
    candidate_targets:tuple[TransferTarget,...]|tuple[dict,...]=(),
    discover_targets:Callable[[TransferSource],list[Any]]|None=None,
    evaluate_relation:Callable[[TransferSource,TransferTarget],dict]|None=None,
    max_targets:int=16,
)->TransferCoreResult:
    """Run bounded TransferCore discovery + admission.

    Target discovery is required only when explicit candidates are absent.
    Evaluation is fail-closed: no evaluator means OPEN rather than guessed transfer.
    """
    targets=[_target_from(x) for x in candidate_targets]
    open_items=[]

    if not targets:
        if discover_targets is None:
            return TransferCoreResult(
                "OPEN",source,(),(),(),(),("TARGET_DISCOVERY_UNBOUND",)
            )
        discovered=list(discover_targets(source) or [])
        if len(discovered)>max_targets:
            return TransferCoreResult(
                "OPEN",source,(),(),(),(),("TARGET_DISCOVERY_BOUND_EXCEEDED",)
            )
        targets=[_target_from(x) for x in discovered]

    # Deduplicate without erasing first-seen provenance/order.
    unique={}
    for t in targets:
        unique.setdefault(t.target_id,t)
    targets=list(unique.values())

    if not targets:
        return TransferCoreResult("NO_EFFECT",source,(),(),(),(),())

    relations=[]
    handoffs=[]
    selected=[]
    for target in targets:
        if evaluate_relation is None:
            rel=TransferRelation(
                source.source_id,target.target_id,TransferStatus.OPEN,
                "OPEN","OPEN", "OPEN","OPEN",None,"OPEN",
                "target mutation not authorized",{},
                ("RELATION_EVALUATOR_UNBOUND",),
            )
        else:
            rel=_relation_from(source,target,evaluate_relation(source,target))
        relations.append(rel)
        if rel.status==TransferStatus.ADMITTED:
            selected.append(target.target_id)
        if rel.open:
            open_items.extend(f"{target.target_id}:{x}" for x in rel.open)
        h=relation_to_handoff(source,target,rel)
        if h is not None:
            handoffs.append(h)

    statuses={r.status for r in relations}
    if TransferStatus.CONFLICT in statuses:
        status="CONFLICT"
    elif TransferStatus.BLOCKED in statuses:
        status="BLOCKED"
    elif TransferStatus.OPEN in statuses:
        status="OPEN"
    elif TransferStatus.ADMITTED in statuses:
        status="ADMITTED"
    elif statuses and statuses <= {TransferStatus.REJECTED,TransferStatus.NO_EFFECT}:
        status="NO_EFFECT"
    else:
        status="OPEN"

    return TransferCoreResult(
        status,source,tuple(targets),tuple(relations),tuple(handoffs),
        tuple(selected),tuple(dict.fromkeys(open_items))
    )

def apply_transfer_feedback(
    result:TransferCoreResult,
    *,
    target_id:str,
    target_verified:bool,
    changed_relation:dict[str,Any]|None=None,
)->dict[str,Any]:
    """Feedback never mutates source/target; it returns the required reentry delta."""
    match=[r for r in result.relations if r.target_id==target_id]
    if not match:
        raise KeyError("TRANSFERCORE_FEEDBACK_TARGET_UNKNOWN")
    rel=match[-1]
    return {
        "source_id":result.source.source_id,
        "target_id":target_id,
        "prior_relation_status":rel.status.value,
        "target_verified":bool(target_verified),
        "relation_recompute_required":bool(changed_relation) or not target_verified,
        "changed_relation":dict(changed_relation or {}),
        "reentry_required":True,
        "target_mutated":False,
    }
