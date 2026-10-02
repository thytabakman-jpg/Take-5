"""Current ICC128 episode adapter for the Kernel 053 prototype.

This adapts the reusable pattern recovered in improvement_core_legacy_candidate.py
to the current ICC128 controller and rho_128 policy.  It deliberately does not
merge child execution state into parent controller state.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Callable, Mapping

from icc128_autonomous_controller import ICC128Controller
import rho128_policy as rho
from improvement_core_tool_bridge import bind_selected_tools, execute_bound_tools
from specification_before_transformation import assess_executable_work_item
from kernel053_child_result import project_child_result
from kernel053_durable_execution import (
    DurableExecutionBackend,
    DurableExecutionReceipt,
    Take5InlineBackend,
    execute_selected_operation,
)


NON_SUCCESS={"OPEN","BLOCKED","CONFLICT"}


@dataclass(frozen=True)
class Kernel053ICC128Result:
    status:str
    state:dict[str,Any]
    memory:dict[str,Any]
    traces:tuple[dict[str,Any],...]
    selection_traces:tuple[dict[str,Any],...]
    results:tuple[dict[str,Any],...]
    durable_receipts:tuple[dict[str,Any],...]
    final_packet:dict[str,Any]


def _work_id(item:Mapping[str,Any])->str:
    value=item.get("id") or item.get("work_id")
    if not value:
        raise ValueError("ICC128_WORK_ID_REQUIRED")
    return str(value)


def _package(item:Mapping[str,Any])->rho.Package:
    jobs=item.get("jobs",())
    if isinstance(jobs,str):
        jobs=(jobs,)
    return rho.Package(
        id=_work_id(item),
        jobs=frozenset(str(x) for x in jobs),
        burden=int(item.get("burden",1)),
        info_gain=int(item.get("info_gain",0)),
        dependency_leverage=int(item.get("dependency_leverage",0)),
        continuation_value=int(item.get("continuation_value",0)),
        protected=bool(item.get("protected",True)),
        authority_ok=bool(item.get("authority_ok",True)),
        inputs_ok=bool(item.get("inputs_ok",True)),
    )


class ICC128EpisodeAdapter:
    def __init__(
        self,
        *,
        generate_questions:Callable[[dict[str,Any],dict[str,Any]],list[dict[str,Any]]],
        generate_work:Callable[[list[dict[str,Any]],dict[str,Any],dict[str,Any]],list[dict[str,Any]]],
        admit_results:Callable[[list[dict[str,Any]],dict[str,Any],dict[str,Any]],dict[str,Any]],
        update_state:Callable[[dict[str,Any],dict[str,Any],dict[str,Any]],tuple[dict[str,Any],dict[str,Any]]],
        generic_execute:Callable[[dict[str,Any],dict[str,Any],dict[str,Any]],Any] | None=None,
        delegated_controller_runners:Mapping[str,Callable[[dict[str,Any],dict[str,Any],dict[str,Any]],Any]] | None=None,
        configured_tool_adapters:Mapping[str,Callable] | None=None,
        durable_backend:DurableExecutionBackend | None=None,
        discovery_closure:Callable | None=None,
        state_from_packet:Callable[[Mapping[str,Any]],dict[str,Any]] | None=None,
        memory_from_packet:Callable[[Mapping[str,Any]],dict[str,Any]] | None=None,
        max_iterations:int=32,
    ):
        self.generate_questions=generate_questions
        self.generate_work=generate_work
        self.admit_results=admit_results
        self.update_state=update_state
        self.generic_execute=generic_execute
        self.delegated_controller_runners=dict(delegated_controller_runners or {})
        self.configured_tool_adapters=dict(configured_tool_adapters or {})
        self.durable_backend=durable_backend or Take5InlineBackend()
        self.discovery_closure=discovery_closure
        self.state_from_packet=state_from_packet
        self.memory_from_packet=memory_from_packet
        self.max_iterations=max_iterations

    def _default_state(self,packet):
        obligations=packet.get("obligations",())
        required=[]
        for item in obligations if isinstance(obligations,(list,tuple)) else ():
            if isinstance(item,Mapping):
                ident=item.get("id") or item.get("job") or item.get("obligation")
                if ident:
                    required.append(str(ident))
            elif item:
                required.append(str(item))
        return {
            "terminal":"CONTINUE",
            "admitted_continuation":True,
            "target":packet.get("identity"),
            "job":packet.get("job"),
            "basis":packet.get("frozen_math_fingerprint"),
            "operational_goal":packet.get("operational_goal"),
            "required_jobs":tuple(required),
            "representation_result_sensitive":True,
            "packet_evidence":dict(packet),
        }

    def __call__(self,packet:Mapping[str,Any])->Kernel053ICC128Result:
        packet=dict(packet)
        initial_state=(
            dict(self.state_from_packet(packet))
            if self.state_from_packet is not None
            else self._default_state(packet)
        )
        initial_memory=(
            dict(self.memory_from_packet(packet))
            if self.memory_from_packet is not None
            else {}
        )
        durable_receipts:list[dict[str,Any]]=[]
        selection_traces:list[dict[str,Any]]=[]

        def select(questions,work,current,mem):
            packages=[_package(x) for x in work]
            required=set(str(x) for x in current.get("required_jobs",()))
            decision=rho.choose(current,packages,required)
            selection_traces.append(dict(decision.get("decision_trace",{})))
            chosen=set(str(x) for x in decision.get("selected",()))
            if decision.get("status")!="SELECTED":
                if questions:
                    current["selection_blocked"]=True
                    current["selection_status"]=decision.get("status","OPEN")
                return []
            return [dict(x) for x in work if _work_id(x) in chosen]

        def run_formal(item,current):
            admission=assess_executable_work_item(item,configured_observer=True)
            if not admission.licensed:
                return {
                    "status":"OPEN",
                    "execution_truth":"NOT_EXECUTED",
                    "blocker":admission.blocker,
                    "execution_admission":admission.__dict__,
                    "work_id":_work_id(item),
                }
            bridge_state={**current,"selected_tools":(str(item["tool_id"]),)}
            try:
                bridge_state,bindings=bind_selected_tools(bridge_state)
            except Exception as exc:
                return {
                    "status":"OPEN",
                    "execution_truth":"NOT_EXECUTED",
                    "blocker":str(exc),
                    "work_id":_work_id(item),
                }
            batch=execute_bound_tools(
                bridge_state,
                bindings,
                self.configured_tool_adapters,
            )
            executions=tuple(asdict(x) for x in batch.executions)
            return {
                "status":batch.status,
                "execution_truth":(
                    "IMPLEMENTATION_EXECUTED"
                    if batch.status=="EXECUTED"
                    else batch.status if batch.status in NON_SUCCESS
                    else "NOT_COMPLETE"
                ),
                "blocker":batch.blocker,
                "work_id":_work_id(item),
                "executions":executions,
                "material_delta":any(bool(x.get("material_delta")) for x in executions),
                "evidence":tuple(
                    e
                    for x in executions
                    for e in x.get("evidence",())
                ),
            }

        def run_delegated(item,current,mem):
            child=str(item.get("delegated_controller") or item.get("controller_id"))
            runner=self.delegated_controller_runners.get(child)
            if runner is None:
                return {
                    "status":"OPEN",
                    "execution_truth":"NOT_EXECUTED",
                    "blocker":f"DELEGATED_CONTROLLER_RUNNER_REQUIRED:{child}",
                    "work_id":_work_id(item),
                }
            raw=runner(dict(item),dict(current),dict(mem))
            executions=()
            if isinstance(raw,Mapping):
                executions=tuple(raw.get("executions",()) or ())
            child_delta=project_child_result(
                child,
                raw,
                executions=executions,
            )
            return {
                "status":child_delta["child_status"],
                "execution_truth":child_delta["execution_truth"],
                "work_id":_work_id(item),
                "child_delta":child_delta,
                "material_delta":bool(child_delta.get("material_result_delta")),
                "evidence":tuple(child_delta.get("child_evidence",())),
            }

        def run_generic(item,current,mem):
            admission=assess_executable_work_item(item,configured_observer=False)
            if not admission.licensed:
                return {
                    "status":"OPEN",
                    "execution_truth":"NOT_EXECUTED",
                    "blocker":admission.blocker,
                    "execution_admission":admission.__dict__,
                    "work_id":_work_id(item),
                }
            if admission.effect_class=="TARGET_TRANSFORM":
                return {
                    "status":"BLOCKED",
                    "execution_truth":"NOT_EXECUTED",
                    "blocker":"KERNEL053_TARGET_TRANSFORM_COMMIT_ADAPTER_REQUIRED",
                    "execution_admission":admission.__dict__,
                    "work_id":_work_id(item),
                }
            if self.generic_execute is None:
                return {
                    "status":"OPEN",
                    "execution_truth":"NOT_EXECUTED",
                    "blocker":"GENERIC_EXECUTOR_REQUIRED",
                    "work_id":_work_id(item),
                }
            raw=self.generic_execute(dict(item),dict(current),dict(mem))
            if isinstance(raw,Mapping):
                out=dict(raw)
                out.setdefault("status","EXECUTED")
                out.setdefault("execution_truth","IMPLEMENTATION_EXECUTED")
                out.setdefault("work_id",_work_id(item))
                return out
            return {
                "status":"EXECUTED",
                "execution_truth":"IMPLEMENTATION_EXECUTED",
                "result":raw,
                "material_delta":True,
                "work_id":_work_id(item),
            }

        def execute(selected,current,mem):
            out=[]
            for item in selected:
                item=dict(item)
                work_id=_work_id(item)
                if item.get("delegated_controller") or item.get("controller_id"):
                    op_kind="delegated"
                    invoke=lambda item=item: run_delegated(item,current,mem)
                elif item.get("tool_id"):
                    op_kind="tool"
                    invoke=lambda item=item: run_formal(item,current)
                else:
                    op_kind="generic"
                    invoke=lambda item=item: run_generic(item,current,mem)

                receipt=execute_selected_operation(
                    self.durable_backend,
                    episode_id=str(packet.get("frozen_math_fingerprint") or packet.get("identity") or "icc128"),
                    operation_id=f"{op_kind}:{work_id}",
                    payload=item,
                    invoke=invoke,
                )
                durable_receipts.append(asdict(receipt))
                raw=receipt.result
                if isinstance(raw,Mapping):
                    result=dict(raw)
                else:
                    result={"result":raw}
                result.setdefault("status",receipt.status)
                result.setdefault("execution_truth",receipt.execution_truth)
                result["d_exec_backend"]=receipt.backend
                result["d_exec_operation_id"]=receipt.operation_id
                result["d_exec_evidence"]=receipt.evidence
                out.append(result)
            return out

        def admit(results,current,mem):
            delta=dict(self.admit_results(results,current,mem) or {})
            child_deltas=[
                dict(result["child_delta"])
                for result in results
                if isinstance(result,Mapping) and isinstance(result.get("child_delta"),Mapping)
            ]
            if child_deltas:
                delta["child_deltas"]=tuple(child_deltas)
            if any(bool(x.get("material_delta")) for x in results if isinstance(x,Mapping)):
                delta["material_result_delta"]=True
            statuses={
                str(x.get("status"))
                for x in results
                if isinstance(x,Mapping)
            }
            if "BLOCKED" in statuses:
                delta["terminal"]="BLOCKED"
            elif "CONFLICT" in statuses:
                delta["terminal"]="CONFLICT"
            elif "OPEN" in statuses:
                delta["terminal"]="OPEN"
            if delta.get("terminal") in NON_SUCCESS:
                blockers=tuple(
                    str(x.get("blocker"))
                    for x in results
                    if isinstance(x,Mapping) and x.get("blocker")
                )
                if blockers:
                    delta["execution_blocker"]=blockers[0]
            if any(str(x.get("status"))=="OPEN" for x in results if isinstance(x,Mapping)):
                delta["new_OPEN"]=True
            if any(str(x.get("status"))=="BLOCKED" for x in results if isinstance(x,Mapping)):
                delta["child_BLOCKED"]=True
            if any(str(x.get("status"))=="CONFLICT" for x in results if isinstance(x,Mapping)):
                delta["child_CONFLICT"]=True
            if rho.needs_reselection(delta):
                delta["rho_reselection_required"]=True
            return delta

        def update(current,mem,delta):
            next_state,next_memory=self.update_state(
                dict(current),dict(mem),dict(delta)
            )
            next_state=dict(next_state)
            next_memory=dict(next_memory)
            terminal=str(delta.get("terminal",""))
            if terminal in NON_SUCCESS:
                next_state["terminal"]=terminal
                next_state["admitted_continuation"]=False
            if delta.get("rho_reselection_required"):
                next_memory["rho_reselection_required"]=True
            return next_state,next_memory

        controller=ICC128Controller(
            gq=self.generate_questions,
            gw=self.generate_work,
            select=select,
            execute=execute,
            admit=admit,
            update=update,
            dcc=self.discovery_closure,
            max_iterations=self.max_iterations,
        )
        out=controller.run(initial_state,initial_memory)
        results=tuple(
            result
            for trace in out["traces"]
            for result in trace.get("results",())
        )
        return Kernel053ICC128Result(
            status=str(out["status"]),
            state=dict(out["state"]),
            memory=dict(out["memory"]),
            traces=tuple(out["traces"]),
            selection_traces=tuple(selection_traces),
            results=results,
            durable_receipts=tuple(durable_receipts),
            final_packet=dict(packet),
        )
