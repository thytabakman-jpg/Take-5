import sys
sys.path.insert(0,"runtime")

from report_lineage import assess_report_lineage

TARGET={
    "repository":"thytabakman-jpg/Take-5",
    "object_id":"PROJECT:X:MANUSCRIPT",
    "selector_role":"resolved_from_current_pointer",
    "immutable_kind":"git_commit",
    "frozen_ref":"0123456789abcdef0123456789abcdef01234567",
    "authority_status":"canonical_working",
}

CLAIM={
    "object_id":"RUN:1",
    "claim_id":"run-1",
    "claimed_level":"EXECUTED",
    "evidence":{
        "identity":"id",
        "plan":"plan",
        "dispatch":"dispatch",
        "execution":"execution",
    },
}

def _receipt(**patch):
    row={
        "run_id":"RUN:1",
        "target_identity":TARGET,
        "report_target_identity":TARGET,
        "execution_claim":CLAIM,
        "report_locator":"reports/run-1.md",
        "report_content_identity":"sha256:"+"a"*64,
        "report_persisted":True,
        "report_read_back_verified":True,
        "owner_routing_status":"ROUTED",
        "affected_state_disposition":"UPDATED",
    }
    row.update(patch)
    return row

def test_complete_report_lineage_passes():
    out=assess_report_lineage(_receipt(),expected_repository="thytabakman-jpg/Take-5")
    assert out.status=="PASS"

def test_wrong_report_target_conflicts():
    wrong={**TARGET,"frozen_ref":"fedcba9876543210fedcba9876543210fedcba98"}
    out=assess_report_lineage(
        _receipt(report_target_identity=wrong),
        expected_repository="thytabakman-jpg/Take-5",
    )
    assert out.status=="CONFLICT"
    assert "REPORT_TARGET_LINEAGE_CONFLICT" in out.conflicts

def test_persisted_report_without_execution_evidence_stays_open():
    claim={**CLAIM,"evidence":{"identity":"id","plan":"plan","dispatch":"dispatch"}}
    out=assess_report_lineage(_receipt(execution_claim=claim))
    assert out.status=="OPEN"
    assert "execution_claim.execution" in out.missing

def test_report_readback_is_required():
    out=assess_report_lineage(_receipt(report_read_back_verified=False))
    assert out.status=="OPEN"
    assert "report_read_back_verified" in out.missing

def test_legacy_repository_target_conflicts_with_take5_authority():
    legacy={**TARGET,"repository":"thytabakman-jpg/Reaserch"}
    out=assess_report_lineage(
        _receipt(target_identity=legacy,report_target_identity=legacy),
        expected_repository="thytabakman-jpg/Take-5",
    )
    assert out.status=="CONFLICT"
    assert any("CANONICAL_REPOSITORY_MISMATCH" in x for x in out.conflicts)
