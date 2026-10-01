import sys
sys.path.insert(0,"runtime")

from full_invocation_portfolio import audit_full_invocation_portfolio
from tool_run_registry import CONFIGURED_RUNS


def test_every_registered_tool_has_one_full_configured_hf2_invocation_path():
    out=audit_full_invocation_portfolio()
    assert out.status=="CLOSED_RELATIVE",out.failures
    assert out.checked==len(CONFIGURED_RUNS)
    assert out.failures==()



def test_prose_full_configured_run_carries_plain_language_gate():
    prose=CONFIGURED_RUNS["Prose"]
    assert "PROSE_PLAIN_LANGUAGE_GATE" in prose.protected_behaviors
    assert prose.recurrence_engine=="HF002"
