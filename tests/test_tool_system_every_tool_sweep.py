import sys
from pathlib import Path
sys.path.insert(0,"runtime")

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


def test_actual_project_manager_input_does_not_invent_missing_project_coordinates():
    project=actual_project_manager_input()
    assert set(project["coordinates"])<=set(project["authority_registry"])
    assert "schedule" not in project["coordinates"]
    assert "resources" not in project["coordinates"]
    assert "communications" not in project["coordinates"]


def test_every_tool_sweep_emits_exactly_one_disposition_per_registered_tool():
    receipt=run()
    rows=receipt["tool_conductor"]["results"]
    assert len(rows)==len(MATERIAL_TOOLS)
    assert tuple(row["tool_id"] for row in rows)==tuple(MATERIAL_TOOLS)
    assert receipt["registered_tool_count"]==len(MATERIAL_TOOLS)


def test_development_audits_are_live():
    dev=development_audits()
    assert dev["current_portfolio_identity"]["status"]=="CLOSED_RELATIVE"
    assert dev["full_invocation_portfolio"]["status"]=="CLOSED_RELATIVE"
    assert dev["protected_transition_portfolio"]["status"] in {"PASS","CLOSED_RELATIVE"}
    assert dev["tool_project_package_audit"]["registry_parity"] is True
