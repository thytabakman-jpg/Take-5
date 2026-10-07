import sys
sys.path.insert(0,"runtime")

import pytest

from exact_target_identity import (
    ExactTargetIdentityError,
    assess_exact_target,
    require_exact_target,
)

GOOD={
    "repository":"thytabakman-jpg/Take-5",
    "object_id":"PROJECT:X:MANUSCRIPT",
    "selector_role":"resolved_from_current_pointer",
    "immutable_kind":"git_commit",
    "frozen_ref":"0123456789abcdef0123456789abcdef01234567",
    "authority_status":"canonical_working",
}

def test_full_commit_target_passes():
    out=assess_exact_target(GOOD,expected_repository="thytabakman-jpg/Take-5")
    assert out.status=="PASS"

def test_mutable_selector_cannot_be_evidentiary_target():
    out=assess_exact_target({**GOOD,"frozen_ref":"main"})
    assert out.status=="CONFLICT"
    assert "IMMUTABLE_TARGET_BASIS_INVALID" in out.conflicts

def test_short_git_sha_is_not_exact_target_identity():
    out=assess_exact_target({**GOOD,"frozen_ref":"abc1234"})
    assert out.status=="CONFLICT"

def test_wrong_repository_fails_canonical_home_check():
    out=assess_exact_target(
        {**GOOD,"repository":"thytabakman-jpg/Reaserch"},
        expected_repository="thytabakman-jpg/Take-5",
    )
    assert out.status=="CONFLICT"
    assert any("CANONICAL_REPOSITORY_MISMATCH" in x for x in out.conflicts)

def test_missing_target_coordinate_fails_open():
    row=dict(GOOD);row.pop("object_id")
    out=assess_exact_target(row)
    assert out.status=="OPEN"
    assert "object_id" in out.missing
    with pytest.raises(ExactTargetIdentityError):
        require_exact_target(row)
