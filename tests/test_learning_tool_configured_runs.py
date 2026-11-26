import sys
sys.path.insert(0,"runtime")

from learning_tool_bridge import SPECS
from tool_run_registry import CONFIGURED_RUNS, LEARNING_TOOLS


def test_every_learning_tool_has_complete_configured_run_identity():
    ids=tuple(spec.program_id for spec in SPECS)
    assert LEARNING_TOOLS==ids
    for pid in ids:
        assert pid in CONFIGURED_RUNS
        spec=CONFIGURED_RUNS[pid]
        assert spec.complete()
        assert spec.recursive
        assert spec.closure_required
        assert spec.reentry_required
        assert spec.external_challenge=="WHEN_STRONG_CLAIM"


def test_registry_rejects_duplicate_identity_before_constructing_mapping():
    import pytest
    from tool_run_registry import _build_configured_runs
    with pytest.raises(RuntimeError, match="TOOL_REGISTRY_DUPLICATE_ID"):
        _build_configured_runs(("MT", "MT"))
