"""Configured HF2 execution for ordinary Take-5 tool invocations.

This module is the shared execution primitive between controller-selected tools and
direct imperative tool commands.

It composes an already-bound full configured ToolExecutionPlan with HF002.  It
does not rebuild the plan, geometry, wrapper, PTI, or native tool semantics.

HF002 itself uses SELF recurrence because wrapping the recurrence engine in a
second HF002 instance would be a category error.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from hf002_recursive_continuation import HF002RecursiveContinuation


SUCCESS_STATUSES={
    "EXECUTED","COMPLETE","CLOSED","CLOSED_RELATIVE","RELATIVE_CLOSE","FULL_MATCH"
}
NON_SUCCESS_STATUSES={"OPEN","BLOCKED","CONFLICT"}
VALID_EXECUTION_TRUTH={
    "FULL_MATCH","IMPLEMENTATION_EXECUTED","SEMANTICALLY_APPLIED",
    "OPEN","BLOCKED","CONFLICT",
}


class ConfiguredHF2ExecutionError(RuntimeError):
    pass


@dataclass(frozen=True)
class ConfiguredHF2ExecutionResult:
    tool_id:str
    recurrence_engine:str
    status:str
    state:Any
    last_raw:dict[str,Any]
    rounds:int
    trace:tuple[dict[str,Any],...]
    call_count:int

    @property
    def closed(self)->bool:
        return self.status in {"RELATIVE_CLOSE","SELF_CLOSE"}


def _raw_mapping(raw:Any)->dict[str,Any]:
    if isinstance(raw,dict):
        out=dict(raw)
    else:
        out={
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":raw,
            "material_delta":False,
        }

    status=str(out.get("status","EXECUTED"))
    if status not in SUCCESS_STATUSES|NON_SUCCESS_STATUSES:
        raise ConfiguredHF2ExecutionError(
            f"CONFIGURED_HF2_STATUS_INVALID:{status}"
        )

    truth=str(out.get("execution_truth",""))
    if not truth:
        truth=status if status in NON_SUCCESS_STATUSES else "IMPLEMENTATION_EXECUTED"
        out["execution_truth"]=truth
    if truth not in VALID_EXECUTION_TRUTH:
        raise ConfiguredHF2ExecutionError(
            f"CONFIGURED_HF2_EXECUTION_TRUTH_INVALID:{truth}"
        )
    return out


def _delta_from_raw(tool_id:str,raw:dict[str,Any])->dict[str,Any]:
    supplied=raw.get("hf2_delta",{})
    delta=dict(supplied) if isinstance(supplied,dict) else {}
    if not any(
        delta.get(k)
        for k in (
            "material_result_delta",
            "material_search_delta",
            "material_discovery_delta",
            "negative_evidence",
            "open_refinement",
            "changed_representation",
        )
    ):
        delta["material_result_delta"]=bool(raw.get("material_delta",False))

    delta.setdefault(
        "route_equivalence",
        str(raw.get("route_equivalence") or f"{tool_id}:configured-hf2")
    )
    if raw.get("invalidating_evidence"):
        delta["invalidating_evidence"]=True
    if raw.get("certified_no_gain"):
        delta["certified_no_gain"]=True
    return delta


def execute_configured_with_hf2(
    *,
    tool_id:str,
    plan,
    state:Any,
    adapter:Callable[[Any,Any],Any],
    max_rounds:int=32,
)->ConfiguredHF2ExecutionResult:
    """Execute one bound configured tool under the canonical recurrence policy.

    Ordinary tools are wrapped by HF002.

    HF002 itself is executed directly and receives a SELF recurrence receipt.
    """

    if not callable(adapter):
        raise ConfiguredHF2ExecutionError(
            f"CONFIGURED_HF2_ADAPTER_REQUIRED:{tool_id}"
        )

    if not bool(getattr(plan,"complete",False)):
        raise ConfiguredHF2ExecutionError(
            f"CONFIGURED_HF2_PLAN_INCOMPLETE:{tool_id}"
        )

    if not bool(getattr(plan,"recurrence_required",False)):
        raise ConfiguredHF2ExecutionError(
            f"CONFIGURED_HF2_RECURRENCE_NOT_REQUIRED:{tool_id}"
        )

    recurrence_engine=str(getattr(plan,"recurrence_engine",""))
    if recurrence_engine=="SELF":
        if str(tool_id)!="HF002":
            raise ConfiguredHF2ExecutionError(
                f"CONFIGURED_HF2_SELF_RECURRENCE_INVALID:{tool_id}"
            )
        raw=_raw_mapping(adapter(state,plan))
        next_state=raw.get("state",state)
        status=str(raw.get("status","EXECUTED"))
        if status in NON_SUCCESS_STATUSES:
            return ConfiguredHF2ExecutionResult(
                str(tool_id),recurrence_engine,status,next_state,raw,1,(),1
            )
        return ConfiguredHF2ExecutionResult(
            str(tool_id),recurrence_engine,"SELF_CLOSE",next_state,raw,1,(),1
        )

    if recurrence_engine!="HF002":
        raise ConfiguredHF2ExecutionError(
            f"CONFIGURED_HF2_ENGINE_INVALID:{tool_id}:{recurrence_engine}"
        )

    holder={"raw":None,"calls":0}

    def run_capability(current,memory):
        raw=_raw_mapping(adapter(current,plan))
        holder["raw"]=raw
        holder["calls"]+=1
        return raw

    def admit_normalize(raw,current,memory):
        normalized=raw.get("state",current)
        return normalized,_delta_from_raw(str(tool_id),raw)

    def trc_verify(before,after,delta):
        raw=holder["raw"] or {}
        return {
            "terminal":bool(raw.get("trc_terminal",True)),
            "evidence":tuple(raw.get("trc_evidence",())),
        }

    def hf1_classify(before,after,delta):
        raw=holder["raw"] or {}
        disposition=str(raw.get("hf1_disposition","STABLE"))
        out={"disposition":disposition}
        if raw.get("hf1_targets"):
            out["targets"]=tuple(raw.get("hf1_targets",()))
        return out

    def live_local(current,memory):
        raw=holder["raw"] or {}
        return bool(raw.get("hf2_live_local",False))

    def local_close(current,memory):
        raw=holder["raw"] or {}
        status=str(raw.get("status","EXECUTED"))
        if status not in SUCCESS_STATUSES:
            return False
        if "hf2_local_close" in raw:
            return bool(raw["hf2_local_close"])
        return not bool(raw.get("hf2_live_local",False))

    engine=HF002RecursiveContinuation(
        run_capability=run_capability,
        admit_normalize=admit_normalize,
        trc_verify=trc_verify,
        hf1_classify=hf1_classify,
        live_local=live_local,
        local_close=local_close,
        max_rounds=max_rounds,
    )
    out=engine.run(state,{})
    raw=dict(holder["raw"] or {})
    status=str(out.get("status","OPEN"))

    return ConfiguredHF2ExecutionResult(
        tool_id=str(tool_id),
        recurrence_engine=recurrence_engine,
        status=status,
        state=out.get("state",state),
        last_raw=raw,
        rounds=len(out.get("trace",())),
        trace=tuple(out.get("trace",())),
        call_count=int(holder["calls"]),
    )
