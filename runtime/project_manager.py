"""Native ProjectManager semantic core.

ProjectManager is a project-control tool, not a domain solver. Its configured
tool run is observer-only. It binds project identity and authority, validates
the project package, preserves OPEN, computes an executable work frontier,
routes bounded change candidates, and emits safe handoffs.

Repository or project mutation remains a separate admitted commit operation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

from project_manager_integrity import assess_project_integrity


CORE_COORDINATES=(
    "identity",
    "charter",
    "goal",
    "scope",
    "authority",
    "stakeholders",
    "deliverables",
    "schedule",
    "resources",
    "dependencies",
    "interfaces",
    "raid",
    "questions",
    "evidence",
    "decisions",
    "lessons",
    "changes",
    "lifecycle",
    "verification",
    "communications",
    "handoffs",
)

DEFINITION_COORDINATES=(
    "goal",
    "core_object",
    "context_binding",
    "mechanism",
    "route",
    "evidence",
    "boundaries",
    "alternatives",
    "open_questions",
)

RECOVERY_OPERATIONS={
    "OBSERVE","DISCOVER","RECOVER","OBJECTIFY","FORMALIZE","COMPARE","AUDIT",
    "VERIFY","DIAGNOSE","RECONSTRUCT",
}
TRANSFORM_OPERATIONS={
    "ARCHITECT","BUILD","MODIFY","TRANSFORM","IMPROVE","REPLACE","PROMOTE",
    "SUPERSEDE","MIGRATE","COMMIT",
}
EFFECT_CLASSES={"EVIDENCE_ONLY","TARGET_TRANSFORM"}


class ProjectManagerError(RuntimeError):
    pass


@dataclass(frozen=True)
class WorkPackage:
    work_id:str
    target_coordinate:str
    target_object:str
    operation_class:str
    effect_class:str
    dependencies:tuple[str,...]=()
    tool_id:str|None=None
    success:str=""
    tests:tuple[str,...]=()
    authority_ref:str|None=None
    status:str="OPEN"

    def structurally_complete(self)->bool:
        base=bool(
            self.work_id
            and self.target_coordinate
            and self.target_object
            and self.operation_class
            and self.effect_class in EFFECT_CLASSES
            and self.success
        )
        if not base:
            return False
        if self.effect_class=="TARGET_TRANSFORM" and not self.tests:
            return False
        return True

    def effect_licensed(self)->bool:
        if self.effect_class=="EVIDENCE_ONLY":
            return True
        return (
            self.effect_class=="TARGET_TRANSFORM"
            and self.operation_class in TRANSFORM_OPERATIONS
            and bool(self.authority_ref)
        )


@dataclass(frozen=True)
class ProjectEvent:
    event_id:str
    request:str
    affected_coordinates:tuple[str,...]
    source:str="USER"
    evidence:tuple[str,...]=()
    operation_class:str="OBSERVE"
    effect_class:str="EVIDENCE_ONLY"
    authority_ref:str|None=None


@dataclass(frozen=True)
class ProjectDelta:
    event_id:str
    owners:tuple[str,...]
    affected_coordinates:tuple[str,...]
    precondition_fingerprint:str
    request:str
    reason:str
    dependencies:tuple[str,...]
    impact_coordinates:tuple[str,...]
    tests:tuple[str,...]
    authority_ref:str|None
    effect_class:str
    status:str


@dataclass(frozen=True)
class ProjectAssessment:
    project_id:str
    status:str
    fingerprint:str
    missing_coordinates:tuple[str,...]
    authority_gaps:tuple[str,...]
    authority_conflicts:tuple[str,...]
    package_conflicts:tuple[str,...]
    executable_frontier:tuple[WorkPackage,...]
    blocked_work:tuple[str,...]
    delta:ProjectDelta|None
    reentry_required:bool
    evidence:tuple[str,...]


@dataclass(frozen=True)
class ImprovementCoreHandoff:
    project_id:str
    project_fingerprint:str
    work:tuple[WorkPackage,...]
    authority:str="NONE"
    effect_class:str="EVIDENCE_ONLY"


@dataclass(frozen=True)
class ProjectDefinitionCandidate:
    candidate_id:str
    coordinates:Mapping[str,Any]
    blocking_open:tuple[str,...]=()
    human_approval_ref:str|None=None
    evidence_refs:tuple[str,...]=()


@dataclass(frozen=True)
class ProjectDefinitionAssessment:
    candidate_id:str
    status:str
    fingerprint:str
    missing_coordinates:tuple[str,...]
    empty_coordinates:tuple[str,...]
    blocking_open:tuple[str,...]
    invalid_blocking_open:tuple[str,...]
    human_approval_ref:str|None
    human_approval_valid:bool
    promotion_ready:bool
    evidence:tuple[str,...]


@dataclass(frozen=True)
class TransferEvidenceCandidate:
    project_id:str
    project_fingerprint:str
    payload:Mapping[str,Any]
    transfercore_identity_status:str
    status:str
    effect_class:str="EVIDENCE_ONLY"
    grants_authority:bool=False


def _plain(value:Any)->Any:
    if hasattr(value,"__dataclass_fields__"):
        return asdict(value)
    if isinstance(value,Mapping):
        return {str(k):_plain(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [_plain(v) for v in value]
    return value


def project_fingerprint(project:Mapping[str,Any])->str:
    payload=json.dumps(_plain(project),sort_keys=True,separators=(",",":"),default=str)
    return sha256(payload.encode("utf-8")).hexdigest()


def _owners_for(registry:Mapping[str,Any],coordinate:str)->tuple[str,...]:
    raw=registry.get(coordinate)
    if raw is None:
        return ()
    if isinstance(raw,str):
        return (raw,) if raw.strip() else ()
    if isinstance(raw,(list,tuple,set)):
        return tuple(str(x) for x in raw if str(x).strip())
    return (str(raw),)


def definition_fingerprint(candidate:ProjectDefinitionCandidate)->str:
    return project_fingerprint({
        "candidate_id":candidate.candidate_id,
        "coordinates":candidate.coordinates,
        "blocking_open":candidate.blocking_open,
        "human_approval_ref":candidate.human_approval_ref,
        "evidence_refs":candidate.evidence_refs,
    })


def _definition_value_present(value:Any)->bool:
    if value is None:
        return False
    if isinstance(value,str):
        return bool(value.strip())
    if isinstance(value,(list,tuple,set,frozenset,dict)):
        return bool(value)
    return True


def assess_project_definition(
    candidate:ProjectDefinitionCandidate,
)->ProjectDefinitionAssessment:
    if not isinstance(candidate,ProjectDefinitionCandidate):
        raise ProjectManagerError("PROJECT_DEFINITION_CANDIDATE_REQUIRED")
    if not candidate.candidate_id.strip():
        raise ProjectManagerError("PROJECT_DEFINITION_CANDIDATE_ID_REQUIRED")
    if not isinstance(candidate.coordinates,Mapping):
        raise ProjectManagerError("PROJECT_DEFINITION_COORDINATES_MAPPING_REQUIRED")

    missing=tuple(c for c in DEFINITION_COORDINATES if c not in candidate.coordinates)
    empty=tuple(
        c for c in DEFINITION_COORDINATES
        if c in candidate.coordinates
        and c!="open_questions"
        and not _definition_value_present(candidate.coordinates.get(c))
    )

    raw_open=candidate.coordinates.get("open_questions",())
    if isinstance(raw_open,str):
        open_questions=(raw_open,)
    elif isinstance(raw_open,(list,tuple,set,frozenset)):
        open_questions=tuple(str(x) for x in raw_open)
    else:
        open_questions=()

    blocking=tuple(str(x) for x in candidate.blocking_open if str(x))
    invalid_blocking=tuple(x for x in blocking if x not in set(open_questions))

    approval_ref=(
        str(candidate.human_approval_ref).strip()
        if candidate.human_approval_ref is not None else None
    )
    approval_valid=bool(approval_ref and approval_ref.startswith("USER:"))
    invalid_approval=bool(approval_ref and not approval_valid)

    ready=not (missing or empty or blocking or invalid_blocking or invalid_approval)
    promotion_ready=bool(ready and approval_valid)

    if promotion_ready:
        status="PROMOTION_READY"
    elif ready:
        status="DEFINITION_READY"
    else:
        status="EXPLORATION_OPEN"

    return ProjectDefinitionAssessment(
        candidate_id=candidate.candidate_id,
        status=status,
        fingerprint=definition_fingerprint(candidate),
        missing_coordinates=missing,
        empty_coordinates=empty,
        blocking_open=blocking,
        invalid_blocking_open=invalid_blocking,
        human_approval_ref=approval_ref,
        human_approval_valid=approval_valid,
        promotion_ready=promotion_ready,
        evidence=tuple(str(x) for x in candidate.evidence_refs if str(x)),
    )


def validate_project_package(project:Mapping[str,Any])->tuple[
    tuple[str,...],tuple[str,...],tuple[str,...],tuple[str,...]
]:
    if not isinstance(project,Mapping):
        raise ProjectManagerError("PROJECT_MAPPING_REQUIRED")
    project_id=str(project.get("project_id","")).strip()
    if not project_id:
        raise ProjectManagerError("PROJECT_ID_REQUIRED")

    coordinates=project.get("coordinates")
    if not isinstance(coordinates,Mapping):
        raise ProjectManagerError("PROJECT_COORDINATES_MAPPING_REQUIRED")

    authority_registry=project.get("authority_registry")
    if not isinstance(authority_registry,Mapping):
        raise ProjectManagerError("PROJECT_AUTHORITY_REGISTRY_REQUIRED")

    missing=tuple(c for c in CORE_COORDINATES if c not in coordinates)
    gaps=[]
    conflicts=[]
    for coordinate in CORE_COORDINATES:
        owners=_owners_for(authority_registry,coordinate)
        if not owners:
            gaps.append(coordinate)
        elif len(set(owners))!=1:
            conflicts.append(coordinate)

    package_conflicts=[]
    deliverable_owner=_owners_for(authority_registry,"deliverables")
    schedule_owner=_owners_for(authority_registry,"schedule")
    if deliverable_owner and schedule_owner and deliverable_owner==schedule_owner:
        package_conflicts.append("WBS_SCHEDULE_AUTHORITY_COLLAPSED")

    return missing,tuple(gaps),tuple(conflicts),tuple(package_conflicts)


def _coordinate_state_blockers(project:Mapping[str,Any])->tuple[str,...]:
    coordinates=project.get("coordinates",{})
    blockers=[]
    bad={"OPEN","BLOCKED","STALE","PENDING","UNKNOWN","UNVERIFIED","CONFLICT"}
    if isinstance(coordinates,Mapping):
        for coordinate,value in coordinates.items():
            if not isinstance(value,Mapping):
                continue
            status=str(value.get("status","")).strip().upper()
            if status in bad:
                blockers.append(f"COORDINATE_STATE:{coordinate}:{status}")
    return tuple(blockers)


def executable_frontier(
    work:Iterable[WorkPackage],
    *,
    completed:Iterable[str]=(),
)->tuple[tuple[WorkPackage,...],tuple[str,...]]:
    completed_ids=frozenset(str(x) for x in completed)
    frontier=[]
    blocked=[]
    seen=set()

    for item in tuple(work):
        if not isinstance(item,WorkPackage):
            raise ProjectManagerError("WORK_PACKAGE_REQUIRED")
        if item.work_id in seen:
            blocked.append(f"{item.work_id}:DUPLICATE_WORK_ID")
            continue
        seen.add(item.work_id)

        if not item.structurally_complete():
            blocked.append(f"{item.work_id}:INCOMPLETE")
            continue
        if item.target_coordinate not in CORE_COORDINATES:
            blocked.append(f"{item.work_id}:UNKNOWN_COORDINATE")
            continue
        if not set(item.dependencies)<=completed_ids:
            blocked.append(f"{item.work_id}:DEPENDENCIES_OPEN")
            continue
        if not item.effect_licensed():
            blocked.append(f"{item.work_id}:EFFECT_UNLICENSED")
            continue
        if item.status in {"COMPLETE","CLOSED","SUPERSEDED"}:
            continue
        if item.status in {"BLOCKED","CONFLICT"}:
            blocked.append(f"{item.work_id}:{item.status}")
            continue
        frontier.append(item)

    return tuple(frontier),tuple(blocked)


def route_event(
    project:Mapping[str,Any],
    event:ProjectEvent,
    *,
    impact_coordinates:Iterable[str]=(),
    tests:Iterable[str]=(),
)->ProjectDelta:
    if not isinstance(event,ProjectEvent):
        raise ProjectManagerError("PROJECT_EVENT_REQUIRED")
    if not event.event_id or not event.request:
        raise ProjectManagerError("PROJECT_EVENT_ID_AND_REQUEST_REQUIRED")
    unknown=tuple(c for c in event.affected_coordinates if c not in CORE_COORDINATES)
    if unknown:
        raise ProjectManagerError("PROJECT_EVENT_UNKNOWN_COORDINATES:"+",".join(unknown))

    registry=project["authority_registry"]
    owners=[]
    unresolved=[]
    conflicts=[]
    for coordinate in event.affected_coordinates:
        found=_owners_for(registry,coordinate)
        if not found:
            unresolved.append(coordinate)
        elif len(set(found))!=1:
            conflicts.append(coordinate)
        else:
            owners.append(found[0])

    status="READY"
    reasons=["ROUTE_TO_CANONICAL_OWNER_AND_IMPACT_MAP"]
    if unresolved:
        status="OPEN"
        reasons.append("AUTHORITY_GAP")
    if conflicts:
        status="CONFLICT"
        reasons.append("AUTHORITY_CONFLICT")

    operation=event.operation_class.upper()
    impact_tuple=tuple(dict.fromkeys(str(x) for x in impact_coordinates if str(x)))
    tests_tuple=tuple(str(x) for x in tests if str(x))
    if operation not in RECOVERY_OPERATIONS|TRANSFORM_OPERATIONS:
        status="OPEN"
        reasons.append("OPERATION_CLASS_OPEN")
    if event.effect_class not in EFFECT_CLASSES:
        status="OPEN"
        reasons.append("EFFECT_CLASS_OPEN")
    if event.effect_class=="TARGET_TRANSFORM":
        if operation not in TRANSFORM_OPERATIONS or not event.authority_ref:
            status="OPEN"
            reasons.append("TRANSFORM_AUTHORITY_REQUIRED")
        if not impact_tuple:
            status="OPEN"
            reasons.append("IMPACT_MAP_REQUIRED")
        if not tests_tuple:
            status="OPEN"
            reasons.append("REGRESSION_VERIFICATION_REQUIRED")

    return ProjectDelta(
        event_id=event.event_id,
        owners=tuple(dict.fromkeys(owners)),
        affected_coordinates=tuple(event.affected_coordinates),
        precondition_fingerprint=project_fingerprint(project),
        request=event.request,
        reason="|".join(reasons),
        dependencies=tuple(str(x) for x in project.get("active_dependencies",())),
        impact_coordinates=impact_tuple,
        tests=tests_tuple,
        authority_ref=event.authority_ref,
        effect_class=event.effect_class,
        status=status,
    )


def assess_project(
    project:Mapping[str,Any],
    *,
    event:ProjectEvent|None=None,
    work:Iterable[WorkPackage]=(),
    completed_work:Iterable[str]=(),
    impact_coordinates:Iterable[str]=(),
    tests:Iterable[str]=(),
)->ProjectAssessment:
    missing,gaps,authority_conflicts,package_conflicts=validate_project_package(project)
    integrity=assess_project_integrity(project)
    integrity_work=tuple(
        WorkPackage(
            work_id=item.work_id,
            target_coordinate=item.target_coordinate,
            target_object=item.target_object,
            operation_class="AUDIT",
            effect_class="EVIDENCE_ONLY",
            success=item.success,
            tests=("project-manager-failure-immunity",),
            status="OPEN",
        )
        for item in integrity.remediation
    )
    frontier,blocked=executable_frontier(
        tuple(work)+integrity_work,
        completed=completed_work,
    )
    blocked=tuple(blocked)+_coordinate_state_blockers(project)
    if integrity.status=="OPEN":
        blocked=blocked+("PROJECT_INTEGRITY_ENVELOPE_OPEN",)
    if integrity.status=="CONFLICT":
        package_conflicts=tuple(package_conflicts)+("PROJECT_INTEGRITY_ENVELOPE_CONFLICT",)
    delta=(
        route_event(project,event,impact_coordinates=impact_coordinates,tests=tests)
        if event is not None else None
    )

    status="CLOSED_RELATIVE"
    if authority_conflicts or package_conflicts or (delta and delta.status=="CONFLICT"):
        status="CONFLICT"
    elif missing or gaps or blocked or frontier or (delta and delta.status=="OPEN"):
        status="OPEN"

    reentry=bool(
        frontier
        or integrity.status!="CURRENT"
        or (delta and delta.status=="READY")
    )
    evidence=tuple(str(x) for x in project.get("evidence_refs",()) if str(x))
    evidence=evidence+(
        f"PROJECT_INTEGRITY:{integrity.status}",
        f"PROJECT_INTEGRITY_CONTROLS:{len(integrity.missing_controls)+len(integrity.open_controls)+len(integrity.invalid_controls)}",
        f"PROJECT_INTEGRITY_ROOTS:{len(integrity.missing_root_invariants)+len(integrity.open_root_invariants)+len(integrity.invalid_root_invariants)}",
    )

    return ProjectAssessment(
        project_id=str(project["project_id"]),
        status=status,
        fingerprint=project_fingerprint(project),
        missing_coordinates=missing,
        authority_gaps=gaps,
        authority_conflicts=authority_conflicts,
        package_conflicts=package_conflicts,
        executable_frontier=frontier,
        blocked_work=blocked,
        delta=delta,
        reentry_required=reentry,
        evidence=evidence,
    )


def improvementcore_handoff(assessment:ProjectAssessment)->ImprovementCoreHandoff:
    return ImprovementCoreHandoff(
        project_id=assessment.project_id,
        project_fingerprint=assessment.fingerprint,
        work=assessment.executable_frontier,
    )


def transfer_evidence_candidate(
    assessment:ProjectAssessment,
    payload:Mapping[str,Any],
    *,
    transfercore_identity_status:str,
)->TransferEvidenceCandidate:
    status=(
        "CANDIDATE_FOR_ADMISSION"
        if transfercore_identity_status=="FULL_MATH_RECOVERED_CURRENT"
        else "OPEN_TRANSFERCORE_IDENTITY"
    )
    return TransferEvidenceCandidate(
        project_id=assessment.project_id,
        project_fingerprint=assessment.fingerprint,
        payload=dict(payload),
        transfercore_identity_status=str(transfercore_identity_status),
        status=status,
    )


def project_manager_adapter(current:Any,plan:Any)->dict[str,Any]:
    if not isinstance(current,Mapping):
        return {
            "status":"OPEN",
            "execution_truth":"OPEN",
            "result":{"blocker":"PROJECT_MANAGER_STATE_MAPPING_REQUIRED"},
            "material_delta":False,
            "hf2_local_close":True,
            "evidence":("runtime/project_manager.py",),
        }

    candidate=current.get("candidate")
    project=current.get("project")

    if candidate is not None and project is not None:
        return {
            "status":"CONFLICT",
            "execution_truth":"CONFLICT",
            "result":{"blocker":"PROJECT_AND_CANDIDATE_SIMULTANEOUSLY_BOUND"},
            "material_delta":False,
            "hf2_local_close":True,
            "evidence":("runtime/project_manager.py",),
        }

    if candidate is not None:
        try:
            candidate_obj=(
                candidate
                if isinstance(candidate,ProjectDefinitionCandidate)
                else ProjectDefinitionCandidate(**candidate)
            )
            from project_manager_management_spine import run_management_spine
            spine=run_management_spine({
                **dict(current),
                "candidate":candidate_obj,
            })
            if spine.status!="CLOSED_RELATIVE":
                return {
                    "status":spine.status,
                    "execution_truth":spine.status,
                    "result":{
                        "blocker":spine.blocker,
                        "management_spine":asdict(spine),
                    },
                    "state":dict(current),
                    "material_delta":False,
                    "hf2_local_close":True,
                    "trc_terminal":True,
                    "evidence":(
                        "runtime/project_manager_management_spine.py",
                        "architecture/PROJECT_MANAGER_FULL_TOOL_MATH_004_2026-09-30.md",
                    ),
                }
            assessment=assess_project_definition(candidate_obj)
        except (ProjectManagerError,TypeError) as exc:
            return {
                "status":"OPEN",
                "execution_truth":"OPEN",
                "result":{"blocker":str(exc)},
                "material_delta":False,
                "hf2_local_close":True,
                "evidence":("runtime/project_manager.py",),
            }

        result={
            "management_spine":asdict(spine),
            "definition_assessment":asdict(assessment),
            "improvementcore_handoff":{
                "candidate_id":assessment.candidate_id,
                "candidate_fingerprint":assessment.fingerprint,
                "blocking_open":assessment.blocking_open,
                "authority":"NONE",
                "effect_class":"EVIDENCE_ONLY",
            },
            "promotion_barrier":{
                "definition_ready":assessment.status in {"DEFINITION_READY","PROMOTION_READY"},
                "human_approval_required":not assessment.human_approval_valid,
                "promotion_ready":assessment.promotion_ready,
                "full_project_created":False,
            },
        }
        semantic_status=(
            "EXECUTED"
            if assessment.status in {"DEFINITION_READY","PROMOTION_READY"}
            else "OPEN"
        )
        return {
            "status":semantic_status,
            "execution_truth":(
                "IMPLEMENTATION_EXECUTED" if semantic_status=="EXECUTED" else "OPEN"
            ),
            "result":result,
            "state":dict(current),
            "material_delta":False,
            "hf2_local_close":True,
            "trc_terminal":True,
            "hf1_disposition":"STABLE",
            "evidence":(
                "runtime/project_manager.py",
                "architecture/PROJECT_MANAGER_FULL_TOOL_MATH_004_2026-09-30.md",
            ),
            "related_objects":("ImprovementCore","ProjectDefinitionCandidate"),
            "dependency_footprint":tuple(DEFINITION_COORDINATES),
        }

    if not isinstance(project,Mapping):
        return {
            "status":"OPEN",
            "execution_truth":"OPEN",
            "result":{"blocker":"PROJECT_OR_CANDIDATE_REQUIRED"},
            "material_delta":False,
            "hf2_local_close":True,
            "evidence":("runtime/project_manager.py",),
        }

    from project_manager_management_spine import run_management_spine
    spine=run_management_spine(dict(current))
    if spine.status!="CLOSED_RELATIVE":
        return {
            "status":spine.status,
            "execution_truth":spine.status,
            "result":{
                "blocker":spine.blocker,
                "management_spine":asdict(spine),
            },
            "state":dict(current),
            "material_delta":False,
            "hf2_local_close":True,
            "trc_terminal":True,
            "evidence":(
                "runtime/project_manager_management_spine.py",
                "architecture/PROJECT_MANAGER_FULL_TOOL_MATH_004_2026-09-30.md",
            ),
        }

    raw_work=current.get("work",())
    work=tuple(x if isinstance(x,WorkPackage) else WorkPackage(**x) for x in raw_work)
    raw_event=current.get("event")
    event=(
        raw_event
        if isinstance(raw_event,ProjectEvent)
        else (ProjectEvent(**raw_event) if isinstance(raw_event,Mapping) else None)
    )
    assessment=assess_project(
        project,
        event=event,
        work=work,
        completed_work=current.get("completed_work",()),
        impact_coordinates=current.get("impact_coordinates",()),
        tests=current.get("tests",()),
    )
    integrity=assess_project_integrity(project)
    result={
        "management_spine":asdict(spine),
        "known_failure_integrity":asdict(integrity),
        "assessment":asdict(assessment),
        "improvementcore_handoff":asdict(improvementcore_handoff(assessment)),
    }
    status=assessment.status
    return {
        "status":"EXECUTED" if status=="CLOSED_RELATIVE" else status,
        "execution_truth":"IMPLEMENTATION_EXECUTED" if status=="CLOSED_RELATIVE" else status,
        "result":result,
        "state":dict(current),
        "material_delta":False,
        "hf2_local_close":True,
        "trc_terminal":True,
        "hf1_disposition":"STABLE",
        "evidence":(
            "runtime/project_manager.py",
            "architecture/PROJECT_MANAGER_FULL_TOOL_MATH_004_2026-09-30.md",
        ),
        "related_objects":("ImprovementCore","TransferCore"),
        "dependency_footprint":tuple(CORE_COORDINATES),
    }
