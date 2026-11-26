"""Protected transition orchestration and the established execution-plan interface.

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
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from prose import ProseContract, ProseEvidence


# Preserve the established public planning imports for existing consumers.
from tool_execution_plan import (
    ToolExecutionBlocked, D36CCell, ToolExecutionPlan, d36c_cells,
    build_tool_execution_plan,
)


# Protected state-transition orchestration (consumes the shared plan).

@dataclass(frozen=True)
class ProtectedExecutionResult:
    value: object
    transition_receipt: ProtectedTransitionReceipt


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
    prose_contract: ProseContract | None=None,
    prose_text_fn=None,
    prose_evidence: ProseEvidence | None=None,
) -> ProtectedExecutionResult:
    """Execute one repository-governed configured transition end to end.

    Each callback returns (value, evidence_ref) except emission_audit_fn, which
    returns an evidence_ref after auditing the final user-visible projection.

    The chain is fail-closed: no successful configured execution result is
    returned until every PTI coordinate has a non-empty witness.
    """
    # Recurrence is a transition dependency, not a planning dependency.
    from configured_hf2_execution import execute_configured_with_hf2

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
            "trc_terminal":hints.get("trc_terminal",True) is True,
            "hf1_disposition":str(hints.get("hf1_disposition","STABLE")),
            "evidence":(str(execution_ev),),
        }
        if hints.get("hf2_delta") is not None:
            raw["hf2_delta"]=hints["hf2_delta"]
        if hints.get("hf1_targets") is not None:
            raw["hf1_targets"]=hints["hf1_targets"]
        # Preserve the configured HF2 affected-scope obligations across PTI.
        for key in ("hf2_affected_frontier", "hf2_scope_deltas"):
            if key in hints:
                raw[key]=hints[key]
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
    if not recurrence.closed:
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

    if prose_contract is not None:
        from prose import ProseAcceptanceError, require_prose_admissible

        if not callable(prose_text_fn):
            raise ToolExecutionBlocked("PROSE_TEXT_PROJECTION_REQUIRED")
        if prose_evidence is None:
            raise ToolExecutionBlocked("PROSE_EVIDENCE_REQUIRED")
        projected=prose_text_fn(reentered,plan)
        try:
            prose_assessment=require_prose_admissible(
                str(projected),prose_contract,prose_evidence
            )
        except ProseAcceptanceError as exc:
            raise ToolExecutionBlocked(str(exc)) from exc
        evidence["prose_acceptance"]=(
            f"{prose_assessment.contract_id}:{prose_assessment.status}:"
            +"|".join(prose_assessment.evidence)
        )

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
