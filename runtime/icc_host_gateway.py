"""Canonical host-facing gateway into Take-5 ICC.

External hosts use this surface after constructing a valid ICCHostIngressReceipt.
It is intentionally thinner than icc_entry: host identity admission belongs here,
while ICC execution semantics remain owned by icc_entry.run_icc.
"""
from __future__ import annotations

from typing import Iterable

from icc_entry import run_icc
from icc_host_ingress import (
    ICCHostIngressReceipt,
    require_icc_host_ingress,
)
from mathematical_color_gate import (
    AssessedMathFragment,
    Fragment,
    MathStatus,
    RecoveryAssessment,
    TextFragment,
)
from result_path_registry import emit_default_result


def run_hosted_icc(
    host_ingress_receipt: ICCHostIngressReceipt | None,
    *args,
    **kwargs,
):
    """Execute ICC only after host-level repository ingress was admitted."""
    require_icc_host_ingress(host_ingress_receipt)
    return run_icc(*args, **kwargs)


def _identity_fragment(label: str, receipt: ICCHostIngressReceipt) -> AssessedMathFragment:
    assessment=RecoveryAssessment(
        object_id=label,
        job="HOST_INGRESS_IDENTITY",
        claim="HOST_INGRESS_RECEIPT_BACKED_IDENTITY",
        required_coordinates=("HOST_INGRESS_RECEIPT",),
        unresolved_coordinates=(),
        complete_for_use=True,
        status=MathStatus.RECOVERED,
        authoritative_claim=False,
        authority_residuals=(),
    )
    return AssessedMathFragment(
        rf"\operatorname{{{label}}}",
        assessment,
    )


def emit_hosted_icc_result(
    host_ingress_receipt: ICCHostIngressReceipt | None,
    fragments: Iterable[Fragment],
) -> str:
    """Emit a repository-backed ICC result with its visible ingress receipt."""
    receipt=require_icc_host_ingress(host_ingress_receipt)
    return emit_default_result((
        _identity_fragment("ICC128",receipt),
        TextFragment(" "),
        _identity_fragment("TAKE5",receipt),
        TextFragment(
            f"/main @{receipt.short_commit} ingress:{receipt.receipt_id[:12]}\n"
        ),
        *tuple(fragments),
    ))
