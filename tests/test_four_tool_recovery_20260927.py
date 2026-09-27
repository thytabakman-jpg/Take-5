import sys
sys.path.insert(0,"runtime")

from architecture_analysis import run_architecture_analysis
from mta import run_mta
from pd import run_pd
from pd_audit import run_pd_audit
from portable_tool_conductor import compilation_witness
from tool_manifest import OVERRIDES, manifest_for
from tool_manifest_audit import audit_tool_identities
from tool_reality_audit import audit_tool_reality
from tool_run_registry import CONFIGURED_RUNS


def test_mta_native_contract_preserves_open():
    base=dict(
        Model="m",Findings=(),FactorBasis=("f",),Residual=None,
        MaterialDeltas=(),DiscoveryDeltas=(),NewOrChangedObjects=(),
        Evidence=("e",),Coverage="bounded",VerificationObligations=(),OPEN=(),
    )
    out=run_mta(
        "T","B",("E",),"K",
        generate_structural_hypotheses=lambda *a:("h",),
        select_analysis_package=lambda *a:("p",),
        reconstruct_protected_model=lambda *a:base,
    )
    assert out["status"]=="RELATIVE_CLOSE"
    opened=dict(base,OPEN=("generator coverage",))
    out=run_mta(
        "T","B",("E",),"K",
        generate_structural_hypotheses=lambda *a:("h",),
        select_analysis_package=lambda *a:("p",),
        reconstruct_protected_model=lambda *a:opened,
    )
    assert out["status"]=="OPEN"


def test_architecture_native_contract_preserves_boundary_state():
    result={
        "ArchClass":"typed","Violations":(),"LocalizationFamilies":(),
        "DependencyState":(),"InteractionState":(),"TransformationFrontier":(),
        "SuccessorFrontier":(),"Coverage":"bounded","OpenConflictBlocked":(),
        "Provenance":("e",),
    }
    out=run_architecture_analysis({}, {}, analyze_architecture=lambda a,k:result)
    assert out["status"]=="RELATIVE_CLOSE"
    opened=dict(result,OpenConflictBlocked=("OPEN",))
    out=run_architecture_analysis({}, {}, analyze_architecture=lambda a,k:opened)
    assert out["status"]=="OPEN"


def test_pd_minimal_sensitivity_and_representation_collapse_are_distinct():
    cases=((0,0),(1,0),(1,1))
    out=run_pd(
        cases,
        rho=lambda x:x[0],
        approx=lambda a,b:a==b,
        representations={"id":lambda x:x},
    )
    assert out["status"]=="RELATIVE_CLOSE"
    assert (0,) in out["result"]["minimal_sensitive"]["id"]
    assert out["result"]["representation_collapse"]==()

    collapsed=run_pd(
        (("a",0),("b",1)),
        rho=lambda x:x[1],
        approx=lambda a,b:a==b,
        representations={"collapsed":lambda x:(0,)},
    )
    assert () in collapsed["result"]["minimal_sensitive"]["collapsed"]
    assert collapsed["result"]["representation_collapse"]==("collapsed",)


def test_pdaudit_preserves_fixed_frame_and_control_separations():
    out=run_pd_audit(
        ((0,0),(1,0),(1,1)),
        rho=lambda x:x[0],
        approx=lambda a,b:a==b,
        representations={"id":lambda x:x},
        kappa_cases=lambda xs:"cases-covered",
        kappa_representations=lambda reps:"representations-covered",
    )
    assert out["status"]=="RELATIVE_CLOSE"
    r=out["result"]
    assert r["raw_output_immutable"] is True
    assert r["normalization_separate"] is True
    assert r["analytic_eligibility_separate_from_governance"] is True
    assert r["zero_incremental_yield_visible"] is True


def test_four_recovered_tools_have_explicit_manifests_and_environment_bound_native_entrypoints():
    expected={
        "MTA":"MTA_STRUCTURAL_MODEL_RECONSTRUCTION",
        "Architecture":"ARCHITECTURE_CONTRACT_RELATIVE_ANALYSIS",
        "PD":"PD_MINIMAL_RESULT_SENSITIVITY",
        "PDAudit":"PDAUDIT_FRAME_FIBER_SENSITIVITY",
    }
    for tool_id,behavior in expected.items():
        assert tool_id in OVERRIDES
        manifest=manifest_for(tool_id)
        assert manifest.complete()
        assert behavior in manifest.behavior_ids()
        witness=compilation_witness(tool_id)
        assert witness.entrypoint is not None
        assert witness.required_environment
        assert witness.status=="PROGRAM_WITH_ENVIRONMENT"


def test_current_finite_repertoire_strong_tool_reality_closes_relative():
    manifests=audit_tool_identities(CONFIGURED_RUNS,OVERRIDES)
    assert manifests.status=="CLOSED_RELATIVE"
    assert manifests.generic_only==()

    audit=audit_tool_reality()
    assert audit.configured_identity_status=="CLOSED_RELATIVE"
    assert audit.explicit_manifest_status=="CLOSED_RELATIVE"
    assert audit.native_execution_status=="CLOSED_RELATIVE"
    assert audit.generic_only==()
    assert audit.native_unrecovered==()
    assert audit.status=="CLOSED_RELATIVE"
