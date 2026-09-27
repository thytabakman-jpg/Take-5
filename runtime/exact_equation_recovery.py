"""Fail-closed exact historical equation recovery.

This module separates:
- exact historical recovery,
- derived reconstruction,
- rejected candidates,
- and unresolved candidates.

A candidate cannot establish its own historical identity. Exact recovery requires
an external evidence receipt, and explicit rejection is durable for the frozen
recovery target until that rejection is explicitly reopened.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class EquationCandidate:
    candidate_id: str
    target_id: str
    expression: str
    derivation_kind: str  # EXACT_COPY | DERIVED | SYNTHESIZED


@dataclass(frozen=True)
class RecoveryReceipt:
    candidate_id: str
    target_id: str
    source_ref: str
    source_kind: str
    exact_expression_match: bool
    evidence: Tuple[str, ...] = ()


@dataclass(frozen=True)
class RecoveryMemory:
    rejected_candidate_ids: Tuple[str, ...] = ()
    rejected_expressions: Tuple[str, ...] = ()
    reopened_candidate_ids: Tuple[str, ...] = ()


@dataclass(frozen=True)
class RecoveryDisposition:
    status: str
    reason: str
    candidate_id: str


def classify(
    candidate: EquationCandidate,
    receipt: RecoveryReceipt | None,
    memory: RecoveryMemory = RecoveryMemory(),
) -> RecoveryDisposition:
    if not candidate.candidate_id or not candidate.target_id or not candidate.expression:
        return RecoveryDisposition("OPEN", "INCOMPLETE_CANDIDATE_IDENTITY", candidate.candidate_id)

    rejected = (
        candidate.candidate_id in memory.rejected_candidate_ids
        or candidate.expression in memory.rejected_expressions
    )
    reopened = candidate.candidate_id in memory.reopened_candidate_ids
    if rejected and not reopened:
        return RecoveryDisposition("REJECTED", "DURABLE_DISCONFIRMATION", candidate.candidate_id)

    if candidate.derivation_kind != "EXACT_COPY":
        return RecoveryDisposition(
            "DERIVED_RECONSTRUCTION",
            "NOT_AN_EXACT_HISTORICAL_COPY",
            candidate.candidate_id,
        )

    if receipt is None:
        return RecoveryDisposition("OPEN", "EXTERNAL_RECOVERY_RECEIPT_REQUIRED", candidate.candidate_id)

    if receipt.candidate_id != candidate.candidate_id or receipt.target_id != candidate.target_id:
        return RecoveryDisposition("CONFLICT", "RECEIPT_IDENTITY_MISMATCH", candidate.candidate_id)

    if not receipt.source_ref or not receipt.source_kind or not receipt.evidence:
        return RecoveryDisposition("OPEN", "SOURCE_PROVENANCE_INCOMPLETE", candidate.candidate_id)

    if not receipt.exact_expression_match:
        return RecoveryDisposition("OPEN", "EXACT_SOURCE_MATCH_NOT_ESTABLISHED", candidate.candidate_id)

    return RecoveryDisposition("EXACT_RECOVERY", "SOURCE_BACKED_EXACT_MATCH", candidate.candidate_id)
