"""Mathematical spine for ImprovementCore.

This module realizes strict-gain mathematics recovered across Take-2, Take-4,
Reaserch, Take-5, and prior ImproveCore/HF work:

1. hard admissibility precedes preference;
2. routing is set-valued over a nondominated frontier, not scalar argmax;
3. OPEN/BLOCKED/CONFLICT remain first-class;
4. representation sufficiency is continuation-relative;
5. discovery, representation, evidence, or authority deltas can reopen work;
6. cumulative verified contributions must remain reachable unless explicitly
   revised or retracted.

It does not replace domain/tool semantics. It constrains controller choice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence


NON_SUCCESS={"OPEN","BLOCKED","CONFLICT","INCOMPARABLE"}
FAILED_MEMORY={"NO_GAIN","REJECTED","FAILED"}


@dataclass(frozen=True)
class ControllerOption:
    option_id:str
    goal_gain:float=0.0
    information_gain:float=0.0
    search_gain:float=0.0
    cost:float=0.0
    risk:float=0.0
    reversible:bool=True
    preserves_protected:bool=True
    authorized:bool=True
    reachable:bool=True
    status:str="CANDIDATE"
    metadata:Mapping[str,Any]=field(default_factory=dict)


@dataclass(frozen=True)
class FrontierResult:
    admissible:tuple[ControllerOption,...]
    nondominated:tuple[ControllerOption,...]
    rejected:tuple[tuple[str,str],...]


@dataclass(frozen=True)
class ClosureInput:
    trc_status:str
    basis_current:bool
    live_frontier:bool
    material_delta:bool
    open_coordinates:tuple[str,...]=()
    blocked_coordinates:tuple[str,...]=()
    conflict_coordinates:tuple[str,...]=()


@dataclass(frozen=True)
class Contribution:
    contribution_id:str
    verified:bool=True
    reachable:bool=True
    status:str="ACTIVE"


def _dominates(a:ControllerOption,b:ControllerOption)->bool:
    """Pareto dominance with gain up, cost/risk down, reversibility preferred."""
    av=(a.goal_gain,a.information_gain,a.search_gain,-a.cost,-a.risk,int(a.reversible))
    bv=(b.goal_gain,b.information_gain,b.search_gain,-b.cost,-b.risk,int(b.reversible))
    ge=all(x>=y for x,y in zip(av,bv))
    gt=any(x>y for x,y in zip(av,bv))
    return ge and gt


def nondominated_frontier(options:Iterable[ControllerOption])->FrontierResult:
    admissible=[]
    rejected=[]
    for o in options:
        if not o.authorized:
            rejected.append((o.option_id,"UNAUTHORIZED")); continue
        if not o.preserves_protected:
            rejected.append((o.option_id,"PROTECTED_BEHAVIOR_REGRESSION")); continue
        if not o.reachable:
            rejected.append((o.option_id,"UNREACHABLE")); continue
        if o.status in NON_SUCCESS:
            rejected.append((o.option_id,f"NON_SUCCESS:{o.status}")); continue
        admissible.append(o)

    nd=[]
    for o in admissible:
        if not any(_dominates(other,o) for other in admissible if other.option_id!=o.option_id):
            nd.append(o)
    return FrontierResult(tuple(admissible),tuple(nd),tuple(rejected))


def representation_sufficient(
    representation_classes:Sequence[frozenset[Any]],
    protected_equivalence_classes:Sequence[frozenset[Any]],
)->bool:
    """Finite witness for ker(q) subseteq protected continuation equivalence.

    Every representation class must sit wholly inside one protected equivalence class.
    """
    protected=tuple(protected_equivalence_classes)
    return all(any(rc<=pc for pc in protected) for rc in representation_classes)


def closure_disposition(x:ClosureInput)->str:
    """Basis-relative closure, not resource-limit closure."""
    if x.blocked_coordinates:
        return "BLOCKED"
    if x.conflict_coordinates:
        return "CONFLICT"
    if x.open_coordinates:
        return "OPEN"
    if x.trc_status!="CLOSED":
        return "OPEN"
    if not x.basis_current:
        return "RETURN_REENTER"
    if x.material_delta or x.live_frontier:
        return "CONTINUE"
    return "RELATIVE_CLOSE"


def reopen_required(delta:Mapping[str,Any])->bool:
    return bool(
        delta.get("material_result_delta")
        or delta.get("material_search_delta")
        or delta.get("material_discovery_delta")
        or delta.get("changed_representation")
        or delta.get("changed_candidate_universe")
        or delta.get("changed_scope_relevance")
        or delta.get("changed_mode_frontier")
        or delta.get("changed_authority")
        or delta.get("changed_evidence")
        or delta.get("changed_runtime_reality")
        or delta.get("open_refinement")
        or delta.get("negative_evidence")
    )


def cumulative_preservation(
    before:Iterable[Contribution],
    after:Iterable[Contribution],
    explicit_revision:Iterable[str]=(),
)->tuple[bool,tuple[str,...]]:
    """Longitudinal anti-loss condition from cumulative-autonomy mathematics."""
    old={x.contribution_id:x for x in before if x.verified and x.status=="ACTIVE"}
    new={x.contribution_id:x for x in after}
    revised=set(explicit_revision)
    lost=[]
    for cid in old:
        if cid in revised:
            continue
        nxt=new.get(cid)
        if nxt is None or not nxt.verified or not nxt.reachable or nxt.status!="ACTIVE":
            lost.append(cid)
    return (not lost,tuple(sorted(lost)))
