from tool_maturity import *
def test_namespaces_are_separate():
    assert len(active_capability_ids())==49
    assert len(historical_witness_ids())==33
    assert not set(active_capability_ids()) & set(historical_witness_ids())
def test_current_when_bound_triggered_and_current():
    assert all(x.disposition is Maturity.CURRENT for x in audit_all())
def test_material_basis_change_requires_revalidation_not_rewrite():
    x={r.program_id:r for r in audit_all(changed_ids=("C11",))}
    assert x["C11"].disposition is Maturity.REVALIDATE
    assert x["C12"].disposition is Maturity.CURRENT
