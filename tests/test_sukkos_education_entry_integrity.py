"""Prevent cross-project and historical/current status regressions in Sukkos education.

This validates only source entrances and exact current-state delegation.
It does not certify learner effects, project release, or Level 2-4.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
FIRST = ROOT / "projects/sukkos-question-booklet"
SECOND = ROOT / "projects/sukkos-question-booklet-2-frame-resolution"


def test_first_question_booklet_delegates_currentness_without_corruption():
    entry = (FIRST / "README.md").read_text(encoding="utf-8")
    current = (FIRST / "CURRENT_STATE.md").read_text(encoding="utf-8")

    assert "The public artifact cannot depend on hidden facilitator instructions." in entry
    assert "facilitator in##" not in entry
    assert "The visual master is not locked." not in entry
    assert "Exact student-facing copy is not locked." not in entry
    assert "[CURRENT_STATE.md](CURRENT_STATE.md)" in entry
    assert "VISUAL_MASTER:\nCOMPLETE_FOR_RENDER_CANDIDATE" in current
    assert "RENDER:\nOPEN" in current
    assert "QA:\nOPEN" in current
    assert "RELEASE:\nOPEN" in current
    assert "four-page" in entry.lower()


def test_frame_resolution_is_independent_and_still_state_owned():
    entry = (SECOND / "README.md").read_text(encoding="utf-8")
    state = json.loads((SECOND / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    first_entry = (FIRST / "README.md").read_text(encoding="utf-8")

    assert state["project_id"] == "sukkos-question-booklet-2-frame-resolution"
    assert "[typed project state](PROJECT_STATE.json)" in entry
    assert "[goal](GOAL.md)" in entry
    assert "questions as frames" in entry
    assert "target, relevant facts and answer test" in entry
    assert "Target.\nRelevant facts.\nAnswer test." in (FIRST / "CURRENT_STATE.md").read_text(encoding="utf-8")
    assert first_entry != entry
    for name in ("GOAL.md", "EXACT_COPY.md", "VERIFICATION.md"):
        assert (SECOND / name).is_file()
