import sys
sys.path.insert(0,"runtime")

from architecture_analysis import run_architecture_analysis,UNIT_JOB_PURITY
from solution_to_my_problem import Problem,Candidate,SolutionReceipt,solve
from improvement_core_return_gate import evaluate_parent_return
from global_tool_execution import execute_protected_transition,ToolExecutionBlocked
from tool_run_registry import CONFIGURED_RUNS
from prose import ProseContract,ProseEvidence


ARCH_REQUIRED=(
    "ArchClass","Violations","LocalizationFamilies","DependencyState",
    "InteractionState","TransformationFrontier","SuccessorFrontier",
    "Coverage","OpenConflictBlocked","Provenance",
)


def _arch_result(**extra):
    base={
        "ArchClass":"X",
        "Violations":(),
        "LocalizationFamilies":(),
        "DependencyState":{},
        "InteractionState":{},
        "TransformationFrontier":(),
        "SuccessorFrontier":(),
        "Coverage":(),
        "OpenConflictBlocked":(),
        "Provenance":("fixture",),
    }
    base.update(extra)
    return base


def test_architecture_fails_open_when_protected_prose_constraint_unwitnessed():
    out=run_architecture_analysis(
        {},
        {},
        analyze_architecture=lambda a,c:_arch_result(),
        protected_constraints=("AFFIRMATIVE_FIRST",),
    )
    assert out["status"]=="OPEN"
    assert "ARCHITECTURE_PROTECTED_CONSTRAINT" in out["blocker"]


def test_architecture_accepts_explicitly_preserved_prose_constraint():
    out=run_architecture_analysis(
        {},
        {},
        analyze_architecture=lambda a,c:_arch_result(
            ProtectedConstraintState={"AFFIRMATIVE_FIRST":"PRESERVED"}
        ),
        protected_constraints=("AFFIRMATIVE_FIRST",),
    )
    assert out["status"]=="RELATIVE_CLOSE"


def test_solution_candidate_must_preserve_protected_prose():
    problem=Problem(
        observed=("negative-first regression",),
        generators=("g",),
        required_effects=("fixed",),
        protected=("semantic",),
        protected_prose=("AFFIRMATIVE_FIRST",),
    )
    candidate=Candidate(
        id="c",
        proposed_attacks=("g",),
        proposed_effects=("fixed",),
        proposed_preservations=("semantic",),
    )
    out=solve(problem,(candidate,))
    assert out.status=="OPEN"
    assert "c" in out.rejected


def test_solution_receipt_closes_only_with_prose_preservation():
    problem=Problem(
        observed=("negative-first regression",),
        generators=("g",),
        required_effects=("fixed",),
        protected=("semantic",),
        protected_prose=("AFFIRMATIVE_FIRST",),
    )
    candidate=Candidate(
        id="c",
        proposed_attacks=("g",),
        proposed_effects=("fixed",),
        proposed_preservations=("semantic","AFFIRMATIVE_FIRST"),
    )
    receipt=SolutionReceipt(
        candidate_id="c",
        source="Prose",
        execution_stage="CONSUMED",
        observed_attacks=("g",),
        observed_effects=("fixed",),
        observed_preservations=("semantic","AFFIRMATIVE_FIRST"),
        verification_status="PASS",
        closure_status="CLOSED",
        evidence=("prose:PASS",),
    )
    assert solve(problem,(candidate,),(receipt,)).status=="SOLVED"


def _return_verifier(state,memory,ctx):
    return {
        "disposition":"RETURN",
        "terminal":"COMPLETE",
        "owned_work_remaining":False,
        "consequence_closed":True,
        "goal_closed":True,
        "evidence":("closure",),
    }



def _fresh_stable(state,memory,context):
    return {
        "status":"NO_GAIN",
        "owned_work_remaining":False,
        "evidence":[f"prose:fresh:{context['challenge_index']}"],
        "challenge_id":f"prose-fresh-{context['challenge_index']}",
    }


def test_improvementcore_complete_requires_prose_receipt_when_context_requires_it():
    try:
        evaluate_parent_return(
            candidate_status="COMPLETE",
            candidate_blocker=None,
            state={},
            memory={},
            context={"prose_receipt_required":True},
            verifier=_return_verifier,
        )
    except RuntimeError as exc:
        assert "PROSE_RECEIPT" in str(exc)
    else:
        raise AssertionError("missing prose receipt did not fail closed")


def test_improvementcore_complete_accepts_pass_prose_receipt():
    out=evaluate_parent_return(
        candidate_status="COMPLETE",
        candidate_blocker=None,
        state={
            "prose_transition_receipts":(
                {"contract_id":"canon","status":"PASS","evidence":("prose:PASS",)},
            ),
        },
        memory={},
        context={"prose_receipt_required":True},
        verifier=_return_verifier,
        fresh_reobserve=_fresh_stable,
    )
    assert out.terminal=="COMPLETE"


def _identity(value,plan):
    return value,"witness"


def _execute(value,plan):
    return value,"execute",{"hf2_local_close":True}


def _emit(value,plan):
    return "emission"


def test_final_emission_blocks_negative_first_prose():
    evidence=ProseEvidence(
        semantic_preservation="PASS",
        earned_claim_strength="PASS",
        no_unsupported_inflation="PASS",
        evidence=("semantic","strength","inflation"),
        plain_language="PASS",
        plain_language_evidence=(
            "the fixture is already ordinary wording; no simpler equivalent is material",
        ),
    )
    try:
        execute_protected_transition(
            CONFIGURED_RUNS["Prose"],
            behavior_id="PROSE_AFFIRMATIVE_FIRST_GATE",
            dispatch_fn=lambda plan:("seed","dispatch"),
            execute_fn=_execute,
            consume_fn=_identity,
            update_fn=_identity,
            reentry_fn=_identity,
            emission_audit_fn=_emit,
            prose_contract=ProseContract("canon"),
            prose_text_fn=lambda value,plan:(
                "Ramban does not merely offer a different emphasis. "
                "He directly attacks the premise."
            ),
            prose_evidence=evidence,
        )
    except ToolExecutionBlocked as exc:
        message=str(exc)
        assert "PROSE_NOT_ADMISSIBLE" in message
        assert "NOT_MERELY" in message
    else:
        raise AssertionError("negative-first prose escaped final emission gate")



def test_architecture_unit_job_purity_rejects_merged_question_and_scope_jobs():
    out=run_architecture_analysis(
        {},
        {},
        analyze_architecture=lambda a,c:_arch_result(
            UnitJobState={
                "paragraph-1":("STATE_RESEARCH_QUESTION","DELIMIT_SCOPE_EXCLUSIONS"),
            },
            UnitJobEvidence=("canonical-authority-1.2-reader-role-analysis",),
        ),
        protected_constraints=(UNIT_JOB_PURITY,),
    )
    assert out["status"]=="OPEN"
    assert "ARCHITECTURE_UNIT_JOB_PURITY_VIOLATION" in out["blocker"]


def test_architecture_unit_job_purity_accepts_separate_reader_jobs():
    out=run_architecture_analysis(
        {},
        {},
        analyze_architecture=lambda a,c:_arch_result(
            UnitJobState={
                "paragraph-1":("STATE_RESEARCH_QUESTION",),
                "paragraph-2":("DELIMIT_SCOPE_EXCLUSIONS",),
            },
            UnitJobEvidence=("canonical-authority-1.2-reader-role-analysis",),
        ),
        protected_constraints=(UNIT_JOB_PURITY,),
    )
    assert out["status"]=="RELATIVE_CLOSE"


def test_architecture_unit_job_purity_missing_evidence_stays_open():
    out=run_architecture_analysis(
        {},
        {},
        analyze_architecture=lambda a,c:_arch_result(
            UnitJobState={"paragraph-1":("STATE_RESEARCH_QUESTION",)},
        ),
        protected_constraints=(UNIT_JOB_PURITY,),
    )
    assert out["status"]=="OPEN"
    assert out["blocker"]=="ARCHITECTURE_UNIT_JOB_EVIDENCE_MISSING"
