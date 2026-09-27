import sys
sys.path.insert(0,"runtime")
from recovered_tool_runtimes import *

def test_mta_contract():
    out=run_mta("T","B",["E"],"K",
        generate_structural_hypotheses=lambda *a:["h"],
        select_analysis_package=lambda *a:["p"],
        reconstruct_protected_model=lambda *a:{"Model":"m","Findings":[],"FactorBasis":[],"Residual":None,"MaterialDeltas":[],"DiscoveryDeltas":[],"NewOrChangedObjects":[],"Evidence":["E"],"Coverage":"bounded","VerificationObligations":[],"OPEN":[]})
    assert out["status"]=="RELATIVE_CLOSE"

def test_architecture_contract():
    keys=("ArchClass","Violations","LocalizationFamilies","DependencyState","InteractionState","TransformationFrontier","SuccessorFrontier","Coverage","OpenConflictBlocked","Provenance")
    out=run_architecture_analysis({}, {}, analyze_architecture=lambda a,k:{x:([] if x!="Coverage" else "bounded") for x in keys})
    assert out["status"]=="RELATIVE_CLOSE"

def test_pd_and_audit_sensitivity():
    cases=((0,0),(1,0),(1,1))
    rho=lambda x:x[0]
    approx=lambda a,b:a==b
    reps={"id":lambda x:x}
    pd=run_pd(cases,rho=rho,approx=approx,representations=reps)
    assert pd["status"]=="RELATIVE_CLOSE"
    assert (0,) in pd["result"]["minimal_sensitive"]["id"]
    au=run_pd_audit(cases,rho=rho,approx=approx,representations=reps)
    assert au["status"]=="RELATIVE_CLOSE"
    assert au["result"]["pair_difference_relation"]

def test_gdos_blocks_goal_pressure_leak():
    assert run_gdos("x",observe=lambda x,c:{"observations":["a"]})["status"]=="RELATIVE_CLOSE"
    assert run_gdos("x",observe=lambda x,c:{"observations":[],"selected_action":"rewrite"})["status"]=="BLOCKED"

def test_discriminator_preserves_open_without_direction_classifier():
    same=run_discriminator("a","b",run_route=lambda x:{"result":1,"trace":[x]},equivalent=lambda a,b:a==b)
    assert same["result"]["class"]=="PATH_ONLY"
    op=run_discriminator("a","b",run_route=lambda x:{"result":x},equivalent=lambda a,b:a==b)
    assert op["status"]=="OPEN"

def test_rtc_frontier_is_nondominated():
    out=run_rtc(0,generators=[lambda s:[1,2]],admissible=lambda a,b:True,preserve=lambda a,b:True,
        strict_gain=lambda a,b:b>a,dominates=lambda a,b:a>b)
    assert out["result"]["ResultFrontier"]==(2,)
    assert out["result"]["maximality_claim"] is False

def test_bias_perturbation_flags_unexplained_instability():
    variants={"BASELINE":{"x":1},"ANON":{"x":2}}
    out=run_bias_perturbation(variants,runner=lambda x:x,protected_decision=lambda x:x["x"])
    assert out["status"]=="OPEN"
    assert out["result"]["bias_signals"]

def test_multi_object_contract():
    out=run_multi_object([1,2],generate_relations=lambda xs:[(1,2)],reconcile_relations=lambda xs,r:{
      "RelationState":r,"LowerOrderSynthesis":r,"Reducibility":"OPEN","HigherOrderResidual":[],"CONFLICT":[],"OPEN":[]})
    assert out["status"]=="RELATIVE_CLOSE"

def test_diagnosis_parameterized_root():
    out=run_diagnosis({"B":[]},causal_support=lambda s:["a","b"],root_selector=lambda cs:["b"])
    assert out["status"]=="RELATIVE_CLOSE"
    assert out["result"]["DetState"]=="UNIQUE"
