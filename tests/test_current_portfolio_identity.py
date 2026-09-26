from current_portfolio_identity import audit_current_portfolio_identity
from tool_run_registry import CONFIGURED_RUNS

def test_every_current_configured_tool_has_reconstructible_current_identity():
    out=audit_current_portfolio_identity()
    assert out.status=="CLOSED_RELATIVE"
    assert out.failures==()
    assert out.checked==len(CONFIGURED_RUNS)
