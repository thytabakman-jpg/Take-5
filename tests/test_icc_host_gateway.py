import sys
sys.path.insert(0,"runtime")

import pytest

import icc_host_gateway
from icc_host_gateway import emit_hosted_icc_result, run_hosted_icc
from icc_host_ingress import HostIngressEvidence, admit_icc_host_ingress, ICCHostIngressBlocked
from mathematical_color_gate import TextFragment


def _receipt():
    evidence=HostIngressEvidence(
        repository="thytabakman-jpg/Take-5",
        ref="main",
        commit_sha="1967e45dc62bbd99795d291be1d430b2f58f329f",
        canonical_repository_verified=True,
        currentness_verified=True,
        entry_contract_bound=True,
        bootstrap_complete=True,
        controller_id="ICC128",
        controller_registered=True,
    )
    return admit_icc_host_ingress("ICC, fix it.",evidence)


def test_host_gateway_refuses_execution_without_ingress_receipt():
    with pytest.raises(ICCHostIngressBlocked,match="ICC_HOST_INGRESS_RECEIPT_REQUIRED"):
        run_hosted_icc(None)


def test_host_gateway_delegates_only_after_receipt(monkeypatch):
    calls=[]
    def fake_run(*args,**kwargs):
        calls.append((args,kwargs))
        return {"status":"OK"}

    monkeypatch.setattr(icc_host_gateway,"run_icc",fake_run)
    out=run_hosted_icc(_receipt(),"binding","state","jane",marker=1)
    assert out=={"status":"OK"}
    assert calls==[(("binding","state","jane"),{"marker":1})]


def test_hosted_emission_requires_receipt_and_exposes_source_identity():
    out=emit_hosted_icc_result(_receipt(),(TextFragment("answer"),))
    assert "ICC128 thytabakman-jpg/Take-5@main:1967e45d ingress:" in out
    assert out.endswith("answer")


def test_hosted_emission_cannot_claim_icc_without_receipt():
    with pytest.raises(ICCHostIngressBlocked,match="ICC_HOST_INGRESS_RECEIPT_REQUIRED"):
        emit_hosted_icc_result(None,(TextFragment("answer"),))
