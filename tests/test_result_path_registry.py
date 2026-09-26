import pytest

from mathematical_color_gate import (
    AssessedMathFragment,
    ColorInvariantViolation,
    MathStatus,
    PORTABLE_TEXT,
    TextFragment,
    assess_recovery,
)
from result_path_registry import PATHS, default_result_path, emit_default_result, result_path


def test_exactly_one_default_result_path():
    path = default_result_path()
    assert path.name == "math_first"
    assert path.emission_gate == "mathematical_color_gate.emit_user_visible"
    assert sum(p.authority == "DEFAULT_RESULT_AUTHORITY" for p in PATHS) == 1


def test_legacy_facades_are_comparators_not_default_result_authority():
    assert result_path("recursive_episode").role == "COMPARATOR"
    assert result_path("inquiry_session").role == "COMPARATOR"


def _assessed(latex, object_id, complete=True):
    a = assess_recovery(
        object_id=object_id,
        job="test-use",
        claim="test-claim",
        required_coordinates=("math",),
        coordinate_status={"math":"VERIFIED" if complete else "OPEN"},
    )
    return AssessedMathFragment(latex, a)


def test_default_result_emission_uses_color_gate():
    out = emit_default_result(
        (
            _assessed(r"\operatorname{ASSERT}", "ASSERT"),
            TextFragment(" "),
            _assessed("A^{36}", "A36"),
        )
    )
    assert out == (
        r"\color{green}{\operatorname{ASSERT}} "
        r"\color{green}{A^{36}}"
    )


def test_default_result_can_use_portable_channel_without_status_loss():
    out = emit_default_result(
        (
            _assessed(r"\operatorname{ASSERT}", "ASSERT"),
            TextFragment(" "),
            _assessed("X", "X", complete=False),
        ),
        channel=PORTABLE_TEXT,
    )
    assert out == r"🟢 \operatorname{ASSERT} 🔴 X"



def test_default_result_rejects_unassessed_math():
    from mathematical_color_gate import MathFragment
    with pytest.raises(ColorInvariantViolation, match="UNASSESSED_MATH_AT_DEFAULT_RESULT_BOUNDARY"):
        emit_default_result((MathFragment("HF1", MathStatus.RECOVERED),))
