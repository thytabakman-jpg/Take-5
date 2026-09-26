from root_cause_recovery import validate_root_cause_recovery

def test_root_cause_and_hf2_recovery_is_current():
    out=validate_root_cause_recovery()
    assert out["status"]=="PASS"
    assert out["missing"]==()
    assert out["failures"]==()
