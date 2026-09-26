from repertoire_reachability import audit_current_repertoire_reachability
from tool_run_registry import CONFIGURED_RUNS

def test_current_finite_repertoire_has_controller_execution_reachability_evidence():
    out=audit_current_repertoire_reachability()
    assert out.status=="CLOSED_RELATIVE"
    assert out.failures==()
    assert out.identity_checked==len(CONFIGURED_RUNS)
    assert out.transition_checked==len(CONFIGURED_RUNS)
    assert out.bridge_execution_checked==len(CONFIGURED_RUNS)
