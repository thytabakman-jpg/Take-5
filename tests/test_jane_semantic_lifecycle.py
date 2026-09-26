from jane_supervisor import JaneSupervisoryState,semantic_capture_obligation

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
