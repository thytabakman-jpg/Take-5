import pytest
from state_commit import CommitRequest,CommitBlocked,StateRole,authorize_commit

def req(**overrides):
    base=dict(
        role=StateRole.RESULT,
        effect="ADMIT_RESULT",
        target="x",
        job="solve",
        baseline="v1",
        authority_before=frozenset({"observe","admit"}),
        authority_after=frozenset({"admit"}),
        evidence=("closure",),
        provenance=("episode-1",),
        execution_receipt="exec-1",
        verification_receipt="verify-1",
        status="CLOSED_RELATIVE",
    )
    base.update(overrides)
    return CommitRequest(**base)

def test_commit_accepts_typed_nonexpanding_verified_transition():
    r=authorize_commit(req(),require_execution=True,require_verification=True,require_evidence=True)
    assert r.role==StateRole.RESULT
    assert r.authority==("admit",)

@pytest.mark.parametrize("status",["OPEN","BLOCKED","INCOMPARABLE","CONFLICT"])
def test_commit_preserves_non_success_as_non_commit(status):
    with pytest.raises(CommitBlocked):
        authorize_commit(req(status=status))

def test_commit_rejects_authority_expansion():
    with pytest.raises(CommitBlocked):
        authorize_commit(req(authority_after=frozenset({"admin"})))

def test_commit_requires_provenance():
    with pytest.raises(CommitBlocked):
        authorize_commit(req(provenance=()))
