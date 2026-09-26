from runtime.core import capability_preservation,KernelChange,legal_change,reentry_required

def test_capability_requires_operational_chain():
    w={k:k for k in ("identity","semantics","reachability","selection","execution","effect","consumer","recovery")}
    assert capability_preservation("c",w).status=="PRESERVED"
    w["consumer"]=""
    assert capability_preservation("c",w).status=="OPEN"

def test_take_two_transition_membrane():
    assert legal_change(KernelChange(True,True,True,True,True,True,True))
    assert not legal_change(KernelChange(True,True,True,True,False,True,True))

def test_material_delta_reenters():
    assert reentry_required(False,True,False)
