import sys
sys.path.insert(0,"runtime")

from multiobject import (
    FrozenObject, RelationFinding, RouteResult, ResidualJudgment,
    ViewRequest, ReconciledFinding, run_multiobject,
)
from portable_tool_conductor import compilation_witness
from tool_manifest import manifest_for
from tool_run_registry import CONFIGURED_RUNS, PROTECTED_BEHAVIORS


def _objects():
    return (
        FrozenObject("A","THEORY","domain-a","target-a"),
        FrozenObject("B","RULE","domain-b","target-b"),
        FrozenObject("C","LAW","domain-c","target-c"),
    )


class Provider:
    def __init__(self, *, open_reconciliation=False, omit_residual=False):
        self.calls=[]
        self.open_reconciliation=open_reconciliation
        self.omit_residual=omit_residual

    def joint(self,objects,*,route_id):
        self.calls.append(("joint",tuple(o.object_id for o in objects)))
        return RouteResult(
            route_id,"FULL_JOINT",tuple(o.object_id for o in objects),
            (RelationFinding("joint-1",("A","B","C"),"COMPOSES_WITH",("joint",),("e-j",)),),
            isolation_receipt="isolated-joint",
        )

    def pair(self,left,right,*,route_id):
        self.calls.append(("pair",(left.object_id,right.object_id)))
        fid="pair-"+left.object_id+right.object_id
        return RouteResult(
            route_id,"PAIR",(left.object_id,right.object_id),
            (RelationFinding(fid,(left.object_id,right.object_id),"NO_LICENSED_RELATION",(),("e-"+fid,)),),
            isolation_receipt="isolated-"+fid,
        )

    def synthesize_pairs(self,pair_routes):
        self.calls.append(("synthesize",tuple(r.route_id for r in pair_routes)))
        return RouteResult(
            "PAIR_SYNTH","PAIR_SYNTHESIS",("A","B","C"),
            (RelationFinding("synth-1",("A","B","C"),"SHARED_DEPENDENCY",("pairs",),("e-s",)),),
            isolation_receipt="synthesis-barrier",
        )

    def challenge_reducibility(self,joint_route,pair_routes,pair_synthesis):
        self.calls.append(("challenge",joint_route.route_id))
        if self.omit_residual:
            return ()
        return (ResidualJudgment("joint-1","HIGHER_ORDER_RESIDUAL",("member-removal",)),)

    def triggered_views(self,objects,joint_route,pair_routes,pair_synthesis,residuals):
        self.calls.append(("triggered_views",len(residuals)))
        return (ViewRequest("direction-ab","DIRECTION",("A","B"),"asymmetry"),)

    def analyze_view(self,request,objects):
        self.calls.append(("view",request.view_id))
        return RouteResult(
            "VIEW:"+request.view_id,"VIEW",request.support,
            (RelationFinding("view-1",request.support,"SUPPORTS",("direction",),("e-v",)),),
            isolation_receipt="isolated-view",
        )

    def reconcile(self,pair_routes,pair_synthesis,joint_route,residuals,view_results):
        self.calls.append(("reconcile",len(view_results)))
        status="OPEN" if self.open_reconciliation else "JOINT_ONLY"
        return (
            ReconciledFinding("joint-1",status,("residual",)),
            ReconciledFinding("synth-1","PAIRWISE_ONLY",("pairs",)),
            ReconciledFinding("view-1","REFINEMENT",("view",)),
        )


def test_multiobject_rejects_provider_route_id_spoofing():
    class SpoofingProvider(Provider):
        def pair(self,left,right,*,route_id):
            route=super().pair(left,right,route_id=route_id)
            return RouteResult(
                "UNRELATED:"+route_id,route.route_kind,route.support,
                route.findings,route.status,route.isolation_receipt,
            )
    out=run_multiobject(_objects(),SpoofingProvider())
    assert out.status=="OPEN"
    assert out.blocker.startswith("MULTIOBJECT_ROUTE_ID_MISMATCH:")


def test_multiobject_requires_reconciliation_of_positive_pair_findings():
    class PositivePairProvider(Provider):
        def pair(self,left,right,*,route_id):
            route=super().pair(left,right,route_id=route_id)
            fid="positive-"+left.object_id+"-"+right.object_id
            return RouteResult(
                route.route_id,route.route_kind,route.support,
                (RelationFinding(fid,route.support,"SUPPORTS",("pair",),("e",)),),
                route.status,route.isolation_receipt,
            )
    out=run_multiobject(_objects(),PositivePairProvider())
    assert out.status=="OPEN"
    assert out.blocker=="MULTIOBJECT_RECONCILIATION_COVERAGE_INCOMPLETE"


def test_multiobject_executes_independent_joint_then_complete_pair_basis_and_views():
    provider=Provider()
    out=run_multiobject(_objects(),provider)
    assert out.status=="CLOSED_RELATIVE"
    assert len(out.state.pair_routes)==3
    assert provider.calls[0]==("joint",("A","B","C"))
    pair_calls=[x for x in provider.calls if x[0]=="pair"]
    assert {tuple(sorted(x[1])) for x in pair_calls}=={
        ("A","B"),("A","C"),("B","C")
    }
    assert out.state.joint_route.isolation_receipt=="isolated-joint"
    assert len(out.state.view_results)==1
    assert out.material_delta is True


def test_multiobject_requires_reducibility_judgment_for_every_joint_finding():
    out=run_multiobject(_objects(),Provider(omit_residual=True))
    assert out.status=="OPEN"
    assert out.blocker=="MULTIOBJECT_REDUCIBILITY_COVERAGE_INCOMPLETE"


def test_multiobject_preserves_open_reconciliation():
    out=run_multiobject(_objects(),Provider(open_reconciliation=True))
    assert out.status=="OPEN"
    assert out.blocker=="MULTIOBJECT_OPEN_PRESERVED"


def test_multiobject_fails_open_on_incomplete_provider():
    class Incomplete:
        pass
    out=run_multiobject(_objects(),Incomplete())
    assert out.status=="OPEN"
    assert out.blocker.startswith("MULTIOBJECT_PROVIDER_INCOMPLETE:")


def test_multiobject_requires_three_unique_typed_objects():
    out=run_multiobject(_objects()[:2],Provider())
    assert out.status=="OPEN"
    assert out.blocker=="MULTIOBJECT_REQUIRES_AT_LEAST_THREE_OBJECTS"


def test_multiobject_has_explicit_manifest_and_environment_bound_native_witness():
    protected=set(PROTECTED_BEHAVIORS["MultiObject"])
    manifest=manifest_for("MultiObject")
    assert protected <= set(manifest.behavior_ids())
    assert "MO_HIGHER_ORDER_RESIDUAL_TYPING" in protected
    assert "MO_MATERIAL_DELTA_REENTRY" in protected
    assert protected == set(manifest.behavior_ids()) - {"PROTECTED_TRANSITION_INTEGRITY", "CONFIGURED_HF2_RECURRENCE", "FULL_CONFIGURED_INVOCATION_PROFILE"}
    assert CONFIGURED_RUNS["MultiObject"].complete()
    assert manifest.lineage_contract=="architecture/MULTIOBJECT_FULL_TOOL_MATH_001_2026-09-27.md"

    witness=compilation_witness("MultiObject")
    assert witness.entrypoint=="multiobject.run_multiobject"
    assert witness.status=="PROGRAM_WITH_ENVIRONMENT"
    assert witness.required_environment==("multiobject_provider",)


def test_multiobject_second_identical_run_has_no_material_delta_when_signature_reused():
    first=run_multiobject(_objects(),Provider())
    assert first.recurrence_signature[0].startswith("MO_SIG_V2:")
    second=run_multiobject(_objects(),Provider(),previous_signature=first.recurrence_signature)
    assert second.status=="CLOSED_RELATIVE"
    assert second.material_delta is False


def test_multiobject_same_finding_id_with_changed_semantics_is_material():
    class ChangedSemanticsProvider(Provider):
        def joint(self,objects,*,route_id):
            original=super().joint(objects,route_id=route_id)
            f=original.findings[0]
            changed=RelationFinding(f.finding_id,f.support,"REFINES",f.grounds,("new-evidence",))
            return RouteResult(original.route_id,original.route_kind,original.support,
                               (changed,),original.status,original.isolation_receipt)
    first=run_multiobject(_objects(),Provider())
    changed=run_multiobject(_objects(),ChangedSemanticsProvider(),
                            previous_signature=first.recurrence_signature)
    assert first.status=="CLOSED_RELATIVE"
    assert changed.status=="CLOSED_RELATIVE"
    assert changed.state.joint_route.findings[0].finding_id=="joint-1"
    assert changed.material_delta is True
    assert changed.recurrence_signature!=first.recurrence_signature


def test_multiobject_changed_object_content_and_residual_grounds_are_material():
    first=run_multiobject(_objects(),Provider())
    objects=(FrozenObject("A","THEORY","domain-a","changed-target"),)+_objects()[1:]
    changed_object=run_multiobject(objects,Provider(),
        previous_signature=first.recurrence_signature)
    assert changed_object.status=="CLOSED_RELATIVE"
    assert changed_object.material_delta is True

    class ChangedGrounds(Provider):
        def challenge_reducibility(self,joint_route,pair_routes,pair_synthesis):
            return (ResidualJudgment("joint-1","HIGHER_ORDER_RESIDUAL",
                                     ("new-member-removal-proof",)),)
    changed_ground=run_multiobject(_objects(),ChangedGrounds(),
        previous_signature=first.recurrence_signature)
    assert changed_ground.status=="CLOSED_RELATIVE"
    assert changed_ground.material_delta is True
