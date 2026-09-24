from historical_reconstruction import ReconstructionCase,compare,contextual_equivalence

def case(**kw):
    d=dict(historical_id="CAP-001",successor_id="C19",frozen_job="discover dependency",protected=("dependency",),predecessor_result={"x":["y"]},successor_result={"x":["y"]},predecessor_witness="old-run",successor_witness="new-run")
    d.update(kw); return ReconstructionCase(**d)

def test_name_similarity_never_enough():
    c=case(predecessor_witness="")
    assert compare(c).status=="OPEN"

def test_matched_protected_result_passes_case():
    assert compare(case()).status=="PASS"

def test_divergence_fails():
    assert compare(case(successor_result={"x":[]})).status=="FAIL"

def test_contextual_equivalence_requires_all_cases():
    assert contextual_equivalence([case(),case(predecessor_witness="")]).status=="OPEN"

def test_contextual_divergence_dominates():
    assert contextual_equivalence([case(),case(successor_result={"z":1})]).status=="FAIL"
