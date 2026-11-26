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

from dataclasses import asdict, dataclass
from itertools import combinations
import json
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
    recurrence_signature:tuple[str,...]=()

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
    if any(not isinstance(o,FrozenObject) for o in objects):
        return "MULTIOBJECT_FROZEN_OBJECT_REQUIRED"
    ids=[o.object_id for o in objects]
    if any(not isinstance(x,str) or not x.strip() for x in ids):
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
    expected_route_id:str|None=None,
)->str|None:
    if not isinstance(route,RouteResult):
        return "MULTIOBJECT_ROUTE_RESULT_REQUIRED"
    if not isinstance(route.route_id,str) or not route.route_id.strip():
        return "MULTIOBJECT_ROUTE_ID_REQUIRED"
    if expected_route_id is not None and route.route_id!=expected_route_id:
        return f"MULTIOBJECT_ROUTE_ID_MISMATCH:{route.route_id}"
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
        if (not finding.support or len(set(finding.support))!=len(finding.support)
                or not set(finding.support)<=set(expected_support)):
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
        any(obj.open_coordinates for obj in state.objects)
        or "OPEN" in route_statuses
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
        expected_route_id="JOINT:"+",".join(object_ids),
    )
    if blocker:
        return _open(frozen,blocker)
    evidence.append(joint.isolation_receipt)

    pair_routes=[]
    route_ids={joint.route_id}
    for left,right in combinations(frozen,2):
        support=(left.object_id,right.object_id)
        route_id="PAIR:"+left.object_id+"|"+right.object_id
        if route_id in route_ids:
            state=MultiObjectState(frozen,joint,tuple(pair_routes),None,(),(),(),())
            return _open(frozen,"MULTIOBJECT_PAIR_ROUTE_ID_COLLISION",state=state,evidence=evidence)
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
        blocker=_validate_route(
            route,expected_kind="PAIR",expected_support=support,
            expected_route_id=route_id,
        )
        if blocker:
            state=MultiObjectState(frozen,joint,tuple(pair_routes),None,(),(),(),())
            return _open(frozen,blocker,state=state,evidence=evidence)
        pair_routes.append(route)
        route_ids.add(route.route_id)
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
    # Synthesis is a distinct route, not an alias for the independent joint
    # route or an individual pair. Its name remains provider-defined, but it
    # cannot reuse an existing route identity.
    if synthesis.route_id in route_ids:
        state=MultiObjectState(frozen,joint,tuple(pair_routes),synthesis,(),(),(),())
        return _open(frozen,"MULTIOBJECT_SYNTHESIS_ROUTE_ID_COLLISION",state=state,evidence=evidence)
    route_ids.add(synthesis.route_id)
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
        # A triggered view without a documented discriminator is not a
        # licensed branch. Empty support, axis or reason cannot establish
        # provenance, even if the provider later fabricates a VIEW receipt.
        if not request.axis or not request.reason or not request.support:
            state=MultiObjectState(
                frozen,joint,tuple(pair_routes),synthesis,residuals,
                view_requests,tuple(view_results),()
            )
            return _open(frozen,"MULTIOBJECT_VIEW_PROVENANCE_REQUIRED",state=state,evidence=evidence)
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
            expected_route_id="VIEW:"+request.view_id,
        )
        if blocker:
            state=MultiObjectState(
                frozen,joint,tuple(pair_routes),synthesis,residuals,
                view_requests,tuple(view_results),()
            )
            return _open(frozen,blocker,state=state,evidence=evidence)
        if route.route_id in route_ids:
            state=MultiObjectState(
                frozen,joint,tuple(pair_routes),synthesis,residuals,
                view_requests,tuple(view_results),()
            )
            return _open(frozen,"MULTIOBJECT_VIEW_ROUTE_ID_COLLISION",state=state,evidence=evidence)
        view_results.append(route)
        route_ids.add(route.route_id)
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

    # Positive pair findings must survive lower-order reconciliation.
    # NO_LICENSED_RELATION stays recorded in the pair ledger.
    material_ids={f.finding_id for f in synthesis.findings}|joint_ids
    material_ids.update(
        f.finding_id for route in pair_routes for f in route.findings
        if f.relation_type!="NO_LICENSED_RELATION"
    )
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

    # A finding ID is a locator, not a content hash. Include semantic types,
    # evidence, grounds, object packets and all typed route/judgment fields so a
    # same-ID changed result cannot be mistaken for an HF002 fixed point.
    # The versioned signature prevents accidental equivalence to the historical
    # identifier-only recurrence signatures.
    signature=("MO_SIG_V2:"+json.dumps(
        asdict(state),sort_keys=True,separators=(",",":"),
    ),)
    material_delta=previous_signature is None or signature!=tuple(previous_signature)

    return MultiObjectResult(
        status,
        state,
        blocker,
        tuple(dict.fromkeys(evidence)),
        material_delta,
        signature,
    )

class DeclaredReferenceProvider:
    """Finite relation algebra over explicit source-reference edges.

    The joint route computes from frozen objects before any pair routes exist.
    Pair routes see only their two objects. Reconciliation reconstructs joint
    direct links, common-reference groups and cyclic components from pair facts.
    No semantic dependency, causal relation or irreducible higher-order claim
    follows from a static reference.
    """
    def __init__(self, objects, source_evidence):
        self.ids=tuple(o.object_id for o in objects)
        self.source_evidence=dict(source_evidence)

    def _finding(self, prefix, support, relation, grounds):
        key=json.dumps([relation,list(support),list(grounds)],separators=(',',':'))
        return RelationFinding(prefix+':'+key,tuple(support),relation,tuple(grounds),
                               tuple(self.source_evidence[x] for x in support))

    def joint(self, objects, *, route_id):
        from architecture_analysis import cyclic_components
        ids=tuple(o.object_id for o in objects)
        graph={o.object_id:tuple(o.dependencies) for o in objects}
        findings=[]
        for source in ids:
            for target in sorted(set(graph[source]) & set(ids)):
                support=tuple(x for x in ids if x in (source,target))
                findings.append(self._finding('JOINT',support,'DECLARED_REFERENCE',(source,target)))
        targets=sorted({t for deps in graph.values() for t in deps})
        for target in targets:
            support=tuple(x for x in ids if target in graph[x])
            if len(support)>1:
                findings.append(self._finding('JOINT',support,'COMMON_REFERENCE_TARGET',(target,)))
        for members in cyclic_components(graph):
            # Self-links are direct facts, not a multi-object interaction.
            if len(members)>1:
                support=tuple(x for x in ids if x in members)
                findings.append(self._finding('JOINT',support,'DECLARED_REFERENCE_CYCLE',tuple(sorted(members))))
        return RouteResult(route_id,'FULL_JOINT',ids,tuple(findings),
                           isolation_receipt='direct-frozen-reference-graph:'+json.dumps(graph,sort_keys=True))

    def pair(self,left,right,*,route_id):
        support=(left.object_id,right.object_id)
        findings=[]
        for source,target in ((left,right),(right,left)):
            if target.object_id in source.dependencies:
                findings.append(self._finding(route_id,support,'DECLARED_REFERENCE',
                                              (source.object_id,target.object_id)))
        # Self-edges are witnessed on every incident pair with singleton support.
        for obj in (left,right):
            if obj.object_id in obj.dependencies:
                findings.append(self._finding(route_id,(obj.object_id,),'DECLARED_REFERENCE',
                                              (obj.object_id,obj.object_id)))
        for target in sorted(set(left.dependencies)&set(right.dependencies)):
            findings.append(self._finding(route_id,support,'COMMON_REFERENCE_TARGET',(target,)))
        return RouteResult(route_id,'PAIR',support,tuple(findings),
                           isolation_receipt='isolated-two-object-reference-data:'+json.dumps(
                               [(o.object_id,o.dependencies) for o in (left,right)]))

    def synthesize_pairs(self,pair_routes):
        findings=tuple(f for route in pair_routes for f in route.findings)
        return RouteResult('REFERENCE-PAIR-UNION','PAIR_SYNTHESIS',self.ids,findings,
                           isolation_receipt='pair-only-reference-union:'+json.dumps([r.route_id for r in pair_routes]))

    def challenge_reducibility(self,joint_route,pair_routes,pair_synthesis):
        from architecture_analysis import cyclic_components
        direct=set()
        common={}
        for f in pair_synthesis.findings:
            if f.relation_type=='DECLARED_REFERENCE':
                direct.add(f.grounds)
            elif f.relation_type=='COMMON_REFERENCE_TARGET':
                common.setdefault(f.grounds[0],set()).add(frozenset(f.support))
        graph={x:[] for x in self.ids}
        for source,target in direct:
            graph[source].append(target)
        cycles={frozenset(c) for c in cyclic_components(graph) if len(c)>1}
        results=[]
        for f in joint_route.findings:
            if f.relation_type=='DECLARED_REFERENCE':
                matches=f.grounds in direct
            elif f.relation_type=='COMMON_REFERENCE_TARGET':
                required={frozenset(p) for p in combinations(f.support,2)}
                matches=required==common.get(f.grounds[0],set())
            elif f.relation_type=='DECLARED_REFERENCE_CYCLE':
                matches=frozenset(f.support) in cycles
            else:
                matches=False
            results.append(ResidualJudgment(f.finding_id,
                'PAIRWISE_RECOVERABLE' if matches else 'OPEN_REDUCIBILITY',
                ('reconstructed from isolated pair reference facts' if matches else 'unreconstructed joint reference finding',)))
        return tuple(results)

    def triggered_views(self,*args):
        # No additional view is licensed by this explicit reference algebra.
        # Broader semantic view adequacy remains OPEN on the frozen objects.
        return ()

    def analyze_view(self,*args):
        raise ValueError('NO_DECLARED_REFERENCE_VIEW_TRIGGER')

    def reconcile(self,pair_routes,pair_synthesis,joint_route,residuals,view_results):
        return tuple(ReconciledFinding(f.finding_id,'PAIRWISE_ONLY',
                                      ('retained isolated reference witness',))
                     for f in pair_synthesis.findings)+tuple(
            ReconciledFinding(r.finding_id,'CONVERGENT' if r.status=='PAIRWISE_RECOVERABLE' else 'OPEN',r.grounds)
            for r in residuals)

