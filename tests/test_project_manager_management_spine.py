import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from project_manager import project_manager_adapter
from project_manager_management_spine import (
    MANDATORY_MANAGEMENT_SPINE,
    run_management_spine,
)


EXPECTED=(
    ("ASSERT","ASSERT"),
    ("GOAL_PRE","GOAL"),
    ("MT","MT"),
    ("PD","PD"),
    ("PDAUDIT","PDAudit"),
    ("GOAL_POST","GOAL"),
    ("CURRENTNESS","CurrentnessAudit"),
    ("QUESTION_WORTH","QuestionWorthAsking"),
)


def _candidate():
    return json.loads(
        (ROOT/"candidates"/"sukkos-question-gap"/"DEFINITION_STATE.json").read_text()
    )


def test_mandatory_management_spine_is_exact_and_goal_brackets_structural_pass():
    assert MANDATORY_MANAGEMENT_SPINE==EXPECTED


def _binding(subject):
    return {
        "subject_id":subject["candidate_id"],
        "object_identity":"fixture:candidate:"+subject["candidate_id"],
        "built_generation":"fixture:exact-state-1",
        "latest_generation":"fixture:exact-state-1",
        "identity_verified":True,
    }


def test_missing_source_currentness_cannot_finish_management_spine():
    candidate=_candidate()
    out=run_management_spine({"candidate":candidate,"basis":"test-main"})
    assert out.status=="OPEN"
    assert out.blocker=="MANAGEMENT_SPINE_CURRENTNESS_OPEN"


def test_wrong_source_identity_cannot_finish_management_spine():
    candidate=_candidate()
    binding=_binding(candidate)
    binding["subject_id"]="different-candidate"
    out=run_management_spine({
        "candidate":candidate,"basis":"test-main","currentness_binding":binding,
    })
    assert out.status=="OPEN"
    assert out.blocker=="MANAGEMENT_SPINE_CURRENTNESS_OPEN"


def test_every_spine_factor_runs_full_configured_hf2():
    candidate=_candidate()
    out=run_management_spine({
        "candidate":candidate,"basis":"test-main",
        "currentness_binding":_binding(candidate),
    })
    assert out.status=="CLOSED_RELATIVE"
    assert tuple((r.stage_id,r.tool_id) for r in out.receipts)==EXPECTED
    assert all(r.cell_count==36 for r in out.receipts)
    assert all(r.question_count==792 for r in out.receipts)
    assert all(r.cognitive_count==144 for r in out.receipts)
    assert all(r.recurrence_engine=="HF002" for r in out.receipts)
    assert all(r.recurrence_status=="RELATIVE_CLOSE" for r in out.receipts)


def test_normal_projectmanager_candidate_run_contains_spine_and_preserves_open():
    candidate=_candidate()
    out=project_manager_adapter({
        "candidate":candidate,"basis":"test-main",
        "currentness_binding":_binding(candidate),
    },None)
    assert out["status"]=="OPEN"
    result=out["result"]
    assert result["definition_assessment"]["status"]=="EXPLORATION_OPEN"
    assert len(result["definition_assessment"]["blocking_open"])==5
    spine=result["management_spine"]
    assert spine["status"]=="CLOSED_RELATIVE"
    assert tuple((r["stage_id"],r["tool_id"]) for r in spine["receipts"])==EXPECTED
    assert result["promotion_barrier"]["full_project_created"] is False


def test_missing_goal_fails_management_spine_open():
    candidate=_candidate()
    candidate["coordinates"]["goal"]=""
    out=run_management_spine({"candidate":candidate,"basis":"test-main"})
    assert out.status=="OPEN"
    assert out.blocker.startswith("MANAGEMENT_SPINE_GOAL_PRE_")
