import pytest
from desired_jane import DesireEvidence,DesireStatus,recover_desired_jane,assertion_safe

def ev(c,p,s="evidence",r="source"):
    return DesireEvidence(c,p,r,s)

def test_recovery_keeps_required_prohibited_and_open_distinct():
    c=recover_desired_jane([
        ev("continuity_supervision","WANT"),
        ev("primary_action_selection","DO_NOT_WANT"),
        ev("alignment_reconstruction","UNKNOWN"),
    ])
    assert c.required==("continuity_supervision",)
    assert c.prohibited==("primary_action_selection",)
    assert c.open==("alignment_reconstruction",)
    assert c.conflicts==()
    assert assertion_safe(c)

def test_conflicting_user_evidence_is_not_silently_resolved():
    c=recover_desired_jane([
        ev("tool_selection","WANT","Jane picks tools"),
        ev("tool_selection","DO_NOT_WANT","IC picks tools"),
    ])
    assert c.conflicts==("tool_selection",)
    assert not assertion_safe(c)

def test_repetition_does_not_create_new_coordinate_or_authority():
    c=recover_desired_jane([
        ev("currentness","WANT","keep current","a"),
        ev("currentness","WANT","keep current","b"),
    ])
    d=c.dispositions[0]
    assert d.status==DesireStatus.REQUIRED
    assert d.source_refs==("a","b")

def test_invalid_polarity_fails_closed():
    with pytest.raises(ValueError):
        recover_desired_jane([ev("x","MAYBE")])
