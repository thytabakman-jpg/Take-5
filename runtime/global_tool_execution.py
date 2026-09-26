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

from configured_run import (
    COGNITIVE_OPERATORS,
    DEFAULT_GEOMETRY,
    DEFAULT_MODE,
    QUESTION_FAMILIES,
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

    executed,execution_ev=execute_fn(dispatched,plan)
    evidence["execution"]=str(execution_ev or "")
    if not evidence["execution"]:
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
