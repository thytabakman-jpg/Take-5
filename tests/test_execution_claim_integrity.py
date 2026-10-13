import sys
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from execution_claim_integrity import (
    ExecutionClaimIntegrityError,
    ExecutionClaimLevel,
    ExecutionClaimReceipt,
    assess_execution_claim,
    extend_execution_claim,
    from_protected_transition,
    require_execution_claim,
)
from protected_transition_integrity import complete_receipt


def test_execution_claim_fails_closed_when_lower_causal_coordinate_is_missing():
    receipt=ExecutionClaimReceipt(
        object_id="artifact-x",
        claim_id="run-1",
        claimed_level=ExecutionClaimLevel.EXECUTED,
        evidence={
            "identity":"id",
            "plan":"plan",
            "dispatch":"dispatch",
            # execution intentionally absent
        },
    )
    out=assess_execution_claim(receipt)
    assert out.status=="OPEN"
    assert out.missing_coordinates==("execution",)
    with pytest.raises(ExecutionClaimIntegrityError):
        require_execution_claim(receipt)


def test_higher_claim_requires_every_lower_coordinate():
    base=ExecutionClaimReceipt(
        object_id="artifact-x",
        claim_id="run-2",
        claimed_level=ExecutionClaimLevel.CONSUMED,
        evidence={
            "identity":"id",
            "plan":"plan",
            "dispatch":"dispatch",
            "execution":"execution",
            "consumption":"consumption",
        },
    )
    require_execution_claim(base,minimum_level=ExecutionClaimLevel.CONSUMED)

    persisted=extend_execution_claim(
        base,
        claimed_level=ExecutionClaimLevel.PERSISTED,
        evidence={"persistence":"commit"},
    )
    verified=extend_execution_claim(
        persisted,
        claimed_level=ExecutionClaimLevel.VERIFIED,
        evidence={"verification":"hash-check"},
    )
    assert assess_execution_claim(verified).status=="VERIFIED"


def test_configured_pti_projects_into_generic_claim_without_replacing_pti():
    pti=complete_receipt(
        object_id="MT",
        behavior_id="configured-execution",
        evidence={
            "canonical_identity":"configured_run:MT",
            "configured_dispatch":"dispatch",
            "execution":"native-run",
            "result_consumption":"consume",
            "state_update":"update",
            "reentry":"reenter",
            "user_visible_boundary":"emit",
        },
    )
    claim=from_protected_transition(
        pti,
        claim_id="mt-run-1",
        plan_evidence="D36_C-plan",
    )
    assert claim.level() is ExecutionClaimLevel.CONSUMED
    assert assess_execution_claim(claim).status=="VERIFIED"
    assert claim.evidence["execution"]=="native-run"

@pytest.mark.parametrize("bad_evidence", [None, False, 0, [], {}, ["not-an-attestation"], {"spurious": "value"}, "  "])
def test_execution_claim_rejects_nonstring_or_blank_evidence(bad_evidence):
    receipt=ExecutionClaimReceipt(
        object_id="artifact-x", claim_id="bad-evidence",
        claimed_level=ExecutionClaimLevel.EXECUTED,
        evidence={
            "identity": "id", "plan": "plan",
            "dispatch": "dispatch", "execution": bad_evidence,
        },
    )
    result=assess_execution_claim(receipt)
    assert result.status=="OPEN"
    assert result.missing_coordinates==("execution",)
    with pytest.raises(ExecutionClaimIntegrityError):
        require_execution_claim(receipt)


def test_extend_execution_claim_does_not_stringify_false_evidence():
    base=ExecutionClaimReceipt(
        object_id="artifact-x", claim_id="extend",
        claimed_level=ExecutionClaimLevel.IDENTIFIED,
        evidence={"identity": "id"},
    )
    with pytest.raises(ExecutionClaimIntegrityError):
        extend_execution_claim(
            base, claimed_level=ExecutionClaimLevel.PLANNED,
            evidence={"plan": False},
        )


def test_pti_projection_does_not_stringify_invalid_plan_evidence():
    pti=complete_receipt(
        object_id="MT", behavior_id="configured-execution",
        evidence={
            "canonical_identity": "configured_run:MT",
            "configured_dispatch": "dispatch",
            "execution": "native-run",
            "result_consumption": "consume",
            "state_update": "update",
            "reentry": "reenter",
            "user_visible_boundary": "emit",
        },
    )
    with pytest.raises(ExecutionClaimIntegrityError):
        from_protected_transition(pti, claim_id="mt-invalid-plan", plan_evidence=False)
