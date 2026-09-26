import pytest

from mathematical_color_gate import (
    ColorInvariantViolation,
    MathFragment,
    assess_recovery,
    MathStatus,
    TextFragment,
    canonical_formal_label,
    emit_user_visible,
    render_math,
    render_formal_label,
    verify_assistant_response,
    verify_rendered_output,
)


def test_recovered_math_renders_green():
    assert render_math(
        MathFragment(r"\Gamma\nvdash_K\varphi", MathStatus.RECOVERED)
    ) == r"\color{green}{\Gamma\nvdash_K\varphi}"


def test_unresolved_math_renders_red():
    assert render_math(
        MathFragment("X", MathStatus.UNRESOLVED)
    ) == r"\color{red}{X}"


def test_emission_preserves_status_and_text():
    out = emit_user_visible(
        (
            TextFragment("Invariant "),
            MathFragment(r"U\neq F", MathStatus.RECOVERED),
            TextFragment("."),
        )
    )
    assert out == r"Invariant \color{green}{U\neq F}."


def test_raw_html_color_markup_is_rejected():
    with pytest.raises(ColorInvariantViolation, match="RAW_COLOR_MARKUP_FORBIDDEN"):
        emit_user_visible((TextFragment('<span style="color:green">ASSERT</span>'),))


@pytest.mark.parametrize("raw", ("\U0001F7E2 ASSERT", "\U0001F534 X"))
def test_status_prefix_fallback_is_rejected(raw):
    with pytest.raises(ColorInvariantViolation, match="STATUS_FALLBACK_FORBIDDEN"):
        emit_user_visible((TextFragment(raw),))


@pytest.mark.parametrize(
    "raw",
    (
        "ASSERT",
        "ICC 128",
        "ImproveCore",
        "Improvement Core",
        "HF1",
        "HF-001",
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


def test_final_render_audit_rejects_raw_html():
    with pytest.raises(ColorInvariantViolation, match="RAW_COLOR_MARKUP_FORBIDDEN"):
        verify_rendered_output('<span style="color:green">ASSERT</span>')


def test_final_render_audit_rejects_status_fallback():
    with pytest.raises(ColorInvariantViolation, match="STATUS_FALLBACK_FORBIDDEN"):
        verify_rendered_output("\U0001F7E2 ASSERT")


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
    assert a.complete_for_use is False
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
    assert a.complete_for_use is True
    assert a.status is MathStatus.RECOVERED


def test_unspecified_required_coordinates_fail_closed():
    a = assess_recovery(
        object_id="HF1",
        job="complete mathematics",
        claim="HF1 is mathematically complete",
        required_coordinates=(),
        coordinate_status={},
    )
    assert a.complete_for_use is False
    assert a.status is MathStatus.UNRESOLVED
    assert a.unresolved_coordinates == ("REQUIRED_COORDINATES_UNSPECIFIED",)


def test_formal_label_uses_latex_glyph_color_not_html():
    out = render_formal_label("ASSERT", MathStatus.RECOVERED)
    assert out == r"\color{green}{\operatorname{ASSERT}}"
    assert "<span" not in out.lower()


@pytest.mark.parametrize(
    ("label","canonical"),
    (
        ("ImproveCore","IMPROVECORE"),
        ("Improve Core","IMPROVECORE"),
        ("Improvement Core","IMPROVECORE"),
        ("HF1","HF1"),
        ("HF-001","HF1"),
    ),
)
def test_current_formal_aliases_are_registered(label,canonical):
    assert canonical_formal_label(label)==canonical


def test_improvecore_and_hf1_render_through_same_typed_path():
    assert render_formal_label("ImproveCore",MathStatus.UNRESOLVED) == (
        r"\color{red}{\operatorname{IMPROVECORE}}"
    )
    assert render_formal_label("HF-001",MathStatus.RECOVERED) == (
        r"\color{green}{\operatorname{HF1}}"
    )


def test_response_boundary_rejects_plain_registered_formal_label():
    with pytest.raises(
        ColorInvariantViolation,
        match="UNTYPED_FORMAL_LABEL_AT_RESPONSE_BOUNDARY",
    ):
        verify_assistant_response("The current ImproveCore is active.")


def test_response_boundary_accepts_typed_colored_formal_label():
    verify_assistant_response(
        r"The current \color{red}{\operatorname{IMPROVECORE}} is unresolved."
    )


def test_unregistered_formal_label_fails_closed():
    with pytest.raises(ColorInvariantViolation, match="FORMAL_LABEL_NOT_REGISTERED"):
        render_formal_label("MADE_UP_TOOL", MathStatus.RECOVERED)
