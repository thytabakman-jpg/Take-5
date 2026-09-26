import sys
sys.path.insert(0,"runtime")

from full_invocation_portfolio import audit_full_invocation_portfolio
from tool_run_registry import CONFIGURED_RUNS


def test_every_registered_tool_has_one_full_configured_hf2_invocation_path():
    out=audit_full_invocation_portfolio()
    assert out.status=="CLOSED_RELATIVE",out.failures
    assert out.checked==len(CONFIGURED_RUNS)
    assert out.failures==()
