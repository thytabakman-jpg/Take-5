from assert_full36 import (
    ASSERT_LAYER_1_STAGES,
    ASSERT_LAYER_2_QUESTION_FAMILIES,
    COGNITIVE_OPERATORS,
    GEOMETRY,
    build_assert_full36_plan,
)
from tool_run_registry import CONFIGURED_RUNS


def test_full_assert_uses_typed_d36c():
    plan = build_assert_full36_plan()
    assert plan.geometry == "D36_C"
    assert len(plan.cells) == 36
    assert plan.complete


def test_layer_1_is_seven_stages_times_36():
    plan = build_assert_full36_plan()
    assert len(ASSERT_LAYER_1_STAGES) == 7
    assert len(plan.layer_1) == 7 * 36


def test_layer_2_is_22_question_families_times_36():
    plan = build_assert_full36_plan()
    assert len(ASSERT_LAYER_2_QUESTION_FAMILIES) == 22
    assert len(plan.layer_2) == 22 * 36


def test_cognitive_surface_is_four_operators_times_36():
    plan = build_assert_full36_plan()
    assert COGNITIVE_OPERATORS == (
        "DIFFERENTIATE",
        "RELATE",
        "RECONSTRUCT",
        "STRENGTHEN",
    )
    assert len(plan.cognitive) == 4 * 36


def test_configured_assert_requires_both_layers_and_cognitive_surface():
    spec = CONFIGURED_RUNS["ASSERT"]
    assert spec.complete()
    assert spec.geometry == GEOMETRY
    assert spec.required_layers == ("ASSERT_LAYER_1","ASSERT_LAYER_2")
    assert spec.required_cognitive_ops == COGNITIVE_OPERATORS
