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
    assert {
        "question","job","responsibility","mathematical_object",
        "native_semantics","wrapper","geometry","protected_behavior",
        "closure","reentry","recurrence","lineage_currentness_runtime",
    }==set(FULL_DIMENSION_NAMES)


def test_hf1_hf2_jobs_cannot_collapse_into_each_other():
    hf1=identity_for("HF001")
    hf2=identity_for("HF002")
    assert hf1.job!=hf2.job
    assert "fresh" in hf1.responsibility.lower()
    assert "local" in hf2.responsibility.lower()
    assert "global tool selection" in hf2.responsibility.lower()
