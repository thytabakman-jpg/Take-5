from hf_controller import hf1_reentry_route

def test_hf1_world_or_discovery_delta_reenters_observation():
    assert hf1_reentry_route(world_changed=True,discovery_changed=False).action=="REENTER_OBSERVE"
    assert hf1_reentry_route(world_changed=False,discovery_changed=True).action=="REENTER_OBSERVE"

def test_hf1_result_sensitive_delta_reverifies():
    assert hf1_reentry_route(
        world_changed=False,
        discovery_changed=False,
        result_sensitive_delta=True,
    ).action=="REVERIFY"

def test_hf1_no_material_delta_does_not_reenter():
    assert hf1_reentry_route(
        world_changed=False,
        discovery_changed=False,
        result_sensitive_delta=False,
    ).action=="NO_REENTRY"
