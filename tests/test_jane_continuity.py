from jane_continuity import recover_continuity,controller_context

def test_jane_recovers_ready_entry_state_without_becoming_controller():
    p=recover_continuity(
        {"target":"ImproveCore","job":"improve","basis":"main","canonical_version":"083"},
        protected_behaviors=("observer_first","open_preservation"),
        capability_gaps=("zero_request",),
        evidence_refs=("integration/CURRENT_IMPROVEMENT_CORE.md",),
    )
    assert p.status=="READY"
    c=controller_context(p)
    assert c["job"]=="improve"
    assert "selected_action" not in c

def test_missing_entry_coordinate_stays_open():
    p=recover_continuity(
        {"target":"ImproveCore","job":None,"basis":"main","canonical_version":"083"}
    )
    assert p.status=="OPEN"
    assert p.missing==("job",)
