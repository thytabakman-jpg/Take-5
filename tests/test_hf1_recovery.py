from hf1_recovery import validate_hf1_recovery

def test_hf1_recovery_is_current():
    out=validate_hf1_recovery()
    assert out["status"]=="PASS"
    assert out["missing"]==()
    assert out["failures"]==()
