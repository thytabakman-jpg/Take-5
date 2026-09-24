from a5_core import A5,Witness,Decision

def test_no_authority_no_transition():
    a=A5(); w=Witness("p1",0,"WRITE")
    before=a.S.version
    try: a.transition(w,"WRITE",{"x":1})
    except PermissionError: pass
    assert a.S.version==before and "x" not in a.S.values

def test_effect_scope():
    a=A5(); w=Witness("p2",0,"WRITE",authority=["WRITE"])
    s,w=a.transition(w,"WRITE",{"x":1})
    assert s.values["x"]==1 and s.version==1 and w.admission.decision==Decision.ALLOW

def test_other_effect_not_licensed():
    a=A5(); w=Witness("p3",0,"WRITE",authority=["WRITE","PROMOTE"])
    try: a.transition(w,"PROMOTE",{"canonical":True})
    except PermissionError: pass
    assert "canonical" not in a.S.values

def test_generation_not_authority():
    a=A5()
    candidates=a.G.generate(lambda:[{"proposal":"x"}])
    assert candidates and a.S.version==0

def test_router_preserves_incomparable_frontier():
    r=A5().R
    xs=[{"id":"a","v":(1,0)},{"id":"b","v":(0,1)}]
    def dominates(x,y): return all(i>=j for i,j in zip(x["v"],y["v"])) and x["v"]!=y["v"]
    assert len(r.frontier(xs,dominates))==2
