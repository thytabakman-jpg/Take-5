"""Backlog continuation terminal safety and old behavior parity."""
import pytest
from continuation_engine import STEPS, run_continuation


def handlers(overrides=None):
    overrides = overrides or {}
    return {step: (lambda state, name=step: overrides.get(name, {"state": state}))
            for step in STEPS}


@pytest.mark.parametrize("step", STEPS[:-1])
def test_early_terminal_cannot_skip_required_closeout(step):
    result = run_continuation(handlers({step: {"terminal": True}}), {})
    assert not result.terminal
    assert result.blocker == f"EARLY_TERMINAL:{step}"
    assert result.receipts[-1].step == step
    assert result.receipts[-1].status == "INVALID_TERMINAL"
    assert len(result.receipts) == STEPS.index(step) + 1


def test_terminal_at_reentry_preserves_success_path():
    result = run_continuation(handlers({"REENTER": {"terminal": True}}), {})
    assert result.terminal and result.blocker is None
    assert tuple(r.step for r in result.receipts) == STEPS


def test_no_change_runs_every_required_step_before_success():
    result = run_continuation(handlers(), {})
    assert result.terminal and len(result.receipts) == len(STEPS)


def test_blocker_preserves_previous_fail_closed_behavior():
    result = run_continuation(handlers({"PERSIST": {"blocked": True}}), {})
    assert not result.terminal and result.blocker == "BLOCKED:PERSIST"
    assert result.receipts[-1].status == "BLOCKED"


def test_unbound_step_preserves_previous_fail_closed_behavior():
    paths = handlers()
    del paths["PERSIST"]
    result = run_continuation(paths, {})
    assert not result.terminal and result.blocker == "UNBOUND:PERSIST"
