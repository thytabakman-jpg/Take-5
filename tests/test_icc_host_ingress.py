import sys
sys.path.insert(0,"runtime")

import pytest

from icc_host_ingress import (
    HostIngressEvidence,
    ICCHostIngressBlocked,
    admit_icc_host_ingress,
    is_icc_request,
    receipt_banner,
    require_icc_host_ingress,
    strip_icc_prefix,
)


def _evidence(**overrides):
    data=dict(
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
    assert r.short_commit=="1967e45d"
    assert r.request_digest
    assert r.receipt_id
    assert require_icc_host_ingress(r) is r
    assert receipt_banner(r).startswith(
        "ICC128 thytabakman-jpg/Take-5@main:1967e45d ingress:"
    )


@pytest.mark.parametrize(("field","value","error"),[
    ("repository","thytabakman-jpg/Reaserch","ICC_CANONICAL_REPOSITORY_MISMATCH"),
    ("ref","dev","ICC_CANONICAL_REF_REQUIRED"),
    ("commit_sha","","ICC_CANONICAL_COMMIT_REQUIRED"),
    ("canonical_repository_verified",False,"ICC_REPOSITORY_VERIFICATION_REQUIRED"),
    ("currentness_verified",False,"ICC_CURRENTNESS_VERIFICATION_REQUIRED"),
    ("entry_contract_bound",False,"ICC_ENTRY_CONTRACT_REQUIRED"),
    ("bootstrap_complete",False,"ICC_BOOTSTRAP_RECEIPT_REQUIRED"),
    ("controller_id","ICC123","ICC_CONTROLLER_IDENTITY_MISMATCH"),
    ("controller_registered",False,"ICC_CONTROLLER_REGISTRATION_REQUIRED"),
])
def test_ingress_fails_closed_on_missing_or_wrong_evidence(field,value,error):
    with pytest.raises(ICCHostIngressBlocked,match=error):
        admit_icc_host_ingress("ICC, fix it.",_evidence(**{field:value}))
