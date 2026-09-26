"""Recursive ImprovementCore parent/child manager.

Parent ImprovementCore owns continuation. Child ImprovementCore runs are typed
work items whose returns must be admitted and reconciled before they can change
parent state. Equivalent reruns without continuation-relevant delta do not count
as progress.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Any, Callable

TERMINAL={"COMPLETE","OPEN","BLOCKED","CONFLICT"}
ADMISSION={"ADMIT","REJECT","RECONCILE","OPEN","NO_GAIN"}

@dataclass
class ChildJob:
    id:str
    job:dict[str,Any]
    basis_id:str

@dataclass
class ChildReturn:
    child_id:str
    job_id:str
    execution_truth:str
    result:dict[str,Any]
    basis_id:str

@dataclass
class ManagerTrace:
    iteration:int
    selected_job:dict[str,Any]
    child_return:dict[str,Any]
    admission:str
    delta:dict[str,Any]
    state_after:dict[str,Any]

@dataclass
class RecursiveImprovementCoreManager:
    select_child_job:Callable[[dict[str,Any],dict[str,Any]], dict[str,Any] | None]
    run_child:Callable[[ChildJob], ChildReturn]
    admit_child:Callable[[ChildReturn,dict[str,Any],dict[str,Any]], tuple[str,dict[str,Any]]]
    update_parent:Callable[[dict[str,Any],dict[str,Any],str,dict[str,Any]], tuple[dict[str,Any],dict[str,Any]]]
    max_iterations:int=32
    traces:list[ManagerTrace]=field(default_factory=list)

    def run(self,state:dict[str,Any],memory:dict[str,Any])->dict[str,Any]:
        z=dict(state); m=dict(memory)
        for i in range(self.max_iterations):
            terminal=str(z.get("terminal","CONTINUE"))
            if terminal in TERMINAL:
                return {"status":terminal,"state":z,"memory":m,"traces":[asdict(t) for t in self.traces]}

            selected=self.select_child_job(z,m)
            if selected is None:
                if z.get("live_continuation"):
                    raise RuntimeError("IC_MANAGER_LIVENESS_FAILURE:live_continuation_without_child_or_other_action")
                z["terminal"]="OPEN"
                return {"status":"OPEN","state":z,"memory":m,"traces":[asdict(t) for t in self.traces]}

            basis=str(selected.get("basis_id") or z.get("basis_id") or f"basis:{i}")
            job=ChildJob(id=f"child:{i}",job=selected,basis_id=basis)

            ret=self.run_child(job)
            if ret.job_id!=selected.get("id"):
                raise RuntimeError("IC_MANAGER_RETURN_MISMATCH:job_id")
            if ret.basis_id!=basis:
                raise RuntimeError("IC_MANAGER_RETURN_MISMATCH:basis_id")
            if ret.execution_truth not in {"FULL_MATCH","IMPLEMENTATION_EXECUTED","SEMANTICALLY_APPLIED","OPEN","BLOCKED"}:
                raise RuntimeError("IC_MANAGER_EXECUTION_TRUTH_INVALID")

            admission,delta=self.admit_child(ret,z,m)
            if admission not in ADMISSION:
                raise RuntimeError("IC_MANAGER_ADMISSION_INVALID")

            z2,m2=self.update_parent(z,m,admission,delta)
            self.traces.append(ManagerTrace(
                iteration=i, selected_job=selected, child_return=asdict(ret),
                admission=admission, delta=delta, state_after=z2
            ))

            material=bool(
                delta.get("material_result_delta")
                or delta.get("material_search_delta")
                or delta.get("open_refinement")
                or delta.get("negative_evidence")
                or delta.get("certified_no_gain")
                or delta.get("changed_representation")
            )
            if not material and str(z2.get("terminal","CONTINUE"))=="CONTINUE":
                raise RuntimeError("IC_MANAGER_NO_PROGRESS:child_return_without_continuation_relevant_delta")

            z,m=z2,m2

        raise RuntimeError("IC_MANAGER_RESOURCE_BOUND:max_iterations")
