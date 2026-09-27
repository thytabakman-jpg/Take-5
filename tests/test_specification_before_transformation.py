import sys
sys.path.insert(0,"runtime")

from specification_before_transformation import (
    SpecificationPacket,
    assess_transformation,
    assess_selected_state,
    progress_specification_licensed,
)
from emergent_admission import Admission,ObjectCandidate,admit
from improvement_core_manager import run_improvement_core_manager
from ic028_operator import GOAL_DIRECTED_STAGES


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
    assert not progress_specification_licensed(
        "CONTROLLER","OPEN",transformation_claim=True
    )
    assert progress_specification_licensed(
        "CONTROLLER","PASS",transformation_claim=True
    )
    assert progress_specification_licensed(
        "ARTIFACT","OPEN",transformation_claim=True
    )
    assert progress_specification_licensed("CONTROLLER","OPEN")


def test_emergent_transform_claim_cannot_be_admitted_from_package_reality_alone():
    candidate=ObjectCandidate(
        object_id="TOOL:NEW",
        object_type="configured_program",
        load_bearing=True,
        transform_claim=True,
        specification_status="OPEN",
    )
    assert admit(candidate,package_verifier=lambda _:True)==Admission.OPEN

    recovered=ObjectCandidate(
        object_id="TOOL:NEW",
        object_type="configured_program",
        load_bearing=True,
        transform_claim=True,
        specification_status="PASS",
    )
    assert admit(recovered,package_verifier=lambda _:True)==Admission.ACCEPT


def _manager_handlers(selected_action):
    handlers={}
    for stage in GOAL_DIRECTED_STAGES:
        def fn(state,stage=stage):
            next_state=dict(state)
            if stage=="SELECT":
                next_state["selected_action"]=dict(selected_action)
            return {
                "state":next_state,
                "material_delta":False,
            }
        handlers[stage]=fn
    handlers["COMPLETE"]=lambda state:{
        "state":state,
        "terminal":True,
        "material_delta":False,
    }
    handlers["REENTER"]=lambda state:{"state":state,"terminal":True}
    return handlers


def test_improvementcore_blocks_selected_transform_before_bind_execute():
    out=run_improvement_core_manager(
        "ImproveCore, improve this device",
        target="TOOL:X",
        job="improve",
        basis="b0",
        state={},
        handlers=_manager_handlers({
            "id":"rewrite-x",
            "operation_class":"IMPROVE",
        }),
    )
    assert not out.result.terminal
    assert out.result.blocker.startswith("SPECIFICATION_OPEN")
    stages=tuple(r.stage for r in out.result.receipts)
    assert "SPECIFICATION_GATE" in stages
    assert "BIND" not in stages
    assert "EXECUTE" not in stages


def test_improvementcore_allows_recovery_work_on_unrecovered_object():
    out=run_improvement_core_manager(
        "ImproveCore, recover this device",
        target="TOOL:X",
        job="recover",
        basis="b0",
        state={},
        handlers=_manager_handlers({
            "id":"recover-x",
            "operation_class":"RECOVER",
        }),
    )
    assert out.result.terminal
