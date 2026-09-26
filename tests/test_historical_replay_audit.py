from historical_replay_audit import audit_historical_replays

def test_declared_historical_replay_basis_is_machine_audited():
    out=audit_historical_replays()
    assert out.status=="PASS"
    assert out.failures==()
    assert out.checked>=10
