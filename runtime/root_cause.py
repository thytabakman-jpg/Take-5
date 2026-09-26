"""RootCause — recurring-failure generator analysis with HF2 recurrence.

The native target is not "a cause". It is the smallest stable upstream generator
that explains the protected recurring failure class under the frozen basis.

This module supplies a typed orchestration substrate. Domain intelligence is
provided as evidence/candidate records, not invented by the controller.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Iterable

from hf002_recursive_continuation import HF002RecursiveContinuation

ROOT_LEVELS=(
    "SYMPTOM",
    "LOCAL_MECHANISM",
    "ENABLING_CONDITION",
    "OWNERSHIP_CONFIGURATION",
    "REPRESENTATION_TRANSITION",
    "ROOT_GENERATOR",
)

@dataclass(frozen=True)
class RootCandidate:
    candidate_id:str
    level:str
    explains:frozenset[str]
    evidence:frozenset[str]=frozenset()
    counterevidence:frozenset[str]=frozenset()
    upstream_of:frozenset[str]=frozenset()
    survives_representation_change:bool=False
    removal_breaks_recurrence:bool=False
    unresolved:frozenset[str]=frozenset()

    def root_score_vector(self, recurrence_class:frozenset[str])->tuple:
        return (
            recurrence_class <= self.explains,
            self.survives_representation_change,
            self.removal_breaks_recurrence,
            len(self.upstream_of),
            -len(self.counterevidence),
            -len(self.unresolved),
        )


@dataclass(frozen=True)
class RootCauseResult:
    status:str
    root_candidates:tuple[str,...]
    rejected_candidates:tuple[str,...]
    unresolved:tuple[str,...]
    rounds:int
    state:dict
    trace:tuple[dict,...]
    parent_handoff:dict


def _dominates(a:RootCandidate,b:RootCandidate,recurrence:frozenset[str])->bool:
    av=a.root_score_vector(recurrence)
    bv=b.root_score_vector(recurrence)
    return all(x>=y for x,y in zip(av,bv)) and any(x>y for x,y in zip(av,bv))


def nondominated_candidates(candidates:Iterable[RootCandidate],recurrence:frozenset[str]):
    xs=tuple(candidates)
    return tuple(
        c for c in xs
        if not any(_dominates(other,c,recurrence) for other in xs if other.candidate_id!=c.candidate_id)
    )


def root_admissible(candidate:RootCandidate,recurrence:frozenset[str])->bool:
    return bool(
        recurrence <= candidate.explains
        and candidate.survives_representation_change
        and candidate.removal_breaks_recurrence
        and not candidate.counterevidence
        and not candidate.unresolved
    )


def run_root_cause_hf2(
    *,
    failure_class:Iterable[str],
    candidates:Iterable[RootCandidate],
    basis_id:str,
    max_rounds:int=8,
)->RootCauseResult:
    recurrence=frozenset(failure_class)
    original={c.candidate_id:c for c in candidates}
    if not recurrence:
        return RootCauseResult(
            "OPEN",(),(),("FAILURE_CLASS_UNFROZEN",),0,{},(),
            {"controller":"ImprovementCore","action":"RECONSTRUCT_FAILURE_CLASS"},
        )
    if not original:
        return RootCauseResult(
            "OPEN",(),(),("NO_CAUSAL_CANDIDATES",),0,{},(),
            {"controller":"ImprovementCore","action":"GENERATE_RIVALS"},
        )

    initial={
        "basis_id":basis_id,
        "round":0,
        "active_ids":tuple(original),
        "root_ids":(),
        "rejected_ids":(),
        "unresolved":("ROOT_DISCRIMINATION_PENDING",),
        "closed":False,
    }

    def capability(state,memory):
        active=[original[x] for x in state["active_ids"]]
        frontier=nondominated_candidates(active,recurrence)

        rejected=sorted(set(original)-{x.candidate_id for x in frontier})
        roots=[x.candidate_id for x in frontier if root_admissible(x,recurrence)]

        unresolved=[]
        for c in frontier:
            if not recurrence<=c.explains:
                unresolved.append(f"{c.candidate_id}:RECURRENCE_COVERAGE")
            if not c.survives_representation_change:
                unresolved.append(f"{c.candidate_id}:REPRESENTATION_STABILITY")
            if not c.removal_breaks_recurrence:
                unresolved.append(f"{c.candidate_id}:COUNTERFACTUAL_REMOVAL")
            unresolved.extend(f"{c.candidate_id}:{u}" for u in sorted(c.unresolved))
            if c.counterevidence:
                unresolved.append(f"{c.candidate_id}:COUNTEREVIDENCE")

        # Same-capability second pass attacks "root" candidates with a smaller-generator challenge.
        round_no=int(state.get("round",0))
        if roots and round_no==0:
            unresolved.append("SMALLER_GENERATOR_CHALLENGE_PENDING")

        return {
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "frontier_ids":tuple(x.candidate_id for x in frontier),
            "root_ids":tuple(sorted(roots)),
            "rejected_ids":tuple(rejected),
            "unresolved":tuple(sorted(set(unresolved))),
            "round":round_no+1,
        }

    def normalize(raw,state,memory):
        nxt=dict(state)
        before=(state.get("active_ids"),state.get("root_ids"),state.get("unresolved"))
        nxt["round"]=raw["round"]
        nxt["active_ids"]=raw["frontier_ids"]
        nxt["root_ids"]=raw["root_ids"]
        nxt["rejected_ids"]=raw["rejected_ids"]
        unresolved=list(raw["unresolved"])
        if nxt["round"]>=2:
            unresolved=[x for x in unresolved if x!="SMALLER_GENERATOR_CHALLENGE_PENDING"]
        nxt["unresolved"]=tuple(unresolved)
        nxt["closed"]=bool(nxt["root_ids"]) and not nxt["unresolved"]
        after=(nxt["active_ids"],nxt["root_ids"],nxt["unresolved"])
        return nxt,{
            "material_result_delta":before!=after,
            "material_search_delta":state.get("round",0)==0,
            "material_discovery_delta":bool(set(nxt["root_ids"])-set(state.get("root_ids",()))),
            "changed_representation":tuple(state.get("active_ids",()))!=tuple(nxt["active_ids"]),
            "route_equivalence":"ROOT_CAUSE:"+",".join(nxt["active_ids"]),
        }

    def trc(pre,post,delta):
        return {"terminal":True}

    def hf1(pre,post,delta):
        return {"disposition":"STABLE"}

    def live(state,memory):
        return not state.get("closed",False) and state.get("round",0)<2

    def close(state,memory):
        return bool(state.get("closed",False))

    hf2=HF002RecursiveContinuation(
        capability,normalize,trc,hf1,live,close,max_rounds=max_rounds
    )
    local=hf2.run(initial,{})
    state=local["state"]

    if local["status"]=="RELATIVE_CLOSE":
        status="RELATIVE_CLOSE"
    elif local["status"]=="RESOURCE_STOP":
        status="OPEN"
    else:
        status=local["status"]

    roots=tuple(state.get("root_ids",()))
    rejected=tuple(state.get("rejected_ids",()))
    unresolved=tuple(state.get("unresolved",()))
    parent={
        "controller":"ImprovementCore",
        "action":"ADMIT_ROOT_CAUSE_AND_REPLAN" if roots and not unresolved else "REENTER_DISCOVERY",
        "basis_id":basis_id,
        "root_candidates":roots,
        "unresolved":unresolved,
        "local_status":local["status"],
    }
    return RootCauseResult(
        status,roots,rejected,unresolved,len(local.get("trace",())),
        state,tuple(local.get("trace",())),parent
    )
