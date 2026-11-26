from runtime.capability_router import coverage, closure_allowed, CoverageStatus

def by_id(receipt,pid):
    return next(x for x in receipt.dispositions if x.program_id==pid)

def test_root_cause_selects_bound_root_cause_tool():
    r=coverage("repeat-tool-nonuse",["repeated_failure","root_cause"],licensed=["C18"])
    assert by_id(r,"C18").status==CoverageStatus.SELECTED

def test_previously_unbound_architecture_capability_is_now_selected():
    r=coverage("system-defect",["system_defect","architecture"])
    assert by_id(r,"C26").status==CoverageStatus.SELECTED
    assert by_id(r,"C20").status==CoverageStatus.NON_APPLICABLE

def test_nonselection_is_explicit():
    r=coverage("identity",["identity_risk"],licensed=["C02"])
    assert by_id(r,"C02").status==CoverageStatus.SELECTED
    assert by_id(r,"C18").status==CoverageStatus.NON_APPLICABLE

def test_every_registered_capability_gets_disposition():
    r=coverage("wide",["architecture"])
    assert {x.program_id for x in r.dispositions} == {f"C{i:02d}" for i in range(1, 50)}
    assert len(r.dispositions) == 49
    assert closure_allowed(r)


def test_missing_current_trigger_still_blocks_coverage_closure(monkeypatch):
    from runtime.capability_router import TRIGGER_TAGS
    monkeypatch.delitem(TRIGGER_TAGS, "C26")
    r = coverage("wide", ["architecture"])
    assert by_id(r, "C26").status == CoverageStatus.OPEN
    assert not closure_allowed(r)
