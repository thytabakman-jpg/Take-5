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
