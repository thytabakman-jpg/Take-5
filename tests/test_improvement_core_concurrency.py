from runtime.improvement_core_concurrency import (
    WorkstreamClaim, compare_claims, preflight
)

def claim(i, r=(), w=(), status="ACTIVE", base="abc"):
    return WorkstreamClaim(i,base,frozenset(r),frozenset(w),status)

def test_disjoint_active_workstreams_are_allowed():
    proposed=claim("new",r={"a"},w={"b"})
    peer=claim("peer",r={"x"},w={"y"})
    out=preflight(proposed,[peer],registry_complete=True,current_base_commit="abc")
    assert out.can_start
    assert out.disposition=="ALLOW"

def test_write_write_overlap_requires_reconciliation():
    proposed=claim("new",w={"shared.md"})
    peer=claim("peer",w={"shared.md"})
    out=preflight(proposed,[peer],registry_complete=True,current_base_commit="abc")
    assert out.disposition=="RECONCILE_REQUIRED"
    assert out.conflicts[0].write_write==frozenset({"shared.md"})

def test_proposed_write_invalidating_peer_read_is_blocked():
    proposed=claim("new",w={"state.yaml"})
    peer=claim("peer",r={"state.yaml"})
    out=preflight(proposed,[peer],registry_complete=True,current_base_commit="abc")
    assert out.disposition=="RECONCILE_REQUIRED"
    assert out.conflicts[0].proposed_writes_peer_reads==frozenset({"state.yaml"})

def test_peer_write_invalidating_proposed_read_is_blocked():
    proposed=claim("new",r={"math.md"})
    peer=claim("peer",w={"math.md"})
    out=preflight(proposed,[peer],registry_complete=True,current_base_commit="abc")
    assert out.disposition=="RECONCILE_REQUIRED"
    assert out.conflicts[0].peer_writes_proposed_reads==frozenset({"math.md"})

def test_terminal_peer_does_not_block():
    proposed=claim("new",w={"shared.md"})
    peer=claim("peer",w={"shared.md"},status="COMPLETE")
    out=preflight(proposed,[peer],registry_complete=True,current_base_commit="abc")
    assert out.can_start

def test_incomplete_registry_fails_closed():
    proposed=claim("new")
    out=preflight(proposed,[],registry_complete=False,current_base_commit="abc")
    assert out.disposition=="BLOCK"
    assert out.blocker=="REGISTRY_INCOMPLETE"

def test_stale_base_fails_closed():
    proposed=claim("new",base="old")
    out=preflight(proposed,[],registry_complete=True,current_base_commit="new")
    assert out.disposition=="BLOCK"
    assert out.blocker=="BASE_STALE"

def test_compare_relation_is_symmetric_for_collision_existence():
    a=claim("a",r={"r1"},w={"w1"})
    b=claim("b",r={"w1"},w={"r1"})
    assert compare_claims(a,b) is not None
    assert compare_claims(b,a) is not None
