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
