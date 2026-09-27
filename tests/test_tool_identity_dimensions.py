import sys
sys.path.insert(0,"runtime")

from tool_identity_dimensions import (
    FULL_DIMENSION_NAMES,audit_current_repertoire,identity_for,
)
from tool_run_registry import MATERIAL_TOOLS


def test_every_current_tool_has_question_job_responsibility_and_species():
    for tool_id in MATERIAL_TOOLS:
        x=identity_for(tool_id)
        assert x.complete()
        assert x.question
        assert x.job
        assert x.responsibility
        assert x.mathematical_object


def test_every_current_tool_projects_every_enforced_dimension():
    out=audit_current_repertoire()
    assert out["status"]=="CLOSED_RELATIVE"
    assert out["parity"] is True
    assert out["tool_count"]==len(MATERIAL_TOOLS)
    assert out["projected_count"]==len(MATERIAL_TOOLS)
    assert not out["missing"]
    assert not out["incomplete"]
    required={
        "identity","question","job","responsibility","goal","mathematical_object",
        "native_semantics","inputs","outputs","state","configured_identity",
        "envelope","mode","orchestration","wrapper","geometry","authority",
        "currentness_provenance","lineage","lifecycle","persistence_propagation",
        "runtime_realization","runtime_behavior","executability",
        "controller_reachability","invocation","run_instance","host_capability",
        "dependencies_transfers","semantic_roles","project_memberships",
        "physical_location","backlog_open_obligations","protected_behavior",
        "closure","reentry","recurrence","verification","evidence_receipts",
        "failure_open_policy","admission_promotion","coverage_surface",
        "question_projection","cognitive_projection",
    }
    assert required==set(FULL_DIMENSION_NAMES)


def test_hf1_hf2_jobs_cannot_collapse_into_each_other():
    hf1=identity_for("HF001")
    hf2=identity_for("HF002")
    assert hf1.job!=hf2.job
    assert "fresh" in hf1.responsibility.lower()
    assert "local" in hf2.responsibility.lower()
    assert "global tool selection" in hf2.responsibility.lower()
