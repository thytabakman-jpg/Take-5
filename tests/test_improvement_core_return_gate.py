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
    )
    assert out.disposition=="CONTINUE"
    assert out.next_state["terminal"]=="CONTINUE"
    assert out.next_state["admitted_continuation"] is True
    assert out.next_state["parent_return_continuation"] is True
    assert out.next_state.get("live_continuation") is not True
    assert out.next_state["next_job"]=="b"


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
            context=_context(),verifier=verifier,
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
            context=_context(),verifier=verifier,
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
            context=_context(),verifier=verifier,
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


def test_missing_verifier_fails_open_not_complete():
    out=evaluate_parent_return(
        candidate_status="COMPLETE",candidate_blocker=None,
        state={"terminal":"COMPLETE"},memory={},
        context=_context(),verifier=None,
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
            context=_context(),verifier=verifier,
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
        context=_context(),verifier=verifier,
    )
    assert out.terminal=="COMPLETE"
    assert out.receipt["authoritative_formal_claim_residuals"]==()


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
            verifier=verifier,
        )


def test_reachable_result_sensitive_open_forces_parent_reentry_instead_of_user_return():
    def verifier(state,memory,context):
        return {
            "disposition":"RETURN",
            "terminal":"OPEN",
            "goal_closed":False,
            "owned_work_remaining":False,
            "consequence_closed":True,
            "blocker":"TRANSFERCORE_IDENTITY_OPEN",
            "evidence":["unit:recoverable-open"],
        }

    state={
        "terminal":"OPEN",
        "open_residuals":[{
            "residual_id":"transfercore",
            "result_sensitive":True,
            "reachable":True,
            "recovery_route":"HistoricalReconstruction->TransferCore",
            "owner":"ImprovementCore",
        }],
    }
    out=evaluate_parent_return(
        candidate_status="OPEN",
        candidate_blocker="TRANSFERCORE_IDENTITY_OPEN",
        state=state,
        memory={},
        context=_context(hf2_status="OPEN"),
        verifier=verifier,
    )
    assert out.disposition=="CONTINUE"
    assert out.terminal=="CONTINUE"
    assert out.next_state["admitted_continuation"] is True
    assert out.next_state["owned_recovery_work"][0]["residual_id"]=="transfercore"
    assert out.receipt["forced_recovery_reentry"] is True


def test_unreachable_external_open_can_still_return_typed_open():
    def verifier(state,memory,context):
        return {
            "disposition":"RETURN",
            "terminal":"OPEN",
            "goal_closed":False,
            "owned_work_remaining":False,
            "consequence_closed":True,
            "blocker":"EXTERNAL_HOST_NOT_OWNED",
            "evidence":["unit:external-open"],
        }

    state={
        "terminal":"OPEN",
        "open_residuals":[{
            "residual_id":"external-host",
            "result_sensitive":True,
            "reachable":False,
            "recovery_route":"",
            "owner":"external",
        }],
    }
    out=evaluate_parent_return(
        candidate_status="OPEN",
        candidate_blocker="EXTERNAL_HOST_NOT_OWNED",
        state=state,
        memory={},
        context=_context(hf2_status="OPEN"),
        verifier=verifier,
    )
    assert out.disposition=="RETURN"
    assert out.terminal=="OPEN"
