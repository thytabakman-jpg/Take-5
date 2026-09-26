from hf002_recursive_continuation import HF002RecursiveContinuation
from root_cause import RootCandidate,run_root_cause_hf2
from root_cause_managed import run_root_cause_child


def test_hf2_reapplies_same_capability_to_changed_successor():
    def cap(state,memory):
        n=state.get("n",0)+1
        return {"execution_truth":"FULL_MATCH","n":n,"finding":"x" if n==1 else "y"}
    def norm(raw,state,memory):
        nxt={**state,"n":raw["n"],"finding":raw["finding"]}
        return nxt,{"material_result_delta":True}
    runner=HF002RecursiveContinuation(
        cap,norm,
        lambda pre,post,delta:{"terminal":True},
        lambda pre,post,delta:{"disposition":"STABLE"},
        lambda state,memory:state.get("n",0)<2,
        lambda state,memory:state.get("n",0)>=2,
    )
    out=runner.run({"n":0},{})
    assert out["status"]=="RELATIVE_CLOSE"
    assert len(out["trace"])==2
    assert out["trace"][0]["disposition"]=="REAPPLY_C"


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
    assert out.rounds==2
    assert out.parent_handoff["controller"]=="ImprovementCore"
    assert out.parent_handoff["action"]=="ADMIT_ROOT_CAUSE_AND_REPLAN"


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
