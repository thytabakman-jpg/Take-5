from exact_equation_recovery import EquationCandidate, RecoveryMemory, RecoveryReceipt, classify

def mk_candidate(**kw):
    d={"candidate_id":"c1","target_id":"t1","expression":"A=B","derivation_kind":"EXACT_COPY"}
    d.update(kw)
    return EquationCandidate(**d)

def mk_receipt(**kw):
    d={"candidate_id":"c1","target_id":"t1","source_ref":"fixture-1","source_kind":"fixture","exact_expression_match":True,"evidence":("match",)}
    d.update(kw)
    return RecoveryReceipt(**d)

def test_requires_receipt():
    assert classify(mk_candidate(), None).status == "OPEN"

def test_derived_is_not_exact():
    assert classify(mk_candidate(derivation_kind="DERIVED"), mk_receipt()).status == "DERIVED_RECONSTRUCTION"

def test_rejected_candidate_stays_rejected():
    memory=RecoveryMemory(rejected_candidate_ids=("c1",))
    assert classify(mk_candidate(), mk_receipt(), memory).status == "REJECTED"

def test_rejected_expression_survives_rename():
    memory=RecoveryMemory(rejected_expressions=("A=B",))
    assert classify(mk_candidate(candidate_id="c2"), mk_receipt(candidate_id="c2"), memory).status == "REJECTED"

def test_reopen_is_explicit():
    memory=RecoveryMemory(rejected_candidate_ids=("c1",), reopened_candidate_ids=("c1",))
    assert classify(mk_candidate(), mk_receipt(), memory).status == "EXACT_RECOVERY"

def test_mismatched_receipt_conflicts():
    assert classify(mk_candidate(), mk_receipt(target_id="t2")).status == "CONFLICT"

def test_exact_match_required():
    assert classify(mk_candidate(), mk_receipt(exact_expression_match=False)).status == "OPEN"

def test_exact_source_match_passes():
    assert classify(mk_candidate(), mk_receipt()).status == "EXACT_RECOVERY"
