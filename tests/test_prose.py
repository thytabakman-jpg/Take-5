import sys
sys.path.insert(0,"runtime")

from prose import (
    AFFIRMATIVE_FIRST,FIRST_MENTION_PERSON_DATES,NUMERIC_YEAR_DATES_ONLY,ORDERED_ANCHORS,
    READER_LOAD,PLAIN_LANGUAGE,QUESTION_TERMINATES_PARAGRAPH,JEWISH_LEXICAL_FORMS,
    ProseContract,ProseEvidence,
    assess_prose,require_prose_admissible,ProseAcceptanceError,
)


PASS_EVIDENCE=ProseEvidence(
    semantic_preservation="PASS",
    earned_claim_strength="PASS",
    no_unsupported_inflation="PASS",
    evidence=("fixture:semantic","fixture:strength","fixture:no-inflation"),
    plain_language="PASS",
    plain_language_evidence=("no simpler known wording preserves less reader burden with equal precision",),
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


def test_person_name_inside_larger_word_is_not_a_first_mention():
    contract=ProseContract(
        "exact-person-boundary",
        constraints=(FIRST_MENTION_PERSON_DATES,),
        person_dates=(("Rashi","1040–1105"),),
    )
    text="PseudoRashi is not the protected person. Rashi (1040–1105) appears later."
    assert require_prose_admissible(text,contract,PASS_EVIDENCE).status=="PASS"


def test_ordered_anchors_pass_in_declared_order():
    contract=ProseContract(
        "local-order",
        constraints=(ORDERED_ANCHORS,),
        ordered_anchors=("claim", "evidence", "implication"),
    )
    out=assess_prose("claim. evidence. implication.",contract,PASS_EVIDENCE)
    assert out.status=="PASS"


def test_ordered_anchors_reject_out_of_order_realization():
    contract=ProseContract(
        "local-order",
        constraints=(ORDERED_ANCHORS,),
        ordered_anchors=("claim", "evidence", "implication"),
    )
    out=assess_prose("evidence. claim. implication.",contract,PASS_EVIDENCE)
    assert out.status=="REPAIR_REQUIRED"
    assert any(v.code=="ORDERED_ANCHOR_OUT_OF_ORDER" for v in out.violations)


def test_ordered_anchors_without_contract_data_stays_open():
    contract=ProseContract("local-order",constraints=(ORDERED_ANCHORS,))
    out=assess_prose("claim. evidence.",contract,PASS_EVIDENCE)
    assert out.status=="OPEN"
    assert "ORDERED_ANCHORS_REQUIRED" in out.residuals



def test_reader_load_repair_required_for_observed_canonical_authority_case():
    text=(
        "The paper therefore asks a deliberately narrow question: when canonical "
        "interpreters make incompatible truth-apt claims, what source-grounded basis, "
        "if any, can give a later evaluator warranted reason to favor one claim as true?"
    )
    evidence=ProseEvidence(
        semantic_preservation="PASS",
        earned_claim_strength="PASS",
        no_unsupported_inflation="PASS",
        evidence=("fixture:semantic","fixture:strength","fixture:no-inflation"),
        reader_load="REPAIR_REQUIRED",
        reader_load_evidence=(
            "buried grammatical spine",
            "multiple simultaneous abstract referents",
            "nested qualification load",
        ),
    )
    out=assess_prose(
        text,
        ProseContract("reader-load",constraints=(READER_LOAD,)),
        evidence,
    )
    assert out.status=="REPAIR_REQUIRED"
    assert any(v.code=="READER_LOAD_REPAIR_REQUIRED" for v in out.violations)


def test_reader_load_pass_requires_concrete_evidence():
    evidence=ProseEvidence(
        semantic_preservation="PASS",
        earned_claim_strength="PASS",
        no_unsupported_inflation="PASS",
        evidence=("fixture:semantic","fixture:strength","fixture:no-inflation"),
        reader_load="PASS",
    )
    out=assess_prose(
        "The paper asks one narrow question.",
        ProseContract("reader-load",constraints=(READER_LOAD,)),
        evidence,
    )
    assert out.status=="OPEN"
    assert "READER_LOAD_EVIDENCE_REQUIRED" in out.residuals


def test_reader_load_passes_with_explicit_evidence():
    evidence=ProseEvidence(
        semantic_preservation="PASS",
        earned_claim_strength="PASS",
        no_unsupported_inflation="PASS",
        evidence=("fixture:semantic","fixture:strength","fixture:no-inflation"),
        reader_load="PASS",
        reader_load_evidence=("main proposition is immediate",),
    )
    out=require_prose_admissible(
        "The paper asks one narrow question.",
        ProseContract("reader-load",constraints=(READER_LOAD,)),
        evidence,
    )
    assert out.status=="PASS"


def test_default_prose_rejects_question_buried_mid_paragraph():
    out=assess_prose(
        "What is the governing claim? The paragraph continues after the question.",
        ProseContract("question-default"),
        PASS_EVIDENCE,
    )
    assert out.status=="REPAIR_REQUIRED"
    assert any(v.code=="QUESTION_BURIED_IN_PARAGRAPH" for v in out.violations)


def test_terminal_question_passes_in_ordinary_paragraph():
    out=require_prose_admissible(
        "The section narrows the issue. What can this source establish?",
        ProseContract("question-terminal"),
        PASS_EVIDENCE,
    )
    assert out.status=="PASS"


def test_question_only_paragraph_passes():
    out=require_prose_admissible(
        "What can this source establish?",
        ProseContract("question-only"),
        PASS_EVIDENCE,
    )
    assert out.status=="PASS"


def test_first_question_ends_paragraph_so_two_questions_fail():
    out=assess_prose(
        "What can this source establish? What follows from that?",
        ProseContract("two-questions"),
        PASS_EVIDENCE,
    )
    assert out.status=="REPAIR_REQUIRED"
    assert any(v.code=="QUESTION_BURIED_IN_PARAGRAPH" for v in out.violations)


def test_terminal_question_with_sup_citation_passes():
    text=(
        "What can this source establish? "
        "<sup>[[C067]](../control/CLAIM_SUPPORT_LEDGER.md#claim-ca-a0155)</sup>"
    )
    out=require_prose_admissible(
        text,
        ProseContract("question-citation"),
        PASS_EVIDENCE,
    )
    assert out.status=="PASS"


def test_question_followed_by_new_paragraph_passes():
    text=(
        "What can this source establish?\n\n"
        "The next paragraph begins the answer."
    )
    out=require_prose_admissible(
        text,
        ProseContract("question-paragraph-break"),
        PASS_EVIDENCE,
    )
    assert out.status=="PASS"


def test_jewish_lexical_gate_requires_explicit_lexicon():
    out=assess_prose(
        "Ramban reads the verse differently.",
        ProseContract(
            "jewish-lexicon-open",
            constraints=(JEWISH_LEXICAL_FORMS,),
        ),
        PASS_EVIDENCE,
    )
    assert out.status=="OPEN"
    assert "JEWISH_LEXICON_REQUIRED" in out.residuals


def test_jewish_lexical_gate_rejects_declared_noncanonical_form():
    contract=ProseContract(
        "jewish-lexicon-repair",
        constraints=(JEWISH_LEXICAL_FORMS,),
        jewish_lexicon=(
            ("Ramban",("ramban",)),
            ("peshat",("pshat","p'shat")),
            ("eilu ve-eilu",("elu v'elu","eilu v'eilu")),
        ),
    )
    out=assess_prose(
        "The pshat reading is attributed to Ramban.",
        contract,
        PASS_EVIDENCE,
    )
    assert out.status=="REPAIR_REQUIRED"
    assert any(
        v.code=="JEWISH_TERM_NONCANONICAL" and "pshat -> peshat" in v.excerpt
        for v in out.violations
    )


def test_jewish_lexical_gate_accepts_canonical_forms():
    contract=ProseContract(
        "jewish-lexicon-pass",
        constraints=(JEWISH_LEXICAL_FORMS,),
        jewish_lexicon=(
            ("Ramban",("ramban",)),
            ("peshat",("pshat","p'shat")),
            ("eilu ve-eilu",("elu v'elu","eilu v'eilu")),
        ),
    )
    out=require_prose_admissible(
        "Ramban presents a peshat reading alongside the eilu ve-eilu discussion.",
        contract,
        PASS_EVIDENCE,
    )
    assert out.status=="PASS"


def test_jewish_lexicon_conflict_fails_open():
    contract=ProseContract(
        "jewish-lexicon-conflict",
        constraints=(JEWISH_LEXICAL_FORMS,),
        jewish_lexicon=(
            ("peshat",("pshat",)),
            ("peshaṭ",("pshat",)),
        ),
    )
    out=assess_prose("The text uses peshat.",contract,PASS_EVIDENCE)
    assert out.status=="OPEN"
    assert any(x.startswith("JEWISH_LEXICON_CONFLICT:pshat:") for x in out.residuals)


def test_terminal_quoted_question_passes():
    out=require_prose_admissible(
        'The source asks, "What follows?"',
        ProseContract("quoted-question"),
        PASS_EVIDENCE,
    )
    assert out.status=="PASS"



def test_default_plain_language_gate_requires_receipt():
    evidence=ProseEvidence(
        semantic_preservation="PASS",
        earned_claim_strength="PASS",
        no_unsupported_inflation="PASS",
        evidence=("fixture:semantic","fixture:strength","fixture:no-inflation"),
    )
    out=assess_prose(
        "The paper states the claim clearly.",
        ProseContract("plain-default"),
        evidence,
    )
    assert out.status=="OPEN"
    assert "PLAIN_LANGUAGE:OPEN" in out.residuals


def test_plain_language_gate_flags_needlessly_academic_wording():
    evidence=ProseEvidence(
        semantic_preservation="PASS",
        earned_claim_strength="PASS",
        no_unsupported_inflation="PASS",
        evidence=("fixture:semantic","fixture:strength","fixture:no-inflation"),
        plain_language="REPAIR_REQUIRED",
        plain_language_evidence=(
            "use works instead of functions as where both preserve the intended meaning",
        ),
    )
    out=assess_prose(
        "The rule functions as the main test.",
        ProseContract("plain-repair",constraints=(PLAIN_LANGUAGE,)),
        evidence,
    )
    assert out.status=="REPAIR_REQUIRED"
    assert any(v.code=="PLAIN_LANGUAGE_REPAIR_REQUIRED" for v in out.violations)


def test_plain_language_gate_allows_required_technical_terms():
    evidence=ProseEvidence(
        semantic_preservation="PASS",
        earned_claim_strength="PASS",
        no_unsupported_inflation="PASS",
        evidence=("fixture:semantic","fixture:strength","fixture:no-inflation"),
        plain_language="PASS",
        plain_language_evidence=(
            "semantic entailment is the required technical relation; simpler substitutes lose precision",
        ),
    )
    out=require_prose_admissible(
        "Semantic entailment requires truth preservation across the relevant models.",
        ProseContract("plain-technical",constraints=(PLAIN_LANGUAGE,)),
        evidence,
    )
    assert out.status=="PASS"


def test_plain_language_cannot_override_failed_semantic_preservation():
    evidence=ProseEvidence(
        semantic_preservation="FAIL",
        earned_claim_strength="PASS",
        no_unsupported_inflation="PASS",
        evidence=("fixture:semantic-fail","fixture:strength","fixture:no-inflation"),
        plain_language="PASS",
        plain_language_evidence=("wording is simple",),
    )
    out=assess_prose(
        "The claim is simple.",
        ProseContract("plain-accuracy-priority",constraints=(PLAIN_LANGUAGE,)),
        evidence,
    )
    assert out.status=="OPEN"
    assert "SEMANTIC_PRESERVATION:FAIL" in out.residuals
