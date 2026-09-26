from tool_manifest import OVERRIDES
from tool_manifest_audit import audit_tool_identities
from tool_run_registry import CONFIGURED_RUNS

def test_portfolio_identity_audit_keeps_remaining_generic_only_tools_open():
    audit=audit_tool_identities(CONFIGURED_RUNS,OVERRIDES)
    assert audit.status=="OPEN"
    assert "MT" in audit.explicit
    assert "ASSERT" in audit.explicit
    assert "HF001" in audit.explicit
    assert "ImprovementCore" in audit.generic_only
    assert "GOAL" in audit.generic_only

def test_explicit_subset_can_close_relative():
    audit=audit_tool_identities(("MT","ASSERT","HF001"),OVERRIDES)
    assert audit.status=="CLOSED_RELATIVE"
    assert audit.generic_only==()
