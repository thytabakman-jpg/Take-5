from currentness_audit import assess,Currentness,audit_complete

def test_no_delta_keeps_component():
    r=assess(component="x",built_basis="v2",latest_basis="v2")
    assert r.status==Currentness.CURRENT and r.action=="KEEP"

def test_new_research_defaults_to_small_patch_when_behavior_preserved():
    r=assess(component="hf",built_basis="old",latest_basis="new",protected=["reentry"],delta=["TRC wrapper"],behavior_preserved=True,local_patch_available=True)
    assert r.status==Currentness.PATCH and r.action=="PATCH_IN_PLACE"

def test_behavioral_incompatibility_requires_replacement():
    r=assess(component="selector",built_basis="old",latest_basis="new",delta=["routing law changed"],behavior_preserved=False)
    assert r.status==Currentness.REPLACE

def test_uncertain_delta_stays_open():
    r=assess(component="pd",built_basis="old",latest_basis="new",delta=["unknown"],behavior_preserved=True,local_patch_available=False)
    assert r.status==Currentness.OPEN

def test_unverified_patch_blocks_currentness_closure():
    r=assess(component="x",built_basis="a",latest_basis="b",delta=["d"],behavior_preserved=True,local_patch_available=True)
    assert not audit_complete([r])

def test_reverified_patch_can_close_currentness():
    r=assess(component="x",built_basis="a",latest_basis="b",delta=["d"],behavior_preserved=True,local_patch_available=True,reverified=True)
    assert audit_complete([r])

def test_open_or_replace_blocks_currentness_closure():
    assert not audit_complete([assess(component="x",built_basis="a",latest_basis="b",delta=["d"],behavior_preserved=True,local_patch_available=False)])
