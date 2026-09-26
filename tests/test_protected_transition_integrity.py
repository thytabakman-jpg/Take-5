import pytest

from protected_transition_integrity import (
    COORDINATES,
    PTIState,
    ProtectedTransitionIntegrityError,
    ProtectedTransitionReceipt,
    assess_protected_transition,
    complete_receipt,
    require_protected_transition,
)


def test_complete_chain_verifies():
    evidence={x:f"witness:{x}" for x in COORDINATES}
    receipt=complete_receipt(
        object_id="Tool",
        behavior_id="B",
        evidence=evidence,
    )
    out=require_protected_transition(receipt)
    assert out.status=="VERIFIED"


def test_missing_any_transition_edge_fails_open():
    states={x:PTIState.VERIFIED for x in COORDINATES if x!="reentry"}
    receipt=ProtectedTransitionReceipt("Tool","B",states,{})
    out=assess_protected_transition(receipt)
    assert out.status=="OPEN"
    assert out.missing_coordinates==("reentry",)
    with pytest.raises(ProtectedTransitionIntegrityError):
        require_protected_transition(receipt)


def test_blocked_edge_dominates_open():
    states={x:PTIState.VERIFIED for x in COORDINATES}
    states["configured_dispatch"]=PTIState.OPEN
    states["execution"]=PTIState.BLOCKED
    out=assess_protected_transition(
        ProtectedTransitionReceipt("Tool","B",states,{})
    )
    assert out.status=="BLOCKED"
    assert out.open_coordinates==("configured_dispatch",)
    assert out.blocked_coordinates==("execution",)


def test_complete_receipt_requires_witness_per_edge():
    evidence={x:f"witness:{x}" for x in COORDINATES}
    evidence.pop("user_visible_boundary")
    with pytest.raises(
        ProtectedTransitionIntegrityError,
        match="PROTECTED_TRANSITION_EVIDENCE_MISSING",
    ):
        complete_receipt(object_id="Tool",behavior_id="B",evidence=evidence)
