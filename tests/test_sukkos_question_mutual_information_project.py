from pathlib import Path
ROOT=Path("projects/sukkos-question-mutual-information")

def test_mutual_information_project_authorities_exist():
    required=["IDENTITY.md","PROJECT_CHARTER.md","GOAL.md","SCOPE.md","AUTHORITY_REGISTRY.md","STAKEHOLDERS.md","WBS.md","SCHEDULE.md","RESOURCES.md","DEPENDENCIES.md","INTERFACES.md","RAID.md","OPEN_QUESTIONS.md","EVIDENCE.md","DECISION_LOG.md","LESSONS_LEDGER.md","CHANGE_CONTROL.md","LIFECYCLE.md","VERIFICATION.md","COMMUNICATIONS.md","HANDOFFS.md","PROJECT_STATE.json","MATHEMATICAL_CORE.md","QUESTION_CONSTRUCTION.md","SOURCE_LOCK.md","FOUR_PAGE_ARCHITECTURE.md","ACTIVITY_MODEL.md","EMOTIONAL_ARC.md","RAISE_THE_CEILING.md","BACKEND_LOCK.md","CURRENT_STATE.md"]
    assert all((ROOT/name).exists() for name in required)

def test_mutual_information_route_identity():
    math=(ROOT/"MATHEMATICAL_CORE.md").read_text()
    assert "Canonical quantity: Mutual information" in math
    assert "I(X;Y)" in math
    assert "Canonical quantity: Shannon entropy" not in math

def test_target_role_is_load_bearing():
    q=(ROOT/"QUESTION_CONSTRUCTION.md").read_text()
    assert "Name target X" in q or "target X" in q
    assert "relevant" in q.lower()

def test_backend_lock_does_not_fake_frontend_completion():
    state=(ROOT/"CURRENT_STATE.md").read_text()
    assert "BACKEND_LOCKED_RELATIVE" in state
    assert "EXACT_COPY: OPEN_BY_DESIGN" in state
    assert "RENDER: NOT_STARTED" in state

def test_page_authorities_and_bridges():
    for i in range(1,5): assert (ROOT/"pages"/f"PAGE_{i}.md").exists()
    arch=(ROOT/"FOUR_PAGE_ARCHITECTURE.md").read_text()
    assert arch.count("Bridge:") >= 3
