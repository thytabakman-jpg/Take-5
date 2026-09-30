import sys
sys.path.insert(0,"runtime")

from whole_job_stability import run_whole_job_stability


def test_missing_reobserver_fails_open():
    out=run_whole_job_stability(
        state={"terminal":"COMPLETE"},memory={},context={},reobserve=None
    )
    assert out.terminal=="OPEN"
    assert out.blocker=="FRESH_WHOLE_JOB_REOBSERVATION_REQUIRED"


def test_material_fresh_discovery_forces_parent_continue():
    def reobserve(state,memory,context):
        return {
            "status":"STABLE",
            "material_search_delta":True,
            "owned_work_remaining":True,
            "state_patch":{"new_job":"MT-on-new-representation"},
            "evidence":["fresh:found-new-work"],
            "challenge_id":"fresh-overview",
        }
    out=run_whole_job_stability(
        state={"terminal":"COMPLETE"},memory={},context={},reobserve=reobserve
    )
    assert out.disposition=="CONTINUE"
    assert out.state["terminal"]=="CONTINUE"
    assert out.state["new_job"]=="MT-on-new-representation"


def test_two_fresh_no_gain_passes_are_required_for_stability():
    calls=[]
    def reobserve(state,memory,context):
        calls.append(context["challenge_index"])
        return {
            "status":"NO_GAIN",
            "owned_work_remaining":False,
            "evidence":[f"fresh:no-gain:{context['challenge_index']}"],
            "challenge_id":f"fresh-{context['challenge_index']}",
        }
    out=run_whole_job_stability(
        state={"terminal":"COMPLETE"},memory={},context={},
        reobserve=reobserve,stable_passes_required=2
    )
    assert out.disposition=="STABLE"
    assert out.terminal=="COMPLETE"
    assert calls==[0,1]
    assert len(out.receipts)==2


def test_second_fresh_pass_can_reopen_after_first_no_gain():
    calls=[]
    def reobserve(state,memory,context):
        i=context["challenge_index"]
        calls.append(i)
        if i==0:
            return {
                "status":"NO_GAIN",
                "evidence":["fresh:first-stable"],
                "challenge_id":"fresh-0",
            }
        return {
            "status":"STABLE",
            "material_result_delta":True,
            "owned_work_remaining":True,
            "state_patch":{"question_frontier":["new-question"]},
            "evidence":["fresh:second-found-new-result"],
            "challenge_id":"fresh-1",
        }
    out=run_whole_job_stability(
        state={"terminal":"COMPLETE"},memory={},context={},
        reobserve=reobserve,stable_passes_required=2
    )
    assert out.disposition=="CONTINUE"
    assert calls==[0,1]
    assert out.state["question_frontier"]==["new-question"]

def test_untyped_fresh_state_change_fails_open():
    def reobserve(state,memory,context):
        return {
            "status":"NO_GAIN",
            "state_patch":{"question_frontier":["new-question"]},
            "evidence":["fresh:untyped-state-change"],
            "challenge_id":"fresh-untyped",
        }

    out=run_whole_job_stability(
        state={"terminal":"COMPLETE"},memory={},context={},reobserve=reobserve
    )

    assert out.disposition=="RETURN"
    assert out.terminal=="OPEN"
    assert out.blocker=="FRESH_REOBSERVATION_UNTYPED_STATE_DELTA"
    assert out.state["question_frontier"]==["new-question"]

