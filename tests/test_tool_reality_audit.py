import sys
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
