import pytest
from delegation import delegate
from lineage_state import LineageState
from state_commit import CommitRequest,StateRole,authorize_commit

def _lineage_receipt(effect,baseline):
    return authorize_commit(
        CommitRequest(
            role=StateRole.LINEAGE,
            effect=effect,
            target="lineage",
            job="preserve-history",
            baseline=baseline,
            authority_before=frozenset({"record_lineage"}),
            authority_after=frozenset({"record_lineage"}),
            evidence=("admitted-delta",),
            provenance=("test",),
            verification_receipt="verified",
        ),
        require_verification=True,
        require_evidence=True,
    )

def test_delegation_executes_local_transform_and_returns_exact_receipt():
    out,r=delegate(episode="e",program_id="C24",authority_in=frozenset({"observe","repair"}),authority_local=frozenset({"repair"}),payload={"x":1},worker=lambda x:{"x":x["x"]+1})
    assert out=={"x":2}
    assert r.executed and r.reintegrated
    assert r.input_hash!=r.output_hash

def test_delegation_cannot_expand_authority():
    with pytest.raises(PermissionError):
        delegate(episode="e",program_id="C24",authority_in=frozenset({"observe"}),authority_local=frozenset({"repair"}),payload={},worker=lambda x:x)

def test_lineage_preserves_prior_material_state_across_episode_updates():
    s=LineageState()
    v1=s.apply("OBSERVATION",{"protected":"p"},"episode-1",commit_receipt=_lineage_receipt("OBSERVATION","v0"))
    s.apply("REENTRY",{"frontier":"next"},"episode-2",commit_receipt=_lineage_receipt("REENTRY","v1"))
    assert s.inherits(v1,"protected","p")
    assert s.events[1]["from"]==1 and s.events[1]["to"]==2

def test_lineage_rejects_ungated_mutation():
    s=LineageState()
    with pytest.raises(TypeError):
        s.apply("OBSERVATION",{"x":1},"episode")
