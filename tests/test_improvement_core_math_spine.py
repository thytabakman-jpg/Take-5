import sys
sys.path.insert(0,"runtime")

from improvement_core_math_spine import (
    ControllerOption, ClosureInput, Contribution,
    nondominated_frontier, policy_correspondence, resolve_policy,
    representation_sufficient, closure_disposition, reopen_required,
    cumulative_preservation,
)


def test_nondominated_frontier_preserves_incomparable_options():
    a=ControllerOption("a",goal_gain=3,information_gain=1,cost=2,risk=1)
    b=ControllerOption("b",goal_gain=1,information_gain=4,cost=1,risk=1)
    out=nondominated_frontier([a,b])
    assert {x.option_id for x in out.nondominated}=={"a","b"}


def test_hard_admissibility_precedes_preference():
    bad=ControllerOption("bad",goal_gain=999,preserves_protected=False)
    safe=ControllerOption("safe",goal_gain=1)
    out=nondominated_frontier([bad,safe])
    assert [x.option_id for x in out.nondominated]==["safe"]
    assert ("bad","PROTECTED_BEHAVIOR_REGRESSION") in out.rejected


def test_dominated_option_is_removed_without_scalar_score():
    a=ControllerOption("a",goal_gain=3,information_gain=3,search_gain=2,cost=1,risk=1,reversible=True)
    b=ControllerOption("b",goal_gain=2,information_gain=2,search_gain=1,cost=2,risk=2,reversible=False)
    out=nondominated_frontier([a,b])
    assert [x.option_id for x in out.nondominated]==["a"]


def test_representation_sufficiency_is_continuation_relative():
    protected=[frozenset({"h1","h2"}),frozenset({"h3"})]
    assert representation_sufficient(
        [frozenset({"h1"}),frozenset({"h2"}),frozenset({"h3"})],
        protected,
    )
    assert not representation_sufficient(
        [frozenset({"h1","h3"}),frozenset({"h2"})],
        protected,
    )


def test_closure_requires_trc_current_basis_and_dead_frontier():
    base=ClosureInput("CLOSED",True,False,False)
    assert closure_disposition(base)=="RELATIVE_CLOSE"
    assert closure_disposition(ClosureInput("CLOSED",False,False,False))=="RETURN_REENTER"
    assert closure_disposition(ClosureInput("CLOSED",True,True,False))=="CONTINUE"
    assert closure_disposition(ClosureInput("OPEN",True,False,False))=="OPEN"


def test_discovery_and_representation_changes_force_reentry():
    assert reopen_required({"material_discovery_delta":True})
    assert reopen_required({"changed_candidate_universe":True})
    assert reopen_required({"changed_mode_frontier":True})
    assert not reopen_required({"cosmetic_label_change":True})


def test_cumulative_contributions_cannot_silently_disappear():
    before=[Contribution("math-map"),Contribution("observer-mode")]
    after=[Contribution("math-map")]
    ok,lost=cumulative_preservation(before,after)
    assert not ok
    assert lost==("observer-mode",)

    ok,lost=cumulative_preservation(before,after,explicit_revision={"observer-mode"})
    assert ok
    assert lost==()


def test_policy_correspondence_is_exactly_set_valued_nondominated_frontier():
    direct=ControllerOption("direct",goal_gain=3,information_gain=1,cost=2)
    probe=ControllerOption(
        "probe",goal_gain=1,information_gain=5,cost=1,
        metadata={"action_kind":"PROBE"},
    )
    out=policy_correspondence([direct,probe])
    assert {x.option_id for x in out}=={"direct","probe"}


def test_policy_resolver_requires_explicit_choice_for_incomparable_frontier():
    a=ControllerOption("a",goal_gain=3,information_gain=1,cost=2)
    b=ControllerOption("b",goal_gain=1,information_gain=4,cost=1)
    out=resolve_policy([a,b],live_continuation=True)
    assert out.selected is None
    assert out.disposition=="OPEN_INCOMPARABLE_FRONTIER"
    chosen=resolve_policy([a,b],frontier_choice_id="b",live_continuation=True)
    assert chosen.selected.option_id=="b"
    assert chosen.disposition=="SELECTED_EXPLICIT_FRONTIER_CHOICE"


def test_policy_resolver_distinguishes_live_no_action_from_terminal_empty():
    live=resolve_policy([],live_continuation=True)
    terminal=resolve_policy([],live_continuation=False)
    assert live.disposition=="OPEN_NO_ADMISSIBLE_ACTION"
    assert terminal.disposition=="TERMINAL_EMPTY"
