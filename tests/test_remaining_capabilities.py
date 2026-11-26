from a5_programs import REGISTRY, run_generic
from capability_router import coverage, CoverageStatus

def test_all_c_capabilities_are_runtime_bound():
    assert all(REGISTRY.get(f"C{i:02d}").executable for i in range(1,50))

def test_remaining_family_preserves_open():
    assert run_generic("C24",{"candidate":{"id":"x"},"protected":["p"],"preserves":[]})["status"]=="OPEN"
    assert run_generic("C47",{"blocking_open":["historical"]})["status"]=="OPEN"

def test_remaining_family_can_realize_typed_cases():
    assert run_generic("C20",{"rivals":[{"id":"r"}]})["status"]=="ACCEPT"
    assert run_generic("C33",{"strict_gain":True,"preserves":True})["status"]=="ACCEPT"
    assert run_generic("C44",{"expected":{"x":1},"actual":{"x":1}})["status"]=="ACCEPT"

def test_router_no_longer_reports_relevant_c20_c48_as_unbound():
    tags=set()
    from capability_router import TRIGGER_TAGS
    for i in range(20,49): tags |= TRIGGER_TAGS[f"C{i:02d}"]
    r=coverage("remaining",tags)
    bad=[x.program_id for x in r.dispositions if x.status==CoverageStatus.UNBOUND and x.program_id.startswith("C")]
    assert bad==[]


def test_missing_comparison_inputs_do_not_certify_regression_or_verification():
    for pid in ("C34","C44"):
        assert run_generic(pid,{})["status"]=="OPEN"
    assert run_generic("C34",{"protected_before":None,"protected_after":None})["status"]=="OPEN"
    assert run_generic("C44",{"expected":None})["status"]=="OPEN"
    assert run_generic("C44",{"expected":None,"actual":None})["status"]=="ACCEPT"


def test_textual_false_is_not_route_license_or_strict_gain():
    assert run_generic("C32",{"routes":[{"licensed":"false","reachable":True}]})["status"]=="OPEN"
    assert run_generic("C33",{"strict_gain":"false","preserves":True})["status"]=="OPEN"
    assert run_generic("C33",{"strict_gain":True,"preserves":"false"})["status"]=="OPEN"
