import re
import sys
from pathlib import Path
sys.path.insert(0,"runtime")

from project_manager import CORE_COORDINATES
from tool_run_registry import MATERIAL_TOOLS
from tool_system_every_tool_sweep import (
    actual_project_manager_input,
    capability_inputs,
    development_audits,
    learning_inputs,
    project_summary,
    run,
)


def test_sweep_inputs_cover_all_atomic_capabilities_and_learning_tools():
    summary=project_summary()
    caps=capability_inputs(summary)
    assert set(caps)=={f"C{i:02d}" for i in range(1,50)}
    learning=learning_inputs(summary)
    assert len(learning)==11


def test_actual_project_manager_input_covers_all_native_project_coordinates_after_repair():
    project=actual_project_manager_input()
    assert set(project["coordinates"])==set(CORE_COORDINATES)
    assert set(project["authority_registry"])==set(CORE_COORDINATES)


def test_every_tool_sweep_emits_exactly_one_disposition_per_registered_tool():
    receipt=run()
    rows=receipt["tool_conductor"]["results"]
    assert len(rows)==len(MATERIAL_TOOLS)
    assert tuple(row["tool_id"] for row in rows)==tuple(MATERIAL_TOOLS)
    assert receipt["registered_tool_count"]==len(MATERIAL_TOOLS)
    assert receipt["campaign_status"]=="CLOSED_RELATIVE"
    assert receipt["tool_conductor"]["open_tools"]==()
    assert receipt["tool_conductor"]["status_counts"]=={
        "EXECUTED":len(MATERIAL_TOOLS)-1,
        "EXECUTED_SELF_WITNESS":1,
    }


def test_development_audits_are_live():
    dev=development_audits()
    assert dev["current_portfolio_identity"]["status"]=="CLOSED_RELATIVE"
    assert dev["full_invocation_portfolio"]["status"]=="CLOSED_RELATIVE"
    assert dev["protected_transition_portfolio"]["status"] in {"PASS","CLOSED_RELATIVE"}
    assert dev["tool_project_package_audit"]["registry_parity"] is True


def test_human_tool_index_is_exactly_in_registry_parity():
    root=Path(__file__).resolve().parents[1]
    text=(root/"projects"/"tool-system"/"TOOL_INDEX.md").read_text(encoding="utf-8")
    listed=tuple(re.findall(r"^- \[([^\]]+)\]\(current-tools/",text,flags=re.MULTILINE))
    assert len(listed)==len(MATERIAL_TOOLS)
    assert set(listed)==set(MATERIAL_TOOLS)
    assert f"Current configured tools: {len(MATERIAL_TOOLS)}" in text
