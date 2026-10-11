"""Durable report-to-execution target lineage.

Execution Claim Integrity proves the causal execution level. This module proves
that a required durable report exists for that run and is about the same exact
immutable target.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any

from exact_target_identity import ExactTargetIdentity, assess_exact_target
from execution_claim_integrity import (
    ExecutionClaimLevel,
    ExecutionClaimReceipt,
    assess_execution_claim,
)

ALLOWED_STATE_DISPOSITIONS={"UPDATED","PENDING_TYPED","NO_STATE_CHANGE_WITH_PROOF"}
ALLOWED_OWNER_DISPOSITIONS={"ROUTED","COMPLETE","PENDING_TYPED","NO_OWNER_CHANGE_WITH_PROOF"}


@dataclass(frozen=True)
class ReportLineageAssessment:
    status:str
    missing:tuple[str,...]
    conflicts:tuple[str,...]
    target_key:tuple[str,str,str,str]|None
    report_target_key:tuple[str,str,str,str]|None


class ReportLineageError(RuntimeError):
    pass


def _execution_claim(row:Any)->ExecutionClaimReceipt|None:
    if not isinstance(row,Mapping):
        return None
    try:
        return ExecutionClaimReceipt(
            object_id=str(row.get("object_id") or ""),
            claim_id=str(row.get("claim_id") or ""),
            claimed_level=str(row.get("claimed_level") or ""),
            evidence=dict(row.get("evidence") or {}),
        )
    except Exception:
        return None


def assess_report_lineage(
    receipt:Mapping[str,Any],
    *,
    expected_repository:str|None=None,
)->ReportLineageAssessment:
    missing=[]
    conflicts=[]

    run_id=str(receipt.get("run_id") or "")
    if not run_id:
        missing.append("run_id")

    target_raw=receipt.get("target_identity")
    report_target_raw=receipt.get("report_target_identity")
    target=None
    report_target=None

    if not isinstance(target_raw,Mapping):
        missing.append("target_identity")
    else:
        target=ExactTargetIdentity.from_mapping(target_raw)
        a=assess_exact_target(target,expected_repository=expected_repository)
        missing.extend("target_identity."+x for x in a.missing)
        conflicts.extend("target_identity."+x for x in a.conflicts)

    if not isinstance(report_target_raw,Mapping):
        missing.append("report_target_identity")
    else:
        report_target=ExactTargetIdentity.from_mapping(report_target_raw)
        a=assess_exact_target(report_target,expected_repository=expected_repository)
        missing.extend("report_target_identity."+x for x in a.missing)
        conflicts.extend("report_target_identity."+x for x in a.conflicts)

    if target and report_target and target.evidence_key()!=report_target.evidence_key():
        conflicts.append("REPORT_TARGET_LINEAGE_CONFLICT")

    claim=_execution_claim(receipt.get("execution_claim"))
    if claim is None:
        missing.append("execution_claim")
    else:
        try:
            assessment=assess_execution_claim(claim)
            if assessment.status!="VERIFIED":
                missing.extend("execution_claim."+x for x in assessment.missing_coordinates)
            level=claim.level()
            order=list(ExecutionClaimLevel)
            if order.index(level)<order.index(ExecutionClaimLevel.EXECUTED):
                conflicts.append("EXECUTION_CLAIM_BELOW_EXECUTED")
        except Exception:
            conflicts.append("EXECUTION_CLAIM_INVALID")

    if not str(receipt.get("report_locator") or ""):
        missing.append("report_locator")
    if not str(receipt.get("report_content_identity") or ""):
        missing.append("report_content_identity")
    if receipt.get("report_persisted") is not True:
        missing.append("report_persisted")
    if receipt.get("report_read_back_verified") is not True:
        missing.append("report_read_back_verified")
    if str(receipt.get("owner_routing_status") or "") not in ALLOWED_OWNER_DISPOSITIONS:
        missing.append("owner_routing_status")
    if str(receipt.get("affected_state_disposition") or "") not in ALLOWED_STATE_DISPOSITIONS:
        missing.append("affected_state_disposition")

    status="PASS" if not missing and not conflicts else ("CONFLICT" if conflicts else "OPEN")
    return ReportLineageAssessment(
        status=status,
        missing=tuple(dict.fromkeys(missing)),
        conflicts=tuple(dict.fromkeys(conflicts)),
        target_key=target.evidence_key() if target else None,
        report_target_key=report_target.evidence_key() if report_target else None,
    )


def require_report_lineage(
    receipt:Mapping[str,Any],
    *,
    expected_repository:str|None=None,
)->ReportLineageAssessment:
    out=assess_report_lineage(receipt,expected_repository=expected_repository)
    if out.status!="PASS":
        raise ReportLineageError(
            f"REPORT_LINEAGE_{out.status}:missing={','.join(out.missing)}:"
            f"conflicts={','.join(out.conflicts)}"
        )
    return out
