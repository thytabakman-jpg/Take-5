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
        commit_sha="519428bc2bf0b4560b2f859f0413b5147917b56a",
        repository_verification_receipt="github:repo:verified",
        currentness_verification_receipt="currentness:main:519428bc",
        entry_contract_receipt="entry:bound:icc128",
        bootstrap_receipt="bootstrap:ASSERT_OBSERVER>GOAL_OBSERVER",
        controller_id="ICC128",
        controller_registration_receipt="registry:ICC128:current",
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
    assert r"\color{green}{\operatorname{ICC128}}" in out
    assert r"\color{green}{\operatorname{TAKE5}}" in out
    assert "/main @519428bc ingress:" in out
    assert out.endswith("answer")


def test_hosted_emission_cannot_claim_icc_without_receipt():
    with pytest.raises(ICCHostIngressBlocked,match="ICC_HOST_INGRESS_RECEIPT_REQUIRED"):
        emit_hosted_icc_result(None,(TextFragment("answer"),))
