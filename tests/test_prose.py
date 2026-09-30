import sys
sys.path.insert(0,"runtime")

from prose import (
    AFFIRMATIVE_FIRST,ProseContract,ProseEvidence,
    assess_prose,require_prose_admissible,ProseAcceptanceError,
)


PASS_EVIDENCE=ProseEvidence(
    semantic_preservation="PASS",
    earned_claim_strength="PASS",
    no_unsupported_inflation="PASS",
    evidence=("fixture:semantic","fixture:strength","fixture:no-inflation"),
)


def test_exact_canonical_authority_regression_is_rejected():
    text=(
        "Ramban does not merely offer a different emphasis. "
        "He directly attacks that supporting generalization."
    )
    out=assess_prose(text,ProseContract("canon"),PASS_EVIDENCE)
    assert out.status=="REPAIR_REQUIRED"
    assert any(v.code=="NOT_MERELY" for v in out.violations)


def test_affirmative_first_repair_passes_with_semantic_receipts():
    text="Ramban directly attacks that supporting generalization."
    out=require_prose_admissible(text,ProseContract("canon"),PASS_EVIDENCE)
    assert out.status=="PASS"


def test_load_bearing_negation_can_be_explicitly_exempted():
    text=(
        "First, the tradition does not guarantee correctness on the disputed matter. "
        "It can still provide defeasible epistemic support."
    )
    contract=ProseContract(
        "trilemma",
        constraints=(AFFIRMATIVE_FIRST,),
        allowed_negative_spans=(
            "the tradition does not guarantee correctness on the disputed matter",
        ),
    )
    assert require_prose_admissible(text,contract,PASS_EVIDENCE).status=="PASS"


def test_surface_pass_without_semantic_receipts_stays_open():
    out=assess_prose(
        "Ramban directly attacks that supporting generalization.",
        ProseContract("canon"),
    )
    assert out.status=="OPEN"


def test_unsupported_constraint_fails_open():
    out=assess_prose(
        "Ramban directly attacks.",
        ProseContract("x",constraints=("UNKNOWN_PROSE_RULE",)),
        PASS_EVIDENCE,
    )
    assert out.status=="OPEN"
    assert out.unsupported_constraints==("UNKNOWN_PROSE_RULE",)
