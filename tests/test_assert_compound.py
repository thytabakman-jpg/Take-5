from assert_compound import (
    ASSERT_STAGE_ORDER,
    AssertState,
    AssertStages,
    run_round,
    run_to_fixed_point,
)


def _append(field, token):
    def stage(state):
        values = tuple(getattr(state, field))
        return state.__class__(**{
            **state.__dict__,
            field: values + (token,),
        })
    return stage


def test_protected_stage_order_and_second_compare():
    seen = []

    def mark(name):
        def stage(state):
            seen.append(name)
            return state
        return stage

    stages = AssertStages(
        assert_stage=mark("ASSERT"),
        compare_stage=mark("COMPARE"),
        resolve_stage=mark("RESOLVE"),
        here_stage=mark("HERE"),
        inquire_stage=mark("INQUIRE"),
        reassert_stage=mark("REASSERT"),
    )

    result = run_round(AssertState(), stages)

    assert result.trace == ASSERT_STAGE_ORDER
    assert seen == [
        "ASSERT",
        "COMPARE",
        "RESOLVE",
        "HERE",
        "COMPARE",
        "INQUIRE",
        "REASSERT",
    ]


def test_here_can_change_state_seen_by_second_compare():
    compare_observations = []

    def compare(state):
        compare_observations.append(tuple(state.here))
        return state

    stages = AssertStages(
        assert_stage=lambda s: s,
        compare_stage=compare,
        resolve_stage=lambda s: s,
        here_stage=_append("here", "new-object"),
        inquire_stage=lambda s: s,
        reassert_stage=lambda s: s,
    )

    run_round(AssertState(), stages)

    assert compare_observations == [(), ("new-object",)]


def test_fixed_point_reenters_then_closes():
    calls = {"assert": 0}

    def assert_stage(state):
        calls["assert"] += 1
        # First round changes discovery; later rounds stabilize.
        value = ("d1",)
        return state.__class__(**{**state.__dict__, "discovery": value})

    stages = AssertStages(
        assert_stage=assert_stage,
        compare_stage=lambda s: s,
        resolve_stage=lambda s: s,
        here_stage=lambda s: s,
        inquire_stage=lambda s: s,
        reassert_stage=lambda s: s,
    )

    result = run_to_fixed_point(AssertState(), stages)

    assert result.status == "CLOSED"
    assert result.rounds == 2
    assert calls["assert"] == 2


def test_closure_gate_preserves_open_until_resolved():
    rounds = {"n": 0}

    def inquire(state):
        rounds["n"] += 1
        q = ("OPEN",) if rounds["n"] < 3 else ()
        return state.__class__(**{**state.__dict__, "questions": q})

    stages = AssertStages(
        assert_stage=lambda s: s,
        compare_stage=lambda s: s,
        resolve_stage=lambda s: s,
        here_stage=lambda s: s,
        inquire_stage=inquire,
        reassert_stage=lambda s: s,
    )

    result = run_to_fixed_point(
        AssertState(),
        stages,
        closure_gate=lambda s: "OPEN" not in tuple(s.questions),
    )

    assert result.status == "CLOSED"
    assert result.rounds == 4


def test_max_rounds_returns_open_when_discovery_never_stabilizes():
    counter = {"n": 0}

    def assert_stage(state):
        counter["n"] += 1
        return state.__class__(**{
            **state.__dict__,
            "discovery": (counter["n"],),
        })

    stages = AssertStages(
        assert_stage=assert_stage,
        compare_stage=lambda s: s,
        resolve_stage=lambda s: s,
        here_stage=lambda s: s,
        inquire_stage=lambda s: s,
        reassert_stage=lambda s: s,
    )

    result = run_to_fixed_point(AssertState(), stages, max_rounds=3)

    assert result.status == "OPEN"
    assert result.rounds == 3
