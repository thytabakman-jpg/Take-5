import sys
sys.path.insert(0,"runtime")

from improvement_core_external_acquisition import (
    ExternalDisposition,
    decide_external_acquisition,
    acquire_external,
)
from improvement_core_regime import run_improvement_core_regime
from ic028_operator import GOAL_DIRECTED_STAGES

def _handlers(seen=None):
    seen=seen if seen is not None else []
    handlers={}
    for stage in GOAL_DIRECTED_STAGES:
        def fn(state,stage=stage):
            seen.append((stage,state))
            return {
                "state":{**state,stage:True},
                "material_delta":stage=="EXECUTE",
                "supervisory_relevant":False,
            }
        handlers[stage]=fn
    handlers["REENTER"]=lambda state: {"state":state,"terminal":True}
    return handlers

def test_external_not_needed_without_signal():
    d=decide_external_acquisition({},available=("web_search",))
    assert d.disposition==ExternalDisposition.NOT_NEEDED

def test_external_gap_is_legal_when_needed_but_unavailable():
    d=decide_external_acquisition(
        {"external_dependency":True},
        available=(),
        allow_gap=True,
    )
    assert d.disposition==ExternalDisposition.OPEN_GAP
    assert d.allow_internal_fallback is False

def test_external_adapter_is_selected_before_internal_work():
    called=[]
    def web(state):
        called.append(True)
        return {
            "external_need_satisfied":True,
            "evidence":["fresh source"],
        }
    r=acquire_external(
        {"currentness_unknown":True},
        {"web_search":web},
    )
    assert r.decision.disposition==ExternalDisposition.ACQUIRE
    assert r.used==("web_search",)
    assert called==[True]

def test_regime_cannot_close_over_unavailable_required_outside_evidence():
    out=run_improvement_core_regime(
        "ImproveCore solve it",
        target="x",
        job="solve",
        basis="current",
        state={"external_dependency":True},
        handlers=_handlers(),
        external_adapters={},
    )
    assert out.status=="OPEN"
    assert out.blocker=="EXTERNAL_ACQUISITION_GAP"
    assert out.external_receipt.decision.disposition==ExternalDisposition.OPEN_GAP

def test_external_evidence_enters_state_before_manager_stages():
    seen=[]
    def web(state):
        return {
            "external_need_satisfied":True,
            "source":"web",
            "fact":"fresh",
        }
    out=run_improvement_core_regime(
        "ImproveCore solve it",
        target="x",
        job="solve",
        basis="current",
        state={"currentness_unknown":True},
        handlers=_handlers(seen),
        external_adapters={"web_search":web},
    )
    assert out.status=="COMPLETE"
    assert out.external_receipt.used==("web_search",)
    first_state=seen[0][1]
    assert first_state["external_evidence"][0]["fact"]=="fresh"
