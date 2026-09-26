from protected_transition_recovery import validate_pti_recovery

def test_protected_transition_recovery_is_current():
    out=validate_pti_recovery()
    assert out["status"]=="PASS"
    assert out["missing"]==()
    assert out["failures"]==()
    assert out["checked"]>0
