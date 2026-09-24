from readiness_proof import ReadinessProof

def test_foundation_readiness_does_not_imply_migration_authority():
    p=ReadinessProof(True,True,True,True,True,True,True,True,True,False)
    assert p.foundation_ready
    assert not p.migration_ready

def test_any_load_bearing_failure_blocks_foundation_readiness():
    p=ReadinessProof(True,True,True,True,True,True,False,True,True,False)
    assert not p.foundation_ready
