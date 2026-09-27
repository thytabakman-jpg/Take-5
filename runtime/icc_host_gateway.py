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
    receipt_banner,
    require_icc_host_ingress,
)
from mathematical_color_gate import Fragment, TextFragment
from result_path_registry import emit_default_result


def run_hosted_icc(
    host_ingress_receipt: ICCHostIngressReceipt | None,
    *args,
    **kwargs,
):
    """Execute ICC only after host-level repository ingress was admitted."""
    require_icc_host_ingress(host_ingress_receipt)
    return run_icc(*args, **kwargs)


def emit_hosted_icc_result(
    host_ingress_receipt: ICCHostIngressReceipt | None,
    fragments: Iterable[Fragment],
) -> str:
    """Emit a repository-backed ICC result with its visible ingress receipt."""
    receipt=require_icc_host_ingress(host_ingress_receipt)
    banner=receipt_banner(receipt)
    return emit_default_result((
        TextFragment(banner+"\n"),
        *tuple(fragments),
    ))
