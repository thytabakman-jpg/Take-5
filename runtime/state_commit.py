"""Typed state-specific commit gates over one common protected transition contract.

This module does not force every state species through one physical store.  It gives
protected state species one receipt shape and one legality contract before mutation.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable


class StateRole(str, Enum):
    SYSTEM_CONTROL = "SYSTEM_CONTROL"
    RESULT = "RESULT"
    LINEAGE = "LINEAGE"
    RESEARCH_CONTROL = "RESEARCH_CONTROL"
    SUPERVISORY = "SUPERVISORY"


NON_SUCCESS = {"OPEN", "BLOCKED", "INCOMPARABLE", "CONFLICT"}


@dataclass(frozen=True)
class CommitRequest:
    role: StateRole
    effect: str
    target: str
    job: str
    baseline: str
    authority_before: frozenset[str]
    authority_after: frozenset[str]
    evidence: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()
    execution_receipt: str | None = None
    verification_receipt: str | None = None
    status: str = "CLOSED_RELATIVE"
    material: bool = True


@dataclass(frozen=True)
class CommitReceipt:
    role: StateRole
    effect: str
    target: str
    job: str
    baseline: str
    status: str
    authority: tuple[str, ...]
    evidence: tuple[str, ...]
    provenance: tuple[str, ...]
    execution_receipt: str | None
    verification_receipt: str | None
    material: bool


class CommitBlocked(PermissionError):
    pass


def authorize_commit(
    req: CommitRequest,
    *,
    require_execution: bool = False,
    require_verification: bool = False,
    require_evidence: bool = False,
    require_provenance: bool = True,
) -> CommitReceipt:
    status = str(req.status)
    if status in NON_SUCCESS:
        raise CommitBlocked(f"NON_SUCCESS_STATUS:{status}")
    if not req.target or not req.job or not req.baseline or not req.effect:
        raise CommitBlocked("IDENTITY_OR_TRANSITION_UNBOUND")
    if not req.authority_after <= req.authority_before:
        raise CommitBlocked("AUTHORITY_ESCALATION")
    if require_execution and not req.execution_receipt:
        raise CommitBlocked("EXECUTION_RECEIPT_REQUIRED")
    if require_verification and not req.verification_receipt:
        raise CommitBlocked("VERIFICATION_RECEIPT_REQUIRED")
    if require_evidence and not req.evidence:
        raise CommitBlocked("EVIDENCE_REQUIRED")
    if require_provenance and not req.provenance:
        raise CommitBlocked("PROVENANCE_REQUIRED")

    return CommitReceipt(
        role=req.role,
        effect=req.effect,
        target=req.target,
        job=req.job,
        baseline=req.baseline,
        status=status,
        authority=tuple(sorted(req.authority_after)),
        evidence=tuple(req.evidence),
        provenance=tuple(req.provenance),
        execution_receipt=req.execution_receipt,
        verification_receipt=req.verification_receipt,
        material=bool(req.material),
    )


def receipt_ref(receipt: CommitReceipt) -> str:
    return f"{receipt.role.value}:{receipt.target}:{receipt.job}:{receipt.baseline}:{receipt.effect}"


def require_role(receipt: CommitReceipt, role: StateRole) -> None:
    if receipt.role != role:
        raise CommitBlocked(f"COMMIT_ROLE_MISMATCH:{receipt.role.value}!={role.value}")
