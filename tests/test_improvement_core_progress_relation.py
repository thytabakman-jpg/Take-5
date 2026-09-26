from runtime.improvement_core_progress_relation import (
    ClaimScope,
    EffectKind,
    EffectWitness,
    EvaluationTarget,
    SemanticStep,
    TransitionComparison,
    certified_no_gain,
    cycle_no_gain,
    retry_licensed,
    strict_progress,
)


def scope(target=EvaluationTarget.CONTROLLER, boundary="controller"):
    return ClaimScope(
        target=target,
        job_id="improvecore",
        basis_id="b0",
        representation_id="r0",
        boundary=boundary,
    )


def witness(kind=EffectKind.ACTION_CHANGED, target=EvaluationTarget.CONTROLLER, boundary="controller"):
    return EffectWitness(
        kind=kind,
        target=target,
        basis_id="b0",
        boundary=boundary,
        evidence={"fixture": True},
    )


def test_documentation_only_change_is_not_controller_progress():
    cmp = TransitionComparison(
        scope=scope(),
        pre_semantic_class="same-runtime",
        post_semantic_class="same-runtime",
        pre_basis_id="b0",
        post_basis_id="b0",
        boundary_verified=True,
    )
    assert strict_progress(cmp) is False
    assert certified_no_gain(cmp) is True


def test_artifact_evidence_does_not_prove_method_gain():
    cmp = TransitionComparison(
        scope=scope(EvaluationTarget.METHOD, "method"),
        pre_semantic_class="m0",
        post_semantic_class="m1",
        pre_basis_id="b0",
        post_basis_id="b0",
        effects=(
            witness(
                EffectKind.COVERAGE_STRENGTHENED,
                EvaluationTarget.ARTIFACT,
                "artifact",
            ),
        ),
        boundary_verified=True,
    )
    assert strict_progress(cmp) is False


def test_selected_but_not_executed_is_not_activation_progress():
    cmp = TransitionComparison(
        scope=scope(EvaluationTarget.ACTIVATION, "runtime"),
        pre_semantic_class="selected",
        post_semantic_class="selected",
        pre_basis_id="b0",
        post_basis_id="b0",
        effects=(
            witness(
                EffectKind.ACTION_CHANGED,
                EvaluationTarget.ACTIVATION,
                "runtime",
            ),
        ),
        boundary_verified=False,
    )
    assert strict_progress(cmp) is False


def test_repository_fix_without_host_witness_is_not_host_progress():
    cmp = TransitionComparison(
        scope=scope(EvaluationTarget.HOST_BOUNDARY, "user-visible"),
        pre_semantic_class="host-old",
        post_semantic_class="host-unknown",
        pre_basis_id="b0",
        post_basis_id="b0",
        effects=(
            witness(
                EffectKind.PROTECTED_FAILURE_PREVENTED,
                EvaluationTarget.HOST_BOUNDARY,
                "user-visible",
            ),
        ),
        boundary_verified=False,
    )
    assert strict_progress(cmp) is False


def test_silent_protected_loss_blocks_gain():
    cmp = TransitionComparison(
        scope=scope(),
        pre_semantic_class="c0",
        post_semantic_class="c1",
        pre_basis_id="b0",
        post_basis_id="b0",
        protected_before=frozenset({"full-wrapper", "observer-first"}),
        protected_after=frozenset({"observer-first"}),
        effects=(witness(EffectKind.NEW_REACHABLE_WORK),),
        boundary_verified=True,
    )
    assert strict_progress(cmp) is False


def test_discovery_that_enlarges_problem_can_be_strict_gain():
    cmp = TransitionComparison(
        scope=scope(),
        pre_semantic_class="u0",
        post_semantic_class="u1-larger",
        pre_basis_id="b0",
        post_basis_id="b0",
        protected_before=frozenset({"observer-first"}),
        protected_after=frozenset({"observer-first"}),
        effects=(witness(EffectKind.MATERIAL_RELATION_DISCOVERED),),
        obligation_states=("CLOSED",),
        boundary_verified=True,
    )
    assert strict_progress(cmp) is True


def test_lower_burden_equivalent_can_be_strict_gain():
    cmp = TransitionComparison(
        scope=scope(),
        pre_semantic_class="same-behavior",
        post_semantic_class="same-behavior",
        pre_basis_id="b0",
        post_basis_id="b0",
        protected_before=frozenset({"full-wrapper"}),
        protected_after=frozenset({"full-wrapper"}),
        effects=(witness(EffectKind.LOWER_BURDEN_EQUIVALENT),),
        obligation_states=("NOT_APPLICABLE",),
        boundary_verified=True,
    )
    assert strict_progress(cmp) is True


def test_same_semantic_state_without_effect_is_certified_no_gain():
    cmp = TransitionComparison(
        scope=scope(),
        pre_semantic_class="q7",
        post_semantic_class="q7",
        pre_basis_id="b0",
        post_basis_id="b0",
        protected_before=frozenset({"x"}),
        protected_after=frozenset({"x"}),
        obligation_states=("CLOSED",),
        boundary_verified=True,
    )
    assert certified_no_gain(cmp) is True


def test_semantic_cycle_ignores_raw_artifact_churn():
    history = [
        SemanticStep("A", "b0"),
        SemanticStep("B", "b0"),
        SemanticStep("A", "b0"),
    ]
    assert cycle_no_gain(history) is True


def test_effectful_cycle_is_not_no_gain_cycle():
    history = [
        SemanticStep("A", "b0"),
        SemanticStep("B", "b0", effects=("new-relation",)),
        SemanticStep("A", "b0"),
    ]
    assert cycle_no_gain(history) is False


def test_basis_change_requires_reconciliation_for_strict_comparison():
    cmp = TransitionComparison(
        scope=scope(),
        pre_semantic_class="a",
        post_semantic_class="b",
        pre_basis_id="old",
        post_basis_id="b0",
        effects=(witness(EffectKind.ACTION_CHANGED),),
        boundary_verified=True,
        basis_reconciled=False,
    )
    assert strict_progress(cmp) is False

    cmp2 = TransitionComparison(
        scope=scope(),
        pre_semantic_class="a",
        post_semantic_class="b",
        pre_basis_id="old",
        post_basis_id="b0",
        effects=(witness(EffectKind.ACTION_CHANGED),),
        boundary_verified=True,
        basis_reconciled=True,
    )
    assert strict_progress(cmp2) is True


def test_relevant_dependency_change_relicenses_no_gain_route():
    assert retry_licensed(
        frozenset({"evidence", "representation"}),
        frozenset({"evidence"}),
    )
    assert not retry_licensed(
        frozenset({"evidence"}),
        frozenset({"unrelated"}),
    )
