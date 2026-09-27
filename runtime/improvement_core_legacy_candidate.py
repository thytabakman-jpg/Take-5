"""ImprovementCore Legacy-loop candidate with modern guard services.

This is a candidate runtime, not the current user-facing ImprovementCore.

It reuses the frozen ICC128 Legacy controller loop and rho_128 policy while
preserving current configured-tool execution truth and typed OPEN/BLOCKED/CONFLICT.
Open-ended semantic G_Q/G_W intelligence remains injected by the active host.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

import icc128_legacy
from improvement_core_tool_bridge import bind_selected_tools, execute_bound_tools
from specification_before_transformation import assess_executable_work_item


TERMINAL={"COMPLETE","OPEN","BLOCKED","CONFLICT"}


@dataclass(frozen=True)
class LegacyCandidateResult:
    status:str
    state:dict[str,Any]
    memory:dict[str,Any]
    traces:tuple[dict[str,Any],...]
    selection_traces:tuple[dict[str,Any],...]


def _package_from_work(rho, item:Mapping[str,Any]):
    return rho.Package(
        id=str(item["id"]),
        jobs=frozenset(str(x) for x in item.get("jobs",())),
        burden=int(item.get("burden",1)),
        info_gain=int(item.get("info_gain",0)),
        dependency_leverage=int(item.get("dependency_leverage",0)),
        continuation_value=int(item.get("continuation_value",0)),
        protected=bool(item.get("protected",True)),
        authority_ok=bool(item.get("authority_ok",True)),
        inputs_ok=bool(item.get("inputs_ok",True)),
    )


def run_legacy_candidate(
    state:Mapping[str,Any],
    memory:Mapping[str,Any],
    *,
    generate_questions:Callable[[dict[str,Any],dict[str,Any]],list[dict[str,Any]]],
    generate_work:Callable[[list[dict[str,Any]],dict[str,Any],dict[str,Any]],list[dict[str,Any]]],
    execute_work:Callable[[list[dict[str,Any]],dict[str,Any],dict[str,Any]],list[dict[str,Any]]] | None,
    admit_results:Callable[[list[dict[str,Any]],dict[str,Any],dict[str,Any]],dict[str,Any]],
    update_state:Callable[[dict[str,Any],dict[str,Any],dict[str,Any]],tuple[dict[str,Any],dict[str,Any]]],
    configured_tool_adapters:Mapping[str,Callable] | None=None,
    discovery_closure:Callable[[dict[str,Any],dict[str,Any],dict[str,Any]],dict[str,Any]] | None=None,
    max_iterations:int=32,
)->LegacyCandidateResult:
    """Run the frozen endogenous loop under current execution guards."""
    activated=icc128_legacy.activate()
    controller_mod=activated["controller"]
    rho=activated["rho_policy"]

    selection_traces=[]

    def select(questions,work,current,mem):
        required=set(str(x) for x in current.get("required_jobs",()))
        packages=[_package_from_work(rho,x) for x in work]
        decision=rho.choose(current,packages,required)
        selection_traces.append(dict(decision.get("decision_trace",{})))
        chosen=set(str(x) for x in decision.get("selected",()))
        if decision.get("status")!="SELECTED":
            if questions:
                current["selection_blocked"]=True
                current["selection_status"]=decision.get("status","OPEN")
            return []
        return [dict(x) for x in work if str(x.get("id")) in chosen]

    def execute(selected,current,mem):
        formal=[x for x in selected if x.get("tool_id")]
        generic=[x for x in selected if not x.get("tool_id")]
        results=[]

        if formal:
            formal_admission=[
                (item,assess_executable_work_item(item,configured_observer=True))
                for item in formal
            ]
            denied=[(item,receipt) for item,receipt in formal_admission if not receipt.licensed]
            if denied:
                return [{
                    "status":"OPEN",
                    "execution_truth":"NOT_EXECUTED",
                    "blocker":denied[0][1].blocker,
                    "selected":formal,
                    "execution_admission":tuple(
                        receipt.__dict__ for _,receipt in formal_admission
                    ),
                }]

            tool_ids=tuple(dict.fromkeys(str(x["tool_id"]) for x in formal))
            bridge_state={**current,"selected_tools":tool_ids}
            try:
                bridge_state,bindings=bind_selected_tools(bridge_state)
            except Exception as exc:
                return [{
                    "status":"OPEN",
                    "execution_truth":"NOT_EXECUTED",
                    "blocker":str(exc),
                    "selected":formal,
                    "state_after_execution":bridge_state,
                }]
            batch=execute_bound_tools(bridge_state,bindings,configured_tool_adapters)
            results.append({
                "status":batch.status,
                "execution_truth":"IMPLEMENTATION_EXECUTED" if batch.status=="EXECUTED" else "NOT_COMPLETE",
                "blocker":batch.blocker,
                "executions":tuple(x.__dict__ for x in batch.executions),
                "selected":formal,
                "state_after_execution":batch.state,
            })

        if generic:
            generic_admission=[
                (item,assess_executable_work_item(item,configured_observer=False))
                for item in generic
            ]
            denied=[(item,receipt) for item,receipt in generic_admission if not receipt.licensed]
            if denied:
                results.append({
                    "status":"OPEN",
                    "execution_truth":"NOT_EXECUTED",
                    "blocker":denied[0][1].blocker,
                    "selected":generic,
                    "execution_admission":tuple(
                        receipt.__dict__ for _,receipt in generic_admission
                    ),
                })
            elif execute_work is None:
                results.append({
                    "status":"OPEN",
                    "execution_truth":"NOT_EXECUTED",
                    "blocker":"GENERIC_EXECUTOR_REQUIRED",
                    "selected":generic,
                })
            else:
                results.extend(execute_work(generic,current,mem))

        return results

    def admit(results,current,mem):
        delta=dict(admit_results(results,current,mem) or {})
        for result in results:
            status=str(result.get("status","EXECUTED"))
            if status in {"OPEN","BLOCKED","CONFLICT"}:
                delta["terminal"]=status
                delta["execution_blocker"]=result.get("blocker")
            if result.get("state_after_execution") is not None:
                delta["execution_state_patch"]=result["state_after_execution"]

        if rho.needs_reselection(delta):
            delta["rho_reselection_required"]=True
        return delta

    def update(current,mem,delta):
        base=dict(current)
        patch=delta.get("execution_state_patch")
        if isinstance(patch,dict):
            base.update(patch)

        next_state,next_memory=update_state(base,dict(mem),delta)
        next_state=dict(next_state)
        next_memory=dict(next_memory)

        if delta.get("rho_reselection_required"):
            next_memory["rho_reselection_required"]=True

        terminal=str(delta.get("terminal",""))
        if terminal in TERMINAL:
            next_state["terminal"]=terminal
            next_state["admitted_continuation"]=False

        return next_state,next_memory

    controller=controller_mod.ICC128Controller(
        gq=generate_questions,
        gw=generate_work,
        select=select,
        execute=execute,
        admit=admit,
        update=update,
        dcc=discovery_closure,
        max_iterations=int(max_iterations),
    )
    out=controller.run(dict(state),dict(memory))
    return LegacyCandidateResult(
        status=str(out["status"]),
        state=dict(out["state"]),
        memory=dict(out["memory"]),
        traces=tuple(out["traces"]),
        selection_traces=tuple(selection_traces),
    )
