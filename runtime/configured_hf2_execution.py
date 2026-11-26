"""Configured HF2 execution for ordinary Take-5 tool invocations.

This module is the shared execution primitive between controller-selected tools and
direct imperative tool commands.

It composes an already-bound full configured ToolExecutionPlan with HF002.  It
does not rebuild the plan, geometry, wrapper, PTI, or native tool semantics.

HF002 itself uses SELF recurrence because wrapping the recurrence engine in a
second HF002 instance would be a category error.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, is_dataclass
from copy import deepcopy
import json
from typing import Any, Callable, Mapping

from hf002_recursive_continuation import (
    HF002RecursiveContinuation, material_delta_present, affected_scope_open,
    TERMINAL, hf2_fixed_point_witness,
)


# I. Configured result vocabulary and recurrence receipts.
# Candidate receiving boundary: recurrence truth and admitted-state projection
# belong here; controller selection and host provenance do not.
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

    @property
    def configured_disposition(self)->str:
        """Project recurrence and native status to the configured caller disposition."""
        if not self.closed:
            return self.status if self.status in NON_SUCCESS_STATUSES else "OPEN"
        raw_status=str(self.last_raw.get("status","EXECUTED"))
        return raw_status if raw_status in NON_SUCCESS_STATUSES else "EXECUTED"

    @property
    def admitted_material_delta(self)->bool:
        """Retain admitted material changes across rounds, including earlier rounds."""
        if not self.trace:
            return self.closed and self.last_raw.get("material_delta",False) is True
        return any(material_delta_present(row["delta"]) for row in self.trace
                   if row["disposition"] in {"REAPPLY_C","RELATIVE_CLOSE","RETURN_REENTER"})

    def receipt_payload(self)->dict[str,Any]:
        """Shared recurrence receipt representation for configured consumers."""
        return {
            "engine":self.recurrence_engine,
            "status":self.status,
            "rounds":self.rounds,
            "call_count":self.call_count,
            "trace":self.trace,
        }


# II. Native adapter return admission and evidence validation.
def _raw_mapping(raw:Any)->dict[str,Any]:
    # A missing adapter result is not an executed formal tool. Keep the
    # configured route OPEN rather than manufacturing successful execution.
    if raw is None:
        return {
            "status":"OPEN",
            "execution_truth":"OPEN",
            "result":None,
            "material_delta":False,
            "blocker":"CONFIGURED_HF2_ADAPTER_NO_RESULT",
        }
    if isinstance(raw,dict):
        if not raw:
            return {
                "status":"OPEN", "execution_truth":"OPEN", "result":None,
                "material_delta":False, "blocker":"CONFIGURED_HF2_ADAPTER_EMPTY_RESULT",
            }
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
    # Status and execution truth are independent inputs; their disagreement
    # cannot turn a BLOCKED/OPEN/CONFLICT tool into a closed HF2 episode.
    if status in SUCCESS_STATUSES and truth in NON_SUCCESS_STATUSES:
        out["status"]=truth
        out["material_delta"]=False
        out["blocker"]=out.get("blocker") or "CONFIGURED_HF2_SUCCESS_WITH_NON_SUCCESS_TRUTH"
        status=truth
    elif status in NON_SUCCESS_STATUSES and truth not in NON_SUCCESS_STATUSES:
        out["execution_truth"]=status
        truth=status
    elif status in NON_SUCCESS_STATUSES and truth in NON_SUCCESS_STATUSES and status!=truth:
        # Preserve both original dispositions as evidence of a contradictory receipt.
        out.update(status="CONFLICT",execution_truth="CONFLICT",material_delta=False,
                   reported_status=status,reported_execution_truth=truth,
                   blocker=out.get("blocker") or "CONFIGURED_HF2_DISPOSITION_CONFLICT")
        status=truth="CONFLICT"
    # Control flags are typed evidence, not arbitrary truthy values. Reject
    # malformed flags before the recurrence engine can admit a successor.
    for key in ("material_delta","hf2_live_local","hf2_local_close","trc_terminal"):
        if key in out and type(out[key]) is not bool:
            disposition=status if status in NON_SUCCESS_STATUSES else "OPEN"
            out.update(status=disposition,execution_truth=disposition,material_delta=False,
                       blocker=f"CONFIGURED_HF2_INVALID_BOOLEAN:{key}")
            return out
    # A success status is a result claim, not proof supplied by the execution plan.
    # Reject wholly empty success receipts, while preserving valid tool-native
    # results and the existing evidence/coverage representations.
    # Explicit, valid scalar results such as False and 0 are real tool outputs,
    # not missing execution receipts. Empty collections or None are not proof.
    def has_witness(value:Any)->bool:
        if value is None:
            return False
        if isinstance(value,(Mapping,list,tuple,set,frozenset,str,bytes)):
            return bool(value)
        return True

    if status in SUCCESS_STATUSES and not any(
        has_witness(out.get(key)) for key in (
            "result","state","evidence","native_receipts","cell_receipts",
            "question_receipts","cognitive_receipts",
        )
    ):
        out.update(
            status="OPEN",
            execution_truth="OPEN",
            material_delta=False,
            blocker=("CONFIGURED_HF2_FULL_MATCH_WITHOUT_EXECUTION_WITNESS"
                     if status=="FULL_MATCH" or truth=="FULL_MATCH"
                     else "CONFIGURED_HF2_SUCCESS_WITHOUT_EXECUTION_WITNESS"),
        )
    return out


# III. Semantic and receipt identity for recurrence.
def _canonical(value:Any)->Any:
    if is_dataclass(value):
        return _canonical(asdict(value))
    if isinstance(value,Mapping):
        # Keep key type and value: 1 and "1" are distinct receipt coordinates.
        # Sort the encoded keys, not their lossy string representations.
        entries=[((type(k).__module__,type(k).__qualname__,_canonical(k)),_canonical(v))
                 for k,v in value.items()]
        return {"__mapping__":sorted(entries,key=lambda item:json.dumps(
            item[0],sort_keys=True,separators=(",",":"),ensure_ascii=False))}
    if isinstance(value,(list,tuple)):
        return [_canonical(v) for v in value]
    if isinstance(value,(set,frozenset)):
        return sorted((_canonical(v) for v in value),key=repr)
    if isinstance(value,(str,int,float,bool)) or value is None:
        return value
    return {"__repr__":repr(value),"__type__":type(value).__qualname__}


_EXECUTION_RECEIPT_KEYS=("native_receipts","cell_receipts","question_receipts","cognitive_receipts")


def _receipt_signature(raw:dict[str,Any])->str:
    return json.dumps(_canonical({key:raw.get(key) for key in _EXECUTION_RECEIPT_KEYS}),
                      sort_keys=True,separators=(",",":"),ensure_ascii=False)


def _semantic_signature(raw:dict[str,Any],current:Any)->str:
    """Fingerprint the admitted semantic payload, excluding recurrence-control flags.

    Configured repository tools are evidence-oriented.  When a clean successor pass
    returns the same semantic evidence/state as the prior pass, the wrapper must
    normalize that repeated evidence to no-new-material-delta rather than spin to
    RESOURCE_STOP because an older adapter blindly repeats material_delta=True.
    """
    payload={
        "state":raw.get("state",current),
        "result":raw.get("result"),
        "evidence":raw.get("evidence",()),
        "related_objects":raw.get("related_objects",()),
        "dependency_footprint":raw.get("dependency_footprint",()),
        "affected_objects":raw.get("affected_objects",()),
        "status":raw.get("status","EXECUTED"),
        "execution_truth":raw.get("execution_truth",""),
        "execution_receipts":{key:raw.get(key) for key in _EXECUTION_RECEIPT_KEYS},
    }
    return json.dumps(_canonical(payload),sort_keys=True,separators=(",",":"),ensure_ascii=False)


# IV. Recurrence delta projection and affected-scope obligations.
def _delta_from_raw(tool_id:str,raw:dict[str,Any])->dict[str,Any]:
    supplied=raw.get("hf2_delta",{})
    delta=dict(supplied) if isinstance(supplied,dict) else {}
    if not material_delta_present(delta):
        delta["material_result_delta"]=bool(raw.get("material_delta",False))

    delta.setdefault(
        "route_equivalence",
        str(raw.get("route_equivalence") or f"{tool_id}:configured-hf2")
    )
    if raw.get("invalidating_evidence"):
        delta["invalidating_evidence"]=True
    if raw.get("certified_no_gain"):
        delta["certified_no_gain"]=True
    # Preserve independently supplied affected-scope obligations.  A producer
    # cannot certify close by reporting a clean local result while its domain
    # has unresolved affected files, sections or other result-sensitive nodes.
    for source_field, delta_field in (
        ("hf2_affected_frontier", "affected_frontier"),
        ("hf2_scope_deltas", "scope_deltas"),
    ):
        if source_field in raw:
            value=raw[source_field]
            if value:
                delta[delta_field]=value
            else:
                delta.setdefault(delta_field,value)
    return delta


# V. SELF recurrence (HF002 only).
def _execute_self_recurrence(tool_id,plan,state,adapter,recurrence_engine):
    if str(tool_id)!="HF002":
        raise ConfiguredHF2ExecutionError(
            f"CONFIGURED_HF2_SELF_RECURRENCE_INVALID:{tool_id}"
        )
    working=deepcopy(state)
    raw=_raw_mapping(adapter(working,plan))
    next_state=raw.get("state",working)
    status=str(raw.get("status","EXECUTED"))
    if status in NON_SUCCESS_STATUSES:
        return ConfiguredHF2ExecutionResult(
            str(tool_id),recurrence_engine,status,state,raw,1,(),1
        )
    native=raw.get("result")
    native_status=native.get("status") if isinstance(native,Mapping) else None
    if isinstance(native_status,str) and native_status in TERMINAL-{"RELATIVE_CLOSE"}:
        raw["blocker"]="CONFIGURED_HF2_SELF_NATIVE_NOT_CLOSED"
        return ConfiguredHF2ExecutionResult(
            str(tool_id),recurrence_engine,native_status,state,raw,1,(),1
        )
    if (raw.get("hf2_live_local") or raw.get("hf2_local_close",True) is not True
            or raw.get("trc_terminal",True) is not True
            or affected_scope_open(_delta_from_raw(str(tool_id),raw))
            or (native_status=="RELATIVE_CLOSE" and "trace" in native
                and not hf2_fixed_point_witness(native["trace"] or ()))):
        raw.update(status="OPEN",execution_truth="OPEN",
                   blocker="CONFIGURED_HF2_SELF_FRONTIER_NOT_CLOSED")
        return ConfiguredHF2ExecutionResult(
            str(tool_id),recurrence_engine,"OPEN",state,raw,1,(),1
        )
    return ConfiguredHF2ExecutionResult(
        str(tool_id),recurrence_engine,"SELF_CLOSE",next_state,raw,1,(),1
    )


# VI. Configured invocation admission and ordinary HF002 execution.
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

    # A valid plan for another tool is still the wrong executable authority.
    # Check binding identity before handing any state to the native adapter.
    if str(getattr(plan,"tool_id",""))!=str(tool_id):
        raise ConfiguredHF2ExecutionError(
            f"CONFIGURED_HF2_TOOL_IDENTITY_MISMATCH:{tool_id}"
        )

    from tool_execution_plan import ToolExecutionPlan
    if type(plan) is not ToolExecutionPlan or not plan.complete:
        raise ConfiguredHF2ExecutionError(
            f"CONFIGURED_HF2_PLAN_INCOMPLETE:{tool_id}"
        )

    if not bool(getattr(plan,"recurrence_required",False)):
        raise ConfiguredHF2ExecutionError(
            f"CONFIGURED_HF2_RECURRENCE_NOT_REQUIRED:{tool_id}"
        )

    recurrence_engine=str(getattr(plan,"recurrence_engine",""))
    if recurrence_engine=="SELF":
        return _execute_self_recurrence(tool_id,plan,state,adapter,recurrence_engine)

    if recurrence_engine!="HF002":
        raise ConfiguredHF2ExecutionError(
            f"CONFIGURED_HF2_ENGINE_INVALID:{tool_id}:{recurrence_engine}"
        )

    holder={"raw":None,"calls":0,"previous_signature":None,"previous_receipts":None}

    def run_capability(current,memory):
        holder["before"]=deepcopy(current)
        raw=_raw_mapping(adapter(current,plan))
        holder["raw"]=raw
        holder["calls"]+=1
        return raw

    def admit_normalize(raw,current,memory):
        normalized=raw.get("state",current)
        delta=_delta_from_raw(str(tool_id),raw)
        # Independently observed state changes override a producer-supplied false delta.
        if normalized != holder["before"]:
            delta["material_result_delta"]=True
        supplied=raw.get("hf2_delta")
        explicit_material=(
            isinstance(supplied,dict)
            and material_delta_present(supplied)
        )
        signature=_semantic_signature(raw,current)
        if (
            not explicit_material
            and bool(raw.get("material_delta",False))
            and holder["previous_signature"]==signature
            and normalized == holder["before"]
        ):
            delta["material_result_delta"]=False
            delta["clean_successor_duplicate_evidence"]=True
        receipts=_receipt_signature(raw)
        if holder["previous_receipts"] is not None and receipts!=holder["previous_receipts"]:
            delta["material_result_delta"]=True
        holder["previous_receipts"]=receipts
        holder["previous_signature"]=signature
        return normalized,delta

    def trc_verify(before,after,delta):
        raw=holder["raw"] or {}
        return {
            "terminal":raw.get("trc_terminal",True) is True,
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
            return raw["hf2_local_close"] is True
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
