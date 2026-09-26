import sys
sys.path.insert(0,"runtime")

from improvement_core_afterrun import run_afterrun_improvement
from improvement_core_learning_memory import LearningMemory
from improvement_core_regime import run_improvement_core_regime
from ic028_operator import GOAL_DIRECTED_STAGES

def _handlers(live=False):
    handlers={}
    for stage in GOAL_DIRECTED_STAGES:
        def fn(state,stage=stage):
            if stage=="COMPLETE" and live:
                return {
                    "state":{**state,"live_continuation":True,"basis_id":"b0","step":0},
                    "terminal":True,
                }
            return {
                "state":{**state,stage:True},
                "material_delta":stage=="EXECUTE",
            }
        handlers[stage]=fn
    handlers["REENTER"]=lambda state: {"state":state,"terminal":True}
    return handlers

def test_afterrun_records_learning_on_clean_success():
    lm=LearningMemory()
    receipt=run_afterrun_improvement(
        episode_id="e1",basis_id="b1",status="COMPLETE",blocker=None,
        state={},learning_memory=lm,
    )
    assert receipt.learning_recorded
    assert receipt.disposition=="NO_STRUCTURAL_GAIN"
    assert lm.records[-1].disposition=="GAIN"

def test_afterrun_generates_candidate_from_blocker():
    lm=LearningMemory()
    receipt=run_afterrun_improvement(
        episode_id="e2",basis_id="b1",status="OPEN",
        blocker="MISSING_BINDING",state={},learning_memory=lm,
    )
    assert receipt.candidate is not None
    assert receipt.candidate.target=="remove_residual_blocker"
    assert receipt.disposition=="CANDIDATE_OPEN"
    assert "STRICT_GAIN_EVALUATOR_UNBOUND" in receipt.open

def test_afterrun_only_applies_strict_gain_with_authorized_applier():
    lm=LearningMemory()
    receipt=run_afterrun_improvement(
        episode_id="e3",basis_id="b1",status="OPEN",
        blocker="MISSING_BINDING",state={},learning_memory=lm,
        strict_gain_evaluator=lambda c,o: {"disposition":"STRICT_GAIN","why":"matched holdout"},
        authorized_applier=lambda c,v: {"applied":True},
    )
    assert receipt.disposition=="STRICT_GAIN"
    assert receipt.applied is True

def test_every_improvecore_regime_use_gets_afterrun_receipt():
    out=run_improvement_core_regime(
        "ImproveCore solve this",target="x",job="solve",basis="b1",
        state={},handlers=_handlers(),
    )
    assert out.afterrun_receipt is not None
    assert out.afterrun_receipt.tool_id=="ImproveCoreAfterRun"
    assert out.afterrun_receipt.learning_recorded

def test_open_improvecore_run_is_still_self_improvement_input():
    out=run_improvement_core_regime(
        "ImproveCore solve this",target="x",job="solve",basis="b1",
        state={},handlers=_handlers(live=True),
    )
    assert out.status=="OPEN"
    assert out.afterrun_receipt is not None
    assert out.afterrun_receipt.candidate is not None
    assert out.afterrun_receipt.observation.blocker=="RECURSIVE_MANAGER_HANDLERS_REQUIRED"
