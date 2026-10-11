import sys
import hashlib
import hmac
import time
from dataclasses import replace
sys.path.insert(0,"runtime")

import pytest

import icc_host_gateway
from icc_host_gateway import emit_hosted_icc_result, run_hosted_icc
from icc_host_ingress import (
    HostIngressEvidence, admit_icc_host_ingress, ICCHostIngressBlocked,
    TrustedHostIngressAttestation, TRUSTED_ISSUER,
)
from mathematical_color_gate import TextFragment


def _receipt():
    evidence=HostIngressEvidence(
        repository="thytabakman-jpg/Take-5",
        ref="main",
        commit_sha="519428bc2bf0b4560b2f859f0413b5147917b56a",
        repository_verification_receipt="github:repo:verified",
        currentness_verification_receipt="currentness:main:519428bc",
        entry_contract_receipt="entry:bound:icc128",
        bootstrap_receipt="bootstrap:ASSERT_OBSERVER>GOAL_OBSERVER",
        controller_id="ICC128",
        controller_registration_receipt="registry:ICC128:current",
    )
    return admit_icc_host_ingress("ICC, fix it.",evidence)


_SECRET = "test-only-host-verifier-secret-longer-than-32-bytes"


def _attestation(receipt, *, issued_at=None, expires_at=None, secret=_SECRET):
    created = int(time.time()) if issued_at is None else issued_at
    expiration = created + 120 if expires_at is None else expires_at
    fields = (
        TRUSTED_ISSUER, receipt.repository, receipt.ref, receipt.commit_sha,
        receipt.controller_id, receipt.request_digest, receipt.evidence_digest,
        receipt.receipt_id, str(created), str(expiration),
    )
    payload = "\n".join(fields).encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return TrustedHostIngressAttestation(
        TRUSTED_ISSUER, receipt.receipt_id, created, expiration, signature,
    )


def _trusted(monkeypatch):
    monkeypatch.setenv("TAKE5_TRUSTED_ICC_INGRESS_KEY", _SECRET)
    receipt = _receipt()
    return receipt, _attestation(receipt)


def test_host_gateway_refuses_execution_without_ingress_receipt():
    with pytest.raises(ICCHostIngressBlocked,match="ICC_HOST_INGRESS_RECEIPT_REQUIRED"):
        run_hosted_icc(None)


def test_host_gateway_delegates_only_after_verified_attestation(monkeypatch):
    calls=[]
    def fake_run(*args,**kwargs):
        calls.append((args,kwargs))
        return {"status":"OK"}

    monkeypatch.setattr(icc_host_gateway,"run_icc",fake_run)
    receipt, attestation = _trusted(monkeypatch)
    out=run_hosted_icc(receipt,"binding","state","jane",trusted_attestation=attestation,marker=1)
    assert out=={"status":"OK"}
    assert calls==[(("binding","state","jane"),{"marker":1})]


def test_hosted_emission_requires_verified_attestation_and_exposes_source_identity(monkeypatch):
    receipt, attestation = _trusted(monkeypatch)
    out=emit_hosted_icc_result(receipt,(TextFragment("answer"),),trusted_attestation=attestation)
    assert r"\color{green}{\operatorname{ICC128}}" in out
    assert r"\color{green}{\operatorname{TAKE5}}" in out
    assert "/main @519428bc ingress:" in out
    assert out.endswith("answer")


def test_hosted_emission_cannot_claim_icc_without_receipt():
    with pytest.raises(ICCHostIngressBlocked,match="ICC_HOST_INGRESS_RECEIPT_REQUIRED"):
        emit_hosted_icc_result(None,(TextFragment("answer"),))


def test_fabricated_receipt_cannot_trigger_execution_without_trusted_verifier(monkeypatch):
    monkeypatch.delenv("TAKE5_TRUSTED_ICC_INGRESS_KEY", raising=False)
    called = []
    monkeypatch.setattr(icc_host_gateway,"run_icc",lambda *a,**k: called.append(True))
    with pytest.raises(ICCHostIngressBlocked,match="ICC_TRUSTED_VERIFIER_NOT_CONFIGURED"):
        run_hosted_icc(_receipt(),trusted_attestation=_attestation(_receipt()))
    assert called == []


def test_fabricated_receipt_cannot_emit_identity_without_attestation(monkeypatch):
    monkeypatch.setenv("TAKE5_TRUSTED_ICC_INGRESS_KEY", _SECRET)
    with pytest.raises(ICCHostIngressBlocked,match="ICC_TRUSTED_ATTESTATION_REQUIRED"):
        emit_hosted_icc_result(_receipt(),(TextFragment("answer"),))


@pytest.mark.parametrize("adversary",["wrong_key","wrong_receipt","expired","too_long","future","wrong_issuer","bad_signature_format"])
def test_trusted_gate_rejects_forged_stale_or_cross_request_attestation(monkeypatch,adversary):
    receipt, attestation = _trusted(monkeypatch)
    if adversary == "wrong_key":
        attestation = _attestation(receipt,secret="completely-different-external-attestation-key")
    elif adversary == "wrong_receipt":
        other = admit_icc_host_ingress("ICC, a different request.",HostIngressEvidence(
            repository=receipt.repository,ref=receipt.ref,commit_sha=receipt.commit_sha,
            repository_verification_receipt="repo",currentness_verification_receipt="current",
            entry_contract_receipt="entry",bootstrap_receipt="bootstrap",
            controller_id=receipt.controller_id,controller_registration_receipt="registry",
        ))
        attestation = _attestation(other)
    elif adversary == "expired":
        attestation = _attestation(receipt,issued_at=int(time.time())-200,expires_at=int(time.time())-60)
    elif adversary == "too_long":
        attestation = _attestation(receipt,expires_at=int(time.time())+600)
    elif adversary == "future":
        attestation = _attestation(receipt,issued_at=int(time.time())+200)
    elif adversary == "wrong_issuer":
        attestation = replace(attestation,issuer="UNTRUSTED")
    elif adversary == "bad_signature_format":
        attestation = replace(attestation,signature="��" * 64)
    with pytest.raises(ICCHostIngressBlocked,match="ICC_TRUSTED_ATTESTATION_"):
        emit_hosted_icc_result(receipt,(TextFragment("answer"),),trusted_attestation=attestation)
