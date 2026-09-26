from runtime.capability_foundry import (
    CapabilityFoundry, CapabilitySpec, CapabilityType, FoundryDisposition
)

def spec(cid="C_NEW", grants=False, transform="x->y"):
    return CapabilitySpec(
        capability_id=cid,
        capability_type=CapabilityType.TOOL,
        trigger="material capability gap",
        input_contract="typed problem state",
        transform=transform,
        output_contract="typed candidate result",
        success="material protected gain",
        failure="OPEN",
        dependencies=("K","C","R"),
        persistence="CANDIDATE",
        grants_authority=grants,
        semantic_object_id=f"TOOL:{cid}",
        mathematical_basis="typed transform/input/output/success/failure contract",
        math_required_coordinates=("input","transform","output","success","failure"),
        math_recovered_coordinates=("input","transform","output","success","failure"),
        semantic_package_current=True,
    )

def never_subsumed(a,b): return False
def always_gain(a): return True
def compatible(a): return True

def test_foundry_cannot_self_authorize():
    r=CapabilityFoundry().evaluate(
        spec(grants=True),
        functionally_subsumed=never_subsumed,
        material_goal_gain=always_gain,
        architecture_compatible=compatible,
        package_verifier=lambda oid: True,
    )
    assert r.disposition == FoundryDisposition.REJECT

def test_complete_novel_candidate_only_requests_admission():
    r=CapabilityFoundry().evaluate(
        spec(),
        functionally_subsumed=never_subsumed,
        material_goal_gain=always_gain,
        architecture_compatible=compatible,
        package_verifier=lambda oid: True,
    )
    assert r.disposition == FoundryDisposition.ADMISSION_REQUEST

def test_duplicate_is_subsumed():
    old=spec("C_OLD")
    f=CapabilityFoundry([old])
    r=f.evaluate(
        spec("C_NEW"),
        functionally_subsumed=lambda a,b: True,
        material_goal_gain=always_gain,
        architecture_compatible=compatible,
        package_verifier=lambda oid: True,
    )
    assert r.disposition == FoundryDisposition.SUBSUME

def test_incomplete_contract_remains_open():
    r=CapabilityFoundry().evaluate(
        spec(transform=""),
        functionally_subsumed=never_subsumed,
        material_goal_gain=always_gain,
        architecture_compatible=compatible,
        package_verifier=lambda oid: True,
    )
    assert r.disposition == FoundryDisposition.OPEN

def test_failed_gain_or_compatibility_remains_open():
    r=CapabilityFoundry().evaluate(
        spec(),
        functionally_subsumed=never_subsumed,
        material_goal_gain=lambda x: False,
        architecture_compatible=lambda x: False,
        package_verifier=lambda oid: True,
    )
    assert r.disposition == FoundryDisposition.OPEN


def test_created_tool_without_math_or_package_remains_open():
    c=CapabilitySpec(
        capability_id="C_UNBOUND",
        capability_type=CapabilityType.TOOL,
        trigger="gap",
        input_contract="x",
        transform="x->y",
        output_contract="y",
        success="closed",
        failure="open",
        persistence="CANDIDATE",
    )
    r=CapabilityFoundry().evaluate(
        c,
        functionally_subsumed=never_subsumed,
        material_goal_gain=always_gain,
        architecture_compatible=compatible,
    )
    assert r.disposition == FoundryDisposition.OPEN
    assert "mathematical_basis_missing" in r.reasons
    assert "required_math_coordinates_unspecified" in r.reasons
    assert "semantic_package_missing_or_stale" in r.reasons


def test_created_tool_with_partial_required_math_remains_open():
    c=CapabilitySpec(
        capability_id="C_PARTIAL",
        capability_type=CapabilityType.TOOL,
        trigger="gap",
        input_contract="x",
        transform="x->y",
        output_contract="y",
        success="closed",
        failure="open",
        persistence="CANDIDATE",
        semantic_object_id="TOOL:C_PARTIAL",
        mathematical_basis="candidate equations",
        math_required_coordinates=("input","transform","output"),
        math_recovered_coordinates=("input","transform"),
        semantic_package_current=True,
    )
    r=CapabilityFoundry().evaluate(
        c,
        functionally_subsumed=never_subsumed,
        material_goal_gain=always_gain,
        architecture_compatible=compatible,
        package_verifier=lambda oid: True,
    )
    assert r.disposition == FoundryDisposition.OPEN
    assert "required_mathematics_unrecovered" in r.reasons


def test_created_tool_cannot_self_assert_package_currentness():
    c=spec("C_SELF")
    r=CapabilityFoundry().evaluate(
        c,
        functionally_subsumed=never_subsumed,
        material_goal_gain=always_gain,
        architecture_compatible=compatible,
    )
    assert r.disposition == FoundryDisposition.OPEN
    assert "semantic_package_missing_or_stale" in r.reasons
