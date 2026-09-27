import sys
sys.path.insert(0,"runtime")

import pytest

from icc_host_ingress import (
    HostIngressEvidence,
    ICCHostIngressBlocked,
    admit_icc_host_ingress,
    is_icc_request,
    require_icc_host_ingress,
    strip_icc_prefix,
)


def _evidence(**overrides):
    data=dict(
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
    data.update(overrides)
    return HostIngressEvidence(**data)


@pytest.mark.parametrize("text",[
    "ICC, fix it.",
    "icc: run MT",
    "Icc do the thing",
])
def test_icc_prefix_is_recognized(text):
    assert is_icc_request(text)


def test_non_icc_request_is_not_claimed_as_icc():
    assert not is_icc_request("Please fix it.")
    with pytest.raises(ICCHostIngressBlocked,match="ICC_PREFIX_REQUIRED"):
        admit_icc_host_ingress("Please fix it.",_evidence())


def test_prefix_is_removed_before_request_identity_is_hashed():
    assert strip_icc_prefix("ICC, fix it.")=="fix it."


def test_complete_external_evidence_admits_and_yields_receipt():
    r=admit_icc_host_ingress("ICC, fix it.",_evidence())
    assert r.status=="HOST_INGRESS_ADMITTED"
    assert r.repository=="thytabakman-jpg/Take-5"
    assert r.ref=="main"
    assert r.controller_id=="ICC128"
    assert r.short_commit=="519428bc"
    assert r.request_digest
    assert r.evidence_digest
    assert r.receipt_id
    assert require_icc_host_ingress(r) is r


@pytest.mark.parametrize(("field","value","error"),[
    ("repository","thytabakman-jpg/Reaserch","ICC_CANONICAL_REPOSITORY_MISMATCH"),
    ("ref","dev","ICC_CANONICAL_REF_REQUIRED"),
    ("commit_sha","","ICC_CANONICAL_COMMIT_REQUIRED"),
    ("repository_verification_receipt","","ICC_REPOSITORY_VERIFICATION_RECEIPT_REQUIRED"),
    ("currentness_verification_receipt","","ICC_CURRENTNESS_VERIFICATION_RECEIPT_REQUIRED"),
    ("entry_contract_receipt","","ICC_ENTRY_CONTRACT_RECEIPT_REQUIRED"),
    ("bootstrap_receipt","","ICC_BOOTSTRAP_RECEIPT_REQUIRED"),
    ("controller_id","ICC123","ICC_CONTROLLER_IDENTITY_MISMATCH"),
    ("controller_registration_receipt","","ICC_CONTROLLER_REGISTRATION_RECEIPT_REQUIRED"),
])
def test_ingress_fails_closed_on_missing_or_wrong_evidence(field,value,error):
    with pytest.raises(ICCHostIngressBlocked,match=error):
        admit_icc_host_ingress("ICC, fix it.",_evidence(**{field:value}))
