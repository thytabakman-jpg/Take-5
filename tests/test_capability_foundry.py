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
    )
    assert r.disposition == FoundryDisposition.REJECT

def test_complete_novel_candidate_only_requests_admission():
    r=CapabilityFoundry().evaluate(
        spec(),
        functionally_subsumed=never_subsumed,
        material_goal_gain=always_gain,
        architecture_compatible=compatible,
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
    )
    assert r.disposition == FoundryDisposition.SUBSUME

def test_incomplete_contract_remains_open():
    r=CapabilityFoundry().evaluate(
        spec(transform=""),
        functionally_subsumed=never_subsumed,
        material_goal_gain=always_gain,
        architecture_compatible=compatible,
    )
    assert r.disposition == FoundryDisposition.OPEN

def test_failed_gain_or_compatibility_remains_open():
    r=CapabilityFoundry().evaluate(
        spec(),
        functionally_subsumed=never_subsumed,
        material_goal_gain=lambda x: False,
        architecture_compatible=lambda x: False,
    )
    assert r.disposition == FoundryDisposition.OPEN
