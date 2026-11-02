import sys
sys.path.insert(0,"runtime")

import pytest

from entry_contract import bind_entry_contract
from repository_authority import RepositoryAuthorityError


def test_canonical_take5_mutation_binds_repository_authority():
    out=bind_entry_contract(
        "Improvement Core handle this",
        target="portfolio",
        job="repair",
        basis="test",
        repository="thytabakman-jpg/Take-5",
        repository_operation="MUTATE",
    )
    assert out.contract.repository_authority["status"]=="PASS"
    assert out.contract.repository_authority["disposition"]=="CANONICAL_WORKING"


def test_legacy_reaserch_mutation_is_blocked_before_substantive_entry():
    with pytest.raises(RepositoryAuthorityError,match="ENTRY_REPOSITORY_AUTHORITY_BLOCKED"):
        bind_entry_contract(
            "Improvement Core handle this",
            target="portfolio",
            job="repair",
            basis="test",
            repository="thytabakman-jpg/Reaserch",
            repository_operation="MUTATE",
        )


def test_legacy_reaserch_reconciliation_read_is_legal_and_typed():
    out=bind_entry_contract(
        "Improvement Core compare this",
        target="legacy drift",
        job="reconcile",
        basis="test",
        repository="thytabakman-jpg/Reaserch",
        repository_operation="RECONCILE",
    )
    assert out.contract.repository_authority["status"]=="PASS"
    assert out.contract.repository_authority["disposition"]=="LEGACY_PROVENANCE_ONLY"
