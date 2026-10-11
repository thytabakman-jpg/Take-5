"""Canonical host-facing gateway into Take-5 ICC.

External hosts use this surface after constructing a valid ICCHostIngressReceipt.
It is intentionally thinner than icc_entry: host identity admission belongs here,
while ICC execution semantics remain owned by icc_entry.run_icc.
"""
from __future__ import annotations

import os
from typing import Iterable

from icc_entry import run_icc
from icc_host_ingress import (
    ICCHostIngressReceipt,
    TrustedHostIngressAttestation,
    require_trusted_icc_host_ingress,
)
from mathematical_color_gate import (
    AssessedMathFragment,
    Fragment,
    MathStatus,
    RecoveryAssessment,
    TextFragment,
)
from result_path_registry import emit_default_result



def _require_authenticated_ingress(
    receipt: ICCHostIngressReceipt | None,
    attestation: TrustedHostIngressAttestation | None,
) -> ICCHostIngressReceipt:
    # This key is trusted deployment configuration, never a host-input parameter.
    key = os.environ.get("TAKE5_TRUSTED_ICC_INGRESS_KEY")
    secret = key.encode("utf-8") if key is not None else None
    return require_trusted_icc_host_ingress(receipt, attestation, secret)


def run_hosted_icc(
    host_ingress_receipt: ICCHostIngressReceipt | None,
    *args,
    trusted_attestation: TrustedHostIngressAttestation | None = None,
    **kwargs,
):
    """Execute ICC only after the trusted verifier attests exact ingress."""
    _require_authenticated_ingress(host_ingress_receipt, trusted_attestation)
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
    *,
    trusted_attestation: TrustedHostIngressAttestation | None = None,
) -> str:
    """Emit verified identity only with a trusted attestation of exact ingress."""
    receipt=_require_authenticated_ingress(host_ingress_receipt, trusted_attestation)
    return emit_default_result((
        _identity_fragment("ICC128",receipt),
        TextFragment(" "),
        _identity_fragment("TAKE5",receipt),
        TextFragment(
            f"/main @{receipt.short_commit} ingress:{receipt.receipt_id[:12]}\n"
        ),
        *tuple(fragments),
    ))
