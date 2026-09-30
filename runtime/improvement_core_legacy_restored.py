"""Legacy-restored ImprovementCore candidate with current guard services.

This is still a candidate entrypoint. It wraps the validated Legacy-loop core with:
- current entry/authority binding;
- observer-mode fail-closed preparation;
- external acquisition;
- durable material-knowledge capture;
- outer HF002 same-capability recurrence;
- current configured-tool execution inherited from the core candidate.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Callable, Mapping

from controller_lease import may_select_actions
from entry_contract import (
    MODE_OBSERVE_DECOUPLED,
    bind_entry_contract,
    entry_is_bound,
)
from hf002_recursive_continuation import HF002RecursiveContinuation
from improvement_core_external_acquisition import (
    ExternalDisposition,
    acquire_external,
    merge_external_outputs,
)
from improvement_core_knowledge_ledger import (
    DEFAULT_KNOWLEDGE_LEDGER_PATH,
    KnowledgeLedger,
)
from improvement_core_legacy_candidate import (
    LegacyCandidateResult,
    run_legacy_candidate,
)


MATERIAL_KEYS=(
    "material_result_delta",
    "material_search_delta",
    "material_discovery_delta",
    "negative_evidence",
    "open_refinement",
    "changed_representation",
    "goal_gap_reduced",
    "execution_truth_strengthened",
)


@dataclass(frozen=True)
class LegacyRestoredResult:
    status:str
    blocker:str|None
    state:dict[str,Any]
    memory:dict[str,Any]
    entry_receipt:str
    external_receipt:Any
    knowledge_summary:tuple
    hf2_status:str
    hf2_trace:tuple
    candidate_traces:tuple
    parent_return_trace:tuple=()


def _fingerprint(value:Any)->str:
    raw=json.dumps(value,sort_keys=True,separators=(",",":"),default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _trace_material(trace:Mapping[str,Any])->bool:
    delta=trace.get("admitted_delta",{})
    return isinstance(delta,Mapping) and any(bool(delta.get(k)) for k in MATERIAL_KEYS)


def _capture_candidate_traces(
    ledger:KnowledgeLedger,
    traces,
    *,
    basis:str,
    episode_id:str,
)->None:
    for trace in traces:
        if not isinstance(trace,Mapping) or not _trace_material(trace):
            continue
        delta=dict(trace.get("admitted_delta",{}))
        selected=trace.get("selected",())
        statement=json.dumps(
            {
                "iteration":trace.get("iteration"),
                "selected":selected,
                "delta":delta,
                "terminal":trace.get("terminal"),
            },
            sort_keys=True,
            separators=(",",":"),
            default=str,
        )
        ledger.record(
            kind="MATERIAL_TRANSITION",
            statement=statement,
            basis_id=str(basis),
            source_episode=str(episode_id),
            source_route="legacy-restored-loop",
            disposition="CAPTURED",
            related_objects=("ImprovementCore","ICC128 Legacy"),
            dependency_footprint=("Legacy-loop","rho128","modern-guards"),
            evidence_refs=("runtime/improvement_core_legacy_candidate.py",),
            metadata={"trace":dict(trace)},
        )


def run_improvement_core_legacy_restored(
    user_text:str,
    *,
    target:str,
    job:str,
    basis:str,
    state:Mapping[str,Any],
    memory:Mapping[str,Any] | None=None,
    generate_questions:Callable,
    generate_work:Callable,
    execute_work:Callable | None,
    admit_results:Callable,
    update_state:Callable,
    configured_tool_adapters:Mapping[str,Callable] | None=None,
    discovery_closure:Callable | None=None,
    external_adapters:Mapping[str,Callable] | None=None,
    force_external:bool=False,
    allow_external_gap:bool=True,
    authority=frozenset(),
    boundary=None,
    explicit_mode=None,
    observer_risk=None,
    observer_prepare:Callable[[dict[str,Any],Any],dict[str,Any]] | None=None,
    knowledge_ledger:KnowledgeLedger | None=None,
    episode_id:str="legacy-restored",
    hf2_enabled:bool=True,
    hf2_max_rounds:int=6,
    max_iterations:int=32,
)->LegacyRestoredResult:
    binding=bind_entry_contract(
        user_text,
        target=target,
        job=job,
        basis=basis,
        authority=frozenset(authority),
        boundary=boundary,
        explicit_mode=explicit_mode,
        observer_risk=observer_risk,
        episode_id=episode_id,
    )
    if not entry_is_bound(binding) or not may_select_actions(binding.lease,"IC-028"):
        return LegacyRestoredResult(
            "BLOCKED","ENTRY_OR_AUTHORITY_DENIED",dict(state),dict(memory or {}),
            binding.contract.receipt,None,(),"BLOCKED",(),(),
        )

    external_receipt=acquire_external(
        dict(state),
        external_adapters,
        force_external=force_external,
        allow_gap=allow_external_gap,
    )
    prepared=merge_external_outputs(dict(state),external_receipt)

    if binding.contract.initial_mode==MODE_OBSERVE_DECOUPLED:
        if observer_prepare is None:
            return LegacyRestoredResult(
                "BLOCKED","OBSERVER_PREPARE_REQUIRED",prepared,dict(memory or {}),
                binding.contract.receipt,external_receipt,(),"BLOCKED",(),(),
            )
        observed=observer_prepare(dict(prepared),binding.contract)
        if not isinstance(observed,dict):
            return LegacyRestoredResult(
                "BLOCKED","OBSERVER_PREPARE_INVALID",prepared,dict(memory or {}),
                binding.contract.receipt,external_receipt,(),"BLOCKED",(),(),
            )
        prepared=dict(observed)

    ledger=knowledge_ledger or KnowledgeLedger.from_durable(
        DEFAULT_KNOWLEDGE_LEDGER_PATH,
        autosave=True,
    )
    base_memory=dict(memory or {})
    all_candidate_traces=[]

    def run_once(current_state,current_memory):
        out=run_legacy_candidate(
            current_state,
            current_memory,
            generate_questions=generate_questions,
            generate_work=generate_work,
            execute_work=execute_work,
            admit_results=admit_results,
            update_state=update_state,
            configured_tool_adapters=configured_tool_adapters,
            discovery_closure=discovery_closure,
            max_iterations=max_iterations,
        )
        all_candidate_traces.extend(out.traces)
        _capture_candidate_traces(
            ledger,out.traces,basis=basis,episode_id=episode_id
        )
        return out

    if not hf2_enabled:
        candidate=run_once(prepared,base_memory)
        status=candidate.status
        blocker=None
        if (
            external_receipt.decision.disposition==ExternalDisposition.OPEN_GAP
            and status=="COMPLETE"
        ):
            status="OPEN"; blocker="EXTERNAL_ACQUISITION_GAP"
        return LegacyRestoredResult(
            status,blocker,candidate.state,candidate.memory,
            binding.contract.receipt,external_receipt,tuple(ledger.summary()),
            "DISABLED",(),tuple(all_candidate_traces),
        )

    last_candidate:LegacyCandidateResult|None=None

    def run_capability(current,hf_memory):
        nonlocal last_candidate
        candidate_memory=dict(current.get("_legacy_restored_memory",base_memory))
        clean={k:v for k,v in current.items() if k!="_legacy_restored_memory"}
        last_candidate=run_once(clean,candidate_memory)
        next_state=dict(last_candidate.state)
        next_state["_legacy_restored_memory"]=dict(last_candidate.memory)
        return {
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "status":last_candidate.status,
            "state":next_state,
            "trace_count":len(last_candidate.traces),
        }

    def admit_normalize(raw,before,hf_memory):
        after=dict(raw["state"])
        before_clean={k:v for k,v in before.items() if k!="_legacy_restored_memory"}
        after_clean={k:v for k,v in after.items() if k!="_legacy_restored_memory"}
        changed=_fingerprint(before_clean)!=_fingerprint(after_clean)
        material=changed and bool(raw.get("trace_count",0))
        delta={
            "material_result_delta":material,
            "route_equivalence":"LegacyRestored:"+_fingerprint(after_clean),
            "certified_no_gain":not changed,
        }
        return after,delta

    def hf1_classify(before,after,delta):
        status=str(after.get("terminal","CONTINUE"))
        if status=="COMPLETE":
            return {"disposition":"STABLE"}
        if status in {"OPEN","BLOCKED","CONFLICT"}:
            return {"disposition":status}
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
        live_local=lambda current,hf_memory:bool(
            current.get("hf2_live_local",False)
        ),
        local_close=lambda current,hf_memory:str(
            current.get("terminal","CONTINUE")
        )=="COMPLETE",
        max_rounds=int(hf2_max_rounds),
    )
    hf_out=hf2.run(dict(prepared),{})

    final_state=dict(hf_out.get("state",prepared))
    final_memory=dict(final_state.pop("_legacy_restored_memory",base_memory))
    status=str(hf_out.get("status","OPEN"))
    blocker=None

    if status=="RELATIVE_CLOSE":
        status="COMPLETE"
    elif status=="RETURN_REENTER":
        status="OPEN"; blocker="HF002_RETURN_REENTER"
    elif status=="RESOURCE_STOP":
        status="OPEN"; blocker="HF002_RESOURCE_STOP"
    elif status in {"OPEN","BLOCKED","CONFLICT"}:
        blocker=f"HF002_{status}"

    if (
        external_receipt.decision.disposition==ExternalDisposition.OPEN_GAP
        and status=="COMPLETE"
    ):
        status="OPEN"
        blocker="EXTERNAL_ACQUISITION_GAP"

    return LegacyRestoredResult(
        status,blocker,final_state,final_memory,
        binding.contract.receipt,external_receipt,tuple(ledger.summary()),
        str(hf_out.get("status","OPEN")),
        tuple(hf_out.get("trace",())),
        tuple(all_candidate_traces),
    )


# Preserve the validated Legacy-restored+HF2 implementation as one parent round.
# The public entry below adds whole-job return closure.
_run_improvement_core_legacy_restored_once=run_improvement_core_legacy_restored


def run_improvement_core_legacy_restored(
    user_text:str,
    *,
    target:str,
    job:str,
    basis:str,
    state:Mapping[str,Any],
    memory:Mapping[str,Any] | None=None,
    generate_questions:Callable,
    generate_work:Callable,
    execute_work:Callable | None,
    admit_results:Callable,
    update_state:Callable,
    configured_tool_adapters:Mapping[str,Callable] | None=None,
    discovery_closure:Callable | None=None,
    external_adapters:Mapping[str,Callable] | None=None,
    force_external:bool=False,
    allow_external_gap:bool=True,
    authority=frozenset(),
    boundary=None,
    explicit_mode=None,
    observer_risk=None,
    observer_prepare:Callable[[dict[str,Any],Any],dict[str,Any]] | None=None,
    knowledge_ledger:KnowledgeLedger | None=None,
    episode_id:str="legacy-restored",
    hf2_enabled:bool=True,
    hf2_max_rounds:int=6,
    max_iterations:int=32,
    return_verifier:Callable|None=None,
    fresh_reobserve:Callable|None=None,
    parent_max_rounds:int=16,
    allow_ungated_debug:bool=False,
)->LegacyRestoredResult:
    """Run Legacy-restored ImprovementCore to parent-level return closure.

    Every parent round executes the complete Legacy loop under the current
    modern guards and its HF2 recurrence.  A candidate terminal state is not a
    user-visible stopping condition until the shared parent return gate either
    licenses RETURN or directs a full re-entry.
    """
    from dataclasses import replace as _replace
    from improvement_core_return_gate import evaluate_parent_return
    from formal_claim_admission import request_requires_formal_claim_receipt
    from improvement_core_hf2_default import _governed_default_fresh_reobserve

    effective_fresh_reobserve=fresh_reobserve or _governed_default_fresh_reobserve

    if not hf2_enabled and not allow_ungated_debug:
        out=_run_improvement_core_legacy_restored_once(
            user_text,target=target,job=job,basis=basis,state=state,memory=memory,
            generate_questions=generate_questions,generate_work=generate_work,
            execute_work=execute_work,admit_results=admit_results,
            update_state=update_state,
            configured_tool_adapters=configured_tool_adapters,
            discovery_closure=discovery_closure,
            external_adapters=external_adapters,force_external=force_external,
            allow_external_gap=allow_external_gap,authority=authority,
            boundary=boundary,explicit_mode=explicit_mode,
            observer_risk=observer_risk,observer_prepare=observer_prepare,
            knowledge_ledger=knowledge_ledger,episode_id=episode_id,
            hf2_enabled=False,hf2_max_rounds=hf2_max_rounds,
            max_iterations=max_iterations,
        )
        return _replace(
            out,status="OPEN",
            blocker="HF2_DISABLE_REQUIRES_EXPLICIT_DEBUG_AUTHORITY",
            parent_return_trace=({
                "gate":"PARENT_RETURN_GATE",
                "status":"OPEN",
                "reason":"HF2_DISABLED_WITHOUT_DEBUG_AUTHORITY",
            },),
        )

    current_state=dict(state)
    current_memory=dict(memory or {})
    parent_trace=[]
    last=None

    for parent_round in range(int(parent_max_rounds)):
        last=_run_improvement_core_legacy_restored_once(
            user_text,
            target=target,
            job=job,
            basis=basis,
            state=current_state,
            memory=current_memory,
            generate_questions=generate_questions,
            generate_work=generate_work,
            execute_work=execute_work,
            admit_results=admit_results,
            update_state=update_state,
            configured_tool_adapters=configured_tool_adapters,
            discovery_closure=discovery_closure,
            external_adapters=external_adapters,
            force_external=force_external,
            allow_external_gap=allow_external_gap,
            authority=authority,
            boundary=boundary,
            explicit_mode=explicit_mode,
            observer_risk=observer_risk,
            observer_prepare=observer_prepare,
            knowledge_ledger=knowledge_ledger,
            episode_id=f"{episode_id}:parent:{parent_round}",
            hf2_enabled=hf2_enabled,
            hf2_max_rounds=hf2_max_rounds,
            max_iterations=max_iterations,
        )

        if allow_ungated_debug and return_verifier is None:
            return _replace(
                last,
                parent_return_trace=tuple(parent_trace)+({
                    "gate":"PARENT_RETURN_GATE",
                    "disposition":"BYPASS_DEBUG",
                    "parent_round":parent_round,
                    "candidate_status":last.status,
                    "hf2_status":last.hf2_status,
                },),
            )

        if (
            last.status=="COMPLETE"
            and hf2_enabled
            and last.hf2_status!="RELATIVE_CLOSE"
        ):
            return _replace(
                last,status="OPEN",
                blocker="PARENT_RETURN_GATE_HF2_NOT_SATURATED",
                parent_return_trace=tuple(parent_trace)+({
                    "gate":"PARENT_RETURN_GATE",
                    "status":"OPEN",
                    "reason":"HF2_NOT_RELATIVE_CLOSE",
                    "parent_round":parent_round,
                    "hf2_status":last.hf2_status,
                },),
            )

        outcome=evaluate_parent_return(
            candidate_status=last.status,
            candidate_blocker=last.blocker,
            state=last.state,
            memory=last.memory,
            context={
                "controller":"ImprovementCore-Legacy-Restored",
                "target":target,
                "job":job,
                "basis":basis,
                "parent_round":parent_round,
                "hf2_status":last.hf2_status,
                "hf2_rounds":len(last.hf2_trace),
                "candidate_status":last.status,
                "candidate_blocker":last.blocker,
                "candidate_trace_count":len(last.candidate_traces),
                "formal_claim_receipt_required":request_requires_formal_claim_receipt(
                    user_text,target=target,job=job
                ),
            },
            verifier=return_verifier,
            fresh_reobserve=effective_fresh_reobserve,
        )
        receipt=dict(outcome.receipt)
        receipt["parent_round"]=parent_round
        receipt["hf2_status"]=last.hf2_status
        receipt["hf2_rounds"]=len(last.hf2_trace)
        parent_trace.append(receipt)

        if outcome.disposition=="RETURN":
            return _replace(
                last,
                status=outcome.terminal,
                blocker=outcome.blocker,
                state=outcome.next_state,
                memory=outcome.next_memory,
                parent_return_trace=tuple(parent_trace),
            )

        current_state=outcome.next_state
        current_memory=outcome.next_memory

    if last is None:
        raise RuntimeError("IMPROVEMENTCORE_PARENT_RETURN_NO_ROUND")

    return _replace(
        last,
        status="OPEN",
        blocker="PARENT_RETURN_GATE_RESOURCE_STOP",
        parent_return_trace=tuple(parent_trace)+({
            "gate":"PARENT_RETURN_GATE",
            "status":"OPEN",
            "reason":"PARENT_MAX_ROUNDS",
            "parent_max_rounds":int(parent_max_rounds),
        },),
    )
