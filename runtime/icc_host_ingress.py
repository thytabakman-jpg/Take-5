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
    -> HOST_INGRESS_ADMITTED structural receipt
    -> separate trusted issuer attestation for hosted execution/identity

The host must carry explicit evidence-receipt identifiers rather than naked
boolean assertions. This module still cannot verify an unrelated host's private
state; it fails closed when the host cannot present the required receipts.

Without a separately authenticated attestation, a structural receipt is only
bookkeeping. The hosted gateway blocks repository-backed ICC execution/identity.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import hmac
import re
import time


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
    repository_verification_receipt: str
    currentness_verification_receipt: str
    entry_contract_receipt: str
    bootstrap_receipt: str
    controller_id: str
    controller_registration_receipt: str


@dataclass(frozen=True)
class ICCHostIngressReceipt:
    status: str
    repository: str
    ref: str
    commit_sha: str
    controller_id: str
    request_digest: str
    evidence_digest: str
    receipt_id: str

    @property
    def short_commit(self) -> str:
        return self.commit_sha[:8]


@dataclass(frozen=True)
class TrustedHostIngressAttestation:
    """Short-lived MAC issued by a separate, trusted execution verifier.

    The verifier must authenticate repository/currentness evidence, the actual
    ASSERT -> GOAL run, and bound controller execution before issuing this MAC.
    This module only authenticates the verifier's attestation, not those events.
    """
    issuer: str
    receipt_id: str
    issued_at: int
    expires_at: int
    signature: str


TRUSTED_ISSUER = "TAKE5_HOST_EXECUTION_VERIFIER_V1"
MAX_ATTESTATION_SECONDS = 300


def _attestation_message(receipt: ICCHostIngressReceipt, attestation: TrustedHostIngressAttestation) -> bytes:
    return "\n".join((
        TRUSTED_ISSUER,
        receipt.repository,
        receipt.ref,
        receipt.commit_sha,
        receipt.controller_id,
        receipt.request_digest,
        receipt.evidence_digest,
        receipt.receipt_id,
        str(attestation.issued_at),
        str(attestation.expires_at),
    )).encode("utf-8")


def require_trusted_icc_host_ingress(
    receipt: ICCHostIngressReceipt | None,
    attestation: TrustedHostIngressAttestation | None,
    secret: bytes | None,
    *,
    now: int | None = None,
) -> ICCHostIngressReceipt:
    """Fail closed unless the exact ingress receipt has a fresh trusted MAC.

    The secret is provisioned only in the trusted execution-verifier/gateway
    environment; user-supplied receipt strings never authorize identity.
    """
    verified = require_icc_host_ingress(receipt)
    if not isinstance(secret, bytes) or len(secret) < 32:
        raise ICCHostIngressBlocked("ICC_TRUSTED_VERIFIER_NOT_CONFIGURED")
    if not isinstance(attestation, TrustedHostIngressAttestation):
        raise ICCHostIngressBlocked("ICC_TRUSTED_ATTESTATION_REQUIRED")
    if attestation.issuer != TRUSTED_ISSUER or attestation.receipt_id != verified.receipt_id:
        raise ICCHostIngressBlocked("ICC_TRUSTED_ATTESTATION_IDENTITY_MISMATCH")
    if (
        not isinstance(attestation.issued_at, int)
        or isinstance(attestation.issued_at, bool)
        or not isinstance(attestation.expires_at, int)
        or isinstance(attestation.expires_at, bool)
    ):
        raise ICCHostIngressBlocked("ICC_TRUSTED_ATTESTATION_TIME_INVALID")
    current = int(time.time()) if now is None else int(now)
    if (
        attestation.issued_at > current + 30
        or attestation.expires_at <= current
        or attestation.expires_at <= attestation.issued_at
        or attestation.expires_at - attestation.issued_at > MAX_ATTESTATION_SECONDS
    ):
        raise ICCHostIngressBlocked("ICC_TRUSTED_ATTESTATION_EXPIRED_OR_INVALID")
    expected = hmac.new(secret, _attestation_message(verified, attestation), sha256).hexdigest()
    if not isinstance(attestation.signature, str) or not hmac.compare_digest(attestation.signature, expected):
        raise ICCHostIngressBlocked("ICC_TRUSTED_ATTESTATION_INVALID_SIGNATURE")
    return verified


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


def _require_receipt(value: str, error: str) -> str:
    receipt=str(value).strip()
    if not receipt:
        raise ICCHostIngressBlocked(error)
    return receipt


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
    repository_receipt=_require_receipt(
        evidence.repository_verification_receipt,
        "ICC_REPOSITORY_VERIFICATION_RECEIPT_REQUIRED",
    )
    currentness_receipt=_require_receipt(
        evidence.currentness_verification_receipt,
        "ICC_CURRENTNESS_VERIFICATION_RECEIPT_REQUIRED",
    )
    entry_receipt=_require_receipt(
        evidence.entry_contract_receipt,
        "ICC_ENTRY_CONTRACT_RECEIPT_REQUIRED",
    )
    bootstrap_receipt=_require_receipt(
        evidence.bootstrap_receipt,
        "ICC_BOOTSTRAP_RECEIPT_REQUIRED",
    )
    if evidence.controller_id != CANONICAL_CONTROLLER:
        raise ICCHostIngressBlocked("ICC_CONTROLLER_IDENTITY_MISMATCH")
    registration_receipt=_require_receipt(
        evidence.controller_registration_receipt,
        "ICC_CONTROLLER_REGISTRATION_RECEIPT_REQUIRED",
    )

    request_body = strip_icc_prefix(user_text)
    request_digest = _digest(request_body)
    evidence_material = "|".join((
        repository_receipt,
        currentness_receipt,
        entry_receipt,
        bootstrap_receipt,
        registration_receipt,
    ))
    evidence_digest = _digest(evidence_material)
    identity_material = "|".join((
        evidence.repository,
        evidence.ref,
        evidence.commit_sha,
        evidence.controller_id,
        request_digest,
        evidence_digest,
        "HOST_INGRESS_ADMITTED_V2",
    ))
    receipt_id = _digest(identity_material)

    return ICCHostIngressReceipt(
        status="HOST_INGRESS_ADMITTED",
        repository=evidence.repository,
        ref=evidence.ref,
        commit_sha=evidence.commit_sha,
        controller_id=evidence.controller_id,
        request_digest=request_digest,
        evidence_digest=evidence_digest,
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
    if (
        not receipt.commit_sha
        or not receipt.request_digest
        or not receipt.evidence_digest
        or not receipt.receipt_id
    ):
        raise ICCHostIngressBlocked("ICC_HOST_INGRESS_RECEIPT_INCOMPLETE")
    return receipt
