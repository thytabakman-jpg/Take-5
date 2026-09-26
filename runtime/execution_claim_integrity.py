"""Fail-closed execution-claim integrity for repository artifacts.

This module governs claims made outside the configured-tool PTI execution path.

It does not replace Protected Transition Integrity.  PTI governs configured
tool transitions.  This gate governs the weaker but still dangerous question:
what level of execution may an artifact truthfully claim from the causal
evidence attached to it?

A higher claim level requires every lower causal coordinate.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Mapping, Any

from protected_transition_integrity import (
    ProtectedTransitionReceipt,
    require_protected_transition,
)


class ExecutionClaimLevel(str, Enum):
    IDENTIFIED="IDENTIFIED"
    PLANNED="PLANNED"
    DISPATCHED="DISPATCHED"
    EXECUTED="EXECUTED"
    CONSUMED="CONSUMED"
    PERSISTED="PERSISTED"
    VERIFIED="VERIFIED"


ORDER=(
    "identity",
    "plan",
    "dispatch",
    "execution",
    "consumption",
    "persistence",
    "verification",
)

LEVEL_INDEX={
    ExecutionClaimLevel.IDENTIFIED:0,
    ExecutionClaimLevel.PLANNED:1,
    ExecutionClaimLevel.DISPATCHED:2,
    ExecutionClaimLevel.EXECUTED:3,
    ExecutionClaimLevel.CONSUMED:4,
    ExecutionClaimLevel.PERSISTED:5,
    ExecutionClaimLevel.VERIFIED:6,
}


@dataclass(frozen=True)
class ExecutionClaimReceipt:
    object_id:str
    claim_id:str
    claimed_level:ExecutionClaimLevel|str
    evidence:Mapping[str,str]

    def level(self)->ExecutionClaimLevel:
        if isinstance(self.claimed_level,ExecutionClaimLevel):
            return self.claimed_level
        return ExecutionClaimLevel(str(self.claimed_level))

    def payload(self)->dict[str,Any]:
        row=asdict(self)
        row["claimed_level"]=self.level().value
        row["evidence"]=dict(self.evidence)
        return row


@dataclass(frozen=True)
class ExecutionClaimAssessment:
    object_id:str
    claim_id:str
    claimed_level:str
    status:str
    required_coordinates:tuple[str,...]
    missing_coordinates:tuple[str,...]


class ExecutionClaimIntegrityError(RuntimeError):
    pass


def required_coordinates(level:ExecutionClaimLevel|str)->tuple[str,...]:
    normalized=level if isinstance(level,ExecutionClaimLevel) else ExecutionClaimLevel(str(level))
    return ORDER[:LEVEL_INDEX[normalized]+1]


def assess_execution_claim(receipt:ExecutionClaimReceipt)->ExecutionClaimAssessment:
    level=receipt.level()
    required=required_coordinates(level)
    evidence={str(k):str(v) for k,v in dict(receipt.evidence).items()}
    missing=tuple(
        coordinate for coordinate in required
        if not evidence.get(coordinate,"").strip()
    )
    return ExecutionClaimAssessment(
        object_id=receipt.object_id,
        claim_id=receipt.claim_id,
        claimed_level=level.value,
        status="VERIFIED" if not missing else "OPEN",
        required_coordinates=required,
        missing_coordinates=missing,
    )


def require_execution_claim(
    receipt:ExecutionClaimReceipt,
    *,
    minimum_level:ExecutionClaimLevel|str|None=None,
)->ExecutionClaimAssessment:
    assessment=assess_execution_claim(receipt)
    if minimum_level is not None:
        minimum=minimum_level if isinstance(minimum_level,ExecutionClaimLevel) else ExecutionClaimLevel(str(minimum_level))
        if LEVEL_INDEX[receipt.level()] < LEVEL_INDEX[minimum]:
            raise ExecutionClaimIntegrityError(
                f"EXECUTION_CLAIM_LEVEL_TOO_LOW:{receipt.object_id}:{receipt.claim_id}:"
                f"{receipt.level().value}<{minimum.value}"
            )
    if assessment.status!="VERIFIED":
        raise ExecutionClaimIntegrityError(
            f"EXECUTION_CLAIM_INCOMPLETE:{receipt.object_id}:{receipt.claim_id}:"
            +"missing="+",".join(assessment.missing_coordinates)
        )
    return assessment


def extend_execution_claim(
    receipt:ExecutionClaimReceipt,
    *,
    claimed_level:ExecutionClaimLevel|str,
    evidence:Mapping[str,str],
)->ExecutionClaimReceipt:
    merged=dict(receipt.evidence)
    merged.update({str(k):str(v) for k,v in dict(evidence).items()})
    out=ExecutionClaimReceipt(
        object_id=receipt.object_id,
        claim_id=receipt.claim_id,
        claimed_level=claimed_level,
        evidence=merged,
    )
    require_execution_claim(out)
    return out


def from_protected_transition(
    receipt:ProtectedTransitionReceipt,
    *,
    claim_id:str,
    plan_evidence:str,
)->ExecutionClaimReceipt:
    """Project a verified configured-tool PTI receipt into this generic claim surface.

    This is intentionally a projection.  The configured-tool path continues to
    be governed by PTI itself.
    """
    require_protected_transition(receipt)
    ev=dict(receipt.evidence)
    out=ExecutionClaimReceipt(
        object_id=receipt.object_id,
        claim_id=str(claim_id),
        claimed_level=ExecutionClaimLevel.CONSUMED,
        evidence={
            "identity":str(ev.get("canonical_identity","")),
            "plan":str(plan_evidence),
            "dispatch":str(ev.get("configured_dispatch","")),
            "execution":str(ev.get("execution","")),
            "consumption":str(ev.get("result_consumption","")),
        },
    )
    require_execution_claim(out,minimum_level=ExecutionClaimLevel.CONSUMED)
    return out
