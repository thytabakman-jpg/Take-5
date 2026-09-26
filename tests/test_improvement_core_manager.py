import sys
sys.path.insert(0,"runtime")

from improvement_core_manager import run_improvement_core_manager
from ic028_operator import GOAL_DIRECTED_STAGES, OBSERVER_FIRST_STAGES
from entry_contract import MODE_OBSERVE_DECOUPLED

def _handlers(stages,calls):
    handlers={}
    for stage in stages:
        def fn(state,stage=stage):
            calls.append(stage)
            return {
                "state":{**state,stage:True},
                "material_delta":stage=="EXECUTE",
                "supervisory_relevant":False,
            }
        handlers[stage]=fn
    handlers["REENTER"]=lambda state: {"state":state,"terminal":True}
    return handlers

def test_improvecore_alias_binds_rich_ic028_manager():
    calls=[]
    out=run_improvement_core_manager(
        "ImproveCore, solve this problem",
        target="problem",
        job="solve",
        basis="current",
        state={},
        handlers=_handlers(GOAL_DIRECTED_STAGES,calls),
    )
    assert out.receipt.controller=="IC-028"
    assert "ENTRY_CONTRACT" in out.receipt.stages
    assert "GENERATE_WORK" in out.receipt.stages
    assert "ADMIT" in out.receipt.stages
    assert "PERSIST" in out.receipt.stages
    assert "VERIFY" in out.receipt.stages
    assert "REENTER" in out.receipt.stages
    assert out.result.terminal

def test_manager_auto_observer_runs_observation_before_goal():
    calls=[]
    out=run_improvement_core_manager(
        "ImproveCore audit the whole system",
        target="system",
        job="audit",
        basis="current",
        state={},
        handlers=_handlers(OBSERVER_FIRST_STAGES,calls),
    )
    assert out.receipt.initial_mode==MODE_OBSERVE_DECOUPLED
    assert calls.index("OBSERVE") < calls.index("RECOVER_GOAL")
    assert out.result.terminal

def test_manager_fails_closed_when_rich_stage_is_missing():
    calls=[]
    handlers=_handlers(GOAL_DIRECTED_STAGES,calls)
    handlers.pop("GENERATE_WORK")
    out=run_improvement_core_manager(
        "ImproveCore, solve this",
        target="problem",
        job="solve",
        basis="current",
        state={},
        handlers=handlers,
    )
    assert not out.result.terminal
    assert out.result.blocker=="UNBOUND:GENERATE_WORK"
