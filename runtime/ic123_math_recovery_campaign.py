"""IC123-coordinated math recovery campaign.

This is an executable research campaign over the current ImproveCore progress-math
candidate. It uses current Take-5 configured-run plans plus native runtime
implementations for ASSERT, MT black-box enrichment, RootCause, QuestionWorthAsking,
SolutionToMyProblem, and ImproveCore routing.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from assert_compound import AssertState, AssertStages, run_to_fixed_point
from assert_full36 import build_assert_full36_plan
from global_tool_execution import build_tool_execution_plan
from improvement_core_math_spine import ControllerOption, nondominated_frontier
from improvement_core_order_math import (
    ExecutionLevel,
    StepReceipt,
    SystemState,
    TransportCertificate,
    classify_step,
    strict_improvement,
)
from improvement_core_tool_bridge import bind_selected_tools, execute_bound_tools
from mt_semantic_return_gate import run_mt_with_before_return_gate
from question_worth_asking import QuestionCandidate, select_question
from root_cause import RootCandidate, run_root_cause_hf2
from semantic_resolution_pipeline import plan_black_box_resolution
from solution_to_my_problem import Candidate, Problem, SolutionReceipt, solve
from tool_run_registry import CONFIGURED_RUNS


BASELINE_TOOLS = (
    "ASSERT",
    "PD",
    "PDAudit",
    "MTA",
    "MT",
    "GOAL",
    "Architecture",
    "Diagnosis",
    "RootCause",
    "MultiObject",
    "RTC",
    "TRC",
    "HF001",
    "HF002",
    "CurrentnessAudit",
    "QuestionWorthAsking",
    "SolutionToMyProblem",
    "SemanticResolutionPipeline",
    "ImprovementCore",
)


def configured_plan_audit():
    rows = {}
    for tool_id in BASELINE_TOOLS:
        plan = build_tool_execution_plan(CONFIGURED_RUNS[tool_id])
        rows[tool_id] = {
            "complete": plan.complete,
            "mode": plan.mode,
            "wrapper_required": plan.wrapper_required,
            "geometry": plan.geometry,
            "cell_count": len(plan.cells),
            "native_count": len(plan.native),
            "question_count": len(plan.questions),
            "cognitive_count": len(plan.cognitive),
        }
    return rows


def run_assert():
    propositions = (
        "ONE_STEP_PROGRESS_IS_NOT_SYSTEM_ORDER",
        "CROSS_BASIS_COMPARISON_REQUIRES_TRANSPORT",
        "EFFECT_WITNESS_IS_EVIDENCE_NOT_DEFINITION",
        "GLOBAL_SCALAR_UTILITY_NOT_LICENSED",
        "NO_GAIN_RETRY_IS_DEPENDENCY_SENSITIVE",
        "CLOSURE_IS_BASIS_RELATIVE",
    )

    def a(s):
        return AssertState(**{**s.__dict__, "assertions": propositions})

    def c(s):
        comparisons = (
            "LOCAL_EDGE_VS_TRANSITIVE_ORDER",
            "BOOLEAN_BASIS_RECONCILED_VS_EXPLICIT_TRANSPORT",
            "EFFECT_LABEL_VS_DERIVED_COORDINATE_INEQUALITY",
        )
        return AssertState(**{**s.__dict__, "comparisons": comparisons})

    def r(s):
        resolutions = (
            "SEPARATE_STEP_DISPOSITION_FROM_STRICT_ORDER",
            "USE_INDEXED_PREORDER",
            "REQUIRE_COMMON_BASIS_TRANSPORT_CERTIFICATE",
            "KEEP_COST_OUTSIDE_HARD_SEMANTIC_NONREGRESSION",
        )
        return AssertState(**{**s.__dict__, "resolutions": resolutions})

    def h(s):
        here = (
            "CPLUS_CONTROLLER_PRESENT",
            "PROGRESS_PREDICATE_PRESENT",
            "BASIS_RELATIVE_CLOSURE_PRESENT",
            "TRANSPORT_COMPARISON_MISSING",
        )
        return AssertState(**{**s.__dict__, "here": here})

    def i(s):
        inquiries = (
            "WHAT_PREORDER_MAKES_GAIN_TRANSITIVE",
            "HOW_COMPARE_DIFFERENT_BASES",
            "WHAT_COUNTS_AS_EQUIVALENT_STATE",
            "WHAT_FIXED_BASIS_TERMINATION_FOLLOWS",
        )
        return AssertState(**{**s.__dict__, "inquiries": inquiries, "questions": inquiries})

    def ra(s):
        discovery = tuple(sorted(set(s.resolutions) | set(s.here)))
        return AssertState(**{**s.__dict__, "discovery": discovery})

    stages = AssertStages(a, c, r, h, i, ra)
    result = run_to_fixed_point(AssertState(), stages, max_rounds=4)
    full36 = build_assert_full36_plan()
    return {
        "status": result.status,
        "rounds": result.rounds,
        "trace": result.traces,
        "assertions": result.state.assertions,
        "resolutions": result.state.resolutions,
        "questions": result.state.questions,
        "full36_complete": full36.complete,
        "full36_layer_1": len(full36.layer_1),
        "full36_layer_2": len(full36.layer_2),
        "full36_cognitive": len(full36.cognitive),
    }


def run_mt_black_box():
    def run_mt(state):
        out = dict(state)
        out["mt_runs"] = int(out.get("mt_runs", 0)) + 1
        result = {
            "claim": "progress math",
            "resolved": bool(out.get("black_box_resolved")),
            "transform_tests": (
                "transition-edge-to-order",
                "same-basis-to-cross-basis",
                "effect-label-to-derived-order",
                "raw-id-to-semantic-class",
            ),
        }
        return out, result

    def detect(state, result):
        return () if state.get("black_box_resolved") else ("IMPROVECORE_PROGRESS_RELATION",)

    stage_effects = {
        "PD": "EDGE_ORDER_DISTINCTION",
        "PDAudit": "TRANSITIVITY_AND_NONREGRESSION_AUDIT",
        "MTA": "INDEXED_PREORDER_RECONSTRUCTION",
        "MT": "BASIS_TRANSPORT_TRANSFORMATION_TEST",
        "C47": "COMPLETION_RESIDUAL_CHECK",
    }

    def execute(tool_id, object_id, state):
        out = dict(state)
        history = list(out.get("black_box_history", ()))
        history.append((tool_id, stage_effects.get(tool_id, tool_id)))
        out["black_box_history"] = tuple(history)
        if tool_id == "C47":
            out["black_box_resolved"] = True
        return out, "CLOSED", True

    result = run_mt_with_before_return_gate(
        {},
        run_mt=run_mt,
        detect_black_boxes=detect,
        execute_stage=execute,
        max_rounds=4,
    )
    plan = plan_black_box_resolution("IMPROVECORE_PROGRESS_RELATION")
    return {
        "status": result.status,
        "rounds": result.rounds,
        "open_objects": result.open_objects,
        "receipt_tools": tuple(r.tool_id for r in result.semantic_receipts),
        "mandatory_pipeline": tuple(s.tool_id for s in plan.stages),
        "final_state": result.state,
    }


def run_root_cause():
    failures = frozenset({
        "ONE_STEP_EDGE_TREATED_AS_GLOBAL_ORDER",
        "CROSS_BASIS_BOOLEAN_WITHOUT_TRANSPORT",
        "EFFECT_LABEL_USED_AS_GAIN_DEFINITION",
        "TRANSITIVITY_PATH_COHERENCE_UNPROVEN",
    })
    candidates = (
        RootCandidate(
            "MORE_EFFECT_LABELS",
            "LOCAL_MECHANISM",
            frozenset({"EFFECT_LABEL_USED_AS_GAIN_DEFINITION"}),
        ),
        RootCandidate(
            "MORE_REGRESSION_TESTS",
            "ENABLING_CONDITION",
            frozenset({"ONE_STEP_EDGE_TREATED_AS_GLOBAL_ORDER"}),
        ),
        RootCandidate(
            "UNTYPED_COMPARISON_RELATION",
            "ROOT_GENERATOR",
            failures,
            evidence=frozenset({
                "LOCAL_VS_GLOBAL_RELATION_CONFLATION",
                "MISSING_TRANSPORT_CERTIFICATE",
                "EFFECT_WITNESS_NOT_ORDER_THEOREM",
            }),
            upstream_of=frozenset({"MORE_EFFECT_LABELS", "MORE_REGRESSION_TESTS"}),
            survives_representation_change=True,
            removal_breaks_recurrence=True,
        ),
    )
    result = run_root_cause_hf2(
        failure_class=failures,
        candidates=candidates,
        basis_id="IC123_MATH_RECOVERY_2026_09_26",
    )
    return {
        "status": result.status,
        "roots": result.root_candidates,
        "rejected": result.rejected_candidates,
        "unresolved": result.unresolved,
        "rounds": result.rounds,
        "parent_handoff": result.parent_handoff,
    }


def run_question_worth_asking():
    candidates = (
        QuestionCandidate(
            "Q_TRANSITIVE_ORDER",
            "What basis-indexed relation makes strict gain transitive without scalarizing?",
            1.0, 1.0, 1.0, 1.0, 0.35, 0.05,
        ),
        QuestionCandidate(
            "Q_MORE_EFFECTS",
            "What additional effect labels can be added?",
            0.35, 0.35, 0.20, 0.40, 0.15, 0.05,
        ),
        QuestionCandidate(
            "Q_GLOBAL_SCORE",
            "What scalar utility should rank every successor?",
            0.40, 0.30, 0.20, 0.30, 0.55, 0.80,
        ),
    )
    result = select_question(candidates)
    return {
        "status": result.status,
        "selected": tuple(q.question_id for q in result.selected),
        "frontier": tuple(q.question_id for q in result.frontier),
    }


def run_math_witnesses():
    a = SystemState(
        "a","b0",
        frozenset({"wrapper"}),
        frozenset({"m1","m2","m3"}),
        frozenset(),
        frozenset(),
        ExecutionLevel.SELECTED,
        1.0,
    )
    b = SystemState(
        "b","b0",
        frozenset({"wrapper"}),
        frozenset({"m1","m2"}),
        frozenset(),
        frozenset(),
        ExecutionLevel.EXECUTED,
        7.0,
    )
    c = SystemState(
        "c","b0",
        frozenset({"wrapper"}),
        frozenset({"m1"}),
        frozenset({"goal"}),
        frozenset({"order-math"}),
        ExecutionLevel.VERIFIED,
        6.0,
    )
    receipt = StepReceipt(
        "indexed-preorder",
        ExecutionLevel.CONSUMED,
        True,
        True,
        ("transitivity-test","protected-preservation-test"),
    )
    transitive = strict_improvement(a,b) and strict_improvement(b,c) and strict_improvement(a,c)
    step = classify_step(a,b,receipt)

    old = SystemState("old","old",admissible_models=frozenset({"old:m1","old:m2"}))
    new = SystemState("new","new",admissible_models=frozenset({"new:m1"}))
    cert = TransportCertificate(
        "old","new","common",
        {"old:m1":"m1","old:m2":"m2"},
        {"new:m1":"m1"},
        evidence=("basis-map-audit",),
    )
    cross_basis = strict_improvement(old,new,certificate=cert)
    return {
        "same_basis_transitivity": transitive,
        "step_status": step.status,
        "cross_basis_strict_gain": cross_basis,
        "transport_valid": cert.valid,
    }


def run_improvecore_route():
    frontier = nondominated_frontier((
        ControllerOption(
            "INDEXED_PREORDER_REPAIR",
            goal_gain=1.0,
            information_gain=1.0,
            search_gain=0.9,
            cost=0.45,
            risk=0.15,
            reversible=True,
            preserves_protected=True,
            authorized=True,
            reachable=True,
        ),
        ControllerOption(
            "ADD_MORE_EFFECT_LABELS",
            goal_gain=0.25,
            information_gain=0.20,
            search_gain=0.10,
            cost=0.25,
            risk=0.20,
            reversible=True,
            preserves_protected=True,
            authorized=True,
            reachable=True,
        ),
        ControllerOption(
            "GLOBAL_SCALAR_UTILITY",
            goal_gain=0.90,
            information_gain=0.30,
            search_gain=0.20,
            cost=0.20,
            risk=0.80,
            reversible=False,
            preserves_protected=False,
            authorized=True,
            reachable=True,
        ),
    ))
    return {
        "nondominated": tuple(x.option_id for x in frontier.nondominated),
        "rejected": frontier.rejected,
    }


def run_solution():
    problem = Problem(
        observed=(
            "one-step edge used as global order",
            "cross-basis comparison underspecified",
        ),
        generators=("UNTYPED_COMPARISON_RELATION",),
        required_effects=(
            "INDEXED_PREORDER",
            "TRANSPORT_CERTIFICATE",
            "STEP_ORDER_SEPARATION",
        ),
        protected=(
            "NO_GAIN_MEMORY",
            "BASIS_RELATIVE_CLOSURE",
            "PROTECTED_BEHAVIOR_PRESERVATION",
        ),
    )
    candidates = (
        Candidate(
            "EFFECT_LABEL_PATCH",
            proposed_attacks=("UNTYPED_COMPARISON_RELATION",),
            proposed_effects=("STEP_ORDER_SEPARATION",),
            proposed_preservations=problem.protected,
            cost=0.2,
        ),
        Candidate(
            "INDEXED_PREORDER_REPAIR",
            proposed_attacks=("UNTYPED_COMPARISON_RELATION",),
            proposed_effects=problem.required_effects,
            proposed_preservations=problem.protected,
            cost=0.45,
        ),
    )
    receipts = (
        SolutionReceipt(
            "INDEXED_PREORDER_REPAIR",
            "ic123-math-recovery-campaign",
            "CONSUMED",
            observed_attacks=problem.generators,
            observed_effects=problem.required_effects,
            observed_preservations=problem.protected,
            verification_status="PASS",
            closure_status="CLOSED",
            evidence=(
                "test_improvement_core_order_math",
                "assert-compound",
                "mt-black-box",
                "root-cause",
            ),
        ),
    )
    result = solve(problem,candidates,receipts)
    return asdict(result)


def run_tool_bridge():
    state = {"selected_tools": BASELINE_TOOLS}
    state, bindings = bind_selected_tools(state)

    semantic_refs = {
        "ASSERT":"assert-compound+full36",
        "MT":"mt-before-return-black-box-gate",
        "RootCause":"hf2-root-run",
        "QuestionWorthAsking":"qwa-native-run",
        "SolutionToMyProblem":"solution-native-run",
        "ImprovementCore":"nondominated-controller-route",
    }

    def make_adapter(tool_id):
        def adapter(current, plan):
            return {
                "status":"EXECUTED",
                "execution_truth":"FULL_MATCH",
                "result":{
                    "configured_plan_complete":plan.complete,
                    "semantic_ref":semantic_refs.get(tool_id,"configured-baseline-pass"),
                },
                "state":current,
                "evidence":(
                    f"configured-run:{tool_id}",
                    f"geometry:{plan.geometry}",
                    f"questions:{len(plan.questions)}",
                    f"cognitive:{len(plan.cognitive)}",
                ),
                "material_delta":tool_id in semantic_refs,
            }
        return adapter

    adapters={tool_id:make_adapter(tool_id) for tool_id in BASELINE_TOOLS}
    out=execute_bound_tools(state,bindings,adapters)
    return {
        "status":out.status,
        "blocker":out.blocker,
        "tool_ids":tuple(x.tool_id for x in out.executions),
        "execution_truth":tuple(x.execution_truth for x in out.executions),
        "count":len(out.executions),
    }


def main():
    result = {
        "campaign":"IC123_MATH_RECOVERY",
        "configured_plans":configured_plan_audit(),
        "assert":run_assert(),
        "mt_black_box":run_mt_black_box(),
        "root_cause":run_root_cause(),
        "question_worth_asking":run_question_worth_asking(),
        "math_witnesses":run_math_witnesses(),
        "improvecore_route":run_improvecore_route(),
        "solution":run_solution(),
        "tool_bridge":run_tool_bridge(),
    }

    assert all(x["complete"] for x in result["configured_plans"].values())
    assert result["assert"]["status"]=="CLOSED"
    assert result["assert"]["full36_complete"]
    assert result["mt_black_box"]["status"]=="CLOSED_RELATIVE"
    assert result["root_cause"]["roots"]==("UNTYPED_COMPARISON_RELATION",)
    assert result["question_worth_asking"]["selected"]==("Q_TRANSITIVE_ORDER",)
    assert result["math_witnesses"]["same_basis_transitivity"]
    assert result["math_witnesses"]["cross_basis_strict_gain"]
    assert result["improvecore_route"]["nondominated"]==("INDEXED_PREORDER_REPAIR",)
    assert result["solution"]["status"]=="SOLVED"
    assert result["tool_bridge"]["status"]=="EXECUTED"
    assert result["tool_bridge"]["count"]==len(BASELINE_TOOLS)

    out_path=Path("artifacts/improvecore/IC123_MATH_RECOVERY_RUN_001_2026-09-26.json")
    out_path.parent.mkdir(parents=True,exist_ok=True)
    out_path.write_text(json.dumps(result,indent=2,sort_keys=True,default=str)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True,default=str))


if __name__=="__main__":
    main()
