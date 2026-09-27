import sys
import json
from pathlib import Path
sys.path.insert(0,"runtime")

from direct_tool_command_gateway import direct_tool_ids,bind_direct_tool_commands
from project_manager import (
    CORE_COORDINATES,
    ProjectEvent,
    WorkPackage,
    assess_project,
    improvementcore_handoff,
    transfer_evidence_candidate,
)
from tool_manifest import manifest_for,reconstructs
from tool_run_registry import CONFIGURED_RUNS


def package(project_id="project-manager"):
    coordinates={c:{"status":"CURRENT"} for c in CORE_COORDINATES}
    authority={c:f"{c.upper()}.md" for c in CORE_COORDINATES}
    return {
        "project_id":project_id,
        "coordinates":coordinates,
        "authority_registry":authority,
        "evidence_refs":("projects/project-manager/EVIDENCE.md",),
    }


def test_project_manager_is_registered_full_configured_tool():
    assert "ProjectManager" in CONFIGURED_RUNS
    spec=CONFIGURED_RUNS["ProjectManager"]
    assert spec.complete()
    assert direct_tool_ids("run project manager")==("ProjectManager",)
    bound=bind_direct_tool_commands("run project management tool")
    assert bound.complete
    plan=bound.bindings[0].plan
    assert len(plan.cells)==36
    assert len(plan.questions)==22*36
    assert len(plan.cognitive)==4*36
    assert plan.recurrence_engine=="HF002"


def test_project_manager_manifest_reconstructs_protected_identity():
    required=CONFIGURED_RUNS["ProjectManager"].protected_behaviors
    manifest=manifest_for("ProjectManager")
    assert manifest.complete()
    assert reconstructs("ProjectManager",required)


def test_project_manager_valid_package_closes_relatively():
    out=assess_project(package())
    assert out.status=="CLOSED_RELATIVE"
    assert out.missing_coordinates==()
    assert out.authority_gaps==()
    assert out.authority_conflicts==()


def test_project_manager_preserves_missing_coordinate_as_open():
    p=package()
    del p["coordinates"]["verification"]
    out=assess_project(p)
    assert out.status=="OPEN"
    assert out.missing_coordinates==("verification",)


def test_project_manager_detects_multiple_authorities():
    p=package()
    p["authority_registry"]["goal"]=("GOAL.md","OTHER_GOAL.md")
    out=assess_project(p)
    assert out.status=="CONFLICT"
    assert out.authority_conflicts==("goal",)


def test_project_manager_keeps_wbs_and_schedule_as_distinct_authorities():
    p=package()
    p["authority_registry"]["deliverables"]="PLAN.md"
    p["authority_registry"]["schedule"]="PLAN.md"
    out=assess_project(p)
    assert out.status=="CONFLICT"
    assert "WBS_SCHEDULE_AUTHORITY_COLLAPSED" in out.package_conflicts


def test_change_routes_to_smallest_owning_authority_without_mutating_project():
    p=package()
    event=ProjectEvent(
        event_id="E1",
        request="change the schedule",
        affected_coordinates=("schedule",),
        operation_class="MODIFY",
        effect_class="TARGET_TRANSFORM",
        authority_ref="USER:E1",
    )
    out=assess_project(
        p,
        event=event,
        impact_coordinates=("dependencies",),
        tests=("schedule-regression",),
    )
    assert out.delta.status=="READY"
    assert out.delta.owners==("SCHEDULE.md",)
    assert out.delta.affected_coordinates==("schedule",)
    assert out.delta.impact_coordinates==("dependencies",)
    assert out.reentry_required


def test_unlicensed_target_transform_fails_open():
    p=package()
    event=ProjectEvent(
        event_id="E2",
        request="replace the goal",
        affected_coordinates=("goal",),
        operation_class="MODIFY",
        effect_class="TARGET_TRANSFORM",
    )
    out=assess_project(p,event=event)
    assert out.status=="OPEN"
    assert out.delta.status=="OPEN"


def test_project_manager_manages_itself_without_special_bypass():
    self_out=assess_project(package("project-manager"))
    other_out=assess_project(package("other-project"))
    assert self_out.status==other_out.status=="CLOSED_RELATIVE"
    assert self_out.project_id=="project-manager"


def test_improvementcore_handoff_is_evidence_only_and_non_authorizing():
    work=WorkPackage(
        work_id="W1",
        target_coordinate="evidence",
        target_object="research gap",
        operation_class="RECONSTRUCT",
        effect_class="EVIDENCE_ONLY",
        success="evidence gap resolved or typed OPEN",
    )
    out=assess_project(package(),work=(work,))
    handoff=improvementcore_handoff(out)
    assert handoff.effect_class=="EVIDENCE_ONLY"
    assert handoff.authority=="NONE"
    assert handoff.work==(work,)


def test_transfercore_boundary_stays_evidence_only_while_identity_open():
    out=assess_project(package())
    transfer=transfer_evidence_candidate(
        out,
        {"lesson":"one owner per mutable object"},
        transfercore_identity_status="OPEN",
    )
    assert transfer.status=="OPEN_TRANSFERCORE_IDENTITY"
    assert transfer.effect_class=="EVIDENCE_ONLY"
    assert not transfer.grants_authority


def test_checked_in_self_project_package_is_managed_by_same_runtime():
    root=Path(__file__).resolve().parents[1]
    project=json.loads(
        (root/"projects"/"project-manager"/"PROJECT_STATE.json").read_text()
    )
    out=assess_project(project)
    assert out.project_id=="project-manager"
    assert out.status=="CLOSED_RELATIVE"
    assert out.missing_coordinates==()
    assert out.authority_gaps==()
    assert out.package_conflicts==()
