import sys
sys.path.insert(0,"runtime")

from object_lifecycle import (
    ObjectLifecycleCandidate,
    bootstrap_object,
    candidates_from_state,
)
from semantic_object_package import expected_transition_names

def test_new_project_gets_semantic_package_and_project_obligations(tmp_path):
    c=ObjectLifecycleCandidate(
        object_id="PROJECT:NEW",
        term="new project",
        kind="PROJECT",
        definition="A newly created project.",
        source="test",
    )
    r=bootstrap_object(tmp_path,c)
    assert r.package_current
    assert r.files_created==38
    assert "PORTFOLIO_REGISTRATION" in r.obligations
    assert "ORIENTATION_PROJECT_PAGE" in r.obligations
    root=tmp_path/"project-new"
    assert (root/"CORE.md").is_file()
    assert (root/"MANIFEST.md").is_file()
    assert len(list((root/"transitions").glob("*.md")))==len(expected_transition_names())==36

def test_new_idea_is_captured_without_auto_promoting_to_project(tmp_path):
    c=ObjectLifecycleCandidate(
        object_id="IDEA:X",
        term="idea x",
        kind="IDEA",
        definition="",
        source="conversation",
        load_bearing=None,
    )
    r=bootstrap_object(tmp_path,c)
    assert r.package_current
    assert "PRESERVE_SOURCE" in r.obligations
    assert "PROMOTE_TO_PROJECT_OR_TOOL_ONLY_WITH_TYPED_TRANSITION" in r.obligations
    assert "load_bearingness" in r.open
    assert "exact_definition" in r.open

def test_created_tool_remains_open_when_required_math_is_incomplete(tmp_path):
    c=ObjectLifecycleCandidate(
        object_id="TOOL:X",
        term="tool x",
        kind="TOOL",
        definition="A candidate tool.",
        source="foundry",
        math_complete_for_use=False,
    )
    r=bootstrap_object(tmp_path,c)
    assert "COMPLETE_REQUIRED_MATHEMATICS_BEFORE_ADMISSION" in r.obligations
    assert "mathematics_complete_for_advertised_use" in r.open

def test_candidates_are_read_from_controller_state():
    xs=candidates_from_state({
        "new_objects":[{
            "object_id":"PROJECT:P",
            "term":"P",
            "kind":"PROJECT",
            "definition":"project",
        }]
    })
    assert len(xs)==1
    assert xs[0].object_id=="PROJECT:P"
