from capability_preservation import evaluate_capability,evaluate_manifest,lost_capabilities

FULL={
    "identity":"manifest:id",
    "semantics":"contract.md",
    "reachability":"dispatcher.py",
    "selection":"router.py",
    "execution":"worker.py",
    "effect":"admission.py",
    "consumer":"reentry.py",
    "recovery":"recovery.json",
}

def test_operational_capability_requires_full_recoverable_chain():
    out=evaluate_capability("x",FULL)
    assert out.preserved
    assert out.missing==()

def test_documented_but_unreachable_capability_is_not_preserved():
    w=dict(FULL)
    w["reachability"]=""
    out=evaluate_capability("x",w)
    assert out.disposition=="OPEN"
    assert out.missing==("reachability",)

def test_named_semantic_object_cannot_fake_operational_execution():
    w=dict(FULL)
    w["execution"]=None
    assert not evaluate_capability("x",w).preserved
    assert evaluate_capability("x",w,operational=False).preserved

def test_manifest_exposes_lost_capabilities():
    bad=dict(FULL)
    bad["consumer"]=None
    manifest={"good":FULL,"lost":bad}
    assert lost_capabilities(manifest)==("lost",)
    assert [r.disposition for r in evaluate_manifest(manifest)]==["PRESERVED","OPEN"]
