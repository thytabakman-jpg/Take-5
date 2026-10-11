import sys
from pathlib import Path
sys.path.insert(0, "runtime")

from tool_reality_audit import audit_tool_reality
from tool_run_registry import CONFIGURED_RUNS


def test_strong_tool_reality_closes_only_after_all_layers_agree():
    audit=audit_tool_reality()
    assert audit.checked==len(CONFIGURED_RUNS)
    assert audit.configured_identity_status=="CLOSED_RELATIVE"
    assert audit.explicit_manifest_status=="CLOSED_RELATIVE"
    assert audit.native_execution_status=="CLOSED_RELATIVE"
    assert audit.generic_only==()
    assert audit.native_unrecovered==()
    assert audit.status=="CLOSED_RELATIVE"


def test_recovered_four_remain_environment_bound_not_self_contained():
    audit=audit_tool_reality()
    for tool_id in ("MTA","Architecture","PD","PDAudit"):
        assert tool_id in audit.environment_bound


def test_tool_reality_document_does_not_promote_three_coordinate_audit_to_four_layer_execution():
    """The GOAL consumer must not inherit an impossible/stale audit gate."""
    text=Path("integration/CURRENT_TOOL_REALITY.md").read_text(encoding="utf-8")
    audit=audit_tool_reality()
    status_fields=(
        "configured_identity_status",
        "explicit_manifest_status",
        "native_execution_status",
    )
    assert all(hasattr(audit, field) for field in status_fields)
    assert len(status_fields)==3
    assert "emits **three** check coordinates" in text
    assert "**historical-audit-basis** claim" in text
    assert "three-coordinate strong-reality" in text
    assert "Constructed configured-plan evidence and end-to-end consumer execution remain **separate**" in text
    assert "verifies all four layers" not in text
    assert "current-basis claim" not in text
    assert "fresh four-layer result" not in text
