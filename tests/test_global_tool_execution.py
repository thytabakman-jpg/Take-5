import pytest

from configured_run import (
    COGNITIVE_OPERATORS,
    FULL_INVOCATION_PROFILE,
    QUESTION_FAMILIES,
)
from global_tool_execution import ToolExecutionBlocked, build_tool_execution_plan
from tool_run_registry import CONFIGURED_RUNS, MATERIAL_TOOLS


def test_every_registered_tool_inherits_global_execution_contract():
    assert MATERIAL_TOOLS
    for tool in MATERIAL_TOOLS:
        spec=CONFIGURED_RUNS[tool]
        assert spec.complete()
        assert spec.wrapper_required
        assert spec.default_mode=="OBSERVER"
        assert spec.geometry=="D36_C"
        assert spec.question_families==QUESTION_FAMILIES
        assert spec.required_cognitive_ops==COGNITIVE_OPERATORS
        assert spec.required_layers
        assert spec.recurrence_required is True
        assert spec.recurrence_engine==("SELF" if tool=="HF002" else "HF002")
        assert spec.invocation_profile==FULL_INVOCATION_PROFILE


def test_every_registered_tool_builds_full_36_plan():
    for tool in MATERIAL_TOOLS:
        spec=CONFIGURED_RUNS[tool]
        plan=build_tool_execution_plan(spec)
        assert plan.complete
        assert len(plan.cells)==36
        assert len(plan.native)==len(spec.required_layers)*36
        assert len(plan.questions)==22*36
        assert len(plan.cognitive)==4*36
        assert plan.recurrence_required is True
        assert plan.recurrence_engine==("SELF" if tool=="HF002" else "HF002")
        assert plan.invocation_profile==FULL_INVOCATION_PROFILE


def test_non_observer_tool_run_is_globally_blocked():
    spec=CONFIGURED_RUNS["GOAL"]
    with pytest.raises(ToolExecutionBlocked, match="NON_OBSERVER_TOOL_RUN_FORBIDDEN"):
        build_tool_execution_plan(spec,requested_mode="EXECUTE")


def test_assert_keeps_two_declared_native_layers():
    spec=CONFIGURED_RUNS["ASSERT"]
    assert spec.required_layers==("ASSERT_LAYER_1","ASSERT_LAYER_2")
    plan=build_tool_execution_plan(spec)
    assert len(plan.native)==2*36


def test_full_plan_rejects_count_preserving_missing_or_repeated_coordinates():
    from dataclasses import replace
    base=build_tool_execution_plan(CONFIGURED_RUNS["MT"])
    assert base.complete
    for key in ("cells","native","questions","cognitive"):
        content=getattr(base,key)
        poison=(content[0],content[0],*content[2:])
        assert len(poison)==len(content)
        assert not replace(base,**{key:tuple(poison)}).complete,key


def test_full_plan_rejects_recursion_profile_or_tool_identity_spoof():
    from dataclasses import replace
    plan=build_tool_execution_plan(CONFIGURED_RUNS["MT"])
    for variant in (
        replace(plan,tool_id="HF002"),
        replace(plan,tool_id=""),
        replace(plan,recurrence_engine="SELF"),
        replace(plan,native=(("layer",plan.cells[0]),)*len(plan.native)),
    ):
        assert not variant.complete
    assert build_tool_execution_plan(CONFIGURED_RUNS["HF002"]).complete
