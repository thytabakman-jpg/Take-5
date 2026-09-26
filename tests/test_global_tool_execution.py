import pytest

from configured_run import COGNITIVE_OPERATORS, QUESTION_FAMILIES
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


def test_every_registered_tool_builds_full_36_plan():
    for tool in MATERIAL_TOOLS:
        spec=CONFIGURED_RUNS[tool]
        plan=build_tool_execution_plan(spec)
        assert plan.complete
        assert len(plan.cells)==36
        assert len(plan.native)==len(spec.required_layers)*36
        assert len(plan.questions)==22*36
        assert len(plan.cognitive)==4*36


def test_non_observer_tool_run_is_globally_blocked():
    spec=CONFIGURED_RUNS["GOAL"]
    with pytest.raises(ToolExecutionBlocked, match="NON_OBSERVER_TOOL_RUN_FORBIDDEN"):
        build_tool_execution_plan(spec,requested_mode="EXECUTE")


def test_assert_keeps_two_declared_native_layers():
    spec=CONFIGURED_RUNS["ASSERT"]
    assert spec.required_layers==("ASSERT_LAYER_1","ASSERT_LAYER_2")
    plan=build_tool_execution_plan(spec)
    assert len(plan.native)==2*36
