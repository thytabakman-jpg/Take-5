from solution_to_my_problem import Problem, Candidate, solve


P = Problem(
    observed=("semantic/runtime confusion",),
    generators=("unsynchronized_semantic_runtime_identity",),
    required_effects=("binding_revalidation","explicit_binding_state","invocation_verification"),
    protected=("open_preservation","authority_integrity"),
)


def test_rejects_symptom_patch_that_does_not_attack_generator():
    r = solve(P, [
        Candidate(
            id="rename_only",
            attacks=("naming_confusion",),
            resolves=("explicit_binding_state",),
            preserves=("open_preservation","authority_integrity"),
            executable=True,
            verified=True,
        )
    ])
    assert r.status == "OPEN"


def test_admissible_unverified_solution_requires_verification():
    r = solve(P, [
        Candidate(
            id="binding_currentness_invariant",
            attacks=("unsynchronized_semantic_runtime_identity",),
            resolves=("binding_revalidation","explicit_binding_state","invocation_verification"),
            preserves=("open_preservation","authority_integrity"),
            executable=True,
            verified=False,
        )
    ])
    assert r.status == "VERIFY_REQUIRED"
    assert r.selected == ("binding_currentness_invariant",)


def test_verified_admissible_solution_closes():
    r = solve(P, [
        Candidate(
            id="binding_currentness_invariant",
            attacks=("unsynchronized_semantic_runtime_identity",),
            resolves=("binding_revalidation","explicit_binding_state","invocation_verification"),
            preserves=("open_preservation","authority_integrity"),
            executable=True,
            verified=True,
        )
    ])
    assert r.status == "SOLVED"


def test_missing_generator_stays_open():
    p = Problem(
        observed=("confusion",),
        generators=(),
        required_effects=("x",),
        protected=(),
    )
    r = solve(p, [])
    assert r.status == "OPEN"
    assert "DIAGNOSED_GENERATOR_MISSING" in r.residual
