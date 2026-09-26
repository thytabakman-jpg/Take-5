"""Mandatory configured-tool execution bridge for ImprovementCore.

The controller may select work generically, but a selected registered formal tool
cannot be satisfied by prose, a stage label, or an execution plan. It must cross
this bridge into a bound configured-tool adapter. Missing execution capability
preserves OPEN rather than silently falling back to host reasoning.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, Callable, Mapping

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


def _normalize_adapter_result(raw:Any,current:Any,tool_id:str,binding:ConfiguredToolBinding):
    if isinstance(raw,dict):
        status=str(raw.get("status","EXECUTED"))
        truth=str(raw.get("execution_truth","IMPLEMENTATION_EXECUTED"))
        result=raw.get("result",raw)
        next_state=raw.get("state",current)
        evidence=tuple(str(x) for x in raw.get("evidence",()) if str(x))
        material=bool(raw.get("material_delta",True))
    else:
        status="EXECUTED"
        truth="IMPLEMENTATION_EXECUTED"
        result=_plain(raw)
        next_state=current
        evidence=()
        material=True

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
            "binding":binding.summary,
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

        raw=adapter(current,binding.plan)
        current,execution=_normalize_adapter_result(
            raw,current,binding.tool_id,binding
        )
        executions.append(execution)

        if execution.status in NON_SUCCESS_STATUSES:
            return ConfiguredToolBatchResult(
                current,
                tuple(executions),
                execution.status,
                f"CONFIGURED_TOOL_{execution.status}:{binding.tool_id}",
            )

    return ConfiguredToolBatchResult(current,tuple(executions),"EXECUTED",None)
