from kernel_f1 import admit_consequential_change

def test_live_kernel_surface_exposes_take_two_transition_membrane():
    ok=admit_consequential_change(
        observed_before=True,
        typed=True,
        authority=True,
        transition_declared=True,
        verified_after=True,
        open_state_preserved=True,
    )
    assert ok.legal

def test_live_kernel_blocks_untyped_direct_change():
    bad=admit_consequential_change(
        observed_before=True,
        typed=False,
        authority=True,
        transition_declared=True,
        verified_after=True,
        open_state_preserved=True,
    )
    assert not bad.legal
    assert "TYPE_REQUIRED" in bad.reasons
