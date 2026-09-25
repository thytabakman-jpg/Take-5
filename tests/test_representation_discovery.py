from representation_discovery import View,candidate_universe,compare_discovery,reentry_required

def test_view_change_can_expose_previously_unavailable_candidate():
    s={"known":["A"]}
    def rel(state,views):
        ids={v.view_id for v in views}
        return ("A-B",) if "bridge" in ids else ()
    before=(View("inventory",("A",)),)
    after=before+(View("bridge",("A","B")),)
    u0=candidate_universe(s,before,{"relation":rel})
    u1=candidate_universe(s,after,{"relation":rel})
    d=compare_discovery(before,after,u0,u1)
    assert u0.candidates==()
    assert "relation:A-B" in u1.candidates
    assert d.view_changed and d.candidate_universe_changed
    assert reentry_required(d)

def test_static_empty_frontier_does_not_certify_dynamic_view_closure():
    s={}
    def rel(state,views):
        return ("hidden",) if any(v.view_id=="alternate" for v in views) else ()
    u0=candidate_universe(s,(View("default",()),),{"relation":rel})
    u1=candidate_universe(s,(View("alternate",()),),{"relation":rel})
    assert not u0.candidates
    assert u1.candidates
