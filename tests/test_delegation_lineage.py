import pytest
from delegation import delegate
from lineage_state import LineageState

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
    v1=s.apply("OBSERVATION",{"protected":"p"},"episode-1")
    s.apply("REENTRY",{"frontier":"next"},"episode-2")
    assert s.inherits(v1,"protected","p")
    assert s.events[1]["from"]==1 and s.events[1]["to"]==2
