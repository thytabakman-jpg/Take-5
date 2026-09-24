from improvement_core import improve

BASE={"identity":"x","type":"system","scope":"local","job":"improve","readings":[],"result_sensitive":[],"selectors":[],"authority":["observe"],"local_authority":["observe"],"provenance":[],"open":[]}

def focus(_): return {"exact_discriminant":True,"independent_local":True}

def test_improvement_core_delegates_and_reenters_until_obligation_closes():
    p=dict(BASE); p["obligations"]=["CHECK_IDENTITY"]
    def c02(x):
        y=dict(x); y["obligations"]=[]; y["identity_checked"]=True; return y
    r=improve(p,{"C02":["CHECK_IDENTITY"]},{"C02":c02},focus)
    assert r.status=="CLOSED_RELATIVE"
    assert r.final_packet["identity_checked"] is True
    assert r.results[0][0]=="C02"

def test_improvement_core_preserves_open_without_reachable_capability():
    p=dict(BASE); p["obligations"]=["UNKNOWN"]
    assert improve(p,{}, {},focus).status=="OPEN"

def test_improvement_core_does_not_loop_same_unresolved_state():
    p=dict(BASE); p["obligations"]=["CHECK_IDENTITY"]
    r=improve(p,{"C02":["CHECK_IDENTITY"]},{"C02":lambda x:dict(x)},focus)
    assert r.status=="CLOSED_RELATIVE" or r.status=="OPEN"
    assert r.rounds<=1
