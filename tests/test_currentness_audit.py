from currentness_audit import assess,Currentness,audit_complete

IDENTITY=dict(
    object_identity="tool:x",
    built_generation="git:built",
    latest_generation="git:latest",
    identity_verified=True,
)

def test_no_delta_keeps_component_when_identity_is_verified():
    r=assess(component="x",built_basis="v2",latest_basis="v2",**IDENTITY)
    assert r.status==Currentness.CURRENT and r.action=="KEEP"

def test_mutable_labels_do_not_establish_currentness_without_immutable_identity():
    r=assess(component="x",built_basis="CURRENT",latest_basis="CURRENT")
    assert r.status==Currentness.OPEN
    assert r.action=="RESOLVE_IMMUTABLE_IDENTITY"
    assert not audit_complete([r])

def test_new_research_defaults_to_small_patch_when_behavior_preserved():
    r=assess(component="hf",built_basis="old",latest_basis="new",protected=["reentry"],delta=["TRC wrapper"],behavior_preserved=True,local_patch_available=True,**IDENTITY)
    assert r.status==Currentness.PATCH and r.action=="PATCH_IN_PLACE"

def test_behavioral_incompatibility_requires_replacement():
    r=assess(component="selector",built_basis="old",latest_basis="new",delta=["routing law changed"],behavior_preserved=False,**IDENTITY)
    assert r.status==Currentness.REPLACE

def test_uncertain_delta_stays_open():
    r=assess(component="pd",built_basis="old",latest_basis="new",delta=["unknown"],behavior_preserved=True,local_patch_available=False,**IDENTITY)
    assert r.status==Currentness.OPEN

def test_unverified_patch_blocks_currentness_closure():
    r=assess(component="x",built_basis="a",latest_basis="b",delta=["d"],behavior_preserved=True,local_patch_available=True,**IDENTITY)
    assert not audit_complete([r])

def test_reverified_patch_can_close_currentness():
    r=assess(component="x",built_basis="a",latest_basis="b",delta=["d"],behavior_preserved=True,local_patch_available=True,reverified=True,**IDENTITY)
    assert audit_complete([r])

def test_open_or_replace_blocks_currentness_closure():
    assert not audit_complete([assess(component="x",built_basis="a",latest_basis="b",delta=["d"],behavior_preserved=True,local_patch_available=False,**IDENTITY)])
