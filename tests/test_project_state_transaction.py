import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from project_manager import (
    CORE_COORDINATES,
    ProjectEvent,
    assess_project,
    project_manager_commit_transaction,
)
from project_manager_integrity import FAILURE_CONTROL_IDS, ROOT_INVARIANT_IDS
from project_state_transaction import (
    ProjectObjectDisposition,
    affected_cone,
    run_project_state_transaction,
)


def disposition(name,status="CURRENT",built="v1",latest="v1",**kwargs):
    return ProjectObjectDisposition(
        object_id=name,
        disposition=status,
        built_basis=built,
        latest_basis=latest,
        evidence=(f"evidence:{name}",),
        **kwargs,
    )


def tx(**overrides):
    graph={"manuscript":("claim_registry","project_page"),"claim_registry":("state",)}
    states={x:disposition(x) for x in ("manuscript","claim_registry","project_page","state")}
    args=dict(
        transaction_id="TX1",
        project_id="p1",
        base_version="v1",
        observed_head="v1",
        commit_head="v1",
        changed_objects=("manuscript",),
        dependency_graph=graph,
        object_dispositions=states,
        authority_before=("project-manager",),
        authority_after=("project-manager",),
        verification_receipt="pytest",
        evidence=("transaction-test",),
        provenance=("test",),
    )
    args.update(overrides)
    return run_project_state_transaction(**args)


def package():
    coordinates={c:{"status":"CURRENT"} for c in CORE_COORDINATES}
    authority={c:f"{c.upper()}.md" for c in CORE_COORDINATES}
    controls={
        c:{
            "status":"CURRENT","owner":"FAILURE_PREVENTION_MATRIX.md",
            "evidence":("failure-history",c),"tests":("failure-immunity-regression",),
        }
        for c in FAILURE_CONTROL_IDS
    }
    roots={
        c:{
            "status":"CURRENT","owner":"CONTROLLER.md",
            "evidence":("failure-history",c),"tests":("failure-immunity-regression",),
        }
        for c in ROOT_INVARIANT_IDS
    }
    return {
        "project_id":"p1","coordinates":coordinates,"authority_registry":authority,
        "failure_controls":controls,"root_invariants":roots,"evidence_refs":("test",),
    }


def test_affected_cone_is_recursive_and_deduplicated():
    graph={"A":("B","C"),"B":("D",),"C":("D",),"D":()}
    assert affected_cone(("A",),graph)==("A","B","C","D")


def test_transaction_commits_once_after_full_affected_cone_accounting():
    out=tx()
    assert out.status=="COMMITTED"
    assert out.affected_cone==("manuscript","claim_registry","project_page","state")
    assert out.closure_accounted_count==4
    assert out.commit_receipt is not None
    assert out.commit_receipt.effect=="PROJECT_STATE_TRANSACTION_COMMIT_ONCE"
    assert out.icc128_reselection_required


def test_missing_affected_object_disposition_fails_open():
    states={
        "manuscript":disposition("manuscript"),
        "claim_registry":disposition("claim_registry"),
    }
    out=tx(object_dispositions=states)
    assert out.status=="OPEN"
    assert out.commit_receipt is None
    assert "project_page" in out.unresolved_open


def test_unverified_patch_cannot_be_called_current():
    states={
        "manuscript":disposition(
            "manuscript",built="v0",latest="v1",delta=("content-change",),reverified=False
        ),
        "claim_registry":disposition("claim_registry"),
        "project_page":disposition("project_page"),
        "state":disposition("state"),
    }
    out=tx(object_dispositions=states)
    assert out.status=="OPEN"
    assert out.blocker.startswith("CURRENTNESS_NOT_REVERIFIED")
    assert out.commit_receipt is None


def test_explicit_open_and_blocked_nodes_are_accounted_and_routed():
    states={
        "manuscript":disposition("manuscript"),
        "claim_registry":disposition("claim_registry",status="OPEN"),
        "project_page":disposition("project_page",status="BLOCKED"),
        "state":disposition("state"),
    }
    out=tx(object_dispositions=states)
    assert out.status=="COMMITTED"
    assert out.closure_status=="BLOCKED"
    assert out.unresolved_open==("claim_registry",)
    assert out.unresolved_blocked==("project_page",)
    assert out.improvementcore_handoff==("claim_registry","project_page")


def test_head_change_recomputes_cone_and_requires_rebase():
    latest={
        "manuscript":("claim_registry","project_page"),
        "claim_registry":("state","new_projection"),
    }
    out=tx(commit_head="v2",latest_dependency_graph=latest)
    assert out.status=="REBASE_REQUIRED"
    assert out.commit_receipt is None
    assert out.cone_recomputed
    assert "new_projection" in out.affected_cone


def test_stale_base_before_execution_recomputes_without_running_commit():
    out=tx(observed_head="v2",commit_head="v2")
    assert out.status=="REBASE_REQUIRED"
    assert out.closure_status=="NOT_RUN"
    assert out.commit_receipt is None


def test_project_manager_ready_delta_uses_transaction_gate():
    p=package()
    event=ProjectEvent(
        event_id="E1",request="change schedule",affected_coordinates=("schedule",),
        operation_class="MODIFY",effect_class="TARGET_TRANSFORM",authority_ref="USER:E1",
    )
    assessment=assess_project(
        p,event=event,impact_coordinates=("dependencies",),tests=("schedule-regression",),
    )
    assert assessment.delta.status=="READY"
    out=project_manager_commit_transaction(
        p,assessment.delta,
        transaction_id="PM-TX",
        base_version="v1",observed_head="v1",commit_head="v1",
        changed_objects=("SCHEDULE.md",),
        dependency_graph={"SCHEDULE.md":("DEPENDENCIES.md",)},
        object_dispositions={
            "SCHEDULE.md":disposition("SCHEDULE.md"),
            "DEPENDENCIES.md":disposition("DEPENDENCIES.md"),
        },
        authority_before=("ProjectManager",),authority_after=("ProjectManager",),
        verification_receipt="schedule-regression",evidence=("PM",),provenance=("E1",),
    )
    assert out.status=="COMMITTED"
    assert out.icc128_reselection_required
