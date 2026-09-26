from lambda_math import EntryState,reconstruct

def e(g="g",t="t",m="m",c="c",s="s",f="f"):
    return EntryState(g,t,m,c,s,f)

def test_empty():
    r=reconstruct([e()],consistent=lambda x:False,continuation_equivalent=lambda a,b:True,result_sensitive=lambda d:True)
    assert r.status=="EMPTY"

def test_equivalent_plural_is_identified():
    a=e(m="m1"); b=e(m="m2")
    r=reconstruct([a,b],consistent=lambda x:True,continuation_equivalent=lambda x,y:True,result_sensitive=lambda d:True)
    assert r.status=="IDENTIFIED"
    assert len(r.equivalence_classes)==1

def test_result_sensitive_plural_requires_clarification():
    a=e(t="A"); b=e(t="B")
    r=reconstruct([a,b],consistent=lambda x:True,continuation_equivalent=lambda x,y:False,result_sensitive=lambda d:d=="T")
    assert r.status=="CLARIFY"
    assert r.ambiguous_coordinates==("T",)

def test_result_insensitive_plural_is_safe():
    a=e(m="A"); b=e(m="B")
    r=reconstruct([a,b],consistent=lambda x:True,continuation_equivalent=lambda x,y:False,result_sensitive=lambda d:False)
    assert r.status=="PLURAL_SAFE"

def test_common_core_only_invariants():
    a=e(t="A"); b=e(t="B")
    r=reconstruct([a,b],consistent=lambda x:True,continuation_equivalent=lambda x,y:False,result_sensitive=lambda d:d=="T")
    core=dict(r.common_core)
    assert "T" not in core
    assert core["G_ext"]=="g"
    assert core["F"]=="f"

def test_no_representative_selected():
    a=e(t="A"); b=e(t="B")
    r=reconstruct([a,b],consistent=lambda x:True,continuation_equivalent=lambda x,y:False,result_sensitive=lambda d:d=="T")
    assert not hasattr(r,"selected")
