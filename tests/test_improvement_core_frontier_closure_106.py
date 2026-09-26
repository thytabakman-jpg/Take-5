import json
from pathlib import Path

from current_portfolio_identity import audit_current_portfolio_identity
from historical_replay_audit import audit_historical_replays
from relation_kernel import current_relation_basis
from repertoire_reachability import audit_current_repertoire_reachability

ROOT=Path(__file__).resolve().parents[1]

def test_current_regime_frontier_is_closed_relative_not_open_world():
    manifest=json.loads((ROOT/"architecture"/"IMPROVEMENT_CORE_RECOVERY_MANIFEST_082.json").read_text())
    assert manifest["regime_version"]=="090"
    assert manifest["open"]==[]
    assert "UNIVERSAL_HOST_INTERCEPTION_EXTERNAL_NOT_OWNED" in manifest["external_limits"]
    assert manifest["reopen_conditions"]
    assert current_relation_basis().complete()
    assert audit_current_portfolio_identity().status=="CLOSED_RELATIVE"
    reach=audit_current_repertoire_reachability()
    assert reach.status=="CLOSED_RELATIVE"
    assert reach.bridge_execution_checked==reach.identity_checked
    assert audit_historical_replays().status=="PASS"

def test_frontier_closure_does_not_claim_open_world_completeness():
    text=(ROOT/"architecture"/"IMPROVEMENT_CORE_FRONTIER_CLOSURE_106.md").read_text()
    assert "REJECT_GLOBAL_COMPLETION_CRITERION" in text
    assert "EXTERNAL_NOT_OWNED" in text
    assert "This does not assert open-world completeness." in text
