"""Mandatory configured-tool execution bridge for ImprovementCore.

The controller may select work generically, but a selected registered formal tool
cannot be satisfied by prose, a stage label, or an execution plan. It must cross
this bridge into a bound configured-tool adapter. Missing execution capability
preserves OPEN rather than silently falling back to host reasoning.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, Callable, Mapping

from configured_hf2_execution import execute_configured_with_hf2
from formal_object_registry import canonical_formal_label
from global_tool_execution import ToolExecutionPlan, build_tool_execution_plan
from tool_run_registry import CONFIGURED_RUNS


SUCCESS_STATUSES={"EXECUTED","COMPLETE","CLOSED","CLOSED_RELATIVE","RELATIVE_CLOSE","FULL_MATCH"}
NON_SUCCESS_STATUSES={"OPEN","BLOCKED","CONFLICT"}


class ToolBridgeBlocked(RuntimeError):
    pass


@dataclass(frozen=True)
class ConfiguredToolBinding:
    tool_id:str
    plan:ToolExecutionPlan

    @property
    def summary(self)->dict[str,Any]:
        return {
            "tool_id":self.tool_id,
            "mode":self.plan.mode,
            "wrapper_required":self.plan.wrapper_required,
            "geometry":self.plan.geometry,
            "cell_count":len(self.plan.cells),
            "native_layers":tuple(dict.fromkeys(layer for layer,_ in self.plan.native)),
            "question_count":len(self.plan.questions),
            "cognitive_count":len(self.plan.cognitive),
            "recurrence_required":self.plan.recurrence_required,
            "recurrence_engine":self.plan.recurrence_engine,
            "invocation_profile":self.plan.invocation_profile,
            "configured_hf2_execution":"SHARED_GATE",
        }


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


@dataclass(frozen=True)
class ConfiguredToolBatchResult:
    state:Any
    executions:tuple[ConfiguredToolExecution,...]
    status:str
    blocker:str|None


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


def bind_selected_tools(state:Any)->tuple[Any,tuple[ConfiguredToolBinding,...]]:
    tool_ids=selected_tool_ids(state)
    if not tool_ids:
        return state,()

    bindings=tuple(
        ConfiguredToolBinding(tool_id,build_tool_execution_plan(CONFIGURED_RUNS[tool_id]))
        for tool_id in tool_ids
    )
    if isinstance(state,dict):
        state={
            **state,
            "configured_tool_bindings":tuple(binding.summary for binding in bindings),
            "configured_tool_binding_status":"BOUND",
        }
    return state,bindings


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
        material=bool(raw.get("material_delta",True))
        related_objects=tuple(str(x) for x in raw.get("related_objects",()) if str(x))
        dependency_footprint=tuple(str(x) for x in raw.get("dependency_footprint",()) if str(x))
        affected_objects=tuple(str(x) for x in raw.get("affected_objects",()) if str(x))
    else:
        status="EXECUTED"
        truth="IMPLEMENTATION_EXECUTED"
        result=_plain(raw)
        next_state=current
        evidence=()
        material=True
        related_objects=()
        dependency_footprint=()
        affected_objects=()

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
            "binding":binding.summary,
            "recurrence":None if recurrence is None else {
                "engine":recurrence.recurrence_engine,
                "status":recurrence.status,
                "rounds":recurrence.rounds,
                "call_count":recurrence.call_count,
                "trace":recurrence.trace,
            },
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
    )


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
        raw=dict(recurrence.last_raw)
        # Preserve whether any recurrence round made material progress.  The
        # terminal zero-delta witness proves closure; it does not erase the
        # material work performed earlier in the same configured execution.
        recurrence_material=any(
            bool((row.get("delta") or {}).get(key))
            for row in recurrence.trace
            for key in (
                "material_result_delta","material_search_delta",
                "material_discovery_delta","negative_evidence",
                "open_refinement","changed_representation",
                "material_relation_delta","goal_gap_reduced",
                "execution_truth_strengthened","resolved_open",
                "resolved_blocked","resolved_conflict",
            )
        )
        if recurrence_material:
            raw["material_delta"]=True
        current,execution=_normalize_adapter_result(
            raw,
            recurrence.state,
            binding.tool_id,
            binding,
            recurrence=recurrence,
        )
        executions.append(execution)

        if recurrence.status not in {"RELATIVE_CLOSE","SELF_CLOSE"}:
            mapped=recurrence.status if recurrence.status in NON_SUCCESS_STATUSES else "OPEN"
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
