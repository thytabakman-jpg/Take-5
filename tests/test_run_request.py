from run_request import Geometry, resolve_run_request


def test_run_mt_defaults_to_full_configured_wrapped_36c():
    r = resolve_run_request("run MT")
    assert r.tool_id == "MT"
    assert r.configured is True
    assert r.wrapper_required is True
    assert r.geometry == Geometry.D36_C
    assert r.recursive is True
    assert r.closure_required is True
    assert r.reentry_required is True
    assert r.semantic_before_return is True


def test_mt_this_has_same_default_contract():
    r = resolve_run_request("MT this")
    assert r.configured is True
    assert r.wrapper_required is True
    assert r.geometry == Geometry.D36_C


def test_bare_mt_is_explicit_escape_hatch():
    r = resolve_run_request("run bare MT")
    assert r.tool_id == "MT"
    assert r.configured is False
    assert r.wrapper_required is False
    assert r.geometry is None
    assert r.recursive is False
    assert r.semantic_before_return is False


def test_core_mt_is_explicit_escape_hatch():
    r = resolve_run_request("core MT")
    assert r.configured is False
    assert r.wrapper_required is False


def test_pd_also_defaults_to_configured_wrapped_geometry():
    r = resolve_run_request("PD this")
    assert r.tool_id == "PD"
    assert r.configured is True
    assert r.wrapper_required is True
    assert r.geometry == Geometry.D36_C


def test_assert_defaults_to_full_configured_wrapped_36c():
    r = resolve_run_request("run ASSERT")
    assert r.tool_id == "ASSERT"
    assert r.configured is True
    assert r.wrapper_required is True
    assert r.geometry == Geometry.D36_C
    assert r.recursive is True
    assert r.closure_required is True
    assert r.reentry_required is True


def test_goal_defaults_to_full_configured_wrapped_36c():
    r = resolve_run_request("run GOAL")
    assert r.tool_id == "GOAL"
    assert r.configured is True
    assert r.wrapper_required is True
    assert r.geometry == Geometry.D36_C
    assert r.recursive is True
    assert r.closure_required is True
    assert r.reentry_required is True


def test_architect_alias_resolves_to_full_configured_architecture():
    r = resolve_run_request("run Architect")
    assert r.tool_id == "Architecture"
    assert r.configured is True
    assert r.wrapper_required is True
    assert r.geometry == Geometry.D36_C
    assert r.recursive is True
    assert r.closure_required is True
    assert r.reentry_required is True


def test_architecture_name_resolves_to_same_configured_tool():
    r = resolve_run_request("run Architecture")
    assert r.tool_id == "Architecture"
    assert r.configured is True
    assert r.geometry == Geometry.D36_C


def test_root_cause_alias_resolves_to_rootcause_not_diagnosis():
    r = resolve_run_request("run Root Cause")
    assert r.tool_id == "RootCause"
    assert r.configured is True
    assert r.wrapper_required is True
    assert r.geometry == Geometry.D36_C
    assert r.recursive is True
    assert r.closure_required is True
    assert r.reentry_required is True
