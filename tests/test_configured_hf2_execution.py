from configured_hf2_execution import _raw_mapping, execute_configured_with_hf2
from global_tool_execution import build_tool_execution_plan
from tool_run_registry import CONFIGURED_RUNS


def test_false_and_zero_outputs_count_as_real_hf2_full_match_results():
    for result in (False, 0, 0.0):
        receipt = _raw_mapping({
            "status": "FULL_MATCH",
            "execution_truth": "FULL_MATCH",
            "result": result,
        })
        assert receipt["status"] == "FULL_MATCH"
        assert receipt["execution_truth"] == "FULL_MATCH"


def test_missing_and_empty_outputs_still_fail_full_match_closed():
    for receipt in ({}, {"result": None}, {"result": ""}, {"result": {}}, {"result": []}):
        out = _raw_mapping({
            "status": "FULL_MATCH",
            "execution_truth": "FULL_MATCH",
            **receipt,
        })
        assert out["status"] == "OPEN"
        assert out["blocker"] == "CONFIGURED_HF2_FULL_MATCH_WITHOUT_EXECUTION_WITNESS"


def test_blocked_adapter_without_result_remains_open():
    out = _raw_mapping(None)
    assert out["status"] == "OPEN"
    assert out["execution_truth"] == "OPEN"


def test_success_status_cannot_override_failed_execution_truth():
    for truth in ("OPEN", "BLOCKED", "CONFLICT"):
        out = _raw_mapping({
            "status": "EXECUTED", "execution_truth": truth,
            "result": {"claimed": "success"}, "material_delta": True,
        })
        assert out["status"] == truth
        assert out["execution_truth"] == truth
        assert out["material_delta"] is False
        assert out["blocker"] == "CONFIGURED_HF2_SUCCESS_WITH_NON_SUCCESS_TRUTH"


def test_failure_status_cannot_keep_success_execution_truth():
    out = _raw_mapping({
        "status": "BLOCKED", "execution_truth": "FULL_MATCH",
        "result": {"claimed": "success"},
    })
    assert out["status"] == "BLOCKED"
    assert out["execution_truth"] == "BLOCKED"


def test_multiobject_configured_hf2_reenters_same_id_changed_evidence():
    """A changed relation with the same finding ID is not a clean successor."""
    plan = build_tool_execution_plan(CONFIGURED_RUNS["MultiObject"])
    seen = []

    def adapter(current, bound_plan):
        assert bound_plan.tool_id == "MultiObject"
        seen.append(current)
        # The first two outcomes share the same ID and status but differ in
        # semantic evidence. The third repeats the second without new content.
        evidence = "old" if len(seen) == 1 else "new"
        return {
            "status": "CLOSED_RELATIVE",
            "execution_truth": "IMPLEMENTATION_EXECUTED",
            "result": {"finding_id": "joint-1", "status": "JOINT_ONLY",
                       "evidence": [evidence]},
            "material_delta": True,
            "evidence": ("native:MultiObject",),
        }

    out = execute_configured_with_hf2(
        tool_id="MultiObject", plan=plan, state={"packet": {}}, adapter=adapter,
    )
    assert out.status == "RELATIVE_CLOSE"
    assert out.call_count == 3
    assert out.trace[0]["disposition"] == "REAPPLY_C"
    assert out.trace[1]["disposition"] == "REAPPLY_C"
    assert out.trace[2]["disposition"] == "RELATIVE_CLOSE"
    assert out.trace[1]["delta"]["material_result_delta"] is True
    assert out.trace[2]["delta"]["material_result_delta"] is False


def test_configured_hf2_rejects_other_tools_plan_before_native_execution():
    import pytest
    from configured_hf2_execution import ConfiguredHF2ExecutionError
    plan=build_tool_execution_plan(CONFIGURED_RUNS["MT"])
    called=[]
    def adapter(current, bound_plan):
        called.append(current)
        return {"status":"EXECUTED","result":True,"material_delta":False}
    with pytest.raises(ConfiguredHF2ExecutionError,match="CONFIGURED_HF2_TOOL_IDENTITY_MISMATCH"):
        execute_configured_with_hf2(
            tool_id="GOAL",plan=plan,state={"packet":"protected"},adapter=adapter,
        )
    assert called==[]


def test_configured_hf2_rejects_count_preserving_missing_plan_cell():
    import pytest
    from dataclasses import replace
    from configured_hf2_execution import ConfiguredHF2ExecutionError
    plan=build_tool_execution_plan(CONFIGURED_RUNS["GOAL"])
    wrong=replace(plan,cells=(plan.cells[0],plan.cells[0],*plan.cells[2:]))
    with pytest.raises(ConfiguredHF2ExecutionError,match="CONFIGURED_HF2_PLAN_INCOMPLETE"):
        execute_configured_with_hf2(
            tool_id="GOAL",plan=wrong,state={},adapter=lambda *args:True,
        )
