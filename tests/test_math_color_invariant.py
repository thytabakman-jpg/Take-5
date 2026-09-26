from math_color_invariant import color_verdict


def test_default_red_when_required_coordinates_unspecified():
    v = color_verdict(
        object_id="HF1",
        job="complete mathematics",
        claim="HF1 is mathematically complete",
        required_coordinates=(),
        coordinate_status={},
    )
    assert v.color == "RED"


def test_partial_object_is_red_for_complete_math_claim():
    v = color_verdict(
        object_id="HF1",
        job="complete mathematics",
        claim="HF1 is mathematically complete",
        required_coordinates=("state_vector","delta_D","delta_R","minimality","integration"),
        coordinate_status={
            "state_vector":"OPEN",
            "delta_D":"PARTIAL",
            "delta_R":"OPEN",
            "minimality":"OPEN",
            "integration":"PARTIAL",
        },
    )
    assert v.color == "RED"
    assert set(v.unresolved_coordinates) == {
        "state_vector","delta_D","delta_R","minimality","integration"
    }


def test_narrow_verified_claim_can_be_green_while_larger_object_is_red():
    v = color_verdict(
        object_id="hf1_reentry_route",
        job="runtime existence",
        claim="the runtime function exists",
        required_coordinates=("runtime_presence",),
        coordinate_status={"runtime_presence":"VERIFIED"},
    )
    assert v.color == "GREEN"


def test_missing_coordinate_is_red():
    v = color_verdict(
        object_id="REENTER_OBSERVE",
        job="complete HF1 semantics",
        claim="branch semantics are complete",
        required_coordinates=("transition_semantics","return_target"),
        coordinate_status={"transition_semantics":"RECOVERED"},
    )
    assert v.color == "RED"
    assert v.unresolved_coordinates == ("return_target",)


def test_all_required_coordinates_must_be_green_status():
    v = color_verdict(
        object_id="X",
        job="claim",
        claim="claim",
        required_coordinates=("a","b"),
        coordinate_status={"a":"ADMITTED","b":"VERIFIED"},
    )
    assert v.color == "GREEN"
