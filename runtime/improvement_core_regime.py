"""Current cumulative-autonomous ImprovementCore regime surface.

The regime preserves canonical zero-request entry at the dispatch boundary, basis-relative route calibration and relation admission in upstream discovery, and a first-class external-acquisition preflight.  When outside
evidence or an outside capability has material expected value, ImprovementCore
uses a bound host adapter before expensive internal reconstruction.  When the
outside capability is unavailable, the regime preserves a typed OPEN gap
instead of pretending internal work closed it.
"""
from dataclasses import dataclass
import json
from typing import Any, Callable, Mapping

from improvement_core_manager import (
    run_improvement_core_manager,
    ImprovementCoreManagerResult,
)
from improvement_core_recursive_manager import RecursiveImprovementCoreManager
from improvement_core_learning_memory import (
    DEFAULT_DURABLE_LEARNING_PATH,
    LearningMemory,
)
from improvement_core_knowledge_ledger import (
    DEFAULT_KNOWLEDGE_LEDGER_PATH,
    KnowledgeLedger,
)
from improvement_core_external_acquisition import (
    ExternalAcquisitionReceipt,
    ExternalDisposition,
    acquire_external,
    merge_external_outputs,
)

REGIME_VERSION="091"

@dataclass(frozen=True)
class ImprovementCoreRegime:
    stage_manager:str
    recursive_manager:str
    learning_memory:str
    external_acquisition:str
    configured_tool_bridge:str
    canonical_progress:str
    durable_learning:str
    knowledge_ledger:str
    default_local_recurrence:str
    controller:str="IC-028"
    version:str=REGIME_VERSION

@dataclass(frozen=True)
class ImprovementCoreRegimeResult:
    manager_result:ImprovementCoreManagerResult
    recursive_result:dict|None
    learning_summary:tuple
    status:str
    blocker:str|None=None
    external_receipt:ExternalAcquisitionReceipt|None=None
    knowledge_summary:tuple=()
    hf2_status:str|None=None
    hf2_trace:tuple=()

    @property
    def receipt(self):
        return self.manager_result.receipt

    @property
    def result(self):
        return self.manager_result.result

CURRENT_REGIME=ImprovementCoreRegime(
    stage_manager="runtime.improvement_core_manager.run_improvement_core_manager",
    recursive_manager="runtime.improvement_core_recursive_manager.RecursiveImprovementCoreManager",
    learning_memory="runtime.improvement_core_learning_memory.LearningMemory",
    external_acquisition="runtime.improvement_core_external_acquisition.acquire_external",
    configured_tool_bridge="runtime.improvement_core_tool_bridge.execute_bound_tools",
    canonical_progress="runtime.improvement_core_progress_relation.strict_progress",
    durable_learning="integration/IMPROVEMENT_CORE_DURABLE_LEARNING_110.json",
    knowledge_ledger="integration/IMPROVEMENT_CORE_KNOWLEDGE_LEDGER_113.json",
    default_local_recurrence="HF002",
)

def _record_stage_learning(state,learning_memory):
    if not isinstance(state,dict):
        return
    events=state.get("learning_events",())
    for event in events:
        if not isinstance(event,dict):
            continue
        required={"route_id","basis_id","disposition"}
        if not required<=set(event):
            continue
        learning_memory.record(
            str(event["route_id"]),
            str(event["basis_id"]),
            str(event["disposition"]),
            set(event.get("dependency_footprint",())),
            dict(event.get("evidence",{})),
        )

def _record_stage_knowledge(state,knowledge_ledger,basis):
    if not isinstance(state,dict):
        return
    for event in state.get("knowledge_events",()):
        if not isinstance(event,dict):
            continue
        knowledge_ledger.record_explicit_event(
            event,
            fallback_basis=str(basis),
            source_episode="improvement-core-stage",
        )


def _record_recursive_knowledge(recursive_result,knowledge_ledger,basis):
    if not isinstance(recursive_result,dict):
        return
    for trace in recursive_result.get("traces",()):
        if not isinstance(trace,dict):
            continue
        knowledge_ledger.capture_material_trace(
            trace,
            fallback_basis=str(basis),
            source_episode="improvement-core-recursive",
        )


def _material_configured_round(raw,delta):
    raw=raw if isinstance(raw,Mapping) else {}
    delta=delta if isinstance(delta,Mapping) else {}
    return bool(
        raw.get("material_delta")
        or delta.get("material_result_delta")
        or delta.get("material_search_delta")
        or delta.get("material_discovery_delta")
        or delta.get("negative_evidence")
        or delta.get("open_refinement")
        or delta.get("changed_representation")
    )


def _record_configured_tool_knowledge(state,knowledge_ledger,basis):
    """Durably capture every material configured-tool round before closure.

    Configured execution state is transient controller state. This bridge converts
    material configured outputs, including intermediate HF2 rounds, into durable
    knowledge nodes with tool identity, execution basis, provenance, evidence,
    dependency coordinates, related/affected objects, and recurrence metadata.
    """
    if not isinstance(state,dict):
        return

    for output_index,output in enumerate(state.get("configured_tool_outputs",())):
        if not isinstance(output,Mapping):
            continue

        tool_id=str(output.get("tool_id","")).strip()
        if not tool_id:
            continue

        binding=output.get("binding",{})
        binding=dict(binding) if isinstance(binding,Mapping) else {}
        recurrence=output.get("recurrence")
        recurrence=dict(recurrence) if isinstance(recurrence,Mapping) else {}
        trace=tuple(recurrence.get("trace",())) if recurrence else ()

        structural_dependencies={
            f"configured_tool:{tool_id}",
        }
        for key in ("invocation_profile","geometry","recurrence_engine"):
            value=binding.get(key)
            if value:
                structural_dependencies.add(f"{key}:{value}")

        captured=False
        for round_index,row in enumerate(trace):
            if not isinstance(row,Mapping):
                continue
            raw=row.get("raw_result",{})
            raw=dict(raw) if isinstance(raw,Mapping) else {}
            delta=row.get("delta",{})
            delta=dict(delta) if isinstance(delta,Mapping) else {}
            if not _material_configured_round(raw,delta):
                continue

            related={
                str(x) for x in raw.get("related_objects",()) if str(x)
            }
            affected={
                str(x) for x in raw.get("affected_objects",()) if str(x)
            }
            related.update(affected)
            related.update({tool_id,f"configured_run:{tool_id}"})

            deps={
                str(x) for x in raw.get("dependency_footprint",()) if str(x)
            }
            deps.update(structural_dependencies)

            statement=json.dumps(
                {
                    "tool_id":tool_id,
                    "status":str(raw.get("status",output.get("status","EXECUTED"))),
                    "execution_truth":str(
                        raw.get(
                            "execution_truth",
                            output.get("execution_truth","IMPLEMENTATION_EXECUTED"),
                        )
                    ),
                    "result":raw.get("result",output.get("result")),
                },
                sort_keys=True,
                separators=(",",":"),
                default=str,
            )
            knowledge_ledger.record(
                kind="MATERIAL_TRANSITION",
                statement=statement,
                basis_id=str(basis),
                source_episode="improvement-core-configured-tool",
                source_route=f"configured_tool:{tool_id}",
                disposition="CAPTURED",
                related_objects=tuple(sorted(related)),
                dependency_footprint=tuple(sorted(deps)),
                evidence_refs=tuple(
                    str(x) for x in raw.get("evidence",output.get("evidence",()))
                    if str(x)
                ),
                metadata={
                    "configured_output_index":output_index,
                    "hf2_round_index":round_index,
                    "binding":binding,
                    "recurrence_engine":recurrence.get("engine"),
                    "recurrence_status":recurrence.get("status"),
                    "recurrence_disposition":row.get("disposition"),
                    "delta":delta,
                    "affected_objects":tuple(sorted(affected)),
                },
            )
            captured=True

        if captured:
            continue
        if not bool(output.get("material_delta",False)):
            continue

        related={
            str(x) for x in output.get("related_objects",()) if str(x)
        }
        affected={
            str(x) for x in output.get("affected_objects",()) if str(x)
        }
        related.update(affected)
        related.update({tool_id,f"configured_run:{tool_id}"})

        deps={
            str(x) for x in output.get("dependency_footprint",()) if str(x)
        }
        deps.update(structural_dependencies)

        statement=json.dumps(
            {
                "tool_id":tool_id,
                "status":str(output.get("status","EXECUTED")),
                "execution_truth":str(
                    output.get("execution_truth","IMPLEMENTATION_EXECUTED")
                ),
                "result":output.get("result"),
            },
            sort_keys=True,
            separators=(",",":"),
            default=str,
        )
        knowledge_ledger.record(
            kind="MATERIAL_TRANSITION",
            statement=statement,
            basis_id=str(basis),
            source_episode="improvement-core-configured-tool",
            source_route=f"configured_tool:{tool_id}",
            disposition="CAPTURED",
            related_objects=tuple(sorted(related)),
            dependency_footprint=tuple(sorted(deps)),
            evidence_refs=tuple(
                str(x) for x in output.get("evidence",()) if str(x)
            ),
            metadata={
                "configured_output_index":output_index,
                "binding":binding,
                "recurrence_engine":recurrence.get("engine"),
                "recurrence_status":recurrence.get("status"),
                "affected_objects":tuple(sorted(affected)),
            },
        )


def run_improvement_core_regime(
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
)->ImprovementCoreRegimeResult:
    lm=learning_memory or LearningMemory.from_durable(
        DEFAULT_DURABLE_LEARNING_PATH,
        autosave=True,
    )
    kl=knowledge_ledger or KnowledgeLedger.from_durable(
        DEFAULT_KNOWLEDGE_LEDGER_PATH,
        autosave=True,
    )

    external_receipt=acquire_external(
        state,
        external_adapters,
        force_external=force_external,
        allow_gap=allow_external_gap,
    )
    prepared_state=merge_external_outputs(state,external_receipt)
    external_gap=(
        external_receipt.decision.disposition==ExternalDisposition.OPEN_GAP
    )

    manager_result=run_improvement_core_manager(
        user_text,
        target=target,
        job=job,
        basis=basis,
        state=prepared_state,
        handlers=handlers,
        authority=authority,
        boundary=boundary,
        explicit_mode=explicit_mode,
        observer_risk=observer_risk,
        jane_update=jane_update,
        controller_decide=controller_decide,
        max_rounds=max_rounds,
        configured_tool_adapters=configured_tool_adapters,
    )
    current=manager_result.result.state
    _record_stage_learning(current,lm)
    _record_stage_knowledge(current,kl,basis)
    _record_configured_tool_knowledge(current,kl,basis)

    live=isinstance(current,dict) and bool(current.get("live_continuation"))
    if not live:
        if external_gap:
            return ImprovementCoreRegimeResult(
                manager_result,None,tuple(lm.summary()),"OPEN",
                "EXTERNAL_ACQUISITION_GAP",external_receipt,
                tuple(kl.summary())
            )
        status="COMPLETE" if manager_result.result.terminal else "OPEN"
        blocker=None if manager_result.result.terminal else manager_result.result.blocker
        return ImprovementCoreRegimeResult(
            manager_result,None,tuple(lm.summary()),status,blocker,external_receipt,
            tuple(kl.summary())
        )

    required=("select_child_job","run_child","admit_child","update_parent")
    if recursive_handlers is None or any(k not in recursive_handlers for k in required):
        return ImprovementCoreRegimeResult(
            manager_result,
            None,
            tuple(lm.summary()),
            "OPEN",
            "RECURSIVE_MANAGER_HANDLERS_REQUIRED",
            external_receipt,
            tuple(kl.summary()),
        )

    recursive=RecursiveImprovementCoreManager(
        select_child_job=recursive_handlers["select_child_job"],
        run_child=recursive_handlers["run_child"],
        admit_child=recursive_handlers["admit_child"],
        update_parent=recursive_handlers["update_parent"],
        max_iterations=int(recursive_handlers.get("max_iterations",32)),
        learning_memory=lm,
    )
    try:
        recursive_result=recursive.run(
            dict(current),
            dict(recursive_handlers.get("memory",{})),
        )
    except RuntimeError as exc:
        return ImprovementCoreRegimeResult(
            manager_result,
            None,
            tuple(lm.summary()),
            "OPEN",
            str(exc),
            external_receipt,
            tuple(kl.summary()),
        )

    _record_recursive_knowledge(recursive_result,kl,basis)

    status=str(recursive_result.get("status","OPEN"))
    blocker=recursive_result.get("blocker")
    if external_gap and status in {"COMPLETE","RELATIVE_CLOSE","CLOSED_RELATIVE"}:
        status="OPEN"
        blocker="EXTERNAL_ACQUISITION_GAP"

    return ImprovementCoreRegimeResult(
        manager_result,
        recursive_result,
        tuple(lm.summary()),
        status,
        blocker,
        external_receipt,
        tuple(kl.summary()),
    )
