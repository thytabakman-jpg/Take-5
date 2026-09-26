from kpd_projection import project,obligation_equivalent
from hf_controller import decide,trc,hf1_reentry_route

BASE={"identity":"i","type":"t","scope":"s","job":"j","readings":[],"result_sensitive":[],"selectors":[],"authority":[],"provenance":[],"open":[]}

def test_kpd_complete_packet_has_no_manufactured_obligation():
    assert project(BASE).obligations==()

def test_kpd_missing_routing_distinction_becomes_obligation():
    x=dict(BASE); x.pop("identity")
    assert "RESOLVE_IDENTITY" in project(x).obligations

def test_obligation_equivalence_is_separate_from_surface_equality():
    a=dict(BASE); b=dict(BASE); b["readings"]=["extra"]
    assert obligation_equivalent(a,b)

def test_hf_routes_obligation_to_reachable_package_and_mode():
    x=dict(BASE); x["obligations"]=["CHECK_IDENTITY"]
    d=decide(x,{"C02":["CHECK_IDENTITY"],"C03":["CHECK_HISTORY"]},{"exact_discriminant":True,"independent_local":True})
    assert d.package==("C02",) and d.mode=="CONTRACT_OBSERVE_DECOUPLED" and d.action=="EXECUTE"

def test_hf_preserves_open_when_no_package_reaches_obligation():
    x=dict(BASE); x["obligations"]=["UNKNOWN"]
    assert decide(x,{},{"exact_discriminant":True}).action=="BLOCKED_OPEN"

def test_trc_reenters_only_on_material_projection_change():
    nxt=dict(BASE); nxt["identity"]="i2"
    assert trc(True,BASE,nxt)=="REENTER_KPD"
    assert trc(False,BASE,nxt)=="NO_REENTRY"

def test_hf1_world_or_discovery_delta_reenters_observation():
    assert hf1_reentry_route(world_changed=True,discovery_changed=False).action=="REENTER_OBSERVE"
    assert hf1_reentry_route(world_changed=False,discovery_changed=True).action=="REENTER_OBSERVE"

def test_hf1_result_sensitive_delta_reverifies_without_world_or_discovery_change():
    assert hf1_reentry_route(
        world_changed=False,
        discovery_changed=False,
        result_sensitive_delta=True,
    ).action=="REVERIFY"
