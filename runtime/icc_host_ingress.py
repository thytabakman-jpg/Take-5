"""Fail-closed host ingress contract for repository-backed ICC identity.

This module does not make an external ChatGPT host become ICC. It defines the
evidence required before any external host may truthfully claim that a request
entered the canonical Take-5 ICC path.

Contract:
    raw user request beginning with ICC
    -> canonical repository/head evidence
    -> currentness evidence
    -> bound entry contract
    -> complete ASSERT->GOAL bootstrap evidence
    -> ICC128 registered-controller evidence
    -> HOST_INGRESS_ADMITTED receipt

Without the receipt, the host may answer as itself, but it may not represent the
answer as a repository-backed ICC execution.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import re


CANONICAL_REPOSITORY = "thytabakman-jpg/Take-5"
CANONICAL_REF = "main"
CANONICAL_CONTROLLER = "ICC128"

ICC_PREFIX = re.compile(
    r"^\s*icc\b(?:\s*[,.:;\-]\s*|\s+)",
    flags=re.IGNORECASE,
)


class ICCHostIngressBlocked(RuntimeError):
    pass


@dataclass(frozen=True)
class HostIngressEvidence:
    repository: str
    ref: str
    commit_sha: str
    canonical_repository_verified: bool
    currentness_verified: bool
    entry_contract_bound: bool
    bootstrap_complete: bool
    controller_id: str
    controller_registered: bool


@dataclass(frozen=True)
class ICCHostIngressReceipt:
    status: str
    repository: str
    ref: str
    commit_sha: str
    controller_id: str
    request_digest: str
    receipt_id: str

    @property
    def short_commit(self) -> str:
        return self.commit_sha[:8]


def is_icc_request(user_text: str) -> bool:
    return bool(ICC_PREFIX.search(str(user_text)))


def strip_icc_prefix(user_text: str) -> str:
    text = str(user_text)
    match = ICC_PREFIX.search(text)
    if not match:
        raise ICCHostIngressBlocked("ICC_PREFIX_REQUIRED")
    payload = text[match.end():].strip()
    if not payload:
        raise ICCHostIngressBlocked("ICC_REQUEST_BODY_REQUIRED")
    return payload


def _digest(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def admit_icc_host_ingress(
    user_text: str,
    evidence: HostIngressEvidence,
) -> ICCHostIngressReceipt:
    if not is_icc_request(user_text):
        raise ICCHostIngressBlocked("ICC_PREFIX_REQUIRED")

    if evidence.repository != CANONICAL_REPOSITORY:
        raise ICCHostIngressBlocked("ICC_CANONICAL_REPOSITORY_MISMATCH")
    if evidence.ref != CANONICAL_REF:
        raise ICCHostIngressBlocked("ICC_CANONICAL_REF_REQUIRED")
    if not evidence.commit_sha or len(evidence.commit_sha) < 8:
        raise ICCHostIngressBlocked("ICC_CANONICAL_COMMIT_REQUIRED")
    if not evidence.canonical_repository_verified:
        raise ICCHostIngressBlocked("ICC_REPOSITORY_VERIFICATION_REQUIRED")
    if not evidence.currentness_verified:
        raise ICCHostIngressBlocked("ICC_CURRENTNESS_VERIFICATION_REQUIRED")
    if not evidence.entry_contract_bound:
        raise ICCHostIngressBlocked("ICC_ENTRY_CONTRACT_REQUIRED")
    if not evidence.bootstrap_complete:
        raise ICCHostIngressBlocked("ICC_BOOTSTRAP_RECEIPT_REQUIRED")
    if evidence.controller_id != CANONICAL_CONTROLLER:
        raise ICCHostIngressBlocked("ICC_CONTROLLER_IDENTITY_MISMATCH")
    if not evidence.controller_registered:
        raise ICCHostIngressBlocked("ICC_CONTROLLER_REGISTRATION_REQUIRED")

    request_body = strip_icc_prefix(user_text)
    request_digest = _digest(request_body)
    identity_material = "|".join((
        evidence.repository,
        evidence.ref,
        evidence.commit_sha,
        evidence.controller_id,
        request_digest,
        "HOST_INGRESS_ADMITTED_V1",
    ))
    receipt_id = _digest(identity_material)

    return ICCHostIngressReceipt(
        status="HOST_INGRESS_ADMITTED",
        repository=evidence.repository,
        ref=evidence.ref,
        commit_sha=evidence.commit_sha,
        controller_id=evidence.controller_id,
        request_digest=request_digest,
        receipt_id=receipt_id,
    )


def require_icc_host_ingress(
    receipt: ICCHostIngressReceipt | None,
) -> ICCHostIngressReceipt:
    if not isinstance(receipt, ICCHostIngressReceipt):
        raise ICCHostIngressBlocked("ICC_HOST_INGRESS_RECEIPT_REQUIRED")
    if receipt.status != "HOST_INGRESS_ADMITTED":
        raise ICCHostIngressBlocked("ICC_HOST_INGRESS_NOT_ADMITTED")
    if receipt.repository != CANONICAL_REPOSITORY:
        raise ICCHostIngressBlocked("ICC_HOST_INGRESS_REPOSITORY_DRIFT")
    if receipt.ref != CANONICAL_REF:
        raise ICCHostIngressBlocked("ICC_HOST_INGRESS_REF_DRIFT")
    if receipt.controller_id != CANONICAL_CONTROLLER:
        raise ICCHostIngressBlocked("ICC_HOST_INGRESS_CONTROLLER_DRIFT")
    if not receipt.commit_sha or not receipt.request_digest or not receipt.receipt_id:
        raise ICCHostIngressBlocked("ICC_HOST_INGRESS_RECEIPT_INCOMPLETE")
    return receipt


def receipt_banner(receipt: ICCHostIngressReceipt) -> str:
    r = require_icc_host_ingress(receipt)
    return (
        f"{r.controller_id} "
        f"{r.repository}@{r.ref}:{r.short_commit} "
        f"ingress:{r.receipt_id[:12]}"
    )
