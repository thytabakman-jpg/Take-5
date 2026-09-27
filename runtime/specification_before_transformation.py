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

EXECUTION_EFFECT_CLASSES=frozenset({
    "EVIDENCE_ONLY",
    "TARGET_TRANSFORM",
})

# These configured tools are intrinsically epistemic/recovery operations in their
# admitted current identity.  Inferring a recovery class for them is safe because
# the inference cannot license an object mutation.  Every other configured tool
# remains fail-closed unless the selected work declares its operation class.
SAFE_RECOVERY_TOOL_OPERATION_CLASS={
    "CurrentnessAudit":"AUDIT",
    "RootCause":"DIAGNOSE",
    "QuestionWorthAsking":"DISCOVER",
    "ASSERT":"VERIFY",
    "PD":"COMPARE",
    "PDAudit":"VERIFY",
    "MTA":"RECONSTRUCT",
    "Diagnosis":"DIAGNOSE",
    "HistoricalReconstruction":"RECONSTRUCT",
    "ZeroRequest":"OBSERVE",
    "GOAL":"FORMALIZE",
    "TRC":"VERIFY",
    "MultiObject":"COMPARE",
}


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


@dataclass(frozen=True)
class ExecutionAdmissionReceipt:
    status:str
    operation_class:str
    effect_class:str
    specification_status:str
    object_id:str|None=None
    basis_id:str|None=None
    reason:str|None=None

    @property
    def licensed(self)->bool:
        return self.status=="PASS"

    @property
    def blocker(self)->str|None:
        if self.licensed:
            return None
        suffix=f":{self.reason}" if self.reason else ""
        return f"EXECUTION_ADMISSION_{self.status}{suffix}"


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


def _selected_tool_names(state:Mapping[str,Any])->tuple[str,...]:
    out=[]
    for key in ("selected_tools","selected_tool_ids"):
        value=state.get(key)
        if isinstance(value,(list,tuple)):
            out.extend(str(x) for x in value if str(x))
        elif value:
            out.append(str(value))
    for key in ("selected_tool","selected_tool_id"):
        value=state.get(key)
        if value:
            out.append(str(value))
    return tuple(dict.fromkeys(out))


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

    tool_names=_selected_tool_names(state)
    if tool_names:
        inferred=tuple(
            SAFE_RECOVERY_TOOL_OPERATION_CLASS.get(name)
            for name in tool_names
        )
        if all(inferred):
            # Multiple selected epistemic tools can differ internally while the
            # batch as a whole remains a recovery-class operation.
            return "RECOVER"
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


def _work_item_state(item:Mapping[str,Any])->dict[str,Any]:
    state={"selected_action":dict(item)}
    tool_id=item.get("tool_id")
    if tool_id:
        state["selected_tool"]=str(tool_id)
    return state


def _effect_class(item:Mapping[str,Any], *, configured_observer:bool)->str:
    for key in ("execution_effect_class","effect_class","execution_effect"):
        value=item.get(key)
        if value:
            return _norm(value)
    if configured_observer:
        return "EVIDENCE_ONLY"
    return ""


def assess_executable_work_item(
    item:Mapping[str,Any],
    *,
    configured_observer:bool=False,
)->ExecutionAdmissionReceipt:
    """License a work callback before it can execute.

    The operation class answers what semantic job is being attempted.
    The effect class answers whether the callback itself can change target
    reality before admission.

    Repository configured-tool execution is observer-only, so callers may set
    configured_observer=True to infer EVIDENCE_ONLY. Generic/higher-order
    callbacks must declare their effect class explicitly.
    """
    if not isinstance(item,Mapping):
        return ExecutionAdmissionReceipt(
            "OPEN","UNSPECIFIED","UNSPECIFIED","OPEN",
            reason="WORK_ITEM_MAPPING_REQUIRED",
        )

    spec=assess_selected_state(_work_item_state(item))
    if not spec.licensed:
        return ExecutionAdmissionReceipt(
            spec.status,
            spec.operation_class,
            _effect_class(item,configured_observer=configured_observer) or "UNSPECIFIED",
            spec.status,
            spec.object_id,
            spec.basis_id,
            spec.reason,
        )

    effect=_effect_class(item,configured_observer=configured_observer)
    if not effect:
        return ExecutionAdmissionReceipt(
            "OPEN",spec.operation_class,"UNSPECIFIED",spec.status,
            spec.object_id,spec.basis_id,"EFFECT_CLASS_REQUIRED",
        )
    if effect not in EXECUTION_EFFECT_CLASSES:
        return ExecutionAdmissionReceipt(
            "OPEN",spec.operation_class,effect,spec.status,
            spec.object_id,spec.basis_id,"EFFECT_CLASS_INVALID",
        )
    if effect=="TARGET_TRANSFORM" and spec.operation_class not in TRANSFORMATION_OPERATION_CLASSES:
        return ExecutionAdmissionReceipt(
            "OPEN",spec.operation_class,effect,spec.status,
            spec.object_id,spec.basis_id,"TARGET_TRANSFORM_OPERATION_REQUIRED",
        )

    return ExecutionAdmissionReceipt(
        "PASS",spec.operation_class,effect,spec.status,
        spec.object_id,spec.basis_id,
        "CONFIGURED_OBSERVER_INFERENCE" if configured_observer and not any(
            item.get(k) for k in ("execution_effect_class","effect_class","execution_effect")
        ) else None,
    )


def progress_specification_licensed(
    target:str,
    status:str,
    *,
    transformation_claim:bool=False,
)->bool:
    """Only object-transforming strict-gain claims consume this gate.

    Ordinary controller progress can be causal and material without being a claim
    that a formal device itself was transformed.  The gate becomes mandatory when
    that stronger transformation claim is present.
    """
    if not transformation_claim:
        return True
    if _norm(target) not in TRANSFORM_SENSITIVE_TARGETS:
        return True
    return _norm(status)=="PASS"
