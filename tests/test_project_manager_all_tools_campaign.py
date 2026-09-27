import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from project_manager_all_tools_campaign import (
    BEST_ORDER,
    compact_receipt,
    order_is_exact,
    run_all_tools_campaign,
)
from tool_run_registry import MATERIAL_TOOLS


def _run():
    project=json.loads(
        (ROOT/"projects"/"project-manager"/"PROJECT_STATE.json").read_text(
            encoding="utf-8"
        )
    )
    current=(
        ROOT/"projects"/"project-manager"/"CURRENT_STATE.md"
    ).read_text(encoding="utf-8")
    return run_all_tools_campaign(
        project=project,
        current_state_text=current,
        basis_ref="main:ProjectManager",
    )


def test_best_order_is_exact_current_repertoire_permutation():
    assert order_is_exact()
    assert len(BEST_ORDER)==len(MATERIAL_TOOLS)==94
    assert set(BEST_ORDER)==set(MATERIAL_TOOLS)


def test_every_registered_tool_runs_under_its_registered_recurrence():
    out=_run()
    assert out.tool_count==94
    assert tuple(r.tool_id for r in out.receipts)==BEST_ORDER
    assert all(r.cell_count==36 for r in out.receipts)
    assert all(r.question_count==792 for r in out.receipts)
    assert all(r.cognitive_count==144 for r in out.receipts)

    for receipt in out.receipts:
        if receipt.tool_id=="HF002":
            assert receipt.recurrence_engine=="SELF"
            assert receipt.recurrence_status=="SELF_CLOSE"
        else:
            assert receipt.recurrence_engine=="HF002"
            assert receipt.recurrence_status=="RELATIVE_CLOSE"


def test_first_pass_reaches_end_and_exposes_only_bounded_project_consequences():
    out=_run()
    print(
        "PROJECT_MANAGER_ALL_TOOLS_DEBUG="
        +json.dumps(compact_receipt(out),sort_keys=True,default=str)
    )
    conductor=next(r for r in out.receipts if r.tool_id=="ToolConductor")
    print(
        "PROJECT_MANAGER_TOOLCONDUCTOR_DEBUG="
        +json.dumps(conductor.native_summary,sort_keys=True,default=str)
    )
    assert out.status in {"ACTION_REQUIRED","CLOSED_RELATIVE"}
    assert out.improvementcore_consumed is True
    assert out.toolconductor_complete is True
    assert out.external_open==()
    assert not any(
        f.finding_id=="PM-ALL-003" for f in out.findings
    )

    # Pass 2 begins only after the pass-1 owner-local lifecycle delta has
    # been applied.  No local project-control action may remain.
    current=(
        ROOT/"projects"/"project-manager"/"CURRENT_STATE.md"
    ).read_text(encoding="utf-8")
    assert "Run repository validation, repair any regression" not in current
    assert out.status=="CLOSED_RELATIVE"
    assert out.local_actions==()

    print(
        "PROJECT_MANAGER_ALL_TOOLS_RECEIPT="
        +json.dumps(compact_receipt(out),sort_keys=True,default=str)
    )
