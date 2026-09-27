import sys
sys.path.insert(0, "runtime")

from tool_reality_audit import audit_tool_reality
from tool_run_registry import CONFIGURED_RUNS


def test_strong_tool_reality_cannot_inherit_narrow_configured_identity_closure():
    audit = audit_tool_reality()
    assert audit.checked == len(CONFIGURED_RUNS)
    assert audit.configured_identity_status == "CLOSED_RELATIVE"
    assert audit.status == "OPEN"
    assert audit.explicit_manifest_status == "OPEN"
    assert "ImprovementCore" not in audit.generic_only
    assert "GOAL" not in audit.generic_only
    assert "MultiObject" not in audit.generic_only
    for recovered in ("GDOS","Discriminator","RTC","BiasPerturbation","Diagnosis"):
        assert recovered not in audit.generic_only
    assert set(audit.generic_only)=={"MTA","Architecture","PD","PDAudit"}


def test_missing_native_realizations_are_explicit_not_silently_substituted():
    audit = audit_tool_reality()
    assert audit.native_execution_status == "OPEN"
    expected = {
        "MTA",
        "Architecture",
        "PD",
        "PDAudit",
    }
    assert set(audit.native_unrecovered) == expected
    assert "MT" not in audit.native_unrecovered
    assert "ASSERT" not in audit.native_unrecovered
    assert "ImprovementCore" not in audit.native_unrecovered
    assert "GOAL" not in audit.native_unrecovered
    assert "MultiObject" not in audit.native_unrecovered
