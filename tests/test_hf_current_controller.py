from kpd_projection import project,obligation_equivalent
from hf_controller import decide,trc

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
    d=decide(x,{"C02":["CHECK_IDENTITY"],"C03":["CHECK_HISTORY"]},{"exact_discriminant":True})
    assert d.package==("C02",) and d.mode=="CONTRACT_OBSERVE" and d.action=="EXECUTE"

def test_hf_preserves_open_when_no_package_reaches_obligation():
    x=dict(BASE); x["obligations"]=["UNKNOWN"]
    assert decide(x,{},{"exact_discriminant":True}).action=="BLOCKED_OPEN"

def test_trc_reenters_only_on_material_projection_change():
    nxt=dict(BASE); nxt["identity"]="i2"
    assert trc(True,BASE,nxt)=="REENTER_KPD"
    assert trc(False,BASE,nxt)=="NO_REENTRY"
