import sys
sys.path.insert(0,"runtime")

import pytest

from repository_authority import (
    RepositoryAuthorityError,
    require_repository_authority,
    resolve_repository_authority,
)


def test_take5_is_canonical_working_repository():
    out=resolve_repository_authority("thytabakman-jpg/Take-5",operation="MUTATE")
    assert out.status=="PASS"
    assert out.disposition=="CANONICAL_WORKING"


def test_reaserch_remains_valid_provenance_read_source():
    out=resolve_repository_authority("thytabakman-jpg/Reaserch",operation="RECONCILE")
    assert out.status=="PASS"
    assert out.disposition=="LEGACY_PROVENANCE_ONLY"


def test_reaserch_new_mutation_fails_closed():
    out=resolve_repository_authority("thytabakman-jpg/Reaserch",operation="MUTATE")
    assert out.status=="BLOCKED"
    assert out.canonical_repository=="thytabakman-jpg/Take-5"
    with pytest.raises(RepositoryAuthorityError):
        require_repository_authority("thytabakman-jpg/Reaserch",operation="MUTATE")


def test_unknown_repository_does_not_gain_authority_by_recency():
    out=resolve_repository_authority("thytabakman-jpg/Take-4",operation="MUTATE")
    assert out.status=="BLOCKED"
    assert out.blocker=="REPOSITORY_NOT_ADMITTED_BY_MIGRATION_STATE"
