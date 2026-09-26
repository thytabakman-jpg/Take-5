import sys
sys.path.insert(0,"runtime")

from improvement_core_recovery import validate_recovery

def test_current_improvement_core_recovery_anchor_is_executable_and_current():
    out=validate_recovery()
    assert out["status"]=="PASS"
    assert out["missing"]==()
    assert out["failures"]==()
    assert out["controller"]=="IC-028"
    assert out["entrypoint"].endswith("run_improvement_core_regime")
    assert out["regime_version"]=="088"
