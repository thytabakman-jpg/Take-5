from kpd_projection import project,effectiveness_obligations

BASE={
    "identity":"i",
    "type":"t",
    "scope":"s",
    "job":"j",
    "readings":[],
    "result_sensitive":[],
    "selectors":[],
    "authority":[],
    "provenance":[],
    "open":[],
}

def test_most_effective_without_compiled_coordinates_stays_open():
    packet=dict(BASE)
    packet["selection_objective"]="MOST_EFFECTIVE"
    assert effectiveness_obligations(packet)==("RESOLVE_EFFECTIVENESS_OBJECTIVE",)
    assert "RESOLVE_EFFECTIVENESS_OBJECTIVE" in project(packet).obligations

def test_most_effective_compiles_protected_coordinates_into_obligations():
    packet=dict(BASE)
    packet["selection_objective"]="MOST_EFFECTIVE"
    packet["protected_effectiveness"]=(
        "Recovery Coverage",
        "Canonical Integration",
        "Future Reachability",
        "User Reprompt Reduction",
    )
    obligations=project(packet).obligations
    assert "EFFECTIVENESS_RECOVERY_COVERAGE" in obligations
    assert "EFFECTIVENESS_CANONICAL_INTEGRATION" in obligations
    assert "EFFECTIVENESS_FUTURE_REACHABILITY" in obligations
    assert "EFFECTIVENESS_USER_REPROMPT_REDUCTION" in obligations
    assert "RESOLVE_EFFECTIVENESS_OBJECTIVE" not in obligations

def test_legacy_packets_do_not_gain_effectiveness_obligations():
    packet=dict(BASE)
    assert effectiveness_obligations(packet)==()
    assert all(not x.startswith("EFFECTIVENESS_") for x in project(packet).obligations)
