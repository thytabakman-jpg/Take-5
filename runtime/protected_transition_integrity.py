"""Protected Transition Integrity (PTI).

PTI is the cross-system invariant recovered from RootCause run 089.

A protected behavior is not considered operationally preserved merely because it
exists in semantics, a manifest, or a runtime file. The chain must remain intact
through identity, dispatch, execution, consumption, state update, reentry, and
user-visible boundary.

This module provides a typed receipt and fail-closed validator for that chain.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class PTIState(str, Enum):
    VERIFIED="VERIFIED"
    OPEN="OPEN"
    BLOCKED="BLOCKED"
    MISSING="MISSING"


COORDINATES=(
    "canonical_identity",
    "configured_dispatch",
    "execution",
    "result_consumption",
    "state_update",
    "reentry",
    "user_visible_boundary",
)


@dataclass(frozen=True)
class ProtectedTransitionReceipt:
    object_id:str
    behavior_id:str
    coordinates:Mapping[str,PTIState|str]
    evidence:Mapping[str,str]

    def normalized(self):
        return {
            key:(value if isinstance(value,PTIState) else PTIState(str(value)))
            for key,value in self.coordinates.items()
        }


@dataclass(frozen=True)
class ProtectedTransitionAssessment:
    object_id:str
    behavior_id:str
    status:str
    open_coordinates:tuple[str,...]
    blocked_coordinates:tuple[str,...]
    missing_coordinates:tuple[str,...]


class ProtectedTransitionIntegrityError(RuntimeError):
    pass


def assess_protected_transition(receipt:ProtectedTransitionReceipt)->ProtectedTransitionAssessment:
    states=receipt.normalized()
    open_coords=[]
    blocked=[]
    missing=[]

    for coordinate in COORDINATES:
        if coordinate not in states:
            missing.append(coordinate)
            continue
        state=states[coordinate]
        if state is PTIState.OPEN:
            open_coords.append(coordinate)
        elif state is PTIState.BLOCKED:
            blocked.append(coordinate)
        elif state is PTIState.MISSING:
            missing.append(coordinate)

    if blocked:
        status="BLOCKED"
    elif missing or open_coords:
        status="OPEN"
    else:
        status="VERIFIED"

    return ProtectedTransitionAssessment(
        receipt.object_id,
        receipt.behavior_id,
        status,
        tuple(open_coords),
        tuple(blocked),
        tuple(missing),
    )


def require_protected_transition(receipt:ProtectedTransitionReceipt)->ProtectedTransitionAssessment:
    assessment=assess_protected_transition(receipt)
    if assessment.status!="VERIFIED":
        details=";".join(
            (
                "open="+",".join(assessment.open_coordinates),
                "blocked="+",".join(assessment.blocked_coordinates),
                "missing="+",".join(assessment.missing_coordinates),
            )
        )
        raise ProtectedTransitionIntegrityError(
            f"PROTECTED_TRANSITION_INCOMPLETE:{receipt.object_id}:{receipt.behavior_id}:{details}"
        )
    return assessment


def complete_receipt(
    *,
    object_id:str,
    behavior_id:str,
    evidence:Mapping[str,str],
)->ProtectedTransitionReceipt:
    missing=[x for x in COORDINATES if not evidence.get(x)]
    if missing:
        raise ProtectedTransitionIntegrityError(
            "PROTECTED_TRANSITION_EVIDENCE_MISSING:"+",".join(missing)
        )
    return ProtectedTransitionReceipt(
        object_id=object_id,
        behavior_id=behavior_id,
        coordinates={x:PTIState.VERIFIED for x in COORDINATES},
        evidence=dict(evidence),
    )
