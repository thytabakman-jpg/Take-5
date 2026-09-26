import sys
sys.path.insert(0,"runtime")

import pytest

from icc_bootstrap import (
    ICCBootstrapBlocked,
    ToolRunReceipt,
    run_icc_bootstrap,
)


def _receipt(tool, *, configured=True, wrapper=True, observer=True,
             executed=True, captured=True, consumed=True, result=None):
    return ToolRunReceipt(
        tool,
        configured,
        wrapper,
        observer,
        executed,
        captured,
        consumed,
        result,
    )


def test_bootstrap_runs_assert_then_goal_and_consumes_both():
    calls=[]

    def assert_run(target,binding):
        calls.append("ASSERT")
        return _receipt("ASSERT", result={"assert":"ok"})

    def goal_run(target,assert_result,binding):
        calls.append(("GOAL",assert_result))
        return _receipt("GOAL", result={"goal":"ok"})

    out=run_icc_bootstrap(
        {"x":1},
        object(),
        assert_observer_fn=assert_run,
        goal_observer_fn=goal_run,
    )

    assert out.complete
    assert out.trace==("ASSERT_OBSERVER","GOAL_OBSERVER")
    assert calls==["ASSERT",("GOAL",{"assert":"ok"})]


@pytest.mark.parametrize("bad",[
    _receipt("ASSERT", configured=False),
    _receipt("ASSERT", wrapper=False),
    _receipt("ASSERT", observer=False),
    _receipt("ASSERT", executed=False),
    _receipt("ASSERT", captured=False),
    _receipt("ASSERT", consumed=False),
])
def test_assert_bootstrap_fails_closed_on_downgrade(bad):
    with pytest.raises(ICCBootstrapBlocked):
        run_icc_bootstrap(
            {},
            object(),
            assert_observer_fn=lambda target,binding:bad,
            goal_observer_fn=lambda target,a,binding:_receipt("GOAL"),
        )


@pytest.mark.parametrize("bad",[
    _receipt("GOAL", configured=False),
    _receipt("GOAL", wrapper=False),
    _receipt("GOAL", observer=False),
    _receipt("GOAL", executed=False),
    _receipt("GOAL", captured=False),
    _receipt("GOAL", consumed=False),
])
def test_goal_bootstrap_fails_closed_on_downgrade(bad):
    with pytest.raises(ICCBootstrapBlocked):
        run_icc_bootstrap(
            {},
            object(),
            assert_observer_fn=lambda target,binding:_receipt("ASSERT"),
            goal_observer_fn=lambda target,a,binding:bad,
        )


def test_goal_cannot_run_before_assert():
    calls=[]

    def assert_run(target,binding):
        calls.append("ASSERT")
        return _receipt("ASSERT")

    def goal_run(target,assert_result,binding):
        calls.append("GOAL")
        return _receipt("GOAL")

    run_icc_bootstrap(
        {},
        object(),
        assert_observer_fn=assert_run,
        goal_observer_fn=goal_run,
    )
    assert calls==["ASSERT","GOAL"]
