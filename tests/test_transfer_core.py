import json
import sys
from pathlib import Path

sys.path.insert(0,"runtime")

from transfer_core import (
    ChallengeResult,
    TargetMutationAuthorization,
    TransferDirection,
    TransferSource,
    TransferStatus,
    TransferTarget,
    TransferUpdateKind,
    apply_transfer_feedback,
    apply_transfer_update,
    bind_target_authority,
    challenge_transfer_relation,
    execute_authorized_target_transition,
    nondominated_targets,
    persist_queue_entry,
    queue_entry_from_handoff,
    run_joint_transfer_core,
    run_transfer_core,
)
from tool_manifest import manifest_for,reconstructs
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

SRC2=TransferSource(
    source_id="s2",
    source_project="other",
    source_result_ref="result:2",
    source_refs=("other.md",),
    object_type="failure_pattern",
    payload={"finding":"y"},
    provenance={"commit":"def"},
)

TARGET=TransferTarget(
    "t1","take5","improve tool","tool",
    {"authority_coordinate":"deliverables","benefit":0.9,"disruption":0.2,"uncertainty":0.1},
)


def admitted_relation(source,target):
    return {
        "relation_statement":"source result applies to target tool",
        "applicability":True,
        "bridge_license":"LICENSED",
        "target_effect":"changes target verification rule",
        "material_effect":True,
        "duplication_status":"NOVEL_EFFECT",
        "authority_state":"target review required",
        "evidence":{"witness":"w1"},
    }


def test_transfercore_is_registered_full_configured_tool():
    spec=CONFIGURED_RUNS["TransferCore"]
    assert spec.complete()
    assert "TRANSFER_NO_AUTHORITY_LAUNDERING" in spec.protected_behaviors
    assert "TRANSFER_JOINT_IRREDUCIBILITY" in spec.protected_behaviors
    assert "TRANSFER_AUTHORIZED_TARGET_TRANSITION" in spec.protected_behaviors
    manifest=manifest_for("TransferCore")
    assert manifest.complete()
    assert reconstructs("TransferCore",spec.protected_behaviors)


def test_single_transfer_admits_relation_but_not_target_mutation():
    out=run_transfer_core(
        SRC,candidate_targets=(TARGET,),evaluate_relation=admitted_relation,
    )
    assert out.status=="ADMITTED"
    assert out.selected_targets==("t1",)
    assert len(out.handoffs)==1
    assert out.handoffs[0].target_mutated is False
    assert out.handoffs[0].authority_state=="target review required"


def test_transfercore_preserves_external_acquisition_as_blocked_dependency():
    out=run_transfer_core(
        SRC,candidate_targets=(TARGET,),
        evaluate_relation=lambda s,t:{
            **admitted_relation(s,t),
            "external_dependencies":("external:bridge-validity",),
        },
    )
    assert out.status=="BLOCKED"
    assert "t1:EXTERNAL_ACQUISITION:external:bridge-validity" in out.open


def test_irreducible_joint_transfer_is_first_class():
    joint=run_joint_transfer_core(
        (SRC,SRC2),TARGET,
        evaluate_joint_relation=lambda sources,target:admitted_relation(sources[0],target),
        evaluate_single_relation=lambda source,target:{
            "relation_statement":"single source insufficient",
            "applicability":True,
            "bridge_license":"LICENSED",
            "target_effect":"no material effect alone",
            "material_effect":False,
            "duplication_status":"NOVEL_EFFECT",
            "authority_state":"target review required",
        },
    )
    assert joint.status=="ADMITTED"
    assert joint.irreducible is True
    assert len(joint.singles)==2
    assert all(x.status==TransferStatus.NO_EFFECT for x in joint.singles)


def test_representation_hierarchy_and_order_challenges_are_typed():
    relation=run_transfer_core(
        SRC,candidate_targets=(TARGET,),evaluate_relation=admitted_relation,
    ).relations[0]
    passed=challenge_transfer_relation(
        relation,
        representation_checks={"result-vs-capability":True},
        hierarchy_checks={"project-to-component":True},
        order_checks={"source-before-target":True},
    )
    assert passed.status=="PASS"

    failed=challenge_transfer_relation(
        relation,
        representation_checks={"alternate-representation":False},
    )
    assert failed.status=="FAIL"
    assert failed.failed==("REPRESENTATION:alternate-representation",)

    opened=challenge_transfer_relation(
        relation,
        hierarchy_checks={"unknown-scale":None},
    )
    assert opened.status=="OPEN"


def test_target_frontier_preserves_incomparability():
    a=TransferTarget("a","p","j","tool",{"benefit":1.0,"disruption":0.8,"uncertainty":0.1})
    b=TransferTarget("b","p","j","tool",{"benefit":0.8,"disruption":0.1,"uncertainty":0.1})
    c=TransferTarget("c","p","j","tool",{"benefit":0.2,"disruption":0.9,"uncertainty":0.9})
    frontier=nondominated_targets((a,b,c))
    assert {x.target_id for x in frontier}=={"a","b"}


def test_transfer_update_algebra_preserves_history_and_retraction():
    relation=run_transfer_core(
        SRC,candidate_targets=(TARGET,),evaluate_relation=admitted_relation,
    ).relations[0]
    from transfer_core import TransferState
    state=TransferState()
    state=apply_transfer_update(state,kind=TransferUpdateKind.ACCUMULATE,relation=relation,reason="admit")
    rid=next(iter(state.relations))
    assert rid in state.relations
    state=apply_transfer_update(
        state,kind=TransferUpdateKind.RETRACT_INVALIDATE,
        relation_id=rid,reason="source superseded",
    )
    assert rid in state.invalidated
    assert state.history[-1][0]=="RETRACT_INVALIDATE"


def test_authority_binding_and_authorized_target_transition_are_separate():
    out=run_transfer_core(
        SRC,candidate_targets=(TARGET,),evaluate_relation=admitted_relation,
    )
    handoff=out.handoffs[0]
    binding=bind_target_authority(
        TARGET,{"deliverables":"WBS.md"},
    )
    assert binding is not None
    assert binding.owner=="WBS.md"

    blocked=execute_authorized_target_transition(
        handoff,binding,None,{"verified":False},
        apply_fn=lambda state,handoff:{**state,"verified":True},
        verify_fn=lambda state,handoff:state["verified"],
    )
    assert blocked.status=="OPEN"

    auth=TargetMutationAuthorization(
        target_id="t1",
        authority_ref=binding.authority_ref,
        operation="APPLY_TRANSFER_SUCCESSOR",
        granted=True,
        evidence=("authorized-test-transition",),
    )
    applied=execute_authorized_target_transition(
        handoff,binding,auth,{"verified":False},
        apply_fn=lambda state,handoff:{**state,"verified":True},
        verify_fn=lambda state,handoff:state["verified"],
    )
    assert applied.status=="VERIFIED"
    assert applied.verified is True
    assert any(x.stage.value=="TARGET_MUTATED" for x in applied.ledger)
    assert any(x.stage.value=="TARGET_VERIFIED" for x in applied.ledger)


def test_persistent_queue_is_non_authoritative_and_stale_safe(tmp_path:Path):
    out=run_transfer_core(
        SRC,candidate_targets=(TARGET,),evaluate_relation=admitted_relation,
    )
    entry=queue_entry_from_handoff(out.handoffs[0])
    assert entry is not None
    assert entry["target_mutated"] is False

    path=tmp_path/"queue.json"
    first=persist_queue_entry(path,entry)
    assert first["status"]=="QUEUED"
    doc=json.loads(path.read_text())
    assert len(doc["items"])==1

    try:
        persist_queue_entry(path,{**entry,"target_effect":"changed"},expected_fingerprint="stale")
    except Exception as exc:
        assert "TRANSFER_QUEUE_STALE_BASELINE" in str(exc)
    else:
        raise AssertionError("stale queue write was accepted")


def test_feedback_reenters_only_when_relation_or_verification_changed():
    out=run_transfer_core(
        SRC,candidate_targets=(TARGET,),evaluate_relation=admitted_relation,
    )
    stable=apply_transfer_feedback(out,target_id="t1",target_verified=True)
    assert stable["reentry_required"] is False

    failed=apply_transfer_feedback(out,target_id="t1",target_verified=False)
    assert failed["reentry_required"] is True
    assert failed["relation_recompute_required"] is True


def test_historical_success_reject_noeffect_and_unlike_holdout():
    success=run_transfer_core(
        SRC,candidate_targets=(TARGET,),evaluate_relation=admitted_relation,
    )
    assert success.status=="ADMITTED"

    rejected=run_transfer_core(
        SRC,candidate_targets=(TARGET,),
        evaluate_relation=lambda s,t:{
            **admitted_relation(s,t),
            "bridge_license":"UNLICENSED",
        },
    )
    assert rejected.status=="NO_EFFECT"
    assert rejected.relations[0].status==TransferStatus.REJECTED

    noeffect=run_transfer_core(
        SRC,candidate_targets=(TARGET,),
        evaluate_relation=lambda s,t:{
            **admitted_relation(s,t),
            "material_effect":False,
        },
    )
    assert noeffect.status=="NO_EFFECT"

    external=TransferSource(
        "external-1","external:unlike-domain","external-result",
        ("external-holdout",),"architecture_pattern",
        {"pattern":"independent-source"},
        {"independent":True},
    )
    holdout=run_transfer_core(
        external,candidate_targets=(TARGET,),evaluate_relation=admitted_relation,
        direction=TransferDirection.INBOUND,
    )
    assert holdout.status=="ADMITTED"
    assert holdout.relations[0].direction==TransferDirection.INBOUND
