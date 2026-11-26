"""Compatibility and ownership checks for the separated runtime responsibilities."""
import configured_run
import execution_profile
import global_tool_execution as gateway
import tool_execution_plan as planning
import prose
import prose_profiles
from tool_run_registry import CONFIGURED_RUNS


def test_planning_exports_preserve_canonical_identity():
    for name in ("ToolExecutionBlocked", "D36CCell", "ToolExecutionPlan",
                 "d36c_cells", "build_tool_execution_plan"):
        assert getattr(gateway, name) is getattr(planning, name)
    assert configured_run.FULL_INVOCATION_PROFILE == execution_profile.FULL_INVOCATION_PROFILE
    for tool_id, spec in CONFIGURED_RUNS.items():
        assert spec.recurrence_engine == execution_profile.recurrence_engine_for(tool_id)
    assert execution_profile.recurrence_engine_for("HF002") == "SELF"
    assert execution_profile.recurrence_engine_for("MT") == "HF002"


def test_prose_policy_exports_keep_existing_identity():
    for name in ("PROSE_PROFILES", "LEGACY_DEFAULT_CONSTRAINTS", "SUPPORTED_CONSTRAINTS"):
        assert getattr(prose, name) is getattr(prose_profiles, name)
    assert prose.ProseContract("default").constraints == prose_profiles.LEGACY_DEFAULT_CONSTRAINTS
    assert prose.ProseContract("semantic", profile="SEMANTIC_ONLY").constraints == ()


def test_registered_plan_rejects_missing_or_substituted_native_layers():
    from dataclasses import replace
    import pytest
    from configured_hf2_execution import ConfiguredHF2ExecutionError, execute_configured_with_hf2

    plan = planning.build_tool_execution_plan(CONFIGURED_RUNS["ASSERT"])
    layer = plan.native[0][0]
    missing = replace(plan, native=tuple(pair for pair in plan.native if pair[0] != layer))
    substituted = replace(plan, native=tuple(
        ("UNREGISTERED_LAYER" if name == layer else name, cell)
        for name, cell in plan.native
    ))
    for invalid in (missing, substituted):
        assert not invalid.complete
        with pytest.raises(ConfiguredHF2ExecutionError, match="CONFIGURED_HF2_PLAN_INCOMPLETE"):
            execute_configured_with_hf2(
                tool_id="ASSERT", plan=invalid, state={}, adapter=lambda *_: True
            )


def test_explicit_empty_mode_override_is_invalid():
    import pytest

    with pytest.raises(planning.ToolExecutionBlocked, match="NON_OBSERVER_TOOL_RUN_FORBIDDEN"):
        planning.build_tool_execution_plan(CONFIGURED_RUNS["MT"], requested_mode="")


def test_configured_specs_require_registered_exact_authority():
    from dataclasses import replace
    import pytest
    from tool_manifest import manifest_for

    spec=CONFIGURED_RUNS["MT"]
    assert spec.complete()
    assert replace(spec).complete()
    assert manifest_for("UNREGISTERED_TEST").complete()  # generic reconstruction only
    for invalid in (
        replace(spec, tool_id="UNREGISTERED_TEST", manifest_id="UNREGISTERED_TEST", protected_behaviors=()),
        replace(spec, manifest_id="GOAL", protected_behaviors=()),
        replace(spec, external_challenge="NONE"),
        replace(spec, protected_behaviors=()),
        replace(spec, required_layers=("SUBSTITUTED",)),
        replace(spec, wrapper_required=1),
    ):
        assert not invalid.complete()
        with pytest.raises(planning.ToolExecutionBlocked, match="INCOMPLETE_CONFIGURED_RUN"):
            planning.build_tool_execution_plan(invalid)
