import sys
sys.path.insert(0,"runtime")

from inquiry_compiler import compile_question
from controller_lease import ControllerLease
from entry_contract import MODE_OBSERVE_DECOUPLED, MODE_GOAL_DIRECTED
from jane import begin_turn
from ic028_operator import (
    run_ic028,
    GOAL_DIRECTED_STAGES,
    OBSERVER_FIRST_STAGES,
)

def test_inquiry_pd_precedes_math():
    calls=[]
    def pd(q):
        calls.append("PD")
        return q+"?"
    def math(q):
        calls.append("MATH")
        return __import__("inquiry_compiler").FormalQuestion(q,"x",("a",))
    q,probes=compile_question("curious",pd,math)
    assert calls==["PD","MATH"]
    assert len(probes)==36

def _handlers_for(stages,calls,material_stage=None):
    def mk(stage):
        def handler(state):
            calls.append(stage)
            return {
                "state":{**state,stage:True},
                "material_delta":stage==material_stage,
                "supervisory_relevant":stage==material_stage,
                "delta":"d" if stage==material_stage else None,
            }
        return handler
    handlers={stage:mk(stage) for stage in stages}
    handlers["REENTER"]=lambda state: {"state":state,"terminal":True}
    return handlers

def test_entry_binds_icc_and_observer_mode():
    binding=begin_turn(
        "ICC rewrite my prompt and run this in observer mode",
        target="the equation",
        job="analyze",
        basis="current",
        episode_id="obs-entry",
    )
    assert binding.contract.controller=="IC-028"
    assert binding.contract.initial_mode==MODE_OBSERVE_DECOUPLED
    assert binding.lease.controller=="IC-028"
    assert "ENTRY_BOUND" in binding.contract.receipt

def test_original_self_application_prompt_auto_selects_observer_first():
    binding=begin_turn(
        "Run the equation on itself, then run Goal and then run Architect.",
        target="the equation",
        job="self-apply",
        basis="current",
        episode_id="auto-observer",
    )
    assert binding.contract.initial_mode==MODE_OBSERVE_DECOUPLED
    assert binding.contract.mode_basis=="PREFLIGHT_CONTAMINATION_RISK"

def test_observer_mode_runs_before_goal_and_plan():
    binding=begin_turn(
        "Run ICC in observer mode",
        target="the equation",
        job="self-apply",
        basis="current",
        episode_id="obs-order",
    )
    calls=[]
    handlers=_handlers_for(OBSERVER_FIRST_STAGES,calls,material_stage="EXECUTE")
    out=run_ic028(
        binding.lease,
        {},
        handlers,
        entry_contract=binding.contract,
    )
    assert out.terminal
    assert calls.index("OBSERVE") < calls.index("OBSERVE_RECONCILE")
    assert calls.index("OBSERVE_RECONCILE") < calls.index("OBSERVE_TRC")
    assert calls.index("OBSERVE_TRC") < calls.index("RECOVER_GOAL")
    assert calls.index("OBSERVE_TRC") < calls.index("PLAN_ORDER")

def test_goal_directed_mode_preserves_normal_order():
    binding=begin_turn(
        "Run ICC on this",
        target="object",
        job="analyze",
        basis="current",
        explicit_mode=MODE_GOAL_DIRECTED,
        episode_id="goal-order",
    )
    calls=[]
    handlers=_handlers_for(GOAL_DIRECTED_STAGES,calls)
    out=run_ic028(
        binding.lease,
        {},
        handlers,
        entry_contract=binding.contract,
    )
    assert out.terminal
    assert calls.index("RECOVER_GOAL") < calls.index("PLAN_ORDER")
    assert calls.index("PLAN_ORDER") < calls.index("OBSERVE")

def test_operator_refuses_unbound_entry():
    lease=ControllerLease("e","IC-028","j","b")
    out=run_ic028(lease,{}, {})
    assert not out.terminal
    assert out.blocker=="ENTRY_CONTRACT_REQUIRED"

def test_operator_runs_and_reenters_with_bound_entry():
    binding=begin_turn(
        "Run ICC",
        target="object",
        job="j",
        basis="b",
        episode_id="e",
    )
    calls=[]
    handlers=_handlers_for(GOAL_DIRECTED_STAGES,calls,material_stage="EXECUTE")
    seen=[]
    out=run_ic028(
        binding.lease,
        {},
        handlers,
        entry_contract=binding.contract,
        jane_update=lambda d:seen.append(d),
    )
    assert out.terminal
    assert seen==["d"]
    assert any(r.stage=="ENTRY_CONTRACT" and r.status=="BOUND" for r in out.receipts)
    assert any(r.stage=="JANE_SYNC" for r in out.receipts)
