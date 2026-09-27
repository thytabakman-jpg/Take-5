#!/usr/bin/env python3
"""State-relative rho_128 policy kernel.

This module implements the non-LLM control semantics of the recovered IC-012 selector:
activation, deep-vs-cheap routing, nondominated package comparison, and reselection.
Open-ended semantic job generation remains supplied by the active model/observer layer.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

DEEP_FLAGS={
 "target_or_job_identity_open","hidden_dependency_plausible","representation_result_sensitive",
 "recurrence_or_prior_failure","multiple_material_packages_fit","project_local_capability_may_matter",
 "transfer_or_external_route_may_matter","state_delta_invalidates_prior_selection",
 "capability_or_tool_selection_is_itself_the_job",
}

@dataclass(frozen=True)
class Package:
    id:str
    jobs:frozenset[str]
    burden:int=1
    info_gain:int=0
    dependency_leverage:int=0
    continuation_value:int=0
    protected:bool=True
    authority_ok:bool=True
    inputs_ok:bool=True

def activation(state:dict[str,Any])->str:
    if any(bool(state.get(k)) for k in DEEP_FLAGS):
        return "FIRE"
    if all(bool(state.get(k)) for k in (
        "task_and_job_well_typed","one_validated_capability_clearly_fits",
        "consequence_bounded","no_material_rival_exposed"
    )) and not state.get("recurrence_or_prior_failure") and not state.get("major_state_change"):
        return "CHEAP_DIRECT"
    return "OPEN"

def dominates(a:Package,b:Package,required_jobs:set[str])->bool:
    if not (a.protected and a.authority_ok and a.inputs_ok): return False
    if not (b.protected and b.authority_ok and b.inputs_ok): return True
    ca=required_jobs.issubset(a.jobs); cb=required_jobs.issubset(b.jobs)
    if ca and not cb: return True
    if cb and not ca: return False
    dims_a=(a.info_gain,a.dependency_leverage,a.continuation_value,-a.burden)
    dims_b=(b.info_gain,b.dependency_leverage,b.continuation_value,-b.burden)
    ge=all(x>=y for x,y in zip(dims_a,dims_b))
    gt=any(x>y for x,y in zip(dims_a,dims_b))
    return ge and gt

def nondominated(packages:list[Package],required_jobs:set[str])->list[Package]:
    admitted=[p for p in packages if p.protected and p.authority_ok and p.inputs_ok]
    covered=[p for p in admitted if required_jobs.issubset(p.jobs)]
    pool=covered or admitted
    return [p for p in pool if not any(dominates(q,p,required_jobs) for q in pool if q!=p)]

def _trace(state:dict[str,Any],packages:list[Package],required_jobs:set[str],mode:str,frontier:list[Package],selected:list[Package])->dict[str,Any]:
    active_flags=sorted(k for k in DEEP_FLAGS if state.get(k))
    return {
        "activation_mode":mode,
        "activation_flags":active_flags,
        "required_jobs":sorted(required_jobs),
        "candidate_packages":[{
            "id":p.id,
            "jobs":sorted(p.jobs),
            "burden":p.burden,
            "info_gain":p.info_gain,
            "dependency_leverage":p.dependency_leverage,
            "continuation_value":p.continuation_value,
            "protected":p.protected,
            "authority_ok":p.authority_ok,
            "inputs_ok":p.inputs_ok,
        } for p in packages],
        "nondominated_frontier":[p.id for p in frontier],
        "selected":[p.id for p in selected],
        "selection_basis":"minimum_burden_on_nondominated_frontier" if mode=="CHEAP_DIRECT" else
                          "all_nondominated_material_packages" if mode=="FIRE" else
                          "insufficient_activation_evidence",
    }

def choose(state:dict[str,Any],packages:list[Package],required_jobs:set[str])->dict[str,Any]:
    mode=activation(state)
    frontier=nondominated(packages,required_jobs) if mode in {"CHEAP_DIRECT","FIRE"} else []
    if mode=="CHEAP_DIRECT":
        if not frontier:
            return {"mode":mode,"status":"OPEN","frontier":[],"selected":[],
                    "decision_trace":_trace(state,packages,required_jobs,mode,[],[])}
        cheapest=min(frontier,key=lambda p:p.burden)
        selected=[cheapest]
        return {"mode":mode,"status":"SELECTED","frontier":[p.id for p in frontier],
                "selected":[cheapest.id],
                "decision_trace":_trace(state,packages,required_jobs,mode,frontier,selected)}
    if mode=="FIRE":
        return {"mode":mode,"status":"SELECTED" if frontier else "OPEN",
                "frontier":[p.id for p in frontier],"selected":[p.id for p in frontier],
                "decision_trace":_trace(state,packages,required_jobs,mode,frontier,frontier)}
    return {"mode":"OPEN","status":"OPEN","frontier":[],"selected":[],
            "decision_trace":_trace(state,packages,required_jobs,"OPEN",[],[])}

def needs_reselection(delta:dict[str,Any])->bool:
    keys={"material_result_delta","material_search_delta","new_OPEN","changed_job_identity",
          "changed_representation","failed_route","new_project_local_capability","changed_authority"}
    return any(bool(delta.get(k)) for k in keys)
