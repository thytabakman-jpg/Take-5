import sys
sys.path.insert(0,"runtime")

from specification_before_transformation import (
    SpecificationPacket,
    assess_transformation,
    assess_selected_state,
    progress_specification_licensed,
)


def packet(**overrides):
    base=dict(
        object_id="TOOL:X",
        basis_id="b0",
        identification_status="IDENTIFIED",
        required_coordinates=frozenset({"native","wrapper","protected"}),
        resolved_coordinates=frozenset({"native","wrapper","protected"}),
        open_coordinates=frozenset(),
        invariant_coordinates=frozenset(),
        candidate_invariant=False,
    )
    base.update(overrides)
    return SpecificationPacket(**base)


def test_recovery_work_is_legal_before_object_is_solved():
    r=assess_transformation(None,"RECOVER")
    assert r.status=="PASS"


def test_transform_without_specification_fails_closed():
    r=assess_transformation(None,"IMPROVE")
    assert r.status=="OPEN"
    assert r.reason=="SPECIFICATION_PACKET_REQUIRED"


def test_missing_required_coordinate_blocks_transform():
    p=packet(
        resolved_coordinates=frozenset({"native","wrapper"}),
        open_coordinates=frozenset({"protected"}),
    )
    r=assess_transformation(p,"ARCHITECT")
    assert r.status=="OPEN"
    assert r.missing_coordinates==("protected",)


def test_open_coordinate_can_be_closed_by_invariance_witness():
    p=packet(
        resolved_coordinates=frozenset({"native","wrapper"}),
        open_coordinates=frozenset({"protected"}),
        invariant_coordinates=frozenset({"protected"}),
    )
    assert assess_transformation(p,"IMPROVE").status=="PASS"


def test_plural_identity_requires_candidate_invariance():
    p=packet(identification_status="PLURAL")
    assert assess_transformation(p,"BUILD").status=="OPEN"
    p2=packet(identification_status="PLURAL",candidate_invariant=True)
    assert assess_transformation(p2,"BUILD").status=="PASS"


def test_selected_work_requires_explicit_operation_class():
    state={"selected_tool":"RootCause"}
    r=assess_selected_state(state)
    assert r.status=="OPEN"
    assert r.reason=="SELECTED_OPERATION_CLASS_REQUIRED"


def test_selected_recovery_tool_does_not_need_full_spec():
    state={
        "selected_tool":"RootCause",
        "selected_operation_class":"DIAGNOSE",
    }
    assert assess_selected_state(state).status=="PASS"


def test_selected_transform_requires_packet():
    state={
        "selected_action":{"id":"rewrite-x","operation_class":"IMPROVE"},
    }
    assert assess_selected_state(state).status=="OPEN"


def test_no_selection_does_not_create_fake_transform_obligation():
    assert assess_selected_state({}).status=="PASS"


def test_transform_sensitive_progress_claim_requires_pass():
    assert not progress_specification_licensed("CONTROLLER","OPEN")
    assert progress_specification_licensed("CONTROLLER","PASS")
    assert progress_specification_licensed("ARTIFACT","OPEN")
