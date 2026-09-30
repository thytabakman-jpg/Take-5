import sys
sys.path.insert(0,"runtime")

from architecture_analysis import run_architecture_analysis
from solution_to_my_problem import Problem,Candidate,SolutionReceipt,solve
from improvement_core_return_gate import evaluate_parent_return


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
    )
    assert out.terminal=="COMPLETE"
