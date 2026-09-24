from a5_programs import REGISTRY,EXPECTED_C,EXPECTED_CAP

def test_full_c_registry_enrolled(): assert {x for x in REGISTRY.ids() if x.startswith("C") and not x.startswith("CAP-")}==EXPECTED_C

def test_full_historical_registry_enrolled(): assert REGISTRY.coverage("CAP-")==EXPECTED_CAP

def test_all_specs_have_valid_bindings():
    for pid in REGISTRY.ids():
        s=REGISTRY.get(pid)
        assert s.required_roles and set(s.required_roles)<=REGISTRY.VALID_ROLES
        assert s.protected_outputs and s.validation_target

def test_enrollment_is_not_execution_claim():
    assert REGISTRY.executable_ids()=={"C01","C02","C03","C04","C05","C06","C07","C08","C09","C10","C11","C12","C13","C49"}
    assert not (EXPECTED_CAP & REGISTRY.executable_ids())


from a5_programs import run_orient

def test_orient_family_bound_executable():
    assert {"C01","C02","C03","C04","C05","C06"} <= REGISTRY.executable_ids()

def test_c01_preserves_multiple_typings_as_open():
    r=run_orient("C01",{"admissible_typings":["research","artifact"]})
    assert r["status"]=="OPEN" and len(r["alternatives"])==2

def test_c02_string_identity_not_enough():
    r=run_orient("C02",{"name":"same"})
    assert r["status"]=="OPEN"

def test_c03_recency_not_authority():
    r=run_orient("C03",{"versions":[{"id":"old","authoritative":True},{"id":"new","authoritative":False}]})
    assert r["current"]=="old"

def test_c04_freezes_source_separately():
    r=run_orient("C04",{"source_id":"s1","claim":"x"})
    assert r["frozen_source_packet"]=={"source_id":"s1","claim":"x"}

def test_c05_freezes_target_and_protected_set():
    r=run_orient("C05",{"target":"migration readiness","protected":["authority","provenance"]})
    assert r["frozen_target_contract"]["target"]=="migration readiness"

def test_c06_unavailable_dependency_is_not_failure():
    r=run_orient("C06",{"dependencies":[{"id":"ext"}]})
    assert r["status"]=="OPEN"


from a5_programs import run_map

def test_map_family_bound_executable():
    assert {"C07","C08","C09","C10","C11","C12","C13","C49"} <= REGISTRY.executable_ids()

def test_map_dependency_materiality():
    r=run_map("C07",{"candidate_edges":[{"id":"a","material":False},{"id":"b","material":True}]})
    assert [x["id"] for x in r["typed_dependency_edges"]]==["b"]

def test_map_plural_spines():
    assert len(run_map("C08",{"spines":[["a","b"],["a","c"]]})["plural_dependency_spines"])==2

def test_map_requires_typed_relation():
    assert run_map("C09",{"edges":[{"a":"x","b":"y"}]})["status"]=="OPEN"

def test_map_representation_sensitivity():
    r=run_map("C10",{"representations":[{"id":"r1","result":1},{"id":"r2","result":2}]})
    assert not r["invariant"] and len(r["representation_residual"])==2

def test_map_result_sensitivity():
    r=run_map("C11",{"coordinates":[{"id":"x","changed_result":False},{"id":"y","changed_result":True}]})
    assert r["minimal_sensitive_supports"]==["y"]

def test_map_invariant_localization():
    r=run_map("C12",{"sensitivity_maps":[["a","b"],["b","c"],["b"]]})
    assert r["invariant_core"]==["b"] and set(r["residual"])=={"a","c"}

def test_map_attribution_separation():
    assert run_map("C13",{"edges":[{"from":"s","to":"c"}]})["status"]=="OPEN"

def test_map_navigation_relevance_not_location():
    r=run_map("C49",{"visited":[{"id":"near","task_relevant":False},{"id":"far","task_relevant":True}]})
    assert r["exact_object_set"]==["far"]
