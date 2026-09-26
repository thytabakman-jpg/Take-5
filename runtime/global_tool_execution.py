"""Non-bypassable global execution profile for registered tools.

Every configured analytical tool inherits:
- canonical wrapper required;
- OBSERVER as the only ordinary tool-run mode;
- typed D36_C geometry;
- its declared native layer(s) across all 36 cells;
- Q01-Q22 across all 36 cells;
- DIFFERENTIATE/RELATE/RECONSTRUCT/STRENGTHEN across all 36 cells.

State mutation is not a tool-run mode. It belongs to a separate admitted
transition/commit path.
"""
from __future__ import annotations

from dataclasses import dataclass

from configured_hf2_execution import execute_configured_with_hf2
from configured_run import (
    COGNITIVE_OPERATORS,
    DEFAULT_GEOMETRY,
    DEFAULT_MODE,
    QUESTION_FAMILIES,
    FULL_INVOCATION_PROFILE,
    ConfiguredRunSpec,
)
from run_geometry import ModeFace
from scope_ontology import Scope
from protected_transition_integrity import (
    COORDINATES,
    PTIState,
    ProtectedTransitionReceipt,
    require_protected_transition,
)


class ToolExecutionBlocked(RuntimeError):
    pass


@dataclass(frozen=True)
class ProtectedExecutionResult:
    value: object
    transition_receipt: ProtectedTransitionReceipt


@dataclass(frozen=True)
class D36CCell:
    scope: Scope
    mode_face: ModeFace


@dataclass(frozen=True)
class ToolExecutionPlan:
    tool_id: str
    mode: str
    wrapper_required: bool
    geometry: str
    recurrence_required: bool
    recurrence_engine: str
    invocation_profile: str
    cells: tuple[D36CCell, ...]
    native: tuple[tuple[str, D36CCell], ...]
    questions: tuple[tuple[str, D36CCell], ...]
    cognitive: tuple[tuple[str, D36CCell], ...]

    @property
    def complete(self) -> bool:
        return (
            self.mode == DEFAULT_MODE
            and self.wrapper_required
            and self.geometry == DEFAULT_GEOMETRY
            and self.recurrence_required
            and self.recurrence_engine in {"HF002","SELF"}
            and self.invocation_profile == FULL_INVOCATION_PROFILE
            and len(self.cells) == 36
            and bool(self.native)
            and len(self.questions) == len(QUESTION_FAMILIES) * 36
            and len(self.cognitive) == len(COGNITIVE_OPERATORS) * 36
        )


def d36c_cells() -> tuple[D36CCell, ...]:
    cells=tuple(D36CCell(scope,face) for scope in Scope for face in ModeFace)
    if len(cells)!=36:
        raise ToolExecutionBlocked("D36_C_NOT_36")
    return cells


def build_tool_execution_plan(spec: ConfiguredRunSpec, *, requested_mode: str | None=None) -> ToolExecutionPlan:
    if not spec.complete():
        raise ToolExecutionBlocked(f"INCOMPLETE_CONFIGURED_RUN:{spec.tool_id}")

    mode=requested_mode or spec.default_mode
    if mode != "OBSERVER":
        raise ToolExecutionBlocked(f"NON_OBSERVER_TOOL_RUN_FORBIDDEN:{spec.tool_id}")

    cells=d36c_cells()
    plan=ToolExecutionPlan(
        tool_id=spec.tool_id,
        mode=mode,
        wrapper_required=spec.wrapper_required,
        geometry=spec.geometry,
        recurrence_required=spec.recurrence_required,
        recurrence_engine=spec.recurrence_engine,
        invocation_profile=spec.invocation_profile,
        cells=cells,
        native=tuple((layer,cell) for layer in spec.required_layers for cell in cells),
        questions=tuple((question,cell) for question in spec.question_families for cell in cells),
        cognitive=tuple((op,cell) for op in spec.required_cognitive_ops for cell in cells),
    )
    if not plan.complete:
        raise ToolExecutionBlocked(f"GLOBAL_TOOL_EXECUTION_INCOMPLETE:{spec.tool_id}")
    return plan



def execute_protected_transition(
    spec: ConfiguredRunSpec,
    *,
    behavior_id: str,
    dispatch_fn,
    execute_fn,
    consume_fn,
    update_fn,
    reentry_fn,
    emission_audit_fn,
    requested_mode: str | None=None,
) -> ProtectedExecutionResult:
    """Execute one repository-governed configured transition end to end.

    Each callback returns (value, evidence_ref) except emission_audit_fn, which
    returns an evidence_ref after auditing the final user-visible projection.

    The chain is fail-closed: no successful configured execution result is
    returned until every PTI coordinate has a non-empty witness.
    """
    plan=build_tool_execution_plan(spec,requested_mode=requested_mode)
    evidence={
        "canonical_identity":f"configured_run:{spec.tool_id}",
    }

    dispatched,dispatch_ev=dispatch_fn(plan)
    evidence["configured_dispatch"]=str(dispatch_ev or "")
    if not evidence["configured_dispatch"]:
        raise ToolExecutionBlocked("PTI_DISPATCH_WITNESS_MISSING")

    execution_refs=[]

    def protected_adapter(current, current_plan):
        payload=current.get("payload") if isinstance(current,dict) else current
        ret=execute_fn(payload,current_plan)

        if not isinstance(ret,tuple) or len(ret) not in {2,3}:
            raise ToolExecutionBlocked(
                "PTI_EXECUTE_FN_MUST_RETURN_VALUE_EVIDENCE_OR_VALUE_EVIDENCE_HINTS"
            )

        executed_value,execution_ev=ret[0],ret[1]
        hints=ret[2] if len(ret)==3 else {}
        if not str(execution_ev or ""):
            raise ToolExecutionBlocked("PTI_EXECUTION_WITNESS_MISSING")
        if hints is None:
            hints={}
        if not isinstance(hints,dict):
            raise ToolExecutionBlocked("PTI_HF2_HINTS_REQUIRE_MAPPING")

        execution_refs.append(str(execution_ev))
        next_payload=hints.get("next_payload",payload)

        raw={
            "status":str(hints.get("status","EXECUTED")),
            "execution_truth":str(
                hints.get("execution_truth","IMPLEMENTATION_EXECUTED")
            ),
            "state":{"payload":next_payload},
            "result":executed_value,
            "material_delta":bool(hints.get("material_delta",False)),
            "hf2_live_local":bool(hints.get("hf2_live_local",False)),
            "hf2_local_close":bool(
                hints.get(
                    "hf2_local_close",
                    not bool(hints.get("hf2_live_local",False)),
                )
            ),
            "trc_terminal":bool(hints.get("trc_terminal",True)),
            "hf1_disposition":str(hints.get("hf1_disposition","STABLE")),
            "evidence":(str(execution_ev),),
        }
        if hints.get("hf2_delta") is not None:
            raw["hf2_delta"]=hints["hf2_delta"]
        if hints.get("hf1_targets") is not None:
            raw["hf1_targets"]=hints["hf1_targets"]
        if hints.get("invalidating_evidence"):
            raw["invalidating_evidence"]=True
        if hints.get("certified_no_gain"):
            raw["certified_no_gain"]=True
        return raw

    recurrence=execute_configured_with_hf2(
        tool_id=spec.tool_id,
        plan=plan,
        state={"payload":dispatched},
        adapter=protected_adapter,
    )
    if recurrence.status not in {"RELATIVE_CLOSE","SELF_CLOSE"}:
        raise ToolExecutionBlocked(
            f"PTI_HF2_RECURRENCE_NOT_CLOSED:{spec.tool_id}:{recurrence.status}"
        )

    executed=recurrence.last_raw.get("result")
    evidence["execution"]=(
        f"configured-recurrence:{recurrence.recurrence_engine}:"
        f"{recurrence.status}:rounds={recurrence.rounds};"
        +"|".join(execution_refs)
    )
    if not execution_refs:
        raise ToolExecutionBlocked("PTI_EXECUTION_WITNESS_MISSING")

    consumed,consume_ev=consume_fn(executed,plan)
    evidence["result_consumption"]=str(consume_ev or "")
    if not evidence["result_consumption"]:
        raise ToolExecutionBlocked("PTI_CONSUMPTION_WITNESS_MISSING")

    updated,update_ev=update_fn(consumed,plan)
    evidence["state_update"]=str(update_ev or "")
    if not evidence["state_update"]:
        raise ToolExecutionBlocked("PTI_STATE_UPDATE_WITNESS_MISSING")

    reentered,reentry_ev=reentry_fn(updated,plan)
    evidence["reentry"]=str(reentry_ev or "")
    if not evidence["reentry"]:
        raise ToolExecutionBlocked("PTI_REENTRY_WITNESS_MISSING")

    emission_ev=emission_audit_fn(reentered,plan)
    evidence["user_visible_boundary"]=str(emission_ev or "")
    if not evidence["user_visible_boundary"]:
        raise ToolExecutionBlocked("PTI_EMISSION_WITNESS_MISSING")

    receipt=ProtectedTransitionReceipt(
        object_id=spec.tool_id,
        behavior_id=behavior_id,
        coordinates={x:PTIState.VERIFIED for x in COORDINATES},
        evidence=evidence,
    )
    require_protected_transition(receipt)
    return ProtectedExecutionResult(reentered,receipt)
