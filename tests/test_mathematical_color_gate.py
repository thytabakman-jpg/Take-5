import pytest

from mathematical_color_gate import (
    ColorInvariantViolation,
    MathFragment,
    assess_recovery,
    MathStatus,
    PORTABLE_TEXT,
    RenderChannel,
    RenderMode,
    TAKE5_LATEX,
    TextFragment,
    emit_user_visible,
    render_math,
)


def test_recovered_math_renders_green_on_latex_channel():
    assert render_math(
        MathFragment(r"\Gamma\nvdash_K\varphi", MathStatus.RECOVERED),
        TAKE5_LATEX,
    ) == r"\color{green}{\Gamma\nvdash_K\varphi}"


def test_unresolved_math_renders_red_on_latex_channel():
    assert render_math(
        MathFragment("X", MathStatus.UNRESOLVED),
        TAKE5_LATEX,
    ) == r"\color{red}{X}"


def test_portable_channel_preserves_recovered_status_without_markup():
    assert render_math(
        MathFragment(r"\operatorname{ASSERT}", MathStatus.RECOVERED),
        PORTABLE_TEXT,
    ) == r"🟢 \operatorname{ASSERT}"


def test_portable_channel_preserves_unresolved_status_without_markup():
    assert render_math(
        MathFragment("X", MathStatus.UNRESOLVED),
        PORTABLE_TEXT,
    ) == "🔴 X"


def test_emission_preserves_status_and_text():
    out = emit_user_visible(
        (
            TextFragment("Invariant "),
            MathFragment(r"U\neq F", MathStatus.RECOVERED),
            TextFragment("."),
        ),
        channel=TAKE5_LATEX,
    )
    assert out == r"Invariant \color{green}{U\neq F}."


def test_portable_emission_contains_no_html_or_color_command():
    out = emit_user_visible(
        (
            MathFragment(r"\operatorname{ASSERT}", MathStatus.RECOVERED),
            TextFragment(" "),
            MathFragment("X", MathStatus.UNRESOLVED),
        ),
        channel=PORTABLE_TEXT,
    )
    assert out == r"🟢 \operatorname{ASSERT} 🔴 X"
    assert "<span" not in out
    assert "color:" not in out
    assert r"\color" not in out


def test_raw_html_color_markup_is_rejected():
    with pytest.raises(ColorInvariantViolation, match="RAW_COLOR_MARKUP_FORBIDDEN"):
        emit_user_visible((TextFragment('<span style="color:green">ASSERT</span>'),))


@pytest.mark.parametrize(
    "raw",
    (
        "ASSERT",
        "ICC 128",
        r"\Gamma\nvdash_K\varphi",
        "U ≠ F",
        "x = y",
    ),
)
def test_load_bearing_math_cannot_bypass_status_as_plain_text(raw):
    with pytest.raises(ColorInvariantViolation, match="UNTYPED_LOAD_BEARING_MATH"):
        emit_user_visible((TextFragment(raw),))


def test_empty_math_is_rejected():
    with pytest.raises(ColorInvariantViolation, match="EMPTY_MATH_FRAGMENT"):
        emit_user_visible((MathFragment("   ", MathStatus.RECOVERED),))


def test_unknown_render_mode_is_rejected():
    class FakeMode(str):
        pass

    bad_channel = RenderChannel("bad", FakeMode("BAD"))
    with pytest.raises(ColorInvariantViolation, match="UNSUPPORTED_RENDER_MODE"):
        render_math(MathFragment("X", MathStatus.RECOVERED), bad_channel)


def test_complete_math_claim_is_unresolved_when_required_coordinates_are_open():
    a = assess_recovery(
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
    assert a.status is MathStatus.UNRESOLVED
    assert set(a.unresolved_coordinates) == {
        "state_vector","delta_D","delta_R","minimality","integration"
    }


def test_verified_narrow_claim_can_be_recovered_while_parent_object_is_unresolved():
    a = assess_recovery(
        object_id="hf1_reentry_route",
        job="runtime existence",
        claim="runtime function exists",
        required_coordinates=("runtime_presence",),
        coordinate_status={"runtime_presence":"VERIFIED"},
    )
    assert a.status is MathStatus.RECOVERED


def test_unspecified_required_coordinates_fail_closed():
    a = assess_recovery(
        object_id="HF1",
        job="complete mathematics",
        claim="HF1 is mathematically complete",
        required_coordinates=(),
        coordinate_status={},
    )
    assert a.status is MathStatus.UNRESOLVED
    assert a.unresolved_coordinates == ("REQUIRED_COORDINATES_UNSPECIFIED",)
