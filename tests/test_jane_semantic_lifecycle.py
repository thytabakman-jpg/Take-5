from jane_supervisor import JaneSupervisoryState,semantic_capture_obligation,semantic_followup_work

def test_discovered_load_bearing_term_creates_capture_work():
    s=JaneSupervisoryState()
    a=semantic_capture_obligation(
        s,
        object_id="TERM:X",
        term="x",
        source="test",
        load_bearing=True,
        package_current=False,
        created_here=False,
    )
    assert a["kind"]=="LOAD_BEARING_TERM_PACKAGE"
    assert a["status"]=="WORK_CANDIDATE"

def test_created_tool_requires_math_and_package():
    s=JaneSupervisoryState()
    a=semantic_capture_obligation(
        s,
        object_id="TOOL:X",
        term="X",
        source="foundry",
        load_bearing=True,
        package_current=True,
        created_here=True,
        math_complete_for_use=False,
    )
    assert a["kind"]=="CREATED_OBJECT_MATH_AND_PACKAGE"

def test_created_tool_with_math_and_package_creates_no_work():
    s=JaneSupervisoryState()
    assert semantic_capture_obligation(
        s,
        object_id="TOOL:X",
        term="X",
        source="foundry",
        load_bearing=True,
        package_current=True,
        created_here=True,
        math_complete_for_use=True,
    ) is None


def test_unknown_load_bearingness_is_captured_not_pruned():
    s=JaneSupervisoryState()
    a=semantic_capture_obligation(
        s,
        object_id="TERM:UNKNOWN",
        term="unknown",
        source="test",
        load_bearing=None,
        package_current=False,
        created_here=False,
    )
    assert a is not None
    assert a["load_bearing_status"]=="OPEN"


def test_black_box_capture_triggers_pd_and_pd_audit():
    s=JaneSupervisoryState()
    a=semantic_capture_obligation(
        s,
        object_id="TERM:BB",
        term="bb",
        source="test",
        load_bearing=None,
        package_current=False,
        created_here=False,
        math_complete_for_use=False,
    )
    assert a["followup_configured_runs"]==("PD","PDAudit")


def test_black_box_followups_become_material_work():
    s=JaneSupervisoryState()
    a=semantic_capture_obligation(
        s,
        object_id="TERM:BB",
        term="bb",
        source="test",
        load_bearing=None,
        package_current=False,
        created_here=False,
        math_complete_for_use=False,
    )
    work=semantic_followup_work(a)
    assert tuple(w.obligation for w in work)==(
        "RUN_CONFIGURED:PD:TERM:BB",
        "RUN_CONFIGURED:PDAudit:TERM:BB",
    )
    assert all(w.material for w in work)
