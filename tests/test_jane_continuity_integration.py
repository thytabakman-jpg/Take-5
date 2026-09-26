from jane import recover_turn_continuity

def test_jane_normal_interface_exposes_continuity_recovery():
    packet,ctx=recover_turn_continuity(
        {"target":"ImproveCore","job":"recover","basis":"main","canonical_version":"100"},
        protected_behaviors=("capability_preservation",),
        evidence_refs=("integration/IMPROVECORE_RECOVERY_BLUEPRINT_100.md",),
    )
    assert packet.status=="READY"
    assert ctx["target"]=="ImproveCore"
    assert "selected_action" not in ctx
