from protected_transition_root_recheck import run_post_pti_root_recheck

def test_post_pti_recheck_moves_remaining_root_to_host_boundary():
    out=run_post_pti_root_recheck()
    # A clean internal portfolio cannot prove an untested external-host cause.
    assert out["status"]=="OPEN"
    assert out["portfolio"].status=="PASS"
    root=out["root_result"]
    assert root.status=="OPEN"
    assert root.root_candidates==()
    assert "HOST_INTEGRATION_BYPASS:EXTERNAL_HOST_REMOVAL_TEST_NOT_OBSERVED" in root.unresolved
    assert "HOST_INTEGRATION_BYPASS:CAUSAL_TEST_EVIDENCE_MISSING" in root.unresolved
    assert "HOST_INTEGRATION_BYPASS:RIVAL_DISCRIMINATION_EVIDENCE_MISSING" in root.unresolved
