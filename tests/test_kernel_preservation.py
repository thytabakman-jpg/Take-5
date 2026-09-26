from kernel_preservation import KernelChange,admit_change

def test_consequential_change_requires_take_two_kernel_law():
    good=KernelChange(True,True,True,True,True,True,True)
    assert admit_change(good).legal

def test_direct_mutation_without_transition_fails():
    bad=KernelChange(True,True,True,True,False,True,True)
    out=admit_change(bad)
    assert not out.legal
    assert out.reasons==("TYPED_TRANSITION_REQUIRED",)

def test_nonconsequential_view_does_not_require_new_surface_transition():
    view=KernelChange(False,False,False,False,False,False,False)
    assert admit_change(view).legal
