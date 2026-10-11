from hf002_recursive_continuation import HF002RecursiveContinuation
from root_cause import RootCandidate,run_root_cause_hf2
from root_cause_managed import run_root_cause_child


def test_hf2_reapplies_same_capability_to_changed_successor_and_requires_clean_pass():
    calls={"n":0}
    def cap(state,memory):
        calls["n"]+=1
        if calls["n"]==1:
            return {"execution_truth":"FULL_MATCH","n":1,"finding":"x"}
        return {"execution_truth":"FULL_MATCH","n":state.get("n",0),"finding":state.get("finding")}
    def norm(raw,state,memory):
        nxt={**state,"n":raw["n"],"finding":raw["finding"]}
        return nxt,{"material_result_delta":nxt!=state}
    runner=HF002RecursiveContinuation(
        cap,norm,
        lambda pre,post,delta:{"terminal":True},
        lambda pre,post,delta:{"disposition":"STABLE"},
        lambda state,memory:False,
        lambda state,memory:state.get("n",0)>=1,
    )
    out=runner.run({"n":0},{})
    assert out["status"]=="RELATIVE_CLOSE"
    assert len(out["trace"])==2
    assert out["trace"][0]["disposition"]=="REAPPLY_C"
    assert out["trace"][1]["disposition"]=="RELATIVE_CLOSE"
    assert out["trace"][1]["delta"]["material_result_delta"] is False


def chat_candidates():
    failures={
        "COLOR_CONTRACT_CLAIMED_REPAIRED_BUT_OUTPUT_VIOLATES",
        "TOOL_EXISTS_BUT_NORMAL_INVOCATION_BYPASSES_IT",
        "FULL_RUN_REQUEST_DOWNGRADES_TO_BARE_OR_PARTIAL_TOOL",
        "MIGRATION_PRESERVES_ARTIFACTS_BUT_LOSES_BEHAVIOR",
        "RECOVERY_DOC_POINTS_TO_STALE_OR_OBSOLETE_PATH",
        "HOST_REASONING_SUBSTITUTES_FOR_CONTROLLER",
    }
    return failures,(
        RootCandidate(
            "FINITE_ALIAS_LIST",
            "LOCAL_MECHANISM",
            frozenset({"COLOR_CONTRACT_CLAIMED_REPAIRED_BUT_OUTPUT_VIOLATES"}),
            survives_representation_change=False,
            removal_breaks_recurrence=False,
        ),
        RootCandidate(
            "DOCUMENTATION_DRIFT",
            "ENABLING_CONDITION",
            frozenset({"RECOVERY_DOC_POINTS_TO_STALE_OR_OBSOLETE_PATH"}),
            survives_representation_change=False,
            removal_breaks_recurrence=False,
        ),
        RootCandidate(
            "ACTIVATION_IDENTITY_LOSS",
            "OWNERSHIP_CONFIGURATION",
            frozenset({
                "TOOL_EXISTS_BUT_NORMAL_INVOCATION_BYPASSES_IT",
                "FULL_RUN_REQUEST_DOWNGRADES_TO_BARE_OR_PARTIAL_TOOL",
                "MIGRATION_PRESERVES_ARTIFACTS_BUT_LOSES_BEHAVIOR",
                "HOST_REASONING_SUBSTITUTES_FOR_CONTROLLER",
            }),
            survives_representation_change=True,
            removal_breaks_recurrence=False,
        ),
        RootCandidate(
            "PROTECTED_TRANSITION_INTEGRITY_FAILURE",
            "ROOT_GENERATOR",
            frozenset(failures),
            evidence=frozenset({
                "COLOR_BOUNDARY_BYPASS",
                "CONFIGURED_RUN_DOWNGRADE",
                "MIGRATION_ACTIVATION_GAP",
                "STALE_RECOVERY_RECONSTRUCTION",
                "HOST_CONTROLLER_SUBSTITUTION",
            }),
            upstream_of=frozenset({
                "FINITE_ALIAS_LIST",
                "DOCUMENTATION_DRIFT",
                "ACTIVATION_IDENTITY_LOSS",
            }),
            survives_representation_change=True,
            removal_breaks_recurrence=True,
            causal_test_evidence=frozenset({"SELECTIVE_INTERVENTION_RECEIPT"}),
            rival_discrimination_evidence=frozenset({"RIVAL_COUNTEREXAMPLE_RECEIPT"}),
        ),
    )


def test_root_cause_chat_fixture_finds_protected_transition_integrity_generator():
    failures,candidates=chat_candidates()
    out=run_root_cause_hf2(
        failure_class=failures,
        candidates=candidates,
        basis_id="CHAT_2026_09_26",
    )
    assert out.status=="RELATIVE_CLOSE"
    assert out.root_candidates==("PROTECTED_TRANSITION_INTEGRITY_FAILURE",)
    assert out.rounds==3
    assert out.trace[-1]["disposition"]=="RELATIVE_CLOSE"
    assert out.trace[-1]["delta"]["material_result_delta"] is False
    assert out.parent_handoff["controller"]=="ImprovementCore"
    assert out.parent_handoff["action"]=="ADMIT_ROOT_CAUSE_AND_REPLAN"


def test_evidenced_root_is_not_removed_by_unverified_broader_rival():
    from root_cause import nondominated_candidates, root_admissible
    failure = frozenset({"recurrence"})
    proven = RootCandidate(
        "PROVEN", "ROOT_GENERATOR", failure,
        evidence=frozenset({"observed-effect"}),
        causal_test_evidence=frozenset({"intervention"}),
        rival_discrimination_evidence=frozenset({"rival-check"}),
        survives_representation_change=True,
        removal_breaks_recurrence=True,
    )
    unverified = RootCandidate(
        "UNVERIFIED", "ROOT_GENERATOR", failure,
        upstream_of=frozenset({"x", "y"}),
        survives_representation_change=True,
        removal_breaks_recurrence=True,
    )
    candidates = nondominated_candidates((proven, unverified), failure)
    assert proven in candidates
    assert root_admissible(proven, failure)
    assert not root_admissible(unverified, failure)


def test_duplicate_candidate_id_cannot_override_causal_evidence():
    failures = frozenset({"failure"})
    good = RootCandidate(
        "SAME", "ROOT_GENERATOR", failures,
        evidence=frozenset({"evidence"}),
        causal_test_evidence=frozenset({"test"}),
        rival_discrimination_evidence=frozenset({"rival"}),
        survives_representation_change=True,
        removal_breaks_recurrence=True,
    )
    bad = RootCandidate("SAME", "ROOT_GENERATOR", failures)
    for ordered in ((good, bad), (bad, good)):
        out = run_root_cause_hf2(
            failure_class=failures, candidates=ordered, basis_id="duplicate",
        )
        assert out.status == "OPEN"
        assert out.root_candidates == ()
        assert "DUPLICATE_ROOT_CANDIDATE_ID" in out.unresolved
        assert out.parent_handoff["action"] == "RECONCILE_CANDIDATE_IDENTITIES"


def test_root_cause_is_local_child_not_global_completion():
    failures,candidates=chat_candidates()
    child=run_root_cause_child(
        job_id="root-chat",
        child_id="child-root",
        failure_class=failures,
        candidates=candidates,
        basis_id="CHAT_2026_09_26",
    )
    assert child.execution_truth=="FULL_MATCH"
    assert child.result["local_status"]=="RELATIVE_CLOSE"
    assert child.result["parent_handoff"]["controller"]=="ImprovementCore"


def test_root_cause_preserves_open_when_no_candidate_passes_rootness():
    out=run_root_cause_hf2(
        failure_class={"A","B"},
        candidates=(
            RootCandidate(
                "LOCAL",
                "LOCAL_MECHANISM",
                frozenset({"A"}),
                survives_representation_change=False,
                removal_breaks_recurrence=False,
            ),
        ),
        basis_id="b",
    )
    assert out.status=="OPEN"
    assert out.unresolved


def test_root_admission_rejects_unsubstantiated_flags():
    from root_cause import root_admissible
    candidate=RootCandidate(
        "UNSUPPORTED", "ROOT_GENERATOR", frozenset({"failure"}),
        evidence=frozenset({"assertion"}),
        survives_representation_change=True,
        removal_breaks_recurrence=True,
    )
    assert not root_admissible(candidate,frozenset({"failure"}))
    out=run_root_cause_hf2(failure_class={"failure"},candidates=(candidate,),basis_id="negative")
    assert out.status=="OPEN"
    assert "UNSUPPORTED:CAUSAL_TEST_EVIDENCE_MISSING" in out.unresolved
    assert "UNSUPPORTED:RIVAL_DISCRIMINATION_EVIDENCE_MISSING" in out.unresolved
