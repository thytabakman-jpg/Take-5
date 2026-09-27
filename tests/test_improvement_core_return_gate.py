import sys
sys.path.insert(0,"runtime")

import pytest

from improvement_core_return_gate import evaluate_parent_return


def _context(**extra):
    out={
        "controller":"ImprovementCore",
        "target":"x",
        "job":"finish all work",
        "basis":"b",
        "parent_round":0,
        "hf2_status":"RELATIVE_CLOSE",
    }
    out.update(extra)
    return out


def _fresh_stable(state,memory,context):
    return {
        "status":"NO_GAIN",
        "owned_work_remaining":False,
        "evidence":[f"fresh:{context['challenge_index']}"],
        "challenge_id":f"fresh-{context['challenge_index']}",
    }


def test_continue_reopens_parent_and_forces_live_continuation():
    def verifier(state,memory,context):
        return {
            "disposition":"CONTINUE",
            "goal_closed":False,
            "owned_work_remaining":True,
            "consequence_closed":True,
            "state_patch":{"next_job":"b"},
            "evidence":["unit:owned-work-remains"],
        }

    out=evaluate_parent_return(
        candidate_status="COMPLETE",
        candidate_blocker=None,
        state={"terminal":"COMPLETE","admitted_continuation":False},
        memory={},
        context=_context(),
        verifier=verifier,
        fresh_reobserve=_fresh_stable,
    )
    assert out.disposition=="CONTINUE"
    assert out.next_state["terminal"]=="CONTINUE"
    assert out.next_state["admitted_continuation"] is True
    assert out.next_state["parent_return_continuation"] is True
    assert out.next_state.get("live_continuation") is not True
    assert out.next_state["next_job"]=="b"


def test_fresh_reobservation_can_force_continue_before_return_verifier():
    verifier_called=[]
    def verifier(state,memory,context):
        verifier_called.append(True)
        return {
            "disposition":"RETURN","terminal":"COMPLETE",
            "goal_closed":True,"owned_work_remaining":False,
            "consequence_closed":True,"evidence":["unit:closed"],
        }
    def fresh(state,memory,context):
        return {
            "status":"STABLE",
            "material_search_delta":True,
            "owned_work_remaining":True,
            "state_patch":{"next_job":"rerun-mt"},
            "evidence":["fresh:found-work"],
            "challenge_id":"fresh-discovery",
        }

    out=evaluate_parent_return(
        candidate_status="COMPLETE",candidate_blocker=None,
        state={"terminal":"COMPLETE"},memory={},
        context=_context(),verifier=verifier,fresh_reobserve=fresh,
    )
    assert out.disposition=="CONTINUE"
    assert out.next_state["next_job"]=="rerun-mt"
    assert verifier_called==[]


def test_complete_requires_fresh_reobservation_binding():
    def verifier(state,memory,context):
        return {
            "disposition":"RETURN","terminal":"COMPLETE",
            "goal_closed":True,"owned_work_remaining":False,
            "consequence_closed":True,"evidence":["unit:closed"],
        }
    out=evaluate_parent_return(
        candidate_status="COMPLETE",candidate_blocker=None,
        state={"terminal":"COMPLETE"},memory={},
        context=_context(),verifier=verifier,fresh_reobserve=None,
    )
    assert out.terminal=="OPEN"
    assert out.blocker=="FRESH_WHOLE_JOB_REOBSERVATION_REQUIRED"


def test_complete_requires_goal_closure():
    def verifier(state,memory,context):
        return {
            "disposition":"RETURN",
            "terminal":"COMPLETE",
            "goal_closed":False,
            "owned_work_remaining":False,
            "consequence_closed":True,
            "evidence":["unit:not-enough"],
        }
    with pytest.raises(RuntimeError,match="COMPLETE_WITHOUT_GOAL_CLOSURE"):
        evaluate_parent_return(
            candidate_status="COMPLETE",candidate_blocker=None,
            state={"terminal":"COMPLETE"},memory={},
            context=_context(),verifier=verifier,fresh_reobserve=_fresh_stable,
        )


def test_return_rejects_owned_work():
    def verifier(state,memory,context):
        return {
            "disposition":"RETURN",
            "terminal":"COMPLETE",
            "goal_closed":True,
            "owned_work_remaining":True,
            "consequence_closed":True,
            "evidence":["unit:owned-work"],
        }
    with pytest.raises(RuntimeError,match="RETURN_WITH_OWNED_WORK"):
        evaluate_parent_return(
            candidate_status="COMPLETE",candidate_blocker=None,
            state={"terminal":"COMPLETE"},memory={},
            context=_context(),verifier=verifier,fresh_reobserve=_fresh_stable,
        )


def test_return_requires_consequence_closure_and_evidence():
    def verifier(state,memory,context):
        return {
            "disposition":"RETURN",
            "terminal":"COMPLETE",
            "goal_closed":True,
            "owned_work_remaining":False,
            "consequence_closed":False,
            "evidence":[],
        }
    with pytest.raises(RuntimeError,match="RETURN_WITH_OPEN_CONSEQUENCE"):
        evaluate_parent_return(
            candidate_status="COMPLETE",candidate_blocker=None,
            state={"terminal":"COMPLETE"},memory={},
            context=_context(),verifier=verifier,fresh_reobserve=_fresh_stable,
        )


def test_noncomplete_return_requires_typed_blocker():
    def verifier(state,memory,context):
        return {
            "disposition":"RETURN",
            "terminal":"OPEN",
            "goal_closed":False,
            "owned_work_remaining":False,
            "consequence_closed":True,
            "evidence":["unit:open-boundary"],
        }
    with pytest.raises(RuntimeError,match="NONCOMPLETE_WITHOUT_BLOCKER"):
        evaluate_parent_return(
            candidate_status="OPEN",candidate_blocker=None,
            state={"terminal":"OPEN"},memory={},
            context=_context(hf2_status="OPEN"),verifier=verifier,
        )


def test_missing_verifier_fails_open_after_fresh_stability():
    out=evaluate_parent_return(
        candidate_status="COMPLETE",candidate_blocker=None,
        state={"terminal":"COMPLETE"},memory={},
        context=_context(),verifier=None,fresh_reobserve=_fresh_stable,
    )
    assert out.terminal=="OPEN"
    assert out.blocker=="PARENT_RETURN_GATE_REQUIRED"
    assert out.next_state["terminal"]=="OPEN"
    assert out.next_state["admitted_continuation"] is False


def test_open_candidate_cannot_be_upgraded_to_complete():
    def verifier(state,memory,context):
        return {
            "disposition":"RETURN",
            "terminal":"COMPLETE",
            "goal_closed":True,
            "owned_work_remaining":False,
            "consequence_closed":True,
            "evidence":["unit:illegal-upgrade"],
        }
    with pytest.raises(RuntimeError,match="ILLEGAL_TERMINAL_UPGRADE"):
        evaluate_parent_return(
            candidate_status="OPEN",candidate_blocker="SOURCE_OPEN",
            state={"terminal":"OPEN"},memory={},
            context=_context(hf2_status="OPEN"),verifier=verifier,
        )


def test_complete_rejects_unclosed_authoritative_formal_claim():
    def verifier(state,memory,context):
        return {
            "disposition":"RETURN",
            "terminal":"COMPLETE",
            "goal_closed":True,
            "owned_work_remaining":False,
            "consequence_closed":True,
            "evidence":["unit:formal-claim-open"],
        }
    state={
        "terminal":"COMPLETE",
        "authoritative_formal_claims":[{
            "status":"OPEN",
            "root_object_id":"ImprovementCore",
            "residuals":["ROOT_CURRENTNESS_MISMATCH"],
        }],
    }
    with pytest.raises(
        RuntimeError,
        match="COMPLETE_WITH_UNCLOSED_AUTHORITATIVE_FORMAL_CLAIM",
    ):
        evaluate_parent_return(
            candidate_status="COMPLETE",candidate_blocker=None,
            state=state,memory={},
            context=_context(),verifier=verifier,fresh_reobserve=_fresh_stable,
        )


def test_complete_accepts_closed_authoritative_formal_claim():
    def verifier(state,memory,context):
        return {
            "disposition":"RETURN",
            "terminal":"COMPLETE",
            "goal_closed":True,
            "owned_work_remaining":False,
            "consequence_closed":True,
            "evidence":["unit:formal-claim-pass"],
        }
    state={
        "terminal":"COMPLETE",
        "authoritative_formal_claims":[{
            "status":"PASS",
            "root_object_id":"ImprovementCore",
            "residuals":[],
        }],
    }
    out=evaluate_parent_return(
        candidate_status="COMPLETE",candidate_blocker=None,
        state=state,memory={},
        context=_context(),verifier=verifier,fresh_reobserve=_fresh_stable,
    )
    assert out.terminal=="COMPLETE"
    assert out.receipt["authoritative_formal_claim_residuals"]==()
    assert out.receipt["whole_job_stability"]["terminal"]=="COMPLETE"
    assert len(out.receipt["whole_job_stability"]["receipts"])==2


def test_formal_math_job_cannot_complete_without_any_formal_claim_receipt():
    def verifier(state,memory,context):
        return {
            "disposition":"RETURN",
            "terminal":"COMPLETE",
            "goal_closed":True,
            "owned_work_remaining":False,
            "consequence_closed":True,
            "evidence":["unit:math-output"],
        }
    with pytest.raises(
        RuntimeError,
        match="COMPLETE_WITHOUT_FORMAL_CLAIM_RECEIPT",
    ):
        evaluate_parent_return(
            candidate_status="COMPLETE",candidate_blocker=None,
            state={"terminal":"COMPLETE"},memory={},
            context=_context(formal_claim_receipt_required=True),
            verifier=verifier,fresh_reobserve=_fresh_stable,
        )
