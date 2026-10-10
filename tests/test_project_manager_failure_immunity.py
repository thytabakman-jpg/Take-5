import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from project_manager import ProjectEvent, WorkPackage, assess_project, project_manager_adapter
from project_manager_integrity import (
    FAILURE_CONTROL_IDS,
    ROOT_INVARIANT_IDS,
    assess_project_integrity,
)


def envelope():
    controls={}
    for control in FAILURE_CONTROL_IDS:
        controls[control]={
            "status":"CURRENT",
            "owner":"FAILURE_PREVENTION_MATRIX.md",
            "evidence":("failure-history",control),
            "tests":("failure-immunity-regression",),
        }
    roots={}
    for root in ROOT_INVARIANT_IDS:
        roots[root]={
            "status":"CURRENT",
            "owner":"FAILURE_PREVENTION_MATRIX.md",
            "evidence":("failure-history",root),
            "tests":("failure-immunity-regression",),
        }
    return controls,roots


def package():
    coordinates={
        key:{"status":"CURRENT"}
        for key in (
            "identity","charter","goal","scope","authority","stakeholders",
            "deliverables","schedule","resources","dependencies","interfaces",
            "raid","questions","evidence","decisions","lessons","changes",
            "lifecycle","verification","communications","handoffs",
        )
    }
    authority={key:f"{key.upper()}.md" for key in coordinates}
    controls,roots=envelope()
    return {
        "project_id":"failure-immunity-fixture",
        "coordinates":coordinates,
        "authority_registry":authority,
        "failure_controls":controls,
        "root_invariants":roots,
        "evidence_refs":("failure-immunity",),
    }


def test_failure_history_has_seventeen_explicit_controls():
    assert len(FAILURE_CONTROL_IDS)==17
    assert len(set(FAILURE_CONTROL_IDS))==17


def test_five_root_generators_are_explicit_closure_invariants():
    assert len(ROOT_INVARIANT_IDS)==5
    assert len(set(ROOT_INVARIANT_IDS))==5


def test_complete_failure_prevention_envelope_is_current():
    out=assess_project_integrity(package())
    assert out.status=="CURRENT"
    assert out.missing_controls==()
    assert out.open_controls==()
    assert out.invalid_controls==()
    assert out.missing_root_invariants==()


def test_missing_failure_control_fails_open_and_generates_remediation_work():
    p=package()
    del p["failure_controls"]["execution_truth"]
    out=assess_project(p)
    assert out.status=="OPEN"
    ids=tuple(w.work_id for w in out.executable_frontier)
    assert "PM-INTEGRITY-CONTROL-execution_truth" in ids
    assert out.reentry_required


def test_stale_failure_control_cannot_silently_close_project():
    p=package()
    p["failure_controls"]["state_currentness"]["status"]="STALE"
    out=assess_project(p)
    assert out.status=="OPEN"
    assert any("state_currentness" in w.work_id for w in out.executable_frontier)


def test_conflicted_failure_control_produces_project_conflict():
    p=package()
    p["failure_controls"]["canonical_authority"]["status"]="CONFLICT"
    out=assess_project(p)
    assert out.status=="CONFLICT"
    assert "PROJECT_INTEGRITY_ENVELOPE_CONFLICT" in out.package_conflicts


def test_current_control_without_evidence_is_invalid_and_open():
    p=package()
    p["failure_controls"]["human_orchestration"]["evidence"]=()
    out=assess_project_integrity(p)
    assert out.status=="OPEN"
    assert any(x.startswith("human_orchestration:") for x in out.invalid_controls)


def test_not_applicable_requires_explicit_reason_and_evidence():
    p=package()
    p["failure_controls"]["artifact_production"]={
        "status":"NOT_APPLICABLE",
        "owner":"FAILURE_PREVENTION_MATRIX.md",
        "evidence":("no-artifact-deliverable",),
        "tests":(),
        "reason":"project has no produced artifact",
    }
    assert assess_project_integrity(p).status=="CURRENT"
    del p["failure_controls"]["artifact_production"]["reason"]
    assert assess_project_integrity(p).status=="OPEN"


def test_target_transform_requires_impact_map_and_regression_tests():
    p=package()
    event=ProjectEvent(
        event_id="T1",
        request="change schedule",
        affected_coordinates=("schedule",),
        operation_class="MODIFY",
        effect_class="TARGET_TRANSFORM",
        authority_ref="USER:T1",
    )
    out=assess_project(p,event=event)
    assert out.status=="OPEN"
    assert out.delta.status=="OPEN"
    assert "IMPACT_MAP_REQUIRED" in out.delta.reason
    assert "REGRESSION_VERIFICATION_REQUIRED" in out.delta.reason


def test_target_transform_with_explicit_impact_and_tests_is_ready_but_not_closed():
    p=package()
    event=ProjectEvent(
        event_id="T2",
        request="change schedule",
        affected_coordinates=("schedule",),
        operation_class="MODIFY",
        effect_class="TARGET_TRANSFORM",
        authority_ref="USER:T2",
    )
    out=assess_project(
        p,
        event=event,
        impact_coordinates=("dependencies",),
        tests=("schedule-regression",),
    )
    assert out.delta.status=="READY"
    assert out.status=="OPEN"
    assert out.reentry_required


def test_executable_frontier_prevents_false_project_closure():
    p=package()
    work=WorkPackage(
        work_id="W1",
        target_coordinate="evidence",
        target_object="source gap",
        operation_class="RECOVER",
        effect_class="EVIDENCE_ONLY",
        success="source gap resolved or typed OPEN",
    )
    out=assess_project(p,work=(work,))
    assert out.status=="OPEN"
    assert out.executable_frontier==(work,)
    assert out.reentry_required


def test_transform_work_package_requires_regression_tests_before_frontier():
    p=package()
    work=WorkPackage(
        work_id="W2",
        target_coordinate="schedule",
        target_object="schedule",
        operation_class="MODIFY",
        effect_class="TARGET_TRANSFORM",
        success="schedule updated",
        authority_ref="USER:W2",
    )
    out=assess_project(p,work=(work,))
    assert out.status=="OPEN"
    assert "W2:INCOMPLETE" in out.blocked_work


def test_open_coordinate_state_prevents_false_closure():
    p=package()
    p["coordinates"]["verification"]["status"]="OPEN"
    out=assess_project(p)
    assert out.status=="OPEN"
    assert "COORDINATE_STATE:verification:OPEN" in out.blocked_work


def test_direct_adapter_exposes_known_failure_integrity():
    p=package()
    out=project_manager_adapter({
        "project":p,
        "basis":"failure-immunity",
        "currentness_binding":{
            "subject_id":p["project_id"],
            "object_identity":"fixture:project:"+p["project_id"],
            "built_generation":"fixture:exact-state-1",
            "latest_generation":"fixture:exact-state-1",
            "identity_verified":True,
        },
    },None)
    assert out["status"]=="EXECUTED"
    integrity=out["result"]["known_failure_integrity"]
    assert integrity["status"]=="CURRENT"
    assert len(integrity["evidence"])>=22


def test_checked_in_project_manager_self_instance_passes_failure_envelope():
    p=json.loads((ROOT/"projects"/"project-manager"/"PROJECT_STATE.json").read_text())
    out=assess_project_integrity(p)
    assert out.status=="CURRENT"
    assert set(p["failure_controls"])==set(FAILURE_CONTROL_IDS)
    assert set(p["root_invariants"])==set(ROOT_INVARIANT_IDS)


def test_failure_matrix_names_every_control_and_root_invariant():
    text=(ROOT/"projects"/"project-manager"/"FAILURE_PREVENTION_MATRIX.md").read_text()
    for item in FAILURE_CONTROL_IDS+ROOT_INVARIANT_IDS:
        assert item in text


def test_every_checked_in_managed_project_state_carries_failure_envelope():
    paths=sorted((ROOT/"projects").glob("*/PROJECT_STATE.json"))
    assert paths
    failures=[]
    for path in paths:
        project=json.loads(path.read_text())
        result=assess_project_integrity(project)
        if result.status!="CURRENT":
            failures.append((str(path.relative_to(ROOT)),result.status))
    assert failures==[]
