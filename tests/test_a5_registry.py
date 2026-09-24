from a5_programs import REGISTRY,EXPECTED_C,EXPECTED_CAP

def test_full_c_registry_enrolled(): assert {x for x in REGISTRY.ids() if x.startswith("C") and not x.startswith("CAP-")}==EXPECTED_C

def test_full_historical_registry_enrolled(): assert REGISTRY.coverage("CAP-")==EXPECTED_CAP

def test_all_specs_have_valid_bindings():
    for pid in REGISTRY.ids():
        s=REGISTRY.get(pid)
        assert s.required_roles and set(s.required_roles)<=REGISTRY.VALID_ROLES
        assert s.protected_outputs and s.validation_target

def test_enrollment_is_not_execution_claim():
    assert REGISTRY.executable_ids()=={"C01","C02","C03","C04","C05","C06"}
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
