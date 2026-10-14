"""Mandatory project-state transaction gate for admitted ProjectManager mutations."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from currentness_audit import Currentness, CurrentnessReceipt, assess as assess_currentness
from rho128_policy import needs_reselection
from state_commit import CommitRequest, CommitReceipt, StateRole, authorize_commit
from tool_run_closure import (
    Consequence,
    ConsumerState,
    Disposition,
    StageResult,
    run_tool_run_closure,
)

ACCOUNTED_DISPOSITIONS={"CURRENT","SUPERSEDED","OPEN","BLOCKED"}


class ProjectStateTransactionError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProjectObjectDisposition:
    object_id:str
    disposition:str
    built_basis:str
    latest_basis:str
    delta:tuple[str,...]=()
    protected:tuple[str,...]=()
    evidence:tuple[str,...]=()
    obligations:tuple[str,...]=()
    dependents:tuple[str,...]=()
    behavior_preserved:bool=True
    local_patch_available:bool=True
    reverified:bool=False
    resume_condition:str|None=None


@dataclass(frozen=True)
class ProjectStateTransactionResult:
    transaction_id:str
    project_id:str
    status:str
    base_version:str
    observed_head:str
    commit_head:str
    changed_objects:tuple[str,...]
    affected_cone:tuple[str,...]
    cone_recomputed:bool
    currentness:tuple[CurrentnessReceipt,...]
    unresolved_open:tuple[str,...]
    unresolved_blocked:tuple[str,...]
    blocker:str|None
    closure_status:str
    closure_accounted_count:int
    commit_receipt:CommitReceipt|None
    icc128_reselection_required:bool
    improvementcore_handoff:tuple[str,...]


def affected_cone(changed_objects:Iterable[str],dependency_graph:Mapping[str,Iterable[str]])->tuple[str,...]:
    """Changed objects plus every transitive dependent, in stable traversal order."""
    queue=deque(str(x) for x in changed_objects if str(x))
    seen=set()
    ordered=[]
    while queue:
        node=queue.popleft()
        if node in seen:
            continue
        seen.add(node)
        ordered.append(node)
        for dependent in dependency_graph.get(node,()):
            dep=str(dependent)
            if dep and dep not in seen:
                queue.append(dep)
    return tuple(ordered)


def _manual_receipt(obj:ProjectObjectDisposition,*,status:Currentness,action:str)->CurrentnessReceipt:
    return CurrentnessReceipt(
        component=obj.object_id,
        built_basis=obj.built_basis,
        latest_basis=obj.latest_basis,
        protected=tuple(obj.protected),
        delta=tuple(obj.delta),
        status=status,
        action=action,
        evidence=tuple(obj.evidence),
        obligations=tuple(obj.obligations),
        dependents=tuple(obj.dependents),
        reverified=bool(obj.reverified),
    )


def _currentness_receipt(obj:ProjectObjectDisposition)->CurrentnessReceipt:
    disposition=str(obj.disposition).upper()
    if disposition=="SUPERSEDED":
        return _manual_receipt(obj,status=Currentness.SUPERSEDED,action="SUPERSEDE")
    if disposition in {"OPEN","BLOCKED"}:
        return _manual_receipt(obj,status=Currentness.OPEN,action=f"ROUTED_{disposition}")
    if disposition!="CURRENT":
        return _manual_receipt(obj,status=Currentness.OPEN,action=f"INVALID_DISPOSITION:{disposition}")
    if obj.built_basis!=obj.latest_basis and not obj.delta:
        return _manual_receipt(obj,status=Currentness.OPEN,action="BASIS_MISMATCH_WITHOUT_DELTA")
    return assess_currentness(
        component=obj.object_id,
        built_basis=obj.built_basis,
        latest_basis=obj.latest_basis,
        protected=obj.protected,
        delta=obj.delta,
        behavior_preserved=obj.behavior_preserved,
        local_patch_available=obj.local_patch_available,
        evidence=obj.evidence,
        obligations=obj.obligations,
        dependents=obj.dependents,
        reverified=obj.reverified,
    )


def _currentness_closed(receipt:CurrentnessReceipt)->bool:
    return (
        receipt.status in {Currentness.CURRENT,Currentness.SUPERSEDED}
        or (receipt.status==Currentness.PATCH and receipt.reverified)
    )


def _result(
    transaction_id,project_id,status,base_version,observed_head,commit_head,
    changed,cone,*,recomputed=False,receipts=(),open_nodes=(),blocked_nodes=(),
    blocker=None,closure_status="NOT_RUN",accounted=0,commit_receipt=None,
    reselection=False,improvementcore=(),
):
    return ProjectStateTransactionResult(
        transaction_id,project_id,status,base_version,observed_head,commit_head,
        tuple(changed),tuple(cone),bool(recomputed),tuple(receipts),tuple(open_nodes),
        tuple(blocked_nodes),blocker,closure_status,int(accounted),commit_receipt,
        bool(reselection),tuple(improvementcore),
    )


def _rebase_result(*,transaction_id,project_id,base_version,observed_head,commit_head,
                   changed_objects,dependency_graph,blocker):
    cone=affected_cone(changed_objects,dependency_graph)
    return _result(
        transaction_id,project_id,"REBASE_REQUIRED",base_version,observed_head,
        commit_head,changed_objects,cone,recomputed=True,blocker=blocker,
        reselection=True,improvementcore=cone,
    )


def run_project_state_transaction(
    *,
    transaction_id:str,
    project_id:str,
    base_version:str,
    observed_head:str,
    commit_head:str,
    changed_objects:Iterable[str],
    dependency_graph:Mapping[str,Iterable[str]],
    object_dispositions:Mapping[str,ProjectObjectDisposition],
    authority_before:Iterable[str],
    authority_after:Iterable[str],
    verification_receipt:str,
    evidence:Iterable[str],
    provenance:Iterable[str],
    latest_dependency_graph:Mapping[str,Iterable[str]]|None=None,
)->ProjectStateTransactionResult:
    """Authorize one coherent commit or return a typed non-commit result.

    Any head drift recomputes the affected cone against the latest supplied graph
    and returns REBASE_REQUIRED. The caller then reruns work on that basis.
    """
    if not transaction_id or not project_id:
        raise ProjectStateTransactionError("TRANSACTION_AND_PROJECT_ID_REQUIRED")
    changed=tuple(dict.fromkeys(str(x) for x in changed_objects if str(x)))
    if not changed:
        raise ProjectStateTransactionError("CHANGED_OBJECT_REQUIRED")
    latest_graph=latest_dependency_graph or dependency_graph

    if observed_head!=base_version:
        return _rebase_result(
            transaction_id=transaction_id,project_id=project_id,
            base_version=base_version,observed_head=observed_head,commit_head=commit_head,
            changed_objects=changed,dependency_graph=latest_graph,
            blocker="BASE_VERSION_STALE_BEFORE_EXECUTION",
        )

    cone=affected_cone(changed,dependency_graph)
    missing=tuple(x for x in cone if x not in object_dispositions)
    if missing:
        return _result(
            transaction_id,project_id,"OPEN",base_version,observed_head,commit_head,
            changed,cone,open_nodes=missing,
            blocker="AFFECTED_OBJECT_DISPOSITION_MISSING:"+",".join(missing),
            improvementcore=missing,
        )

    objects=tuple(object_dispositions[x] for x in cone)
    invalid=tuple(
        obj.object_id for obj in objects
        if str(obj.disposition).upper() not in ACCOUNTED_DISPOSITIONS
    )
    if invalid:
        return _result(
            transaction_id,project_id,"CONFLICT",base_version,observed_head,commit_head,
            changed,cone,blocker="AFFECTED_OBJECT_DISPOSITION_INVALID:"+",".join(invalid),
            improvementcore=invalid,
        )

    receipts=tuple(_currentness_receipt(obj) for obj in objects)
    by_id={r.component:r for r in receipts}
    failures=tuple(
        obj.object_id for obj in objects
        if str(obj.disposition).upper() in {"CURRENT","SUPERSEDED"}
        and not _currentness_closed(by_id[obj.object_id])
    )
    if failures:
        return _result(
            transaction_id,project_id,"OPEN",base_version,observed_head,commit_head,
            changed,cone,receipts=receipts,open_nodes=failures,
            blocker="CURRENTNESS_NOT_REVERIFIED:"+",".join(failures),
            improvementcore=failures,
        )

    open_nodes=tuple(obj.object_id for obj in objects if str(obj.disposition).upper()=="OPEN")
    blocked_nodes=tuple(obj.object_id for obj in objects if str(obj.disposition).upper()=="BLOCKED")

    def harvest_fn(_result,_pre,_post):
        return tuple(
            Consequence(
                referent=obj.object_id,
                effect_class="PROJECT_STATE_SYNC",
                target_state=str(obj.disposition).upper(),
                authority_scope="PROJECTMANAGER_COMMIT",
                source_version=base_version,
                protected_class="PROJECT_STATE",
                payload=obj,
            )
            for obj in objects
        )

    def disposition_fn(consequence,_state):
        status=str(consequence.target_state).upper()
        if status=="OPEN":
            return Disposition.OPEN
        if status=="BLOCKED":
            return Disposition.BLOCKED
        if status=="SUPERSEDED":
            return Disposition.CERTIFIED_NO_EFFECT
        return Disposition.REALIZE

    def realize_fn(consequence,state):
        return StageResult(state,status="REALIZED",evidence=(f"affected:{consequence.referent}",))

    def verify_fn(consequence,state):
        receipt=by_id[consequence.referent]
        return StageResult(
            state,
            status="VERIFIED" if _currentness_closed(receipt) else "OPEN",
            evidence=tuple(receipt.evidence)+(f"currentness:{receipt.status.value}",),
            resume_condition=None if _currentness_closed(receipt) else "CURRENTNESS_REVERIFY",
        )

    def consume_fn(consequence,state):
        return StageResult(
            state,status=ConsumerState.CONSUMED.value,
            evidence=(f"accounted:{consequence.referent}",),
        )

    closure=run_tool_run_closure(
        tool_result={"transaction_id":transaction_id},
        pre_state={"base_version":base_version},
        post_state={"base_version":base_version},
        harvest_fn=harvest_fn,
        disposition_fn=disposition_fn,
        realize_fn=realize_fn,
        verify_fn=verify_fn,
        consume_fn=consume_fn,
        harvest_basis=f"PROJECT_STATE_TRANSACTION:{base_version}",
        harvest_complete=True,
    )

    if closure.certificate.accounted_count!=len(cone):
        unresolved=tuple(dict.fromkeys(open_nodes+blocked_nodes))
        return _result(
            transaction_id,project_id,"OPEN",base_version,observed_head,commit_head,
            changed,cone,receipts=receipts,open_nodes=open_nodes,
            blocked_nodes=blocked_nodes,blocker="AFFECTED_CONE_NOT_FULLY_ACCOUNTED",
            closure_status=closure.certificate.status,
            accounted=closure.certificate.accounted_count,improvementcore=unresolved,
        )

    if commit_head!=base_version:
        return _rebase_result(
            transaction_id=transaction_id,project_id=project_id,
            base_version=base_version,observed_head=observed_head,commit_head=commit_head,
            changed_objects=changed,dependency_graph=latest_graph,
            blocker="HEAD_CHANGED_BEFORE_COMMIT",
        )

    commit_receipt=authorize_commit(
        CommitRequest(
            role=StateRole.SUPERVISORY,
            effect="PROJECT_STATE_TRANSACTION_COMMIT_ONCE",
            target=project_id,
            job=transaction_id,
            baseline=base_version,
            authority_before=frozenset(str(x) for x in authority_before),
            authority_after=frozenset(str(x) for x in authority_after),
            evidence=tuple(str(x) for x in evidence if str(x)),
            provenance=tuple(str(x) for x in provenance if str(x)),
            execution_receipt=f"affected:{len(cone)};accounted:{closure.certificate.accounted_count}",
            verification_receipt=str(verification_receipt),
            status="CLOSED_RELATIVE",
            material=True,
        ),
        require_execution=True,
        require_verification=True,
        require_evidence=True,
    )

    reentry_payload={
        "material_result_delta":True,
        "new_OPEN":bool(open_nodes or blocked_nodes),
        "state_delta_invalidates_prior_selection":True,
    }
    reselection=needs_reselection(reentry_payload)
    unresolved=tuple(dict.fromkeys(open_nodes+blocked_nodes))
    return _result(
        transaction_id,project_id,"COMMITTED",base_version,observed_head,commit_head,
        changed,cone,receipts=receipts,open_nodes=open_nodes,
        blocked_nodes=blocked_nodes,closure_status=closure.certificate.status,
        accounted=closure.certificate.accounted_count,commit_receipt=commit_receipt,
        reselection=reselection,improvementcore=unresolved,
    )
