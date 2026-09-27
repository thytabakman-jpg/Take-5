import sys
import json
from pathlib import Path
sys.path.insert(0,"runtime")

from direct_tool_command_gateway import direct_tool_ids,bind_direct_tool_commands
from project_manager import (
    CORE_COORDINATES,
    DEFINITION_COORDINATES,
    ProjectDefinitionCandidate,
    ProjectEvent,
    WorkPackage,
    assess_project,
    assess_project_definition,
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


def definition_candidate(*,approval=None,blocking=()):
    coordinates={
        "goal":{"X":"learner","T":"change","I":"booklet","Sigma":"observable transfer"},
        "core_object":"question as a structured gap",
        "context_binding":"Sukkos must add nondecorative educational work",
        "mechanism":"distinguish random absence from a structured answerable gap",
        "route":("encounter","model","Sukkos embodiment","transfer"),
        "evidence":"learner can turn an unknown into a question with a closure condition",
        "boundaries":("preserve Project 1","no full build before promotion"),
        "alternatives":("existing partition route","structured-gap route"),
        "open_questions":tuple(blocking),
    }
    return ProjectDefinitionCandidate(
        "sukkos-question-gap",
        coordinates,
        blocking_open=tuple(blocking),
        human_approval_ref=approval,
        evidence_refs=("candidate-definition",),
    )


def test_definition_gate_has_nine_distinct_coordinates():
    assert len(DEFINITION_COORDINATES)==9
    assert DEFINITION_COORDINATES==(
        "goal","core_object","context_binding","mechanism","route",
        "evidence","boundaries","alternatives","open_questions",
    )


def test_definition_ready_does_not_self_promote():
    out=assess_project_definition(definition_candidate())
    assert out.status=="DEFINITION_READY"
    assert out.human_approval_valid is False
    assert out.promotion_ready is False


def test_blocking_open_preserves_exploration_state():
    out=assess_project_definition(
        definition_candidate(blocking=("exact Sukkos embodiment unresolved",))
    )
    assert out.status=="EXPLORATION_OPEN"
    assert out.blocking_open==("exact Sukkos embodiment unresolved",)
    assert out.promotion_ready is False


def test_tool_or_system_cannot_impersonate_human_approval():
    out=assess_project_definition(definition_candidate(approval="TOOL:auto"))
    assert out.status=="EXPLORATION_OPEN"
    assert out.human_approval_valid is False
    assert out.promotion_ready is False


def test_explicit_user_approval_crosses_only_the_promotion_barrier():
    out=assess_project_definition(definition_candidate(approval="USER:approved"))
    assert out.status=="PROMOTION_READY"
    assert out.human_approval_valid is True
    assert out.promotion_ready is True


def test_project_manager_adapter_manages_candidate_without_creating_project():
    from project_manager import project_manager_adapter
    candidate=definition_candidate()
    raw=project_manager_adapter({"candidate":candidate},None)
    assert raw["status"]=="EXECUTED"
    result=raw["result"]
    assert result["definition_assessment"]["status"]=="DEFINITION_READY"
    assert result["promotion_barrier"]["full_project_created"] is False
    assert result["promotion_barrier"]["human_approval_required"] is True
    assert result["improvementcore_handoff"]["effect_class"]=="EVIDENCE_ONLY"
    assert result["improvementcore_handoff"]["authority"]=="NONE"


def test_candidate_and_full_project_cannot_be_bound_as_one_state():
    from project_manager import project_manager_adapter
    raw=project_manager_adapter(
        {"candidate":definition_candidate(),"project":package()},
        None,
    )
    assert raw["status"]=="CONFLICT"
    assert raw["result"]["blocker"]=="PROJECT_AND_CANDIDATE_SIMULTANEOUSLY_BOUND"


def test_current_transfercore_identity_still_does_not_grant_project_authority():
    out=assess_project(package())
    transfer=transfer_evidence_candidate(
        out,
        {"lesson":"transfer admission is not target authority"},
        transfercore_identity_status="FULL_MATH_RECOVERED_CURRENT",
    )
    assert transfer.status=="CANDIDATE_FOR_ADMISSION"
    assert transfer.effect_class=="EVIDENCE_ONLY"
    assert transfer.grants_authority is False
