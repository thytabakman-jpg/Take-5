import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from configured_hf2_execution import execute_configured_with_hf2
from global_tool_execution import build_tool_execution_plan
from goal import GoalCandidate,GoalObject,recover_goal
from mt_semantic_return_gate import run_mt_with_before_return_gate
from solution_to_my_problem import Problem,Candidate,SolutionReceipt,solve
from tool_run_registry import CONFIGURED_RUNS
from improvement_core_dispatch import dispatch_improvement_core
from ic028_operator import GOAL_DIRECTED_STAGES


GOAL_INITIAL=GoalObject(
    X="all conversation evidence for the second Sukkos question-booklet candidate",
    T="reach a definition-ready candidate that the user can approve or reject before full project build",
    I="explore and compare rival models of what a question is and their genuinely Sukkos-native bindings",
    Sigma="Project 1 remains untouched; no full Project 2 is built before explicit user approval; the surviving candidate has a precise core object, mechanism, holiday surplus, observable learner evidence, and preserved OPEN",
)

GOAL_REFINED=GoalObject(
    X="the full second-booklet candidate space plus the conversation evidence and newly recovered distinctions",
    T="recover a nondominated source-grounded question model plus Sukkos binding and package it as a definition-ready candidate for user approval",
    I="keep rivals open until structural comparison; distinguish question from ignorance, issue from presupposition, and holiday instantiation from metaphor; then consume the winning evidence without building pages",
    Sigma="Project 1 remains untouched; source content is separated from educational application; no page build or project promotion occurs before explicit user approval",
)


def _configured(tool_id,native):
    plan=build_tool_execution_plan(CONFIGURED_RUNS[tool_id])
    assert plan.complete
    assert len(plan.cells)==36
    assert len(plan.questions)==792
    assert len(plan.cognitive)==144
    holder={}
    def adapter(state,plan):
        value=native()
        holder["value"]=value
        status=str(getattr(value,"status","EXECUTED"))
        if status in {"OPEN","BLOCKED","CONFLICT"}:
            return {
                "status":status,
                "execution_truth":status,
                "result":value,
                "state":state,
                "material_delta":False,
                "hf2_local_close":True,
                "trc_terminal":True,
                "evidence":(f"whole-conversation:{tool_id}",),
            }
        return {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":value,
            "state":state,
            "material_delta":False,
            "hf2_live_local":False,
            "hf2_local_close":True,
            "trc_terminal":True,
            "hf1_disposition":"STABLE",
            "evidence":(f"whole-conversation:{tool_id}",),
        }
    out=execute_configured_with_hf2(
        tool_id=tool_id,
        plan=plan,
        state={"basis":"whole-conversation"},
        adapter=adapter,
    )
    assert out.status=="RELATIVE_CLOSE"
    assert out.recurrence_engine=="HF002"
    return holder["value"],out,plan


def _goal_initial():
    return recover_goal((
        GoalCandidate(
            "WHOLE_CONVERSATION_GOVERNING_GOAL",
            GOAL_INITIAL,
            constraints=(
                "PRESERVE_PROJECT_1",
                "PREPROJECT_GATE",
                "GRADE_5_6",
                "FOUR_PAGE_CAUSAL_ARTIFACT",
                "NO_INFRASTRUCTURE_WORK_UNLESS_IT_DIRECTLY_ADVANCES_THE_BOOKLET",
            ),
            evidence=(
                "conversation:request-another-possibility",
                "conversation:highest-level-approval-before-build",
                "conversation:move-on-and-actually-get-what-we-need",
                "candidates/sukkos-question-gap/DEFINITION.md",
            ),
            grounded=True,
            authority_typed=True,
            determinate_enough=True,
        ),
    ))


def _mt():
    def run_mt(state):
        return state,{
            "distinctions":(
                "BOOKLET_GOAL!=INFRASTRUCTURE_GOAL",
                "EXPLORATORY_CANDIDATE!=SELECTED_PROJECT",
                "QUESTION!=EPISTEMIC_GAP",
                "UNRESOLVED_STATE!=RESOLUTION_CONDITION",
                "PRESUPPOSITION!=OPEN_ISSUE",
                "SUKKOS_METAPHOR!=SUKKOS_NATIVE_BINDING",
                "SOURCE_CONTENT!=EDUCATIONAL_APPLICATION",
                "DEFINITION_READY!=USER_APPROVED",
            ),
            "finding":"The process prematurely collapsed the candidate space around structured-gap before rival question models and Sukkos-native bindings were compared.",
            "black_boxes":(),
        }
    return run_mt_with_before_return_gate(
        {"basis":"whole-conversation"},
        run_mt=run_mt,
        detect_black_boxes=lambda state,result:result["black_boxes"],
        execute_stage=lambda tool_id,object_id,state:(state,"CLOSED_RELATIVE",False),
    )


def _goal_refined():
    return recover_goal((
        GoalCandidate(
            "POST_MT_GOVERNING_GOAL",
            GOAL_REFINED,
            constraints=(
                "PRESERVE_PROJECT_1",
                "PREPROJECT_GATE",
                "NO_PREMATURE_CANDIDATE_COLLAPSE",
                "SOURCE_APPLICATION_BOUNDARY",
                "NO_PAGE_BUILD_BEFORE_USER_APPROVAL",
            ),
            evidence=(
                "GOAL1:CLOSED_RELATIVE",
                "GOAL2:CLOSED_RELATIVE",
                "MT:PREMATURE_CANDIDATE_COLLAPSE",
                "SEP:question-resolution-and-presupposition",
                "REMA:Kohelet-on-Sukkot",
                "KOHELET_7_10:question-evaluated-as-unwise",
            ),
            grounded=True,
            authority_typed=True,
            determinate_enough=True,
        ),
    ))


PROBLEM=Problem(
    observed=(
        "The original task asked for another possibility of what a question is and a broad question-x-Sukkos exploration.",
        "Structured-gap was one exploratory output but became the assumed object to optimize.",
        "The phrase structured-gap conflates an unresolved information state with the question that specifies how resolution works.",
        "The proposed physical-sukkah incompleteness analogy is not load-bearing: a fit sukkah need not be maximally incomplete.",
        "Infrastructure work repeatedly displaced substantive booklet work.",
    ),
    generators=(
        "PREMATURE_CANDIDATE_COLLAPSE",
        "QUESTION_GAP_CONFLATION",
        "HOLIDAY_METAPHOR_BEFORE_STRUCTURAL_TEST",
        "INFRASTRUCTURE_DRIFT",
    ),
    required_effects=(
        "REOPEN_AND_COMPARE_RIVAL_QUESTION_MODELS",
        "RECOVER_PRECISE_QUESTION_OBJECT",
        "RECOVER_SUKKOS_NATIVE_BINDING",
        "RETURN_DEFINITION_READY_CANDIDATE",
        "STOP_INFRASTRUCTURE_DRIFT",
    ),
    protected=(
        "PROJECT_1_UNCHANGED",
        "PREPROJECT_GATE",
        "GRADE_5_6_LEARNER_GOAL",
        "FOUR_PAGE_CAUSAL_ARCHITECTURE",
        "SOURCE_APPLICATION_BOUNDARY",
        "USER_PROMOTION_AUTHORITY",
    ),
    constraints=(
        "No full Project 2 build before user approval",
        "No claim that one formal theory is the unique philosophical definition of question",
    ),
    evidence=(
        "whole-conversation",
        "formal-question-semantics",
        "Kohelet-7:10",
        "Rema-Orach-Chayim-490:9",
    ),
)

CANDIDATES=(
    Candidate(
        "STRUCTURED_GAP_ONLY",
        proposed_attacks=("QUESTION_GAP_CONFLATION",),
        proposed_effects=("RECOVER_PRECISE_QUESTION_OBJECT",),
        proposed_preservations=PROBLEM.protected,
        cost=0.2,
    ),
    Candidate(
        "ISSUE_RESOLUTION_PLUS_SUKKAH_SUFFICIENCY",
        proposed_attacks=PROBLEM.generators,
        proposed_effects=PROBLEM.required_effects,
        proposed_preservations=PROBLEM.protected,
        cost=0.6,
    ),
    Candidate(
        "FRAME_RESOLUTION_PLUS_KOHELET",
        proposed_attacks=PROBLEM.generators,
        proposed_effects=PROBLEM.required_effects,
        proposed_preservations=PROBLEM.protected,
        cost=0.3,
    ),
)

FRAME_RECEIPT=SolutionReceipt(
    candidate_id="FRAME_RESOLUTION_PLUS_KOHELET",
    source="whole-conversation-goal-mt-research-run",
    execution_stage="CONSUMED",
    observed_attacks=PROBLEM.generators,
    observed_effects=PROBLEM.required_effects,
    observed_preservations=PROBLEM.protected,
    observed_violations=(),
    verification_status="PASS",
    closure_status="CLOSED",
    evidence=(
        "SEP Questions: presuppositions and resolution conditions",
        "Inquisitive semantics: issues as downward-closed resolving information states",
        "Kohelet 7:10: the text explicitly evaluates a question as not wise",
        "Rema Orach Chayim 490:9: custom to read Kohelet on Sukkot",
        "Sukkah 6b/7b and 2a: physical incompleteness is not a clean defining invariant",
    ),
)


def _solution():
    return solve(PROBLEM,CANDIDATES,(FRAME_RECEIPT,))


def _ic_handlers():
    handlers={}
    for stage in GOAL_DIRECTED_STAGES:
        def fn(state,stage=stage):
            if stage=="EXECUTE":
                already=bool(state.get("solution_applied"))
                next_state=dict(state)
                next_state.update({
                    "solution_applied":True,
                    "selected_solution":"FRAME_RESOLUTION_PLUS_KOHELET",
                    "question_model":{
                        "formal":"q=<P,I> relative to context s; I is a nonempty downward-closed cover of s; t resolves q iff t in I; nontrivial iff s notin I",
                        "student_projection":("ASSUMES","OPENS","SETTLES"),
                        "structured_gap_disposition":"retained as intuition for unresolvedness, not the identity of a question",
                    },
                    "sukkos_binding":{
                        "primary":"Kohelet 7:10, read on Sukkot in the Ashkenazi custom, provides a holiday-native case in which the wisdom of a question itself is evaluated",
                        "application":"inspect what a question takes for granted, what it leaves open, and what would settle it",
                    },
                    "candidate_status":"DEFINITION_READY",
                    "full_project_created":False,
                })
                return {
                    "state":next_state,
                    "material_delta":not already,
                    "supervisory_relevant":False,
                }
            return {
                "state":state,
                "material_delta":False,
                "supervisory_relevant":False,
            }
        handlers[stage]=fn
    handlers["REENTER"]=lambda state:{"state":state,"terminal":True}
    return handlers


def _return_verifier(state,memory,context):
    ok=bool(state.get("solution_applied")) and state.get("candidate_status")=="DEFINITION_READY"
    return {
        "disposition":"RETURN" if ok else "REENTER",
        "terminal":"COMPLETE" if ok else "OPEN",
        "goal_closed":ok,
        "owned_work_remaining":False if ok else True,
        "consequence_closed":ok,
        "blocker":None if ok else "SOLUTION_NOT_APPLIED",
        "evidence":["whole-conversation:definition-ready-candidate"] if ok else [],
    }


def test_requested_whole_conversation_sequence_and_solution():
    g1,g1run,g1plan=_configured("GOAL",_goal_initial)
    assert g1.status=="CLOSED_RELATIVE"
    assert g1.active_goal==GOAL_INITIAL

    g2,g2run,g2plan=_configured("GOAL",_goal_initial)
    assert g2.status=="CLOSED_RELATIVE"
    assert g2.active_goal==GOAL_INITIAL

    mt,mtrun,mtplan=_configured("MT",_mt)
    assert mt.status=="CLOSED_RELATIVE"
    assert "PREMATURE_CANDIDATE_COLLAPSE" in mt.mt_result["finding"]

    g3,g3run,g3plan=_configured("GOAL",_goal_refined)
    assert g3.status=="CLOSED_RELATIVE"
    assert g3.active_goal==GOAL_REFINED

    solution,solrun,solplan=_configured("SolutionToMyProblem",_solution)
    assert solution.status=="SOLVED"
    assert solution.selected==("FRAME_RESOLUTION_PLUS_KOHELET",)
    assert "STRUCTURED_GAP_ONLY" in solution.rejected

    for run in (g1run,g2run,mtrun,g3run,solrun):
        assert run.recurrence_engine=="HF002"
        assert run.status=="RELATIVE_CLOSE"
    for plan in (g1plan,g2plan,mtplan,g3plan,solplan):
        assert len(plan.cells)==36
        assert len(plan.questions)==792
        assert len(plan.cognitive)==144

    _,ic=dispatch_improvement_core(
        "Improvement Core, solve the governing whole-conversation problem",
        target="sukkos-question-booklet-2-candidate",
        job="consume the solved problem result and produce a definition-ready candidate without creating the full project",
        basis="whole-conversation-plus-current-research",
        state={
            "problem_result":"SOLVED",
            "selected_solution":"FRAME_RESOLUTION_PLUS_KOHELET",
            "solution_applied":False,
        },
        handlers=_ic_handlers(),
        return_verifier=_return_verifier,
    )
    assert ic.status=="COMPLETE"
    assert ic.hf2_status=="RELATIVE_CLOSE"
    assert ic.result.state["candidate_status"]=="DEFINITION_READY"
    assert ic.result.state["full_project_created"] is False
    assert ic.result.state["selected_solution"]=="FRAME_RESOLUTION_PLUS_KOHELET"
