import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from project_manager import assess_project
from configured_hf2_execution import execute_configured_with_hf2
from global_tool_execution import build_tool_execution_plan
from mt_semantic_return_gate import run_mt_with_before_return_gate
from tool_run_registry import CONFIGURED_RUNS

BASE=ROOT/"projects"/"sukkos-question-booklet-2-frame-resolution"


def test_project_2_package_closes_relative_without_touching_project_1():
    project=json.loads((BASE/"PROJECT_STATE.json").read_text())
    out=assess_project(project)
    assert out.status=="CLOSED_RELATIVE"
    assert out.missing_coordinates==()
    assert out.authority_gaps==()
    assert out.authority_conflicts==()
    assert out.package_conflicts==()
    assert (ROOT/"projects"/"sukkos-question-booklet"/"EXACT_COPY.md").exists()


def test_exact_copy_has_four_pages_and_core_student_coordinates():
    text=(BASE/"EXACT_COPY.md").read_text()
    assert text.count("# PAGE ")==4
    for label in ("ASSUMES","OPENS","SETTLES"):
        assert label in text
    assert "Why were the earlier days better than these?" in text
    assert "Why is Bridge A stronger than Bridge B?" in text


def test_source_application_boundary_is_explicit():
    copy=(BASE/"EXACT_COPY.md").read_text()
    lock=(BASE/"SOURCE_LOCK.md").read_text()
    assert "Our model is one way to inspect its wording." in copy
    assert "Kohelet calls the question unwise." in lock
    assert "educational application" in lock.lower()


def test_mt_build_witness_runs_full_configured_hf2():
    plan=build_tool_execution_plan(CONFIGURED_RUNS["MT"])
    assert plan.complete
    assert len(plan.cells)==36
    assert len(plan.questions)==792
    assert len(plan.cognitive)==144

    def native():
        def run_mt(state):
            return state,{
                "distinctions":(
                    "QUESTION!=EPISTEMIC_GAP",
                    "PRESUPPOSITION!=OPEN_ISSUE",
                    "SOURCE_CONTENT!=EDUCATIONAL_APPLICATION",
                    "PAGE_3_SUPPORT!=PAGE_4_TRANSFER",
                ),
                "black_boxes":(),
            }
        return run_mt_with_before_return_gate(
            {"project":"sukkos-question-booklet-2-frame-resolution"},
            run_mt=run_mt,
            detect_black_boxes=lambda state,result:result["black_boxes"],
            execute_stage=lambda tool_id,object_id,state:(state,"CLOSED_RELATIVE",False),
        )

    holder={}
    def adapter(state,plan):
        value=native()
        holder["value"]=value
        return {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":value,
            "state":state,
            "material_delta":False,
            "hf2_live_local":False,
            "hf2_local_close":True,
            "trc_terminal":True,
            "hf1_disposition":"STABLE",
            "evidence":("project-2-mt-build-witness",),
        }

    out=execute_configured_with_hf2(
        tool_id="MT",
        plan=plan,
        state={"project":"sukkos-question-booklet-2-frame-resolution"},
        adapter=adapter,
    )
    assert out.status=="RELATIVE_CLOSE"
    assert out.recurrence_engine=="HF002"
    assert holder["value"].status=="CLOSED_RELATIVE"
