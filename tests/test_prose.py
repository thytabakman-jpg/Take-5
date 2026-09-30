import sys
sys.path.insert(0,"runtime")

from prose import (
    AFFIRMATIVE_FIRST,FIRST_MENTION_PERSON_DATES,NUMERIC_YEAR_DATES_ONLY,
    ProseContract,ProseEvidence,
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


def test_first_mention_person_date_is_required_at_first_occurrence():
    contract=ProseContract(
        "dates",
        constraints=(FIRST_MENTION_PERSON_DATES,),
        person_dates=(("Rashi","1040–1105"),),
    )
    out=assess_prose(
        "Rashi reads the verse this way. Rashi (1040–1105) later adds a proof.",
        contract,
        PASS_EVIDENCE,
    )
    assert out.status=="REPAIR_REQUIRED"
    assert any(v.code=="FIRST_MENTION_DATE_MISSING" for v in out.violations)


def test_first_mention_person_date_passes_and_later_mentions_stay_clean():
    contract=ProseContract(
        "dates",
        constraints=(FIRST_MENTION_PERSON_DATES,),
        person_dates=(("Rashi","1040–1105"),("Ramban","1194–1270")),
    )
    out=require_prose_admissible(
        "Rashi (1040–1105) argues first. Rashi then adds a grammatical point. "
        "Ramban (1194–1270) rejects the reading. Ramban develops the objection.",
        contract,
        PASS_EVIDENCE,
    )
    assert out.status=="PASS"


def test_unknown_person_date_stays_open_instead_of_being_guessed():
    contract=ProseContract(
        "dates",
        constraints=(FIRST_MENTION_PERSON_DATES,),
        person_dates=(("Some Scholar",""),),
    )
    out=assess_prose(
        "Some Scholar argues that the reading fails.",
        contract,
        PASS_EVIDENCE,
    )
    assert out.status=="OPEN"
    assert "PERSON_DATE_UNRESOLVED:Some Scholar" in out.residuals


def test_default_prose_contract_rejects_numeric_century_label():
    out=assess_prose(
        "Rashi lived in the 11th century.",
        ProseContract("numeric-years"),
        PASS_EVIDENCE,
    )
    assert out.status=="REPAIR_REQUIRED"
    assert any(v.code=="NUMERIC_CENTURY_LABEL" for v in out.violations)


def test_default_prose_contract_rejects_word_century_label():
    out=assess_prose(
        "Rambam wrote in the twelfth century.",
        ProseContract("numeric-years"),
        PASS_EVIDENCE,
    )
    assert out.status=="REPAIR_REQUIRED"
    assert any(v.code=="WORD_CENTURY_LABEL" for v in out.violations)


def test_numeric_uncertainty_formats_pass():
    contract=ProseContract(
        "numeric-years",
        constraints=(NUMERIC_YEAR_DATES_ONLY,FIRST_MENTION_PERSON_DATES),
        person_dates=(
            ("Scholar A","c. 1075–1141"),
            ("Scholar B","fl. 1170–1190"),
            ("Scholar C","d. 1204"),
        ),
    )
    text=(
        "Scholar A (c. 1075–1141) appears first. "
        "Scholar B (fl. 1170–1190) appears next. "
        "Scholar C (d. 1204) appears last."
    )
    assert require_prose_admissible(text,contract,PASS_EVIDENCE).status=="PASS"


def test_person_date_century_substitute_is_rejected():
    contract=ProseContract(
        "numeric-years",
        constraints=(NUMERIC_YEAR_DATES_ONLY,FIRST_MENTION_PERSON_DATES),
        person_dates=(("Some Scholar","12th century"),),
    )
    out=assess_prose(
        "Some Scholar (12th century) argues for the reading.",
        contract,
        PASS_EVIDENCE,
    )
    assert out.status=="REPAIR_REQUIRED"
    assert any(
        v.code in {"NUMERIC_CENTURY_LABEL","PERSON_DATE_CENTURY_LABEL_FORBIDDEN"}
        for v in out.violations
    )


def test_person_date_without_numeric_year_is_rejected_not_guessed():
    contract=ProseContract(
        "numeric-years",
        constraints=(NUMERIC_YEAR_DATES_ONLY,FIRST_MENTION_PERSON_DATES),
        person_dates=(("Some Scholar","medieval"),),
    )
    out=assess_prose(
        "Some Scholar (medieval) argues for the reading.",
        contract,
        PASS_EVIDENCE,
    )
    assert out.status=="REPAIR_REQUIRED"
    assert any(v.code=="PERSON_DATE_NUMERIC_YEAR_REQUIRED" for v in out.violations)
