from tool_run_registry import CONFIGURED_RUNS

def test_desired_jane_is_registered_as_strong_recursive_tool():
    s=CONFIGURED_RUNS["DesiredJane"]
    assert s.recursive
    assert s.closure_required
    assert s.reentry_required
    assert s.external_challenge=="WHEN_STRONG_CLAIM"
    assert s.preserves_open
