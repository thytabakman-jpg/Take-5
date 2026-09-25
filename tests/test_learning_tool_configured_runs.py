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
