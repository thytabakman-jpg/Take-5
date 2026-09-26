import pytest
from solution_to_my_problem import Problem, Candidate, SolutionReceipt, solve


P = Problem(
    observed=("semantic/runtime confusion",),
    generators=("unsynchronized_semantic_runtime_identity",),
    required_effects=("binding_revalidation","explicit_binding_state","invocation_verification"),
    protected=("open_preservation","authority_integrity"),
)


GOOD = Candidate(
    id="binding_currentness_invariant",
    proposed_attacks=("unsynchronized_semantic_runtime_identity",),
    proposed_effects=("binding_revalidation","explicit_binding_state","invocation_verification"),
    proposed_preservations=("open_preservation","authority_integrity"),
)


def test_candidate_cannot_self_declare_verified_or_executable():
    with pytest.raises(TypeError):
        Candidate(
            id="cheat",
            proposed_attacks=("unsynchronized_semantic_runtime_identity",),
            proposed_effects=("binding_revalidation","explicit_binding_state","invocation_verification"),
            proposed_preservations=("open_preservation","authority_integrity"),
            verified=True,
        )


def test_rejects_symptom_patch_that_does_not_attack_generator():
    r = solve(P, [
        Candidate(
            id="rename_only",
            proposed_attacks=("naming_confusion",),
            proposed_effects=("explicit_binding_state",),
            proposed_preservations=("open_preservation","authority_integrity"),
        )
    ])
    assert r.status == "OPEN"


def test_matching_proposal_without_external_receipt_cannot_solve():
    r = solve(P, [GOOD])
    assert r.status == "VERIFY_REQUIRED"
    assert r.selected == ("binding_currentness_invariant",)


def test_incomplete_receipt_cannot_solve():
    r = solve(P, [GOOD], [
        SolutionReceipt(
            candidate_id=GOOD.id,
            source="test-run",
            execution_stage="EXECUTED",
            observed_attacks=P.generators,
            observed_effects=P.required_effects,
            observed_preservations=P.protected,
            verification_status="PASS",
            closure_status="CLOSED",
            evidence=("receipt-1",),
        )
    ])
    assert r.status == "VERIFY_REQUIRED"


def test_candidate_claims_do_not_substitute_for_observed_effects():
    r = solve(P, [GOOD], [
        SolutionReceipt(
            candidate_id=GOOD.id,
            source="test-run",
            execution_stage="CONSUMED",
            observed_attacks=P.generators,
            observed_effects=("binding_revalidation",),
            observed_preservations=P.protected,
            verification_status="PASS",
            closure_status="CLOSED",
            evidence=("receipt-2",),
        )
    ])
    assert r.status == "VERIFY_REQUIRED"


def test_external_closed_receipt_can_establish_solution():
    r = solve(P, [GOOD], [
        SolutionReceipt(
            candidate_id=GOOD.id,
            source="independent-verifier",
            execution_stage="CONSUMED",
            observed_attacks=P.generators,
            observed_effects=P.required_effects,
            observed_preservations=P.protected,
            observed_violations=(),
            verification_status="PASS",
            closure_status="CLOSED",
            evidence=("execution-receipt","verification-receipt","closure-certificate"),
        )
    ])
    assert r.status == "SOLVED"


def test_missing_generator_stays_open():
    p = Problem(observed=("confusion",),generators=(),required_effects=("x",),protected=())
    r = solve(p, [])
    assert r.status == "OPEN"
    assert "DIAGNOSED_GENERATOR_MISSING" in r.residual
