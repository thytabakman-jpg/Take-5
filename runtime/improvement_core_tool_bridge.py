"""Shared configured-tool execution bridge.

Owns the execution of already-bound, ordered tool batches and the projection
of their results into caller-visible receipts and state. Direct commands and
ImprovementCore use the same execution boundary. Missing execution capability
preserves OPEN rather than substituting host reasoning.

The historical module path and selection-state interface remain supported for
compatibility. This bridge does not select work, interpret natural-language
authorization, construct execution plans, or own native HF2 recurrence.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, Callable, Mapping

from configured_hf2_execution import (
    NON_SUCCESS_STATUSES, SUCCESS_STATUSES, execute_configured_with_hf2,
    project_recurrence_result,
)
from formal_object_registry import canonical_formal_label
from tool_execution_plan import (
    ToolExecutionPlan, build_tool_execution_plan, ConfiguredToolBinding,
    bind_registered_ids as _bind_registered_ids,
)
from tool_run_registry import CONFIGURED_RUNS


# I. Shared configured-execution contracts.
# ConfiguredToolBinding is owned by tool_execution_plan.py and re-exported
# here for compatibility. Ordered batch contracts remain local.
class ToolBridgeBlocked(RuntimeError):
    pass


@dataclass(frozen=True)
class ConfiguredToolExecution:
    tool_id:str
    status:str
    execution_truth:str
    result:Any
    evidence:tuple[str,...]
    material_delta:bool
    binding:dict[str,Any]
    recurrence_engine:str=""
    recurrence_status:str=""
    recurrence_rounds:int=0
    adapter_blocker:Any=None
    adapter_provenance:dict[str,Any]|None=None


@dataclass(frozen=True)
class ConfiguredToolBatchResult:
    state:Any
    executions:tuple[ConfiguredToolExecution,...]
    status:str
    blocker:str|None


# II. Shared adapter result and receipt normalization.
# Recurrence projection is owned by configured_hf2_execution.py.
# Controller output history and caller-specific receipt adaptation remain here.
def _plain(value:Any)->Any:
    if is_dataclass(value):
        return asdict(value)
    return value


def _normalize_adapter_result(
    raw:Any,
    current:Any,
    tool_id:str,
    binding:ConfiguredToolBinding,
    *,
    recurrence=None,
):
    if isinstance(raw,dict):
        status=str(raw.get("status","EXECUTED"))
        truth=str(raw.get("execution_truth","IMPLEMENTATION_EXECUTED"))
        result=raw.get("result",raw)
        next_state=raw.get("state",current)
        evidence=tuple(str(x) for x in raw.get("evidence",()) if str(x))
        material=bool(raw.get("material_delta",False))
        related_objects=tuple(str(x) for x in raw.get("related_objects",()) if str(x))
        dependency_footprint=tuple(str(x) for x in raw.get("dependency_footprint",()) if str(x))
        affected_objects=tuple(str(x) for x in raw.get("affected_objects",()) if str(x))
        # Preserve the supplied diagnostic and provenance without upgrading
        # their execution-truth status or replacing the stable batch blocker.
        adapter_blocker=raw.get("blocker")
        adapter_provenance={
            key:raw[key] for key in (
                "provenance","adapter_provenance","adapter_id","adapter_identity",
                "provider","provider_identity","scope",
            ) if key in raw
        } or None
    else:
        status="EXECUTED"
        truth="IMPLEMENTATION_EXECUTED"
        result=_plain(raw)
        next_state=current
        evidence=()
        material=False
        related_objects=()
        dependency_footprint=()
        affected_objects=()
        adapter_blocker=None
        adapter_provenance=None

    status,truth,next_state,material,adapter_provenance=project_recurrence_result(
        recurrence,status,truth,next_state,material,adapter_provenance)

    if status not in SUCCESS_STATUSES|NON_SUCCESS_STATUSES:
        raise ToolBridgeBlocked(f"CONFIGURED_TOOL_STATUS_INVALID:{tool_id}:{status}")
    if not truth:
        raise ToolBridgeBlocked(f"CONFIGURED_TOOL_EXECUTION_TRUTH_MISSING:{tool_id}")

    if isinstance(next_state,dict):
        prior=tuple(next_state.get("configured_tool_outputs",()))
        output={
            "tool_id":tool_id,
            "status":status,
            "execution_truth":truth,
            "result":_plain(result),
            "evidence":evidence,
            "material_delta":material,
            "related_objects":related_objects,
            "dependency_footprint":dependency_footprint,
            "affected_objects":affected_objects,
            "adapter_blocker":adapter_blocker,
            "adapter_provenance":adapter_provenance,
            "binding":binding.summary,
            "recurrence":None if recurrence is None else recurrence.receipt_payload(),
        }
        next_state={**next_state,"configured_tool_outputs":prior+(output,)}

    return next_state,ConfiguredToolExecution(
        tool_id=tool_id,
        status=status,
        execution_truth=truth,
        result=_plain(result),
        evidence=evidence,
        material_delta=material,
        binding=binding.summary,
        recurrence_engine="" if recurrence is None else recurrence.recurrence_engine,
        recurrence_status="" if recurrence is None else recurrence.status,
        recurrence_rounds=0 if recurrence is None else recurrence.rounds,
        adapter_blocker=adapter_blocker,
        adapter_provenance=adapter_provenance,
    )


# III. Shared ordered batch execution.
# The current batch is fail-fast and state-dependent; independent calls are
# isolated by execute_tool_packet.py. Do not change this policy implicitly.
def execute_bound_tools(
    state:Any,
    bindings:tuple[ConfiguredToolBinding,...],
    adapters:Mapping[str,Callable[[Any,ToolExecutionPlan],Any]]|None,
)->ConfiguredToolBatchResult:
    if not bindings:
        return ConfiguredToolBatchResult(state,(),"NO_TOOL_SELECTED",None)

    adapters=dict(adapters or {})
    current=state
    executions=[]

    for binding in bindings:
        adapter=adapters.get(binding.tool_id)
        if adapter is None:
            return ConfiguredToolBatchResult(
                current,
                tuple(executions),
                "OPEN",
                f"CONFIGURED_TOOL_ADAPTER_REQUIRED:{binding.tool_id}",
            )

        recurrence=execute_configured_with_hf2(
            tool_id=binding.tool_id,
            plan=binding.plan,
            state=current,
            adapter=adapter,
        )
        raw=recurrence.last_raw
        current,execution=_normalize_adapter_result(
            raw,
            recurrence.state,
            binding.tool_id,
            binding,
            recurrence=recurrence,
        )
        executions.append(execution)

        if not recurrence.closed:
            mapped=recurrence.configured_disposition
            return ConfiguredToolBatchResult(
                current,
                tuple(executions),
                mapped,
                f"CONFIGURED_TOOL_HF2_{recurrence.status}:{binding.tool_id}",
            )

        if execution.status in NON_SUCCESS_STATUSES:
            return ConfiguredToolBatchResult(
                current,
                tuple(executions),
                execution.status,
                f"CONFIGURED_TOOL_{execution.status}:{binding.tool_id}",
            )

    return ConfiguredToolBatchResult(current,tuple(executions),"EXECUTED",None)


# IV. Independent read-only batch execution; no controller selection or state promotion.
def execute_independent_read_only_tools(
    state:dict,
    bindings:tuple[ConfiguredToolBinding,...],
    adapters:Mapping[str,Callable[[Any,ToolExecutionPlan],Any]]|None,
)->ConfiguredToolBatchResult:
    """Execute explicitly independent read-only work on isolated snapshots.

    No successor or material delta is admitted into the shared controller state.
    Adapters remain trusted to honor the read-only contract; copying is not a
    sandbox for external side effects. All dispositions survive independently.
    """
    if not bindings:
        return ConfiguredToolBatchResult(state,(),"NO_TOOL_SELECTED",None)
    if not isinstance(state,dict):
        raise ToolBridgeBlocked("INDEPENDENT_READ_ONLY_STATE_REQUIRED")
    records=[]
    executions=[]
    outputs=list(state.get("configured_tool_outputs",()))
    priority={"EXECUTED":0,"OPEN":1,"BLOCKED":2,"CONFLICT":3}
    status="EXECUTED"
    for binding in bindings:
        isolated=deepcopy(state)
        isolated["configured_tool_outputs"]=()
        batch=execute_bound_tools(isolated,(binding,),adapters)
        disposition=batch.status
        blocker=batch.blocker
        if any(execution.material_delta for execution in batch.executions):
            if priority[disposition]<priority["OPEN"]:
                disposition="OPEN"
            blocker=blocker or "INDEPENDENT_READ_ONLY_MATERIAL_DELTA:"+binding.tool_id
        records.append({"tool_id":binding.tool_id,"status":disposition,"blocker":blocker})
        executions.extend(batch.executions)
        if isinstance(batch.state,dict):
            outputs.extend(batch.state.get("configured_tool_outputs",()))
        if priority[disposition]>priority[status]:
            status=disposition
    result={**state,"configured_tool_outputs":tuple(outputs),
            "configured_independent_tool_batches":tuple(records)}
    blockers=tuple(x["blocker"] for x in records if x["blocker"])
    return ConfiguredToolBatchResult(result,tuple(executions),status,
                                     ";".join(blockers) or None)


# V. Legacy controller compatibility: selection-state interpretation.
# This is an adapter for callers using the historical selection-state schema,
# not a requirement of shared batch execution. Explicitly bound batches bypass it.
# Exact identity normalization remains delegated to formal_object_registry.
def _canonical_registered(value:Any)->str:
    raw=str(value).strip()
    if not raw:
        raise ToolBridgeBlocked("CONFIGURED_TOOL_EMPTY_ID")
    try:
        tool_id=canonical_formal_label(raw)
    except KeyError as exc:
        raise ToolBridgeBlocked(f"CONFIGURED_TOOL_NOT_REGISTERED:{raw}") from exc
    if tool_id not in CONFIGURED_RUNS:
        raise ToolBridgeBlocked(f"CONFIGURED_TOOL_NOT_REGISTERED:{tool_id}")
    return tool_id


def _tool_from_mapping(value:Mapping[str,Any])->str|None:
    for key in ("tool_id","formal_tool","tool"):
        raw=value.get(key)
        if raw:
            return _canonical_registered(raw)
    return None


def selected_tool_ids(state:Any)->tuple[str,...]:
    """Return explicit configured-tool selections in controller order.

    Formal-tool selection is intentionally explicit. Candidate IDs and ordinary
    strings are not guessed into tools because that would turn tool salience into
    accidental authority.
    """
    if not isinstance(state,dict):
        return ()

    raw_items=[]
    for key in ("selected_tools","selected_tool_ids"):
        value=state.get(key)
        if value:
            if isinstance(value,(list,tuple)):
                raw_items.extend(value)
            else:
                raw_items.append(value)

    for key in ("selected_tool","selected_tool_id"):
        value=state.get(key)
        if value:
            raw_items.append(value)

    for key in ("selected_action","selected_job","selected_next_candidate"):
        value=state.get(key)
        if isinstance(value,Mapping):
            mapped=_tool_from_mapping(value)
            if mapped:
                raw_items.append(mapped)

    out=[]
    for item in raw_items:
        if isinstance(item,Mapping):
            tool_id=_tool_from_mapping(item)
            if tool_id is None:
                continue
        else:
            tool_id=_canonical_registered(item)
        if tool_id not in out:
            out.append(tool_id)
    return tuple(out)


# VI. Legacy controller compatibility: selection-to-binding state projection.
# Exact registered-ID binding is owned by tool_execution_plan.py.
# The compatibility layer translates caller state only; it does not own execution.
def bind_selected_tools(state:Any)->tuple[Any,tuple[ConfiguredToolBinding,...]]:
    tool_ids=selected_tool_ids(state)
    if not tool_ids:
        return state,()

    bindings=_bind_registered_ids(tool_ids)
    if isinstance(state,dict):
        state={
            **state,
            "configured_tool_bindings":tuple(binding.summary for binding in bindings),
            "configured_tool_binding_status":"BOUND",
        }
    return state,bindings
