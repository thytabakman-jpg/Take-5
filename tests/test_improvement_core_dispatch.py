import sys
sys.path.insert(0,"runtime")

from improvement_core_dispatch import (
    resolve_improvement_core_invocation,
    dispatch_improvement_core,
)
from ic028_operator import GOAL_DIRECTED_STAGES

def _handlers(calls):
    handlers={}
    for stage in GOAL_DIRECTED_STAGES:
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

def test_improvecore_user_phrase_resolves_to_current_regime():
    r=resolve_improvement_core_invocation("ImproveCore, solve this")
    assert r.controller=="IC-028"
    assert r.entrypoint.endswith("run_improvement_core_with_hf2")

def test_improvement_core_phrase_resolves_to_same_regime():
    a=resolve_improvement_core_invocation("ImproveCore this")
    b=resolve_improvement_core_invocation("Improvement Core, take control")
    assert a==b

def test_dispatch_executes_rich_controller_path_through_current_regime():
    calls=[]
    resolution,out=dispatch_improvement_core(
        "ImproveCore, solve this",
        target="problem",
        job="solve",
        basis="current",
        state={},
        handlers=_handlers(calls),
    )
    assert resolution.controller=="IC-028"
    assert resolution.entrypoint.endswith("run_improvement_core_with_hf2")
    assert "GENERATE_WORK" in out.receipt.stages
    assert "ADMIT" in out.receipt.stages
    assert "PERSIST" in out.receipt.stages
    assert "VERIFY" in out.receipt.stages
    assert "REENTER" in out.receipt.stages
    assert out.result.terminal
    assert out.status=="COMPLETE"
    assert out.hf2_status=="RELATIVE_CLOSE"


def test_dispatch_can_seed_from_corpus_without_host_supplied_job_coordinates():
    calls=[]
    resolution,out=dispatch_improvement_core(
        "Run ImproveCore",
        corpus=[
            {"id":"m1","text":"Run ImproveCore with no assignment."},
            {"id":"m2","text":"Look at everything."},
            {"id":"m3","text":"Fix it."},
        ],
        state={},
        handlers=_handlers(calls),
    )
    assert resolution.controller=="IC-028"
    assert out.result.state["upstream_discovery"]["status"]=="OBSERVED"
    assert out.result.state["upstream_discovery"]["corpus_size"]==3
    assert "RECOVER_GOAL" in out.receipt.stages
    assert "GENERATE_WORK" in out.receipt.stages
    assert out.status=="COMPLETE"

def test_dispatch_rejects_partial_host_coordinates():
    try:
        dispatch_improvement_core(
            "ImproveCore",
            target="problem",
            state={},
            handlers=_handlers([]),
        )
    except RuntimeError as exc:
        assert str(exc)=="IMPROVEMENT_CORE_PARTIAL_ENTRY_COORDINATES"
    else:
        raise AssertionError("expected partial entry coordinates to fail closed")

def test_dispatch_requires_corpus_when_no_job_coordinates_are_supplied():
    try:
        dispatch_improvement_core(
            "ImproveCore",
            state={},
            handlers=_handlers([]),
        )
    except RuntimeError as exc:
        assert str(exc)=="IMPROVEMENT_CORE_CORPUS_REQUIRED_FOR_UPSTREAM_DISCOVERY"
    else:
        raise AssertionError("expected missing corpus to fail closed")
