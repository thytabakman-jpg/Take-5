"""Current TransferCore semantic/runtime core.

TransferCore determines whether one or more source results license a material
target-side consequence.  It preserves source provenance, bridge licensing,
target effect, duplication, target authority, OPEN, and execution truth.

Admission never launders mutation authority.  Target mutation is a distinct
authorized transition with its own verification ledger.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from enum import Enum
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Callable, Iterable, Mapping, Sequence


class TransferCoreError(RuntimeError):
    pass


class TransferStatus(str,Enum):
    ADMITTED="ADMITTED"
    REJECTED="REJECTED"
    PARKED="PARKED"
    NO_EFFECT="NO_EFFECT"
    OPEN="OPEN"
    BLOCKED="BLOCKED"
    CONFLICT="CONFLICT"


class TransferDirection(str,Enum):
    OUTBOUND="OUTBOUND"
    INBOUND="INBOUND"
    BIDIRECTIONAL="BIDIRECTIONAL"
    MULTI_SOURCE="MULTI_SOURCE"
    MULTI_TARGET="MULTI_TARGET"


class TransferUpdateKind(str,Enum):
    ACCUMULATE="ACCUMULATE"
    REVISE_REPLACE="REVISE_REPLACE"
    STRUCTURAL_TOPOLOGY="STRUCTURAL_TOPOLOGY"
    RETRACT_INVALIDATE="RETRACT_INVALIDATE"


class TransferLedgerStage(str,Enum):
    ANALYTIC_RELATION="ANALYTIC_RELATION"
    HANDOFF_EMITTED="HANDOFF_EMITTED"
    QUEUED="QUEUED"
    TARGET_AUTHORIZED="TARGET_AUTHORIZED"
    TARGET_MUTATED="TARGET_MUTATED"
    TARGET_VERIFIED="TARGET_VERIFIED"
    RETRACTED="RETRACTED"


@dataclass(frozen=True)
class TransferSource:
    source_id:str
    source_project:str
    source_result_ref:str
    source_refs:tuple[str,...]
    object_type:str
    payload:Any
    provenance:Mapping[str,Any]


@dataclass(frozen=True)
class TransferTarget:
    target_id:str
    target_project:str
    target_job:str
    target_type:str
    metadata:Mapping[str,Any]


@dataclass(frozen=True)
class TransferRelation:
    source_ids:tuple[str,...]
    target_id:str
    status:TransferStatus
    relation_statement:str
    applicability:bool|None
    bridge_license:str
    target_effect:str
    material_effect:bool|None
    duplication_status:str
    authority_state:str
    evidence:Mapping[str,Any]
    direction:TransferDirection=TransferDirection.OUTBOUND
    open:tuple[str,...]=()
    external_dependencies:tuple[str,...]=()

    @property
    def source_id(self)->str:
        return self.source_ids[0] if len(self.source_ids)==1 else "+".join(self.source_ids)


@dataclass(frozen=True)
class TransferHandoff:
    handoff_id:str
    source_result_refs:tuple[str,...]
    source_projects:tuple[str,...]
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
class TargetAuthorityBinding:
    target_id:str
    authority_ref:str
    owner:str
    status:str="BOUND"


@dataclass(frozen=True)
class TargetMutationAuthorization:
    target_id:str
    authority_ref:str
    operation:str
    granted:bool
    evidence:tuple[str,...]=()


@dataclass(frozen=True)
class TransferLedgerEvent:
    stage:TransferLedgerStage
    transfer_id:str
    target_id:str
    evidence:tuple[str,...]=()


@dataclass(frozen=True)
class TransferCoreResult:
    status:str
    sources:tuple[TransferSource,...]
    targets:tuple[TransferTarget,...]
    relations:tuple[TransferRelation,...]
    handoffs:tuple[TransferHandoff,...]
    selected_targets:tuple[str,...]
    open:tuple[str,...]
    ledger:tuple[TransferLedgerEvent,...]=()
    execution_truth:str="IMPLEMENTATION_EXECUTED"

    @property
    def source(self)->TransferSource:
        if not self.sources:
            raise TransferCoreError("TRANSFERCORE_RESULT_HAS_NO_SOURCE")
        return self.sources[0]


@dataclass(frozen=True)
class JointTransferResult:
    status:str
    relation:TransferRelation|None
    singles:tuple[TransferRelation,...]
    irreducible:bool|None
    open:tuple[str,...]=()


@dataclass(frozen=True)
class ChallengeResult:
    status:str
    relation_id:str
    passed:tuple[str,...]
    failed:tuple[str,...]
    open:tuple[str,...]


@dataclass(frozen=True)
class TransferState:
    relations:Mapping[str,TransferRelation]=field(default_factory=dict)
    invalidated:frozenset[str]=frozenset()
    topology:Mapping[str,tuple[str,...]]=field(default_factory=dict)
    history:tuple[tuple[str,str],...]=()


@dataclass(frozen=True)
class TargetMutationResult:
    status:str
    target_id:str
    state:Any
    verified:bool
    ledger:tuple[TransferLedgerEvent,...]
    reentry_required:bool


def _fingerprint(value:Any)->str:
    raw=json.dumps(value,sort_keys=True,default=str,separators=(",",":")).encode()
    return sha256(raw).hexdigest()


def _hid(source_ids:Sequence[str],target_id:str)->str:
    raw="|".join(tuple(source_ids)+(target_id,)).encode()
    return "XFER:"+sha256(raw).hexdigest()[:16]


def _relation_id(rel:TransferRelation)->str:
    return _hid(rel.source_ids,rel.target_id)


def _target_from(value:Any)->TransferTarget:
    if isinstance(value,TransferTarget):
        return value
    if not isinstance(value,Mapping):
        raise TypeError("TRANSFERCORE_TARGET_MUST_BE_MAPPING")
    required=("target_id","target_project","target_job","target_type")
    missing=[x for x in required if not value.get(x)]
    if missing:
        raise ValueError("TRANSFERCORE_TARGET_MISSING:"+",".join(missing))
    return TransferTarget(
        str(value["target_id"]),
        str(value["target_project"]),
        str(value["target_job"]),
        str(value["target_type"]),
        dict(value.get("metadata",{})),
    )


def _relation_from(
    sources:tuple[TransferSource,...],
    target:TransferTarget,
    value:Any,
    *,
    direction:TransferDirection,
)->TransferRelation:
    if isinstance(value,TransferRelation):
        return value
    if not isinstance(value,Mapping):
        raise TypeError("TRANSFERCORE_RELATION_MUST_BE_MAPPING")

    applicability=value.get("applicability")
    material=value.get("material_effect")
    bridge=str(value.get("bridge_license","OPEN"))
    duplication=str(value.get("duplication_status","OPEN"))
    authority=str(value.get("authority_state","target mutation not authorized"))
    statement=str(value.get("relation_statement","")).strip()
    effect=str(value.get("target_effect","")).strip()
    open_items=list(value.get("open",()) or ())
    external=tuple(str(x) for x in value.get("external_dependencies",()) if str(x))

    if not statement:
        open_items.append("RELATION_STATEMENT_MISSING")
    if not effect:
        open_items.append("TARGET_EFFECT_MISSING")

    explicit=value.get("status")
    if explicit is not None:
        status=TransferStatus(str(explicit))
    elif external:
        status=TransferStatus.BLOCKED
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
        tuple(s.source_id for s in sources),
        target.target_id,
        status,
        statement,
        applicability,
        bridge,
        effect,
        material,
        duplication,
        authority,
        dict(value.get("evidence",{})),
        direction,
        tuple(dict.fromkeys(str(x) for x in open_items)),
        external,
    )


def relation_to_handoff(
    sources:tuple[TransferSource,...],
    target:TransferTarget,
    rel:TransferRelation,
)->TransferHandoff|None:
    if rel.status in {TransferStatus.REJECTED,TransferStatus.NO_EFFECT}:
        return None
    review_trigger=(
        "target_authority_review"
        if rel.status==TransferStatus.ADMITTED
        else "resolve_transfer_open_or_blocker"
    )
    refs=[]
    for source in sources:
        refs.extend(source.source_refs)
    return TransferHandoff(
        handoff_id=_hid(rel.source_ids,target.target_id),
        source_result_refs=tuple(s.source_result_ref for s in sources),
        source_projects=tuple(s.source_project for s in sources),
        source_refs=tuple(dict.fromkeys(refs)),
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
    candidate_targets:Iterable[TransferTarget|Mapping[str,Any]]=(),
    discover_targets:Callable[[TransferSource],Iterable[Any]]|None=None,
    evaluate_relation:Callable[[TransferSource,TransferTarget],Mapping[str,Any]]|None=None,
    max_targets:int=16,
    direction:TransferDirection=TransferDirection.OUTBOUND,
)->TransferCoreResult:
    sources=(source,)
    targets=[_target_from(x) for x in candidate_targets]
    open_items=[]

    if not targets:
        if discover_targets is None:
            return TransferCoreResult(
                "OPEN",sources,(),(),(),(),("TARGET_DISCOVERY_UNBOUND",)
            )
        discovered=list(discover_targets(source) or ())
        if len(discovered)>max_targets:
            return TransferCoreResult(
                "OPEN",sources,(),(),(),(),("TARGET_DISCOVERY_BOUND_EXCEEDED",)
            )
        targets=[_target_from(x) for x in discovered]

    unique={}
    for target in targets:
        unique.setdefault(target.target_id,target)
    targets=list(unique.values())

    if not targets:
        return TransferCoreResult("NO_EFFECT",sources,(),(),(),(),())

    relations=[]
    handoffs=[]
    selected=[]
    ledger=[]
    for target in targets:
        if evaluate_relation is None:
            rel=TransferRelation(
                (source.source_id,),
                target.target_id,
                TransferStatus.OPEN,
                "OPEN",
                None,
                "OPEN",
                "OPEN",
                None,
                "OPEN",
                "target mutation not authorized",
                {},
                direction,
                ("RELATION_EVALUATOR_UNBOUND",),
                (),
            )
        else:
            rel=_relation_from(
                sources,target,evaluate_relation(source,target),direction=direction
            )
        relations.append(rel)
        ledger.append(TransferLedgerEvent(
            TransferLedgerStage.ANALYTIC_RELATION,
            _relation_id(rel),
            target.target_id,
            (rel.status.value,),
        ))
        if rel.status==TransferStatus.ADMITTED:
            selected.append(target.target_id)
        if rel.open:
            open_items.extend(f"{target.target_id}:{x}" for x in rel.open)
        if rel.external_dependencies:
            open_items.extend(
                f"{target.target_id}:EXTERNAL_ACQUISITION:{x}"
                for x in rel.external_dependencies
            )
        handoff=relation_to_handoff(sources,target,rel)
        if handoff is not None:
            handoffs.append(handoff)
            ledger.append(TransferLedgerEvent(
                TransferLedgerStage.HANDOFF_EMITTED,
                handoff.handoff_id,
                target.target_id,
                (handoff.relation_status,),
            ))

    statuses={rel.status for rel in relations}
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
        status,
        sources,
        tuple(targets),
        tuple(relations),
        tuple(handoffs),
        tuple(selected),
        tuple(dict.fromkeys(open_items)),
        tuple(ledger),
    )


def run_joint_transfer_core(
    sources:Iterable[TransferSource],
    target:TransferTarget,
    *,
    evaluate_joint_relation:Callable[[tuple[TransferSource,...],TransferTarget],Mapping[str,Any]],
    evaluate_single_relation:Callable[[TransferSource,TransferTarget],Mapping[str,Any]]|None=None,
)->JointTransferResult:
    xs=tuple(sources)
    if len(xs)<2:
        return JointTransferResult("OPEN",None,(),None,("JOINT_TRANSFER_REQUIRES_MULTIPLE_SOURCES",))
    if not callable(evaluate_joint_relation):
        return JointTransferResult("OPEN",None,(),None,("JOINT_RELATION_EVALUATOR_UNBOUND",))

    joint=_relation_from(
        xs,target,evaluate_joint_relation(xs,target),
        direction=TransferDirection.MULTI_SOURCE,
    )
    singles=[]
    if evaluate_single_relation is not None:
        for source in xs:
            singles.append(_relation_from(
                (source,),target,evaluate_single_relation(source,target),
                direction=TransferDirection.OUTBOUND,
            ))

    irreducible=None
    if singles:
        irreducible=(
            joint.status==TransferStatus.ADMITTED
            and all(rel.status!=TransferStatus.ADMITTED for rel in singles)
        )

    status=joint.status.value
    return JointTransferResult(status,joint,tuple(singles),irreducible,joint.open)


def challenge_transfer_relation(
    relation:TransferRelation,
    *,
    representation_checks:Mapping[str,bool|None]=(),
    hierarchy_checks:Mapping[str,bool|None]=(),
    order_checks:Mapping[str,bool|None]=(),
)->ChallengeResult:
    passed=[]
    failed=[]
    open_items=[]
    for family,checks in (
        ("REPRESENTATION",representation_checks),
        ("HIERARCHY",hierarchy_checks),
        ("ORDER",order_checks),
    ):
        for name,value in dict(checks).items():
            key=f"{family}:{name}"
            if value is True:
                passed.append(key)
            elif value is False:
                failed.append(key)
            else:
                open_items.append(key)
    status="FAIL" if failed else ("OPEN" if open_items else "PASS")
    return ChallengeResult(
        status,_relation_id(relation),tuple(passed),tuple(failed),tuple(open_items)
    )


def nondominated_targets(
    targets:Iterable[TransferTarget],
    *,
    benefit_key:str="benefit",
    disruption_key:str="disruption",
    uncertainty_key:str="uncertainty",
)->tuple[TransferTarget,...]:
    xs=tuple(targets)
    def vector(t:TransferTarget)->tuple[float,float,float]:
        meta=t.metadata
        return (
            float(meta.get(benefit_key,0.0)),
            -float(meta.get(disruption_key,0.0)),
            -float(meta.get(uncertainty_key,0.0)),
        )
    def dominates(a:TransferTarget,b:TransferTarget)->bool:
        av,bv=vector(a),vector(b)
        return all(x>=y for x,y in zip(av,bv)) and any(x>y for x,y in zip(av,bv))
    return tuple(
        t for t in xs
        if not any(other.target_id!=t.target_id and dominates(other,t) for other in xs)
    )


def apply_transfer_update(
    state:TransferState,
    *,
    kind:TransferUpdateKind,
    relation:TransferRelation|None=None,
    relation_id:str|None=None,
    topology_patch:Mapping[str,Iterable[str]]|None=None,
    reason:str="",
)->TransferState:
    relations=dict(state.relations)
    invalidated=set(state.invalidated)
    topology={k:tuple(v) for k,v in state.topology.items()}
    history=list(state.history)

    rid=relation_id or (_relation_id(relation) if relation is not None else None)
    if kind==TransferUpdateKind.ACCUMULATE:
        if relation is None:
            raise TransferCoreError("TRANSFER_UPDATE_RELATION_REQUIRED")
        relations.setdefault(_relation_id(relation),relation)
    elif kind==TransferUpdateKind.REVISE_REPLACE:
        if relation is None:
            raise TransferCoreError("TRANSFER_UPDATE_RELATION_REQUIRED")
        relations[_relation_id(relation)]=relation
        invalidated.discard(_relation_id(relation))
    elif kind==TransferUpdateKind.STRUCTURAL_TOPOLOGY:
        if topology_patch is None:
            raise TransferCoreError("TRANSFER_TOPOLOGY_PATCH_REQUIRED")
        for key,value in topology_patch.items():
            topology[str(key)]=tuple(str(x) for x in value)
    elif kind==TransferUpdateKind.RETRACT_INVALIDATE:
        if not rid:
            raise TransferCoreError("TRANSFER_RELATION_ID_REQUIRED")
        invalidated.add(rid)
    else:
        raise TransferCoreError("TRANSFER_UPDATE_KIND_UNKNOWN")

    history.append((kind.value,reason or rid or "topology"))
    return TransferState(relations, frozenset(invalidated), topology, tuple(history))


def bind_target_authority(
    target:TransferTarget,
    authority_registry:Mapping[str,Any],
    *,
    coordinate:str|None=None,
)->TargetAuthorityBinding|None:
    coord=coordinate or str(target.metadata.get("authority_coordinate",""))
    if not coord:
        return None
    raw=authority_registry.get(coord)
    if raw is None:
        return None
    owners=(raw,) if isinstance(raw,str) else tuple(raw) if isinstance(raw,(list,tuple,set)) else (str(raw),)
    owners=tuple(str(x) for x in owners if str(x))
    if len(set(owners))!=1:
        return None
    owner=owners[0]
    return TargetAuthorityBinding(target.target_id,f"{coord}:{owner}",owner)


def queue_entry_from_handoff(handoff:TransferHandoff)->dict[str,Any]|None:
    if handoff.relation_status in {TransferStatus.REJECTED.value,TransferStatus.NO_EFFECT.value}:
        return None
    status={
        TransferStatus.ADMITTED.value:"target_review_pending",
        TransferStatus.PARKED.value:"parked",
        TransferStatus.OPEN.value:"pending_review",
        TransferStatus.BLOCKED.value:"blocked",
        TransferStatus.CONFLICT.value:"conflict",
    }.get(handoff.relation_status,"pending_review")
    return {
        "transfer_id":handoff.handoff_id,
        "source_result_refs":list(handoff.source_result_refs),
        "source_projects":list(handoff.source_projects),
        "source_refs":list(handoff.source_refs),
        "relation_status":handoff.relation_status,
        "relation_statement":handoff.relation_statement,
        "candidate_targets":list(handoff.candidate_targets),
        "target_effect":handoff.target_effect,
        "bridge_license":handoff.bridge_license,
        "duplication_status":handoff.duplication_status,
        "authority_state":handoff.authority_state,
        "review_trigger":handoff.review_trigger,
        "status":status,
        "target_mutated":False,
    }


def persist_queue_entry(
    path:Path,
    entry:Mapping[str,Any],
    *,
    expected_fingerprint:str|None=None,
)->dict[str,Any]:
    path=Path(path)
    if path.exists():
        raw=json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw,dict) or not isinstance(raw.get("items"),list):
            raise TransferCoreError("TRANSFER_QUEUE_INVALID")
    else:
        raw={"schema_version":1,"items":[]}

    before=_fingerprint(raw)
    if expected_fingerprint is not None and before!=expected_fingerprint:
        raise TransferCoreError("TRANSFER_QUEUE_STALE_BASELINE")

    items=list(raw["items"])
    transfer_id=str(entry.get("transfer_id",""))
    if not transfer_id:
        raise TransferCoreError("TRANSFER_QUEUE_ID_REQUIRED")
    index=next(
        (i for i,row in enumerate(items)
         if isinstance(row,Mapping) and str(row.get("transfer_id"))==transfer_id),
        None,
    )
    if index is None:
        items.append(dict(entry))
        action="created"
    else:
        merged=dict(items[index])
        merged.update(dict(entry))
        items[index]=merged
        action="updated"

    candidate={"schema_version":1,"items":items}
    rendered=json.dumps(candidate,indent=2,sort_keys=True,default=str)+"\n"
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix="transfercore-",suffix=".json",dir=path.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as handle:
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    after=_fingerprint(candidate)
    return {
        "status":"QUEUED",
        "action":action,
        "transfer_id":transfer_id,
        "before_fingerprint":before,
        "after_fingerprint":after,
        "target_mutated":False,
    }


def execute_authorized_target_transition(
    handoff:TransferHandoff,
    binding:TargetAuthorityBinding|None,
    authorization:TargetMutationAuthorization|None,
    target_state:Any,
    *,
    apply_fn:Callable[[Any,TransferHandoff],Any],
    verify_fn:Callable[[Any,TransferHandoff],bool],
)->TargetMutationResult:
    target_id=handoff.candidate_targets[0] if handoff.candidate_targets else ""
    ledger=[
        TransferLedgerEvent(
            TransferLedgerStage.HANDOFF_EMITTED,handoff.handoff_id,target_id,
            (handoff.relation_status,),
        )
    ]
    if handoff.relation_status!=TransferStatus.ADMITTED.value:
        return TargetMutationResult("OPEN",target_id,target_state,False,tuple(ledger),False)
    if binding is None or binding.target_id!=target_id:
        return TargetMutationResult("OPEN",target_id,target_state,False,tuple(ledger),False)
    if (
        authorization is None
        or not authorization.granted
        or authorization.target_id!=target_id
        or authorization.authority_ref!=binding.authority_ref
    ):
        return TargetMutationResult("OPEN",target_id,target_state,False,tuple(ledger),False)

    ledger.append(TransferLedgerEvent(
        TransferLedgerStage.TARGET_AUTHORIZED,handoff.handoff_id,target_id,
        authorization.evidence,
    ))
    next_state=apply_fn(target_state,handoff)
    ledger.append(TransferLedgerEvent(
        TransferLedgerStage.TARGET_MUTATED,handoff.handoff_id,target_id,
        (authorization.operation,),
    ))
    verified=bool(verify_fn(next_state,handoff))
    ledger.append(TransferLedgerEvent(
        TransferLedgerStage.TARGET_VERIFIED,handoff.handoff_id,target_id,
        ("PASS" if verified else "FAIL",),
    ))
    return TargetMutationResult(
        "VERIFIED" if verified else "OPEN",
        target_id,
        next_state,
        verified,
        tuple(ledger),
        not verified,
    )


def apply_transfer_feedback(
    result:TransferCoreResult,
    *,
    target_id:str,
    target_verified:bool,
    changed_relation:Mapping[str,Any]|None=None,
)->dict[str,Any]:
    matches=[rel for rel in result.relations if rel.target_id==target_id]
    if not matches:
        raise KeyError("TRANSFERCORE_FEEDBACK_TARGET_UNKNOWN")
    rel=matches[-1]
    return {
        "source_ids":result.sources and tuple(s.source_id for s in result.sources) or (),
        "target_id":target_id,
        "prior_relation_status":rel.status.value,
        "target_verified":bool(target_verified),
        "relation_recompute_required":bool(changed_relation) or not target_verified,
        "changed_relation":dict(changed_relation or {}),
        "reentry_required":bool(changed_relation) or not target_verified,
        "target_mutated":False,
    }


def transfer_core_adapter(current:Any,plan:Any)->dict[str,Any]:
    packet=current.get("packet",current) if isinstance(current,Mapping) else {}
    raw_source=packet.get("transfer_source")
    raw_targets=packet.get("transfer_targets",())
    if not isinstance(raw_source,TransferSource):
        return {
            "status":"OPEN",
            "execution_truth":"OPEN",
            "result":{"blocker":"TRANSFER_SOURCE_REQUIRED"},
            "material_delta":False,
            "hf2_local_close":True,
            "evidence":("runtime/transfer_core.py",),
        }
    evaluator=packet.get("transfer_relation_evaluator")
    discover=packet.get("transfer_target_discovery")
    out=run_transfer_core(
        raw_source,
        candidate_targets=raw_targets,
        discover_targets=discover if callable(discover) else None,
        evaluate_relation=evaluator if callable(evaluator) else None,
    )
    terminal=out.status not in {"OPEN","BLOCKED","CONFLICT"}
    return {
        "status":"EXECUTED" if terminal else out.status,
        "execution_truth":"IMPLEMENTATION_EXECUTED" if terminal else out.status,
        "result":asdict(out),
        "material_delta":False,
        "hf2_live_local":False,
        "hf2_local_close":True,
        "trc_terminal":True,
        "hf1_disposition":"STABLE",
        "evidence":(
            "runtime/transfer_core.py",
            "architecture/TRANSFERCORE_FULL_TOOL_001_2026-09-27.md",
        ),
    }
