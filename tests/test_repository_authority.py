import sys
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from repository_authority import (
    RepositoryAuthorityError,
    assess_repository_operation,
    require_canonical_mutation,
)

def test_take5_is_only_current_canonical_mutation_target():
    r=require_canonical_mutation("thytabakman-jpg/Take-5","UPDATE")
    assert r.status=="ADMITTED"
    assert r.mutation_allowed is True
    assert r.canonical_effect is True

@pytest.mark.parametrize("repo",[
    "thytabakman-jpg/Reaserch",
    "thytabakman-jpg/Take-2",
    "thytabakman-jpg/Take-3",
    "thytabakman-jpg/Take-4",
])
def test_noncanonical_repositories_fail_closed_for_mutation(repo):
    r=assess_repository_operation(repo,"UPDATE")
    assert r.status=="BLOCKED"
    assert r.mutation_allowed is False
    assert r.evidence_only is True
    with pytest.raises(RepositoryAuthorityError):
        require_canonical_mutation(repo,"UPDATE")

def test_legacy_repository_remains_available_as_evidence():
    r=assess_repository_operation("thytabakman-jpg/Reaserch","RECOVER_EVIDENCE")
    assert r.status=="ADMITTED"
    assert r.evidence_only is True
    assert r.mutation_allowed is False

def test_unknown_repository_is_open_not_guessed():
    r=assess_repository_operation("thytabakman-jpg/Unknown","UPDATE")
    assert r.status=="OPEN"
    assert r.role=="UNRESOLVED"
    assert r.mutation_allowed is False
