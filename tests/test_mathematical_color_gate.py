import pytest

from mathematical_color_gate import (
    ColorInvariantViolation,
    MathFragment,
    MathStatus,
    TextFragment,
    emit_user_visible,
    render_math,
)


def test_recovered_math_renders_green():
    assert render_math(MathFragment(r"\Gamma\nvdash_K\varphi", MathStatus.RECOVERED)) == (
        r"\color{green}{\Gamma\nvdash_K\varphi}"
    )


def test_unresolved_math_renders_red():
    assert render_math(MathFragment("X", MathStatus.UNRESOLVED)) == r"\color{red}{X}"


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
