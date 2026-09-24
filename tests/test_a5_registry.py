from a5_programs import REGISTRY,EXPECTED_C,EXPECTED_CAP

def test_full_c_registry_enrolled(): assert REGISTRY.coverage("C")==EXPECTED_C

def test_full_historical_registry_enrolled(): assert REGISTRY.coverage("CAP-")==EXPECTED_CAP

def test_all_specs_have_valid_bindings():
    for pid in REGISTRY.ids():
        s=REGISTRY.get(pid)
        assert s.required_roles and set(s.required_roles)<=REGISTRY.VALID_ROLES
        assert s.protected_outputs and s.validation_target

def test_enrollment_is_not_execution_claim():
    assert REGISTRY.executable_ids()==set()
