"""Default HF2 local recurrence for user-facing ImprovementCore.

Ordinary ImprovementCore invocation is lifted through HF002 so the same complete
ImprovementCore capability is reapplied after a completed pass only when that
pass produced both:
  1. an explicit material-effect witness, and
  2. a changed semantic state.

HF2 owns this local same-capability recurrence only. ImprovementCore retains
global work selection, cross-capability replanning, admission, and terminality.

Direct run_improvement_core_regime(...) remains the one-pass/low-level surface.
"""
from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from typing import Any, Callable

from hf002_recursive_continuation import HF002RecursiveContinuation
from improvement_core_learning_memory import (
    DEFAULT_DURABLE_LEARNING_PATH,
    LearningMemory,
)
from improvement_core_knowledge_ledger import (
    DEFAULT_KNOWLEDGE_LEDGER_PATH,
    KnowledgeLedger,
)
from improvement_core_regime import (
    ImprovementCoreRegimeResult,
    run_improvement_core_regime,
)


_INTERNAL_PREFIX="_hf2_ic_"


def _clean_state(state:dict[str,Any])->dict[str,Any]:
    return {
        k:v for k,v in state.items()
        if not str(k).startswith(_INTERNAL_PREFIX)
    }


def _fingerprint(state:dict[str,Any])->str:
    raw=json.dumps(
        _clean_state(state),
        sort_keys=True,
        separators=(",",":"),
        default=repr,
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _operator_material(result:ImprovementCoreRegimeResult)->bool:
    for receipt in result.result.receipts:
        value=getattr(receipt,"value",None)
        if isinstance(value,dict) and value.get("material_delta"):
            return True
        executions=getattr(value,"executions",None)
        if executions and any(bool(getattr(x,"material_delta",False)) for x in executions):
            return True

    recursive=result.recursive_result
    if isinstance(recursive,dict):
        for trace in recursive.get("traces",()):
            if not isinstance(trace,dict):
                continue
            if trace.get("strict_progress") or trace.get("progress_effects"):
                return True
            delta=trace.get("delta",{})
            if isinstance(delta,dict) and any(
                delta.get(k) for k in (
                    "material_result_delta",
                    "material_search_delta",
                    "material_discovery_delta",
                    "material_relation_delta",
                    "open_refinement",
                    "changed_representation",
                    "goal_gap_reduced",
                    "execution_truth_strengthened",
                    "resolved_open",
                    "resolved_blocked",
                    "resolved_conflict",
                )
            ):
                return True
    return False


def run_improvement_core_with_hf2(
    user_text:str,
    *,
    target:str,
    job:str,
    basis:str,
    state:Any,
    handlers:dict[str,Callable],
    authority=frozenset(),
    boundary=None,
    explicit_mode=None,
    observer_risk=None,
    jane_update:Callable|None=None,
    controller_decide:Callable|None=None,
    max_rounds:int=8,
    recursive_handlers:dict[str,Callable]|None=None,
    learning_memory:LearningMemory|None=None,
    knowledge_ledger:KnowledgeLedger|None=None,
    external_adapters:dict[str,Callable]|None=None,
    force_external:bool=False,
    allow_external_gap:bool=True,
    configured_tool_adapters:dict[str,Callable]|None=None,
    hf2_enabled:bool=True,
    hf2_max_rounds:int=6,
)->ImprovementCoreRegimeResult:
    """Run ordinary ImprovementCore with default HF2 local recurrence.

    A non-mapping state or explicit hf2_enabled=False falls back to the
    one-pass regime without changing its semantics.
    """
    lm=learning_memory or LearningMemory.from_durable(
        DEFAULT_DURABLE_LEARNING_PATH,
        autosave=True,
    )
    kl=knowledge_ledger or KnowledgeLedger.from_durable(
        DEFAULT_KNOWLEDGE_LEDGER_PATH,
        autosave=True,
    )

    def run_once(current_state):
        return run_improvement_core_regime(
            user_text,
            target=target,
            job=job,
            basis=basis,
            state=current_state,
            handlers=handlers,
            authority=authority,
            boundary=boundary,
            explicit_mode=explicit_mode,
            observer_risk=observer_risk,
            jane_update=jane_update,
            controller_decide=controller_decide,
            max_rounds=max_rounds,
            recursive_handlers=recursive_handlers,
            learning_memory=lm,
            knowledge_ledger=kl,
            external_adapters=external_adapters,
            force_external=force_external,
            allow_external_gap=allow_external_gap,
            configured_tool_adapters=configured_tool_adapters,
        )

    if not hf2_enabled or not isinstance(state,dict):
        out=run_once(state)
        return replace(
            out,
            hf2_status="DISABLED" if not hf2_enabled else "NOT_APPLICABLE",
            hf2_trace=(),
        )

    last_result:ImprovementCoreRegimeResult|None=None

    def run_capability(current,memory):
        nonlocal last_result
        clean=_clean_state(dict(current))
        last_result=run_once(clean)
        after=last_result.result.state
        if not isinstance(after,dict):
            after={"value":after}
        return {
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "state":dict(after),
            "ic_status":last_result.status,
            "ic_blocker":last_result.blocker,
            "material_reported":_operator_material(last_result),
        }

    def admit_normalize(raw,before,memory):
        before_clean=_clean_state(dict(before))
        after_clean=_clean_state(dict(raw["state"]))
        changed=_fingerprint(before_clean)!=_fingerprint(after_clean)
        material=bool(raw.get("material_reported")) and changed
        normalized=dict(after_clean)
        normalized[_INTERNAL_PREFIX+"material"]=material
        normalized[_INTERNAL_PREFIX+"status"]=str(raw.get("ic_status","OPEN"))
        normalized[_INTERNAL_PREFIX+"blocker"]=raw.get("ic_blocker")
        delta={
            "material_result_delta":material,
            "route_equivalence":"ImprovementCore:"+_fingerprint(after_clean),
            "certified_no_gain":bool(raw.get("material_reported")) and not changed,
        }
        if normalized.get("invalidating_evidence"):
            delta["invalidating_evidence"]=True
        return normalized,delta

    def hf1_classify(before,after,delta):
        status=str(after.get(_INTERNAL_PREFIX+"status","OPEN"))
        if status in {"OPEN","BLOCKED","CONFLICT"}:
            return {"disposition":status}
        explicit=str(after.get("hf1_disposition",""))
        if explicit in {"REENTER","OPEN","BLOCKED","CONFLICT"}:
            return {
                "disposition":explicit,
                "targets":after.get("hf1_targets",()),
            }
        if after.get("upstream_invalidated"):
            return {
                "disposition":"REENTER",
                "targets":after.get("upstream_reentry_targets",()),
            }
        return {"disposition":"STABLE"}

    hf2=HF002RecursiveContinuation(
        run_capability=run_capability,
        admit_normalize=admit_normalize,
        trc_verify=lambda before,after,delta:{"terminal":True},
        hf1_classify=hf1_classify,
        live_local=lambda current,memory:bool(
            current.get(_INTERNAL_PREFIX+"material")
            and not current.get("hf2_disable_local_recurrence",False)
        ),
        local_close=lambda current,memory:bool(
            current.get(_INTERNAL_PREFIX+"status")=="COMPLETE"
            and not current.get(_INTERNAL_PREFIX+"material")
        ),
        max_rounds=int(hf2_max_rounds),
    )

    hf2_out=hf2.run(dict(state),{})
    if last_result is None:
        raise RuntimeError("IMPROVEMENTCORE_HF2_NO_CAPABILITY_RESULT")

    final_state=last_result.result.state
    if isinstance(final_state,dict):
        last_result.result.state=_clean_state(final_state)

    hf2_status=str(hf2_out.get("status","OPEN"))
    blocker=last_result.blocker
    status=last_result.status
    if hf2_status=="RETURN_REENTER":
        status="OPEN"
        blocker="HF002_RETURN_REENTER"
    elif hf2_status=="RESOURCE_STOP":
        status="OPEN"
        blocker="HF002_RESOURCE_STOP"
    elif hf2_status in {"OPEN","BLOCKED","CONFLICT"} and status=="COMPLETE":
        status=hf2_status
        blocker=blocker or f"HF002_{hf2_status}"

    return replace(
        last_result,
        status=status,
        blocker=blocker,
        hf2_status=hf2_status,
        hf2_trace=tuple(hf2_out.get("trace",())),
    )
