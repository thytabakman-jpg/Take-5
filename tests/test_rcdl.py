from rcdl import regenerate
from representation_discovery import View

def test_admitted_state_change_can_reopen_candidate_universe():
    def views(s):
        return View("bridge",tuple(s.get("known",())))
    def relations(s,vs):
        return ("A-B",) if "B" in vs[0].payload else ()
    before={"known":["A"]}
    after={"known":["A","B"]}
    r0=regenerate(before,[views],{"relation":relations})
    r1=regenerate(after,[views],{"relation":relations},r0.views,r0.universe,state_changed=True)
    assert not r0.universe.candidates
    assert "relation:A-B" in r1.universe.candidates
    assert r1.delta.material
