from protected_transition_root_recheck import run_post_pti_root_recheck

def test_post_pti_recheck_moves_remaining_root_to_host_boundary():
    out=run_post_pti_root_recheck()
    assert out["status"]=="PASS"
    assert out["portfolio"].status=="PASS"
    root=out["root_result"]
    assert root.status=="RELATIVE_CLOSE"
    assert root.root_candidates==("HOST_INTEGRATION_BYPASS",)
    assert root.rounds==2
