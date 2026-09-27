"""Specification-before-transformation invariant.

Discovery may operate on an unresolved object.  Object-transforming work may not.

The gate is job/basis relative rather than requiring omniscience: every coordinate
that the selected transformation can depend on must either be resolved or carry
an explicit invariance witness proving that varying the unresolved coordinate
cannot change the protected result.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


RECOVERY_OPERATION_CLASSES=frozenset({
    "OBSERVE","DISCOVER","RECOVER","OBJECTIFY","FORMALIZE",
    "COMPARE","AUDIT","VERIFY","DIAGNOSE","RECONSTRUCT",
})

TRANSFORMATION_OPERATION_CLASSES=frozenset({
    "ARCHITECT","BUILD","MODIFY","TRANSFORM","IMPROVE","REPLACE",
    "PROMOTE","SUPERSEDE","MIGRATE","INTEGRATE_TRANSFORM",
    "EXECUTE_TRANSFORM",
})

TRANSFORM_SENSITIVE_TARGETS=frozenset({
    "METHOD","INTERACTION","REDUCTION","ACTIVATION",
    "HOST_BOUNDARY","CONTROLLER",
})


@dataclass(frozen=True)
class SpecificationPacket:
    object_id:str
    basis_id:str
    identification_status:str
    required_coordinates:frozenset[str]
    resolved_coordinates:frozenset[str]
    open_coordinates:frozenset[str]=frozenset()
    invariant_coordinates:frozenset[str]=frozenset()
    candidate_invariant:bool=False


@dataclass(frozen=True)
class SpecificationReceipt:
    status:str
    operation_class:str
    object_id:str|None
    basis_id:str|None
    missing_coordinates:tuple[str,...]=()
    conflicting_coordinates:tuple[str,...]=()
    reason:str|None=None

    @property
    def licensed(self)->bool:
        return self.status=="PASS"

    @property
    def blocker(self)->str|None:
        if self.status=="PASS":
            return None
        suffix=f":{self.reason}" if self.reason else ""
        return f"SPECIFICATION_{self.status}{suffix}"


def _norm(value:Any)->str:
    return str(value or "").strip().upper()


def packet_from_mapping(value:Mapping[str,Any]|None)->SpecificationPacket|None:
    if not isinstance(value,Mapping):
        return None
    object_id=str(value.get("object_id","")).strip()
    basis_id=str(value.get("basis_id","")).strip()
    status=_norm(value.get("identification_status"))
    required=frozenset(str(x) for x in value.get("required_coordinates",()) if str(x))
    resolved=frozenset(str(x) for x in value.get("resolved_coordinates",()) if str(x))
    opened=frozenset(str(x) for x in value.get("open_coordinates",()) if str(x))
    invariant=frozenset(str(x) for x in value.get("invariant_coordinates",()) if str(x))
    return SpecificationPacket(
        object_id=object_id,
        basis_id=basis_id,
        identification_status=status,
        required_coordinates=required,
        resolved_coordinates=resolved,
        open_coordinates=opened,
        invariant_coordinates=invariant,
        candidate_invariant=bool(value.get("candidate_invariant",False)),
    )


def assess_transformation(
    packet:SpecificationPacket|None,
    operation_class:str,
)->SpecificationReceipt:
    op=_norm(operation_class)
    if op in RECOVERY_OPERATION_CLASSES:
        return SpecificationReceipt("PASS",op,None,None,reason="RECOVERY_OPERATION")
    if op not in TRANSFORMATION_OPERATION_CLASSES:
        return SpecificationReceipt("OPEN",op or "UNSPECIFIED",None,None,reason="OPERATION_CLASS_UNRESOLVED")
    if packet is None:
        return SpecificationReceipt("OPEN",op,None,None,reason="SPECIFICATION_PACKET_REQUIRED")
    if not packet.object_id:
        return SpecificationReceipt("OPEN",op,None,packet.basis_id or None,reason="OBJECT_ID_REQUIRED")
    if not packet.basis_id:
        return SpecificationReceipt("OPEN",op,packet.object_id,None,reason="BASIS_ID_REQUIRED")

    status=_norm(packet.identification_status)
    if status=="BLOCKED":
        return SpecificationReceipt("BLOCKED",op,packet.object_id,packet.basis_id,reason="OBJECT_IDENTIFICATION_BLOCKED")
    if status=="OPEN":
        return SpecificationReceipt("OPEN",op,packet.object_id,packet.basis_id,reason="OBJECT_IDENTIFICATION_OPEN")
    if status=="PLURAL" and not packet.candidate_invariant:
        return SpecificationReceipt("OPEN",op,packet.object_id,packet.basis_id,reason="OBJECT_IDENTITY_PLURAL")
    if status not in {"IDENTIFIED","PLURAL"}:
        return SpecificationReceipt("OPEN",op,packet.object_id,packet.basis_id,reason="IDENTIFICATION_STATUS_REQUIRED")

    if not packet.required_coordinates:
        return SpecificationReceipt("OPEN",op,packet.object_id,packet.basis_id,reason="REQUIRED_COORDINATES_REQUIRED")

    conflicts=tuple(sorted(
        packet.required_coordinates
        & packet.resolved_coordinates
        & packet.open_coordinates
        - packet.invariant_coordinates
    ))
    if conflicts:
        return SpecificationReceipt(
            "CONFLICT",op,packet.object_id,packet.basis_id,
            conflicting_coordinates=conflicts,
            reason="REQUIRED_COORDINATE_BOTH_RESOLVED_AND_OPEN",
        )

    licensed_coordinates=packet.resolved_coordinates|packet.invariant_coordinates
    missing=tuple(sorted(packet.required_coordinates-licensed_coordinates))
    if missing:
        return SpecificationReceipt(
            "OPEN",op,packet.object_id,packet.basis_id,
            missing_coordinates=missing,
            reason="REQUIRED_COORDINATES_UNRECOVERED",
        )

    return SpecificationReceipt("PASS",op,packet.object_id,packet.basis_id)


def _selected_mapping(state:Mapping[str,Any])->Mapping[str,Any]|None:
    for key in ("selected_action","selected_job","selected_next_candidate"):
        value=state.get(key)
        if isinstance(value,Mapping):
            return value
    return None


def has_explicit_selection(state:Any)->bool:
    if not isinstance(state,Mapping):
        return False
    for key in (
        "selected_tools","selected_tool_ids","selected_tool","selected_tool_id",
        "selected_action","selected_job","selected_next_candidate",
    ):
        value=state.get(key)
        if value:
            return True
    return False


def selected_operation_class(state:Mapping[str,Any])->str:
    explicit=state.get("selected_operation_class")
    if explicit:
        return _norm(explicit)
    selected=_selected_mapping(state)
    if selected is not None:
        for key in ("operation_class","work_class"):
            value=selected.get(key)
            if value:
                return _norm(value)
    return ""


def selected_specification(state:Mapping[str,Any])->SpecificationPacket|None:
    selected=_selected_mapping(state)
    if selected is not None and isinstance(selected.get("object_specification"),Mapping):
        return packet_from_mapping(selected.get("object_specification"))
    return packet_from_mapping(state.get("object_specification"))


def assess_selected_state(state:Any)->SpecificationReceipt:
    if not isinstance(state,Mapping):
        return SpecificationReceipt("OPEN","UNSPECIFIED",None,None,reason="STATE_MAPPING_REQUIRED")
    if not has_explicit_selection(state):
        return SpecificationReceipt("PASS","NO_SELECTION",None,None,reason="NO_SELECTED_TRANSFORMATION")
    op=selected_operation_class(state)
    if not op:
        return SpecificationReceipt("OPEN","UNSPECIFIED",None,None,reason="SELECTED_OPERATION_CLASS_REQUIRED")
    return assess_transformation(selected_specification(state),op)


def progress_specification_licensed(target:str, status:str)->bool:
    """Strict-gain claims at transform-sensitive targets need a PASS receipt."""
    if _norm(target) not in TRANSFORM_SENSITIVE_TARGETS:
        return True
    return _norm(status)=="PASS"
