import sys
sys.path.insert(0,"runtime")

from transfer_core import (
    TransferSource, TransferTarget, TransferStatus,
    run_transfer_core, apply_transfer_feedback,
)
from tool_run_registry import CONFIGURED_RUNS

SRC=TransferSource(
    source_id="s1",
    source_project="research",
    source_result_ref="result:1",
    source_refs=("source.md",),
    object_type="mathematical_result",
    payload={"finding":"x"},
    provenance={"commit":"abc"},
)

def test_transfercore_is_registered_configured_tool():
    spec=CONFIGURED_RUNS["TransferCore"]
    assert spec.complete()
    assert "TRANSFER_NO_AUTHORITY_LAUNDERING" in spec.protected_behaviors

def test_transfercore_discovers_bounded_target_and_admits_relation():
    target=TransferTarget("t1","take5","improve tool","tool",{})
    out=run_transfer_core(
        SRC,
        discover_targets=lambda s:[target],
        evaluate_relation=lambda s,t:{
            "relation_statement":"source result applies to target tool",
            "applicability":True,
            "bridge_license":"LICENSED",
            "target_effect":"changes target verification rule",
            "material_effect":True,
            "duplication_status":"NOVEL_EFFECT",
            "authority_state":"target mutation not authorized",
            "evidence":{"witness":"w1"},
        },
    )
    assert out.status=="ADMITTED"
    assert out.selected_targets==("t1",)
    assert len(out.handoffs)==1
    assert out.handoffs[0].target_mutated is False
    assert out.handoffs[0].authority_state=="target mutation not authorized"

def test_transfercore_rejects_unlicensed_bridge():
    target=TransferTarget("t1","take5","improve tool","tool",{})
    out=run_transfer_core(
        SRC,candidate_targets=(target,),
        evaluate_relation=lambda s,t:{
            "relation_statement":"looks similar",
            "applicability":True,
            "bridge_license":"UNLICENSED",
            "target_effect":"unknown",
            "material_effect":True,
            "duplication_status":"NOVEL_EFFECT",
            "authority_state":"none",
        },
    )
    assert out.status=="NO_EFFECT"
    assert out.relations[0].status==TransferStatus.REJECTED
    assert out.handoffs==()

def test_transfercore_preserves_open_when_evaluator_missing():
    target=TransferTarget("t1","take5","improve tool","tool",{})
    out=run_transfer_core(SRC,candidate_targets=(target,))
    assert out.status=="OPEN"
    assert "t1:RELATION_EVALUATOR_UNBOUND" in out.open

def test_transfercore_bounds_target_discovery():
    out=run_transfer_core(
        SRC,
        discover_targets=lambda s:[
            {"target_id":f"t{i}","target_project":"p","target_job":"j","target_type":"tool"}
            for i in range(20)
        ],
        evaluate_relation=lambda s,t:{},
        max_targets=4,
    )
    assert out.status=="OPEN"
    assert out.open==("TARGET_DISCOVERY_BOUND_EXCEEDED",)

def test_target_feedback_reenters_without_mutating_target():
    target=TransferTarget("t1","take5","improve tool","tool",{})
    out=run_transfer_core(
        SRC,candidate_targets=(target,),
        evaluate_relation=lambda s,t:{
            "relation_statement":"licensed relation",
            "applicability":True,
            "bridge_license":"LICENSED",
            "target_effect":"material",
            "material_effect":True,
            "duplication_status":"NOVEL_EFFECT",
            "authority_state":"target review required",
        },
    )
    fb=apply_transfer_feedback(out,target_id="t1",target_verified=False)
    assert fb["reentry_required"] is True
    assert fb["relation_recompute_required"] is True
    assert fb["target_mutated"] is False
