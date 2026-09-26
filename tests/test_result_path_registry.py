from mathematical_color_gate import MathFragment, MathStatus, TextFragment
from result_path_registry import PATHS, default_result_path, emit_default_result, result_path


def test_exactly_one_default_result_path():
    path = default_result_path()
    assert path.name == "math_first"
    assert path.emission_gate == "mathematical_color_gate.emit_user_visible"
    assert sum(p.authority == "DEFAULT_RESULT_AUTHORITY" for p in PATHS) == 1


def test_legacy_facades_are_comparators_not_default_result_authority():
    assert result_path("recursive_episode").role == "COMPARATOR"
    assert result_path("inquiry_session").role == "COMPARATOR"


def test_default_result_emission_uses_color_gate():
    out = emit_default_result(
        (
            TextFragment("ASSERT "),
            MathFragment("A^{36}", MathStatus.RECOVERED),
        )
    )
    assert out == r"ASSERT \\color{green}{A^{36}}"
