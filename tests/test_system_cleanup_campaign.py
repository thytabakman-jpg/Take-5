import sys
sys.path.insert(0,"runtime")

from system_cleanup_campaign import run_cleanup_campaign


def test_cleanup_campaign_joins_narrow_green_surfaces_without_overclaiming():
    out=run_cleanup_campaign()
    assert out.system_closed is True
    assert out.configured_identity_status=="CLOSED_RELATIVE"
    assert out.protected_transition_status=="PASS"
    assert out.full_invocation_status=="CLOSED_RELATIVE"
    assert out.reachability_status=="CLOSED_RELATIVE"
    assert out.capability_repair==()
    assert out.tool_reality_status=="OPEN"
    assert set(out.native_unrecovered)=={"MTA","Architecture","PD","PDAudit"}
    assert out.status=="OPEN"
