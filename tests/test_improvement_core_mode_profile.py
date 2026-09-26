import sys
sys.path.insert(0,"runtime")

from entry_contract import (
    EXPAND, CONTRACT, OBSERVE, ACT, DECOUPLED, COUPLED,
    MODE_GOAL_DIRECTED, MODE_OBSERVE_DECOUPLED,
    bind_entry_contract, preflight_mode_profile,
)
from controller_lease import may_select_actions


def test_broad_observer_is_expand_observe_decoupled():
    p=preflight_mode_profile("ImproveCore in observer mode, look at the whole system")
    assert (p.breadth,p.direction,p.coupling)==(EXPAND,OBSERVE,DECOUPLED)


def test_focused_resolution_is_contract_observe_decoupled():
    p=preflight_mode_profile("ImproveCore, focused resolution on this exact discriminant")
    assert (p.breadth,p.direction,p.coupling)==(CONTRACT,OBSERVE,DECOUPLED)


def test_default_improvecore_is_expand_act_coupled():
    p=preflight_mode_profile("ImproveCore, improve this system")
    assert (p.breadth,p.direction,p.coupling)==(EXPAND,ACT,COUPLED)


def test_focus_and_observer_are_not_opposites():
    broad=preflight_mode_profile("ImproveCore observer mode")
    focused=preflight_mode_profile("ImproveCore focused mode")
    assert broad.direction==focused.direction==OBSERVE
    assert broad.breadth==EXPAND
    assert focused.breadth==CONTRACT


def test_entry_contract_projects_observe_profiles_to_observer_first_legacy_mode():
    b=bind_entry_contract(
        "ImproveCore focused mode",
        target="x",job="inspect",basis="b",
    )
    assert b.contract.initial_mode==MODE_OBSERVE_DECOUPLED
    assert b.contract.mode_profile.mode_id=="CONTRACT_OBSERVE_DECOUPLED"
    assert may_select_actions(b.lease,"IC-028")


def test_goal_directed_compatibility_projects_to_act_coupled():
    b=bind_entry_contract(
        "ImproveCore improve this",
        target="x",job="improve",basis="b",
        explicit_mode=MODE_GOAL_DIRECTED,
    )
    assert b.contract.initial_mode==MODE_GOAL_DIRECTED
    assert b.contract.mode_profile.mode_id=="EXPAND_ACT_COUPLED"
