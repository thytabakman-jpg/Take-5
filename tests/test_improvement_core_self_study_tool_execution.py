import sys
from pathlib import Path

sys.path.insert(0,"runtime")

from improvement_core_self_study import run


def test_self_study_executes_and_consumes_powerful_configured_tools(tmp_path:Path):
    report=run(tmp_path/"self-study.json")

    outputs=tuple(report["configured_tool_outputs"])
    assert [x["tool_id"] for x in outputs]==[
        "CurrentnessAudit",
        "RootCause",
        "QuestionWorthAsking",
        "ASSERT",
    ]
    assert all(x["binding"]["cell_count"]==36 for x in outputs)
    assert all(x["binding"]["wrapper_required"] is True for x in outputs)
    assert report["verification"]["configured_tool_execution_evidence"] is True
    assert report["verification"]["all_configured_tools_full_36"] is True

    root=next(x for x in outputs if x["tool_id"]=="RootCause")
    assert "TOOL_SELECTION_EXECUTION_SEAM_MISSING" in root["result"]["root_candidates"]

    question=next(x for x in outputs if x["tool_id"]=="QuestionWorthAsking")
    assert question["result"]["selected"][0]["question_id"]=="q-execution"

    assertion=next(x for x in outputs if x["tool_id"]=="ASSERT")
    assert assertion["result"]["status"]=="CLOSED"



def test_self_study_consumes_ordered_structured_handoff_causally(tmp_path:Path):
    report=run(tmp_path/"self-study-handoff.json")

    assert report["verification"]["structured_handoff_loaded"] is True
    assert report["verification"]["selected_candidate_reflects_handoff"] is True
    assert report["verification"]["structured_handoff_signal"]=="IC-HOST-CAPABILITY-DISCOVERY"
    assert report["selected_next_candidate"]["id"]=="IC-HOST-CAPABILITY-DISCOVERY"
    assert report["selected_next_candidate"]["upstream_signal_counts"]["IC-HOST-CAPABILITY-DISCOVERY"]==3
    assert report["selected_next_candidate"]["upstream_signal_counts"]["IC-DURABLE-RUN-JOURNAL"]==1

    # Upstream evidence changes selection but cannot self-authorize runtime admission.
    assert report["admission"]["admitted_for_next_implementation_experiment"]==[]
    assert report["admission"]["selected_candidate_status"]=="OPEN_HOST_BOUNDARY"
    assert "universal host boundary remains OPEN" in report["architecture_decision"]
