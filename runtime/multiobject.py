"""Native MultiObject v0.2 orchestration core.

This runtime owns the recovered control semantics of MultiObject:
- freeze/validate >=3 distinct objects;
- an independent full-joint route;
- every currently required unordered pair route;
- lower-order synthesis;
- reducibility challenge for every joint finding;
- gated view expansion;
- typed reconciliation with OPEN/CONFLICT preservation.

Domain relation generation remains an explicit provider boundary.  The provider
must return route-isolation receipts; missing semantic machinery fails OPEN.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Any, Iterable, Protocol


ROUTE_STATUSES={"EXECUTED","OPEN","CONFLICT"}
RECONCILIATION_STATUSES={
    "CONVERGENT","PAIRWISE_ONLY","JOINT_ONLY","REFINEMENT","CONFLICT","OPEN"
}
RESIDUAL_STATUSES={
    "PAIRWISE_RECOVERABLE","ZERO_RELATIVE_RESIDUAL","EXPLAINED_RESIDUAL",
    "HIGHER_ORDER_RESIDUAL","OPEN_REDUCIBILITY","CONFLICT","OPEN"
}


@dataclass(frozen=True)
class FrozenObject:
    object_id:str
    semantic_type:str
    scope:str
    target:str
    primitives:tuple[str,...]=()
    dependencies:tuple[str,...]=()
    role:str=""
    outputs:tuple[str,...]=()
    open_coordinates:tuple[str,...]=()


@dataclass(frozen=True)
class RelationFinding:
    finding_id:str
    support:tuple[str,...]
    relation_type:str
    grounds:tuple[str,...]=()
    evidence:tuple[str,...]=()


@dataclass(frozen=True)
class RouteResult:
    route_id:str
    route_kind:str
    support:tuple[str,...]
    findings:tuple[RelationFinding,...]
    status:str="EXECUTED"
    isolation_receipt:str=""


@dataclass(frozen=True)
class ResidualJudgment:
    finding_id:str
    status:str
    grounds:tuple[str,...]=()


@dataclass(frozen=True)
class ViewRequest:
    view_id:str
    axis:str
    support:tuple[str,...]
    reason:str


@dataclass(frozen=True)
class ReconciledFinding:
    finding_id:str
    status:str
    grounds:tuple[str,...]=()


@dataclass(frozen=True)
class MultiObjectState:
    objects:tuple[FrozenObject,...]
    joint_route:RouteResult|None
    pair_routes:tuple[RouteResult,...]
    pair_synthesis:RouteResult|None
    residuals:tuple[ResidualJudgment,...]
    view_requests:tuple[ViewRequest,...]
    view_results:tuple[RouteResult,...]
    reconciliation:tuple[ReconciledFinding,...]


@dataclass(frozen=True)
class MultiObjectResult:
    status:str
    state:MultiObjectState
    blocker:str|None
    evidence:tuple[str,...]
    material_delta:bool

    @property
    def execution_truth(self)->str:
        if self.status=="CLOSED_RELATIVE":
            return "IMPLEMENTATION_EXECUTED"
        return self.status


class MultiObjectProvider(Protocol):
    def joint(
        self,
        objects:tuple[FrozenObject,...],
        *,
        route_id:str,
    )->RouteResult: ...

    def pair(
        self,
        left:FrozenObject,
        right:FrozenObject,
        *,
        route_id:str,
    )->RouteResult: ...

    def synthesize_pairs(
        self,
        pair_routes:tuple[RouteResult,...],
    )->RouteResult: ...

    def challenge_reducibility(
        self,
        joint_route:RouteResult,
        pair_routes:tuple[RouteResult,...],
        pair_synthesis:RouteResult,
    )->tuple[ResidualJudgment,...]: ...

    def triggered_views(
        self,
        objects:tuple[FrozenObject,...],
        joint_route:RouteResult,
        pair_routes:tuple[RouteResult,...],
        pair_synthesis:RouteResult,
        residuals:tuple[ResidualJudgment,...],
    )->tuple[ViewRequest,...]: ...

    def analyze_view(
        self,
        request:ViewRequest,
        objects:tuple[FrozenObject,...],
    )->RouteResult: ...

    def reconcile(
        self,
        pair_routes:tuple[RouteResult,...],
        pair_synthesis:RouteResult,
        joint_route:RouteResult,
        residuals:tuple[ResidualJudgment,...],
        view_results:tuple[RouteResult,...],
    )->tuple[ReconciledFinding,...]: ...


_REQUIRED_PROVIDER_METHODS=(
    "joint","pair","synthesize_pairs","challenge_reducibility",
    "triggered_views","analyze_view","reconcile",
)


def _empty_state(objects:tuple[FrozenObject,...]=())->MultiObjectState:
    return MultiObjectState(objects,None,(),None,(),(),(),())


def _open(
    objects:tuple[FrozenObject,...],
    blocker:str,
    *,
    state:MultiObjectState|None=None,
    evidence:Iterable[str]=(),
)->MultiObjectResult:
    return MultiObjectResult(
        "OPEN",
        state or _empty_state(objects),
        blocker,
        tuple(evidence),
        False,
    )


def _validate_objects(objects:tuple[FrozenObject,...])->str|None:
    if len(objects)<3:
        return "MULTIOBJECT_REQUIRES_AT_LEAST_THREE_OBJECTS"
    ids=[o.object_id for o in objects]
    if any(not x for x in ids):
        return "MULTIOBJECT_OBJECT_ID_REQUIRED"
    if len(ids)!=len(set(ids)):
        return "MULTIOBJECT_OBJECT_IDS_NOT_UNIQUE"
    for obj in objects:
        if not obj.semantic_type:
            return f"MULTIOBJECT_TYPE_REQUIRED:{obj.object_id}"
        if not obj.scope:
            return f"MULTIOBJECT_SCOPE_REQUIRED:{obj.object_id}"
        if not obj.target:
            return f"MULTIOBJECT_TARGET_REQUIRED:{obj.object_id}"
    return None


def _provider_gap(provider:Any)->tuple[str,...]:
    return tuple(
        name for name in _REQUIRED_PROVIDER_METHODS
        if not callable(getattr(provider,name,None))
    )


def _validate_route(
    route:RouteResult,
    *,
    expected_kind:str,
    expected_support:tuple[str,...],
)->str|None:
    if not isinstance(route,RouteResult):
        return "MULTIOBJECT_ROUTE_RESULT_REQUIRED"
    if route.route_kind!=expected_kind:
        return f"MULTIOBJECT_ROUTE_KIND_MISMATCH:{route.route_id}"
    if tuple(route.support)!=tuple(expected_support):
        return f"MULTIOBJECT_ROUTE_SUPPORT_MISMATCH:{route.route_id}"
    if route.status not in ROUTE_STATUSES:
        return f"MULTIOBJECT_ROUTE_STATUS_INVALID:{route.route_id}"
    if not route.isolation_receipt:
        return f"MULTIOBJECT_ISOLATION_RECEIPT_REQUIRED:{route.route_id}"
    seen=set()
    for finding in route.findings:
        if not isinstance(finding,RelationFinding):
            return f"MULTIOBJECT_FINDING_REQUIRED:{route.route_id}"
        if not finding.finding_id or finding.finding_id in seen:
            return f"MULTIOBJECT_FINDING_ID_INVALID:{route.route_id}"
        seen.add(finding.finding_id)
        if not set(finding.support)<=set(expected_support):
            return f"MULTIOBJECT_FINDING_SUPPORT_INVALID:{finding.finding_id}"
        if not finding.relation_type:
            return f"MULTIOBJECT_RELATION_TYPE_REQUIRED:{finding.finding_id}"
    return None


def _terminal_from_state(state:MultiObjectState)->tuple[str,str|None]:
    route_statuses=[
        r.status for r in (
            ((state.joint_route,) if state.joint_route else ())
            +state.pair_routes
            +((state.pair_synthesis,) if state.pair_synthesis else ())
            +state.view_results
        )
    ]
    recon_statuses=[r.status for r in state.reconciliation]
    residual_statuses=[r.status for r in state.residuals]

    if "CONFLICT" in route_statuses or "CONFLICT" in recon_statuses or "CONFLICT" in residual_statuses:
        return "CONFLICT","MULTIOBJECT_CONFLICT_PRESERVED"
    if (
        "OPEN" in route_statuses
        or "OPEN" in recon_statuses
        or "OPEN" in residual_statuses
        or "OPEN_REDUCIBILITY" in residual_statuses
    ):
        return "OPEN","MULTIOBJECT_OPEN_PRESERVED"
    return "CLOSED_RELATIVE",None


def run_multiobject(
    objects:Iterable[FrozenObject],
    provider:MultiObjectProvider|None,
    *,
    previous_signature:tuple[str,...]|None=None,
)->MultiObjectResult:
    """Execute the recovered MultiObject orchestration against a semantic provider."""
    frozen=tuple(objects)
    blocker=_validate_objects(frozen)
    if blocker:
        return _open(frozen,blocker)

    if provider is None:
        return _open(frozen,"MULTIOBJECT_PROVIDER_REQUIRED")
    gaps=_provider_gap(provider)
    if gaps:
        return _open(frozen,"MULTIOBJECT_PROVIDER_INCOMPLETE:"+",".join(gaps))

    object_ids=tuple(o.object_id for o in frozen)
    evidence=[]

    # The full-joint route is intentionally called before any pair result exists
    # and receives only the frozen object tuple. This enforces dataflow
    # independence from same-cycle lower-order findings.
    try:
        joint=provider.joint(frozen,route_id="JOINT:"+",".join(object_ids))
    except Exception as exc:
        return _open(frozen,f"MULTIOBJECT_JOINT_PROVIDER_ERROR:{type(exc).__name__}")
    blocker=_validate_route(
        joint,
        expected_kind="FULL_JOINT",
        expected_support=object_ids,
    )
    if blocker:
        return _open(frozen,blocker)
    evidence.append(joint.isolation_receipt)

    pair_routes=[]
    for left,right in combinations(frozen,2):
        support=(left.object_id,right.object_id)
        route_id="PAIR:"+left.object_id+"|"+right.object_id
        try:
            route=provider.pair(left,right,route_id=route_id)
        except Exception as exc:
            state=MultiObjectState(frozen,joint,tuple(pair_routes),None,(),(),(),())
            return _open(
                frozen,
                f"MULTIOBJECT_PAIR_PROVIDER_ERROR:{route_id}:{type(exc).__name__}",
                state=state,
                evidence=evidence,
            )
        blocker=_validate_route(route,expected_kind="PAIR",expected_support=support)
        if blocker:
            state=MultiObjectState(frozen,joint,tuple(pair_routes),None,(),(),(),())
            return _open(frozen,blocker,state=state,evidence=evidence)
        pair_routes.append(route)
        evidence.append(route.isolation_receipt)

    required_pairs={
        tuple(sorted((a.object_id,b.object_id)))
        for a,b in combinations(frozen,2)
    }
    actual_pairs={tuple(sorted(r.support)) for r in pair_routes}
    if actual_pairs!=required_pairs:
        state=MultiObjectState(frozen,joint,tuple(pair_routes),None,(),(),(),())
        return _open(frozen,"MULTIOBJECT_PAIR_COVERAGE_INCOMPLETE",state=state,evidence=evidence)

    try:
        synthesis=provider.synthesize_pairs(tuple(pair_routes))
    except Exception as exc:
        state=MultiObjectState(frozen,joint,tuple(pair_routes),None,(),(),(),())
        return _open(
            frozen,
            f"MULTIOBJECT_SYNTHESIS_PROVIDER_ERROR:{type(exc).__name__}",
            state=state,
            evidence=evidence,
        )
    blocker=_validate_route(
        synthesis,
        expected_kind="PAIR_SYNTHESIS",
        expected_support=object_ids,
    )
    if blocker:
        state=MultiObjectState(frozen,joint,tuple(pair_routes),None,(),(),(),())
        return _open(frozen,blocker,state=state,evidence=evidence)
    evidence.append(synthesis.isolation_receipt)

    try:
        residuals=tuple(provider.challenge_reducibility(
            joint,tuple(pair_routes),synthesis
        ))
    except Exception as exc:
        state=MultiObjectState(frozen,joint,tuple(pair_routes),synthesis,(),(),(),())
        return _open(
            frozen,
            f"MULTIOBJECT_REDUCIBILITY_PROVIDER_ERROR:{type(exc).__name__}",
            state=state,
            evidence=evidence,
        )

    residual_by_id={}
    for residual in residuals:
        if not isinstance(residual,ResidualJudgment):
            state=MultiObjectState(frozen,joint,tuple(pair_routes),synthesis,residuals,(),(),())
            return _open(frozen,"MULTIOBJECT_RESIDUAL_JUDGMENT_REQUIRED",state=state,evidence=evidence)
        if residual.status not in RESIDUAL_STATUSES:
            state=MultiObjectState(frozen,joint,tuple(pair_routes),synthesis,residuals,(),(),())
            return _open(
                frozen,
                f"MULTIOBJECT_RESIDUAL_STATUS_INVALID:{residual.finding_id}",
                state=state,
                evidence=evidence,
            )
        if residual.finding_id in residual_by_id:
            state=MultiObjectState(frozen,joint,tuple(pair_routes),synthesis,residuals,(),(),())
            return _open(
                frozen,
                f"MULTIOBJECT_DUPLICATE_RESIDUAL:{residual.finding_id}",
                state=state,
                evidence=evidence,
            )
        residual_by_id[residual.finding_id]=residual

    joint_ids={f.finding_id for f in joint.findings}
    if set(residual_by_id)!=joint_ids:
        state=MultiObjectState(frozen,joint,tuple(pair_routes),synthesis,residuals,(),(),())
        return _open(
            frozen,
            "MULTIOBJECT_REDUCIBILITY_COVERAGE_INCOMPLETE",
            state=state,
            evidence=evidence,
        )

    try:
        view_requests=tuple(provider.triggered_views(
            frozen,joint,tuple(pair_routes),synthesis,residuals
        ))
    except Exception as exc:
        state=MultiObjectState(frozen,joint,tuple(pair_routes),synthesis,residuals,(),(),())
        return _open(
            frozen,
            f"MULTIOBJECT_VIEW_TRIGGER_ERROR:{type(exc).__name__}",
            state=state,
            evidence=evidence,
        )

    view_results=[]
    seen_views=set()
    for request in view_requests:
        if not isinstance(request,ViewRequest) or not request.view_id or request.view_id in seen_views:
            state=MultiObjectState(
                frozen,joint,tuple(pair_routes),synthesis,residuals,
                view_requests,tuple(view_results),()
            )
            return _open(frozen,"MULTIOBJECT_VIEW_REQUEST_INVALID",state=state,evidence=evidence)
        seen_views.add(request.view_id)
        if not set(request.support)<=set(object_ids):
            state=MultiObjectState(
                frozen,joint,tuple(pair_routes),synthesis,residuals,
                view_requests,tuple(view_results),()
            )
            return _open(
                frozen,
                f"MULTIOBJECT_VIEW_SUPPORT_INVALID:{request.view_id}",
                state=state,
                evidence=evidence,
            )
        try:
            route=provider.analyze_view(request,frozen)
        except Exception as exc:
            state=MultiObjectState(
                frozen,joint,tuple(pair_routes),synthesis,residuals,
                view_requests,tuple(view_results),()
            )
            return _open(
                frozen,
                f"MULTIOBJECT_VIEW_PROVIDER_ERROR:{request.view_id}:{type(exc).__name__}",
                state=state,
                evidence=evidence,
            )
        blocker=_validate_route(
            route,
            expected_kind="VIEW",
            expected_support=tuple(request.support),
        )
        if blocker:
            state=MultiObjectState(
                frozen,joint,tuple(pair_routes),synthesis,residuals,
                view_requests,tuple(view_results),()
            )
            return _open(frozen,blocker,state=state,evidence=evidence)
        view_results.append(route)
        evidence.append(route.isolation_receipt)

    try:
        reconciliation=tuple(provider.reconcile(
            tuple(pair_routes),synthesis,joint,residuals,tuple(view_results)
        ))
    except Exception as exc:
        state=MultiObjectState(
            frozen,joint,tuple(pair_routes),synthesis,residuals,
            view_requests,tuple(view_results),()
        )
        return _open(
            frozen,
            f"MULTIOBJECT_RECONCILIATION_PROVIDER_ERROR:{type(exc).__name__}",
            state=state,
            evidence=evidence,
        )

    recon_by_id={}
    for row in reconciliation:
        if not isinstance(row,ReconciledFinding):
            state=MultiObjectState(
                frozen,joint,tuple(pair_routes),synthesis,residuals,
                view_requests,tuple(view_results),reconciliation
            )
            return _open(frozen,"MULTIOBJECT_RECONCILIATION_ROW_REQUIRED",state=state,evidence=evidence)
        if row.status not in RECONCILIATION_STATUSES:
            state=MultiObjectState(
                frozen,joint,tuple(pair_routes),synthesis,residuals,
                view_requests,tuple(view_results),reconciliation
            )
            return _open(
                frozen,
                f"MULTIOBJECT_RECONCILIATION_STATUS_INVALID:{row.finding_id}",
                state=state,
                evidence=evidence,
            )
        if row.finding_id in recon_by_id:
            state=MultiObjectState(
                frozen,joint,tuple(pair_routes),synthesis,residuals,
                view_requests,tuple(view_results),reconciliation
            )
            return _open(
                frozen,
                f"MULTIOBJECT_DUPLICATE_RECONCILIATION:{row.finding_id}",
                state=state,
                evidence=evidence,
            )
        recon_by_id[row.finding_id]=row

    material_ids={f.finding_id for f in synthesis.findings}|joint_ids
    material_ids.update(
        f.finding_id for route in view_results for f in route.findings
    )
    if not material_ids<=set(recon_by_id):
        state=MultiObjectState(
            frozen,joint,tuple(pair_routes),synthesis,residuals,
            view_requests,tuple(view_results),reconciliation
        )
        return _open(
            frozen,
            "MULTIOBJECT_RECONCILIATION_COVERAGE_INCOMPLETE",
            state=state,
            evidence=evidence,
        )

    state=MultiObjectState(
        frozen,joint,tuple(pair_routes),synthesis,residuals,
        view_requests,tuple(view_results),reconciliation
    )
    status,blocker=_terminal_from_state(state)

    signature=tuple(sorted(
        [
            f"PAIR:{r.route_id}:{r.status}:"+",".join(f.finding_id for f in r.findings)
            for r in pair_routes
        ]
        +[
            "JOINT:"+joint.status+":"+",".join(f.finding_id for f in joint.findings),
            "SYNTH:"+synthesis.status+":"+",".join(f.finding_id for f in synthesis.findings),
        ]
        +[
            "RESID:"+x.finding_id+":"+x.status for x in residuals
        ]
        +[
            "VIEW:"+r.route_id+":"+r.status+":"+",".join(f.finding_id for f in r.findings)
            for r in view_results
        ]
        +[
            "RECON:"+x.finding_id+":"+x.status for x in reconciliation
        ]
    ))
    material_delta=previous_signature is None or signature!=tuple(previous_signature)

    return MultiObjectResult(
        status,
        state,
        blocker,
        tuple(dict.fromkeys(evidence)),
        material_delta,
    )
