import sys
sys.path.insert(0,"runtime")

from improvement_core_afterrun import run_afterrun_improvement
from improvement_core_learning_memory import LearningMemory

def test_afterrun_always_carries_response_and_bias_receipt():
    out=run_afterrun_improvement(
        episode_id="e",basis_id="b",status="COMPLETE",blocker=None,
        state={},learning_memory=LearningMemory(),
        user_text="solve all of my projects always",
        object_package_base=None,
    )
    assert "RESULT_FIRST" in out.response_profile
    assert out.bias_audit is not None
    assert "CLOSURE_SCOPE_PRESSURE" in out.bias_audit.input_framing_risks

def test_afterrun_bootstraps_new_project_when_storage_is_bound(tmp_path):
    state={
        "new_objects":[{
            "object_id":"PROJECT:A",
            "term":"A",
            "kind":"PROJECT",
            "definition":"A project",
            "source":"test",
        }]
    }
    out=run_afterrun_improvement(
        episode_id="e2",basis_id="b",status="COMPLETE",blocker=None,
        state=state,learning_memory=LearningMemory(),
        user_text="new project A",
        object_package_base=tmp_path,
    )
    assert out.object_lifecycle
    assert out.object_lifecycle[0].package_current
    assert "object_lifecycle:PROJECT:A" in out.next_frontier
