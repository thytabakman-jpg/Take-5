"""Exhaustive development sweep of the organized tool-system project.

Claim levels stay separate:
1. full_invocation_portfolio proves every registered identity traverses the
   configured wrapper/36/Q22/cognitive/HF2 route using a synthetic route witness;
2. ToolConductor attempts every registered factor once. C01-C49 and learning
   operators receive project-grounded development fixtures; named tools without
   safe semantic bindings remain OPEN rather than being simulated;
3. ProjectManager receives the actual project-file control surface;
4. repository development audits judge identity, invocation, transitions,
   maturity, reality, system closure, and package reality.

The receipt is evidence. It is not mutation authority.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, is_dataclass
import json
from pathlib import Path
from typing import Any

from current_portfolio_identity import audit_current_portfolio_identity
from full_invocation_portfolio import audit_full_invocation_portfolio
from portable_tool_conductor import run_tool_conductor
from project_manager import CORE_COORDINATES, assess_project
from project_manager_integrity import FAILURE_CONTROL_IDS, ROOT_INVARIANT_IDS
from protected_transition_portfolio import audit_protected_transition_portfolio
from system_audit import run_audit, audit_audits
from historical_replay_audit import audit_historical_replays
from repertoire_reachability import audit_current_repertoire_reachability
from system_cleanup_campaign import run_cleanup_campaign
from tool_manifest import OVERRIDES
from tool_manifest_audit import audit_tool_identities
from tool_maturity import audit_all as audit_maturity
from tool_project_packages import audit_materialized
from tool_reality_audit import audit_tool_reality
from tool_run_registry import CONFIGURED_RUNS, MATERIAL_TOOLS
from learning_operator_tools import FunctionalStackState,OODAState,RateDistortionCandidate
from improvement_core_dispatch import dispatch_improvement_core
from ic028_operator import GOAL_DIRECTED_STAGES
from icc128_autonomous_controller import ICC128Controller
from mt_semantic_return_gate import run_mt_with_before_return_gate
from mta import run_mta
from architecture_analysis import run_architecture_analysis
from pd import run_pd
from pd_audit import run_pd_audit
from gdos import run_gdos
from discriminator import run_discriminator
from reconcile import reconcile
from delegation import delegate
from hf1_episode import HF1Execution, HF1Closure, run_hf1_episode
from hf002_recursive_continuation import HF002RecursiveContinuation
from root_cause import RootCandidate, run_root_cause_hf2
from tool_run_closure import Consequence, ConsumerState, Disposition, StageResult, run_tool_run_closure
from raise_the_ceiling import raise_the_ceiling
from bias_perturbation import run_bias_perturbation
from currentness_audit import assess as assess_currentness
from capability_foundry import CapabilityFoundry, CapabilitySpec, CapabilityType
from emergent_admission import ObjectCandidate, admit as admit_emergent
from historical_reconstruction import ReconstructionCase, compare as compare_historical
from zero_request_episode import zero_request_episode
from multiobject import (
    FrozenObject, RelationFinding, RouteResult, ResidualJudgment,
    ReconciledFinding, run_multiobject,
)
from diagnosis import diagnose
from assert_compound import AssertState, AssertStages, run_to_fixed_point
from goal import GoalCandidate, GoalObject, recover_goal
from solution_to_my_problem import Problem, Candidate, SolutionReceipt, solve
from prose import ProseContract, ProseEvidence, assess_prose
from desired_jane import DesireEvidence, recover_desired_jane
from question_worth_asking import QuestionCandidate, select_question
from lambda_math import EntryState, reconstruct as reconstruct_lambda
from semantic_resolution_pipeline import plan_black_box_resolution
from recursive_compiler import CompilerNode, evaluate_global_closure


ROOT=Path(__file__).resolve().parents[1]
PROJECT_ROOT=ROOT/"projects"/"tool-system"


def plain(value:Any)->Any:
    if is_dataclass(value):
        return {k:plain(v) for k,v in asdict(value).items()}
    if isinstance(value,dict):
        return {str(k):plain(v) for k,v in value.items()}
    if isinstance(value,(list,tuple,set,frozenset)):
        return [plain(v) for v in value]
    if isinstance(value,Path):
        return str(value)
    if callable(value):
        return getattr(value,"__name__",type(value).__name__)
    return value


def project_summary()->dict[str,Any]:
    package=audit_materialized(ROOT)
    files=sorted(p.name for p in PROJECT_ROOT.iterdir() if p.is_file())
    return {
        "target":"projects/tool-system",
        "package_audit":package,
        "root_files":files,
        "registered_tools":len(MATERIAL_TOOLS),
    }


def capability_inputs(summary:dict[str,Any])->dict[str,dict[str,Any]]:
    protected=("ONE_OWNER","APPEND_ONLY","NO_SILENT_OVERWRITE","TWO_36_SEPARATE")
    candidate={"id":"current-organization","preserves":list(protected)}
    source_effects=list(protected)
    target_effects=list(protected)+["EVERY_TOOL_SWEEP"]
    inputs={
        "C01":{"admissible_typings":["TOOL_SYSTEM_PROJECT"]},
        "C02":{"same_lineage":True},
        "C03":{"versions":[{"id":"main","authoritative":True}]},
        "C04":{"source_id":"integration/CURRENT_TOOL_PROJECT_ORGANIZATION.md","claim":"non-destructive anti-loss project organization"},
        "C05":{"target":"projects/tool-system","protected":list(protected)},
        "C06":{"dependencies":[
            {"id":"tool_run_registry","availability":True},
            {"id":"tool_manifest","availability":True},
            {"id":"project_packages","availability":True},
        ]},
        "C07":{"candidate_edges":[{"source":"registry","target":"packages","material":True}]},
        "C08":{"spines":[["registry","manifest","package","validation"]]},
        "C09":{"edges":[{"source":"registry","target":"package-index","relation_type":"AUTHORITY_PROJECTION"}]},
        "C10":{"representations":[{"id":"docs","result":"separate-authorities"},{"id":"runtime","result":"separate-authorities"}]},
        "C11":{"coordinates":[{"id":"authority","changed_result":True},{"id":"history","changed_result":True},{"id":"font","changed_result":False}]},
        "C12":{"sensitivity_maps":[["authority","history"],["authority","history","coverage"]]},
        "C13":{"edges":[{"source":"finding","target":"owner","attribution":"AUTHORITY_REGISTRY"}]},
        "C14":{"findings":[],"interaction_findings":[]},
        "C15":{"source_effects":source_effects,"target_effects":target_effects,"different_terms":False},
        "C16":{"protected":list(protected),"candidates":[candidate]},
        "C17":{"failures":[]},
        "C18":{"causal_chain":[{"id":"single-owner-rule","evidence":True,"terminal":True}]},
        "C19":{"seed_frontier":["project"],"graph":{"project":["packages","regression"],"packages":["coverage"],"regression":[],"coverage":[]}},
        "C20":{"rivals":[{"id":"monolith"},{"id":"owned-packages"}]},
        "C21":{"candidates":[candidate]},
        "C22":{"improvement_frontier":[candidate]},
        "C23":{"typed_relation":{"source":"Sukkos-pattern","target":"tool-system","type":"EVIDENCE_TRANSFER_WITH_LOCAL_ADMISSION"}},
        "C24":{"repaired_candidate":candidate,"protected":list(protected),"preserves":list(protected)},
        "C25":{"equivalent_candidate":candidate,"protected":list(protected),"preserves":list(protected)},
        "C26":{"architecture_successor":candidate,"protected":list(protected),"preserves":list(protected)},
        "C27":{"subsystem_successor":candidate,"protected":list(protected),"preserves":list(protected)},
        "C28":{"component_successor":candidate,"protected":list(protected),"preserves":list(protected)},
        "C29":{"interface_successor":candidate,"protected":list(protected),"preserves":list(protected)},
        "C30":{"boundary_successor":candidate,"protected":list(protected),"preserves":list(protected)},
        "C31":{"synchronized_architecture":candidate,"protected":list(protected),"preserves":list(protected)},
        "C32":{"routes":[{"id":"package-owner-route","licensed":True,"reachable":True}]},
        "C33":{"strict_gain":True,"preserves":list(protected)},
        "C34":{"protected_before":list(protected),"protected_after":list(protected)},
        "C35":{"nondominated_set":[candidate]},
        "C36":{"affected_update":{"target":"project-control","scope":"local"}},
        "C37":{"provenance_chain":["Sukkos","tool-system","validated-main"]},
        "C38":{"license_disposition":"USER_AUTHORIZED_PROJECT_ORGANIZATION"},
        "C39":{"target_effect":{"target":"projects/tool-system","effect":"ORGANIZATION_ONLY"}},
        "C40":{"coverage":{"current_tools":summary["package_audit"]["current_tool_count"],"cells_per_package":36}},
        "C41":{"rescue_disposition":"REENTER_ON_NEW_TOOL_OR_VARIANT"},
        "C42":{"transfer_status":"EVIDENCE_ONLY"},
        "C43":{"handoff":{"from":"audit","to":"canonical-owner"}},
        "C44":{"expected":"NO_SILENT_OVERWRITE","actual":"NO_SILENT_OVERWRITE"},
        "C45":{"preregistered":True,"pass":True},
        "C46":{"with_component":"collision-detected","without_component":"silent-overwrite"},
        "C47":{"blocking_open":[]},
        "C48":{"candidates":[]},
        "C49":{"visited":[
            {"id":"projects/tool-system","task_relevant":True},
            {"id":"runtime/tool_project_packages.py","task_relevant":True},
            {"id":"runtime/tool_run_registry.py","task_relevant":True},
        ]},
    }
    return inputs


def learning_inputs(summary:dict[str,Any])->dict[str,dict[str,Any]]:
    state={"project":"tool-system","registered_tools":summary["registered_tools"]}
    return {
        "L-D6":{
            "state":state,
            "sense":lambda x:{**x,"sensed":True},
            "d4":lambda x:{**x,"d4":"separate-owned-dimensions"},
            "ground":lambda x:{**x,"grounded_in":"repository"},
        },
        "L-D8":{
            "state":state,
            "sense":lambda x:{**x,"sensed":True},
            "orient":lambda x:{**x,"orientation":"anti-loss"},
            "d4":lambda x:{**x,"d4":"separate-owned-dimensions"},
            "ground":lambda x:{**x,"grounded_in":"repository"},
            "prune":lambda x:{**x,"pruned":"duplicate-authority"},
        },
        "L-KOLB":{
            "experience":"project-organization-migration",
            "reflect":lambda x:"overwrites-regressions-and-loss-are-primary-failures",
            "abstract":lambda x:"one-owner-plus-append-only-plus-regression",
            "experiment":lambda x:"per-object-packages-and-coverage-cells",
            "enact":lambda x:"validated-tool-system-project",
        },
        "L-DIKW":{
            "data":summary,
            "context":"Take-5 tool organization",
            "contextualize":lambda d,c:{"data":d,"context":c},
            "models":["monolith","single-owner-packages"],
            "description_length":lambda m,i: 2.0 if m=="monolith" else 1.0,
            "actions":["rewrite","route-local-change"],
            "expected_utility":lambda m,a: 2.0 if a=="route-local-change" else 0.0,
        },
        "L-PP":{
            "observation":summary["package_audit"]["status"],
            "model":{"prediction":"CLOSED_RELATIVE"},
            "predict":lambda m:m["prediction"],
            "prediction_error":lambda obs,pred:0 if obs==pred else 1,
            "revise":lambda m,obs,err:({**m,"last_error":err},float(err)),
        },
        "L-BAYES":{
            "prior":{"organized":0.8,"regressed":0.2},
            "likelihood":{"organized":0.95,"regressed":0.05},
        },
        "L-ACTIVE-INFERENCE":{
            "policies":["local-change","clean-rebuild"],
            "expected_free_energy":lambda p:0.1 if p=="local-change" else 2.0,
        },
        "L-ACTOR-CRITIC":{
            "reward":1.0,"discount":0.9,"value_now":0.5,"value_next":0.7,
            "value_parameters":{"v":0.5},"policy_parameters":{"p":"local-change"},
            "critic_update":lambda p,d:{**p,"delta":d},
            "actor_update":lambda p,d:{**p,"delta":d},
        },
        "L-RATE-DISTORTION":{
            "candidates":[
                RateDistortionCandidate("single-owner-index",1.0,0.0),
                RateDistortionCandidate("duplicate-everything",3.0,0.0),
            ],
            "max_distortion":0.0,
        },
        "L-OODA":{
            "state":OODAState(world=summary,orientation="anti-loss"),
            "observe":lambda w:w["package_audit"]["status"],
            "orient":lambda obs,old:{"old":old,"observed":obs},
            "decide":lambda o:"preserve-local-authority",
            "act":lambda world,decision:{**world,"development_decision":decision},
        },
        "L-FUNCTIONAL-STACK":{
            "state":FunctionalStackState("registry","packages","two-36-surfaces","ICC"),
            "input_layer":lambda s:"registry-observation",
            "operational_layer":lambda s:"package-audit",
            "structural_layer":lambda s:"separate-authority-surfaces",
            "executive_layer":lambda s:"fail-closed-reentry",
        },
    }


def actual_project_manager_input()->dict[str,Any]:
    # Only coordinates with a concrete project-level owner are admitted here.
    owner_candidates={
        "identity":"README.md",
        "charter":"PROJECT_CHARTER.md",
        "goal":"GOAL.md",
        "scope":"PROJECT_CHARTER.md",
        "authority":"AUTHORITY_REGISTRY.md",
        "stakeholders":"STAKEHOLDERS.md",
        "deliverables":"WBS.md",
        "schedule":"SCHEDULE.md",
        "resources":"RESOURCES.md",
        "dependencies":"SOURCE_MAP.md",
        "interfaces":"TWO_36_SURFACES.md",
        "raid":"RAID.md",
        "questions":"OPEN_QUESTIONS.md",
        "evidence":"BACKFILL_LEDGER.md",
        "decisions":"DECISION_LOG.md",
        "lessons":"LESSONS_LEDGER.md",
        "changes":"CHANGE_CONTROL.md",
        "lifecycle":"CURRENT_STATE.md",
        "verification":"REGRESSION_CONTRACT.md",
        "communications":"COMMUNICATIONS.md",
        "handoffs":"TWO_36_SURFACES.md",
    }
    coordinates={}
    authority={}
    for coordinate,file_name in owner_candidates.items():
        if (PROJECT_ROOT/file_name).is_file():
            coordinates[coordinate]={"status":"CURRENT","owner":file_name}
            authority[coordinate]=file_name
    failure_controls={
        control:{
            "status":"CURRENT",
            "owner":"projects/tool-system/REGRESSION_CONTRACT.md",
            "evidence":(
                "projects/tool-system/AUTHORITY_REGISTRY.md",
                "projects/tool-system/CURRENT_STATE.md",
                "projects/tool-system/REGRESSION_CONTRACT.md",
            ),
            "tests":("tests/test_tool_system_every_tool_sweep.py",),
        }
        for control in FAILURE_CONTROL_IDS
    }
    root_invariants={
        root:{
            "status":"CURRENT",
            "owner":"projects/tool-system/REGRESSION_CONTRACT.md",
            "evidence":(
                "integration/CURRENT_TOOL_PROJECT_ORGANIZATION.md",
                "projects/tool-system/REGRESSION_CONTRACT.md",
            ),
            "tests":("tests/test_tool_system_every_tool_sweep.py",),
        }
        for root in ROOT_INVARIANT_IDS
    }
    return {
        "project_id":"take5-tool-system",
        "coordinates":coordinates,
        "authority_registry":authority,
        "failure_controls":failure_controls,
        "root_invariants":root_invariants,
        "evidence_refs":(
            "integration/CURRENT_TOOL_PROJECT_ORGANIZATION.md",
            "projects/tool-system/BACKFILL_LEDGER.md",
        ),
    }


def project_manager_adapter(packet:dict[str,Any])->dict[str,Any]:
    assessment=assess_project(actual_project_manager_input())
    return {
        "status":"EXECUTED" if assessment.status=="CLOSED_RELATIVE" else assessment.status,
        "execution_truth":"IMPLEMENTATION_EXECUTED",
        "result":plain(assessment),
        "material_delta":False,
        "evidence":("runtime/project_manager.py","projects/tool-system/"),
    }



def _dev_executed(native:Any, *, evidence:str)->dict[str,Any]:
    return {
        "status":"EXECUTED",
        "execution_truth":"IMPLEMENTATION_EXECUTED",
        "result":plain(native),
        "material_delta":False,
        "evidence":(evidence,),
    }


def _improvement_core_adapter(packet:dict[str,Any])->dict[str,Any]:
    handlers={}
    for stage in GOAL_DIRECTED_STAGES:
        def fn(state,stage=stage):
            return {
                "state":{**state,stage:True},
                "material_delta":stage=="EXECUTE",
                "supervisory_relevant":False,
            }
        handlers[stage]=fn
    handlers["REENTER"]=lambda state:{"state":state,"terminal":True}
    _,out=dispatch_improvement_core(
        "ImproveCore, inspect the tool-system organization",
        target="projects/tool-system",
        job="development audit",
        basis="every-tool-sweep",
        state={},
        handlers=handlers,
        hf2_enabled=False,
        allow_ungated_debug=True,
    )
    return _dev_executed(out,evidence="native:ImprovementCore")


def _icc128_adapter(packet:dict[str,Any])->dict[str,Any]:
    def gq(z,m):
        return [] if z["step"]>=2 else [{"id":f"q{z['step']}","target":"tool-system"}]
    def gw(q,z,m):
        return [{"id":"w:"+x["id"],"job":"inspect organization"} for x in q]
    def select(q,w,z,m):
        return w[:1]
    def execute(selected,z,m):
        return [{"id":x["id"],"finding":"organization-evidence"} for x in selected]
    def admit(results,z,m):
        return {"material_result_delta":bool(results),"results":results}
    def update(z,m,d):
        z=dict(z);m=dict(m);z["step"]+=1
        if z["step"]>=2:
            z["terminal"]="COMPLETE";z["admitted_continuation"]=False
        else:
            z["terminal"]="CONTINUE";z["admitted_continuation"]=True
        m[f"step{z['step']}"]=d
        return z,m
    out=ICC128Controller(gq,gw,select,execute,admit,update,max_iterations=4).run(
        {"step":0,"terminal":"CONTINUE","admitted_continuation":True},{}
    )
    return _dev_executed(out,evidence="native:ICC128")


def _mt_adapter(packet:dict[str,Any])->dict[str,Any]:
    state={"target":"projects/tool-system","package_status":packet["project_summary"]["package_audit"]["status"]}
    out=run_mt_with_before_return_gate(
        state,
        run_mt=lambda s:(s,{"target":"projects/tool-system","finding":"organized-project-under-development-sweep"}),
        detect_black_boxes=lambda s,r:(),
        execute_stage=lambda tool_id,object_id,s:(s,"CLOSED_RELATIVE",False),
    )
    return _dev_executed(out,evidence="native:MT")


def _mta_adapter(packet:dict[str,Any])->dict[str,Any]:
    def reconstruct(target,hypotheses,package,shared_math,evidence,contract):
        return {
            "Model":"single-owner non-destructive project packages",
            "Findings":("separate authority from projection","append-only evidence"),
            "FactorBasis":("authority","history","coverage","validation"),
            "Residual":(),
            "MaterialDeltas":(),
            "DiscoveryDeltas":(),
            "NewOrChangedObjects":(),
            "Evidence":("projects/tool-system/","runtime/tool_project_packages.py"),
            "Coverage":"current registered repertoire",
            "VerificationObligations":("registry parity","overwrite guard"),
            "OPEN":(),
        }
    out=run_mta(
        "projects/tool-system",
        {"two_36_surfaces":True},
        ("tool-system project","validation receipts"),
        {"protected":("one-owner","append-only","no-overwrite")},
        generate_structural_hypotheses=lambda *args:("owned-package architecture",),
        select_analysis_package=lambda *args:("authority","history","regression"),
        reconstruct_protected_model=reconstruct,
    )
    return _dev_executed(out,evidence="native:MTA")


def _architecture_adapter(packet:dict[str,Any])->dict[str,Any]:
    def analyze(a,k):
        return {
            "ArchClass":"NON_DESTRUCTIVE_PROJECT_PACKAGE_OVERLAY",
            "Violations":(),
            "LocalizationFamilies":("current-tools","icc-variants"),
            "DependencyState":("registry->packages","manifest->source-map"),
            "InteractionState":("coverage!=handoff",),
            "TransformationFrontier":(),
            "SuccessorFrontier":(),
            "Coverage":"93 current tools plus recovered variant inventory",
            "OpenConflictBlocked":(),
            "Provenance":("projects/tool-system","integration/CURRENT_TOOL_PROJECT_ORGANIZATION.md"),
        }
    out=run_architecture_analysis(
        {"target":"projects/tool-system"},
        {"protected":("one-owner","append-only","no-overwrite")},
        analyze_architecture=analyze,
    )
    return _dev_executed(out,evidence="native:Architecture")


def _pd_adapter(packet:dict[str,Any])->dict[str,Any]:
    cases=((0,0),(1,0),(1,1))
    out=run_pd(
        cases,
        rho=lambda x:x[0],
        approx=lambda a,b:a==b,
        representations={"organization-coordinate":lambda x:x},
    )
    return _dev_executed(out,evidence="native:PD")


def _pdaudit_adapter(packet:dict[str,Any])->dict[str,Any]:
    cases=((0,0),(1,0),(1,1))
    out=run_pd_audit(
        cases,
        rho=lambda x:x[0],
        approx=lambda a,b:a==b,
        representations={"organization-coordinate":lambda x:x},
        kappa_cases=lambda xs:{"case_count":len(xs)},
        kappa_representations=lambda reps:{"representation_count":len(reps)},
    )
    return _dev_executed(out,evidence="native:PDAudit")


def _gdos_adapter(packet:dict[str,Any])->dict[str,Any]:
    target=packet["project_summary"]
    out=run_gdos(
        target,
        observers=(
            lambda x:{"package_status":x["package_audit"]["status"]},
            lambda x:{"registered_tools":x["registered_tools"]},
            lambda x:{"root_file_count":len(x["root_files"])},
        ),
        reconcile_fn=lambda rows:{"observations":rows,"agreement":"NO_MUTATION"},
    )
    return _dev_executed(out,evidence="native:GDOS")


def _discriminator_adapter(packet:dict[str,Any])->dict[str,Any]:
    out=run_discriminator(
        ("single-owner-packages","rewrite-monolith"),
        lambda x:x=="single-owner-packages",
    )
    return _dev_executed(out,evidence="native:Discriminator")


def _reconciler_adapter(packet:dict[str,Any])->dict[str,Any]:
    out=reconcile(
        {"project":"tool-system"},
        ({"finding":"package parity"},{"finding":"project-control complete"}),
        lambda state,results:{
            **state,
            "admitted_evidence":results,
            "conflicts":(),
            "open_coordinates":(),
        },
    )
    return _dev_executed(out,evidence="native:Reconciler")


def _delegated_executor_adapter(packet:dict[str,Any])->dict[str,Any]:
    out,receipt=delegate(
        episode="every-tool-sweep",
        program_id="TOOL_SYSTEM_READ_ONLY_CHECK",
        authority_in=frozenset({"observe","verify"}),
        authority_local=frozenset({"observe"}),
        payload={"project":"tool-system","status":packet["project_summary"]["package_audit"]["status"]},
        worker=lambda payload:{"observed":payload,"mutation":False},
    )
    return _dev_executed({"output":out,"receipt":receipt},evidence="native:DelegatedExecutor")


def _hf1_adapter(packet:dict[str,Any])->dict[str,Any]:
    initial={
        "identity":"tool-system","type":"PROJECT","scope":"SYSTEM","job":"VERIFY",
        "readings":(),"result_sensitive":("organization",),"selectors":(),
        "authority":"OBSERVE","provenance":"Take-5","open":(),
        "obligations":("VERIFY_ORGANIZATION",),
        "world_state":"stable","discovery_state":"stable","result_sensitive_state":"stable",
    }
    def execute_fn(package,mode,current):
        nxt=dict(current)
        nxt["obligations"]=()
        return HF1Execution(nxt,{"package":package,"mode":mode},True,True)
    def closure_fn(execution,current):
        return HF1Closure(execution.packet,"CLOSED")
    out=run_hf1_episode(
        initial,
        package_index={"dev-verify":("VERIFY_ORGANIZATION",)},
        mode_flags={"exact_discriminant":True,"independent_local":True},
        execute_fn=execute_fn,
        closure_fn=closure_fn,
        max_rounds=3,
    )
    return _dev_executed(out,evidence="native:HF001")


def _hf2_adapter(packet:dict[str,Any])->dict[str,Any]:
    hf2=HF002RecursiveContinuation(
        run_capability=lambda s,m:{
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":{"project":"tool-system","verified":True},
        },
        admit_normalize=lambda raw,s,m:(dict(s),{
            "material_result_delta":False,
            "route_equivalence":"tool-system-dev-hf2",
        }),
        trc_verify=lambda pre,post,delta:{"terminal":True},
        hf1_classify=lambda pre,post,delta:{"disposition":"STABLE"},
        live_local=lambda s,m:False,
        local_close=lambda s,m:True,
        max_rounds=2,
    )
    out=hf2.run({"project":"tool-system"},{})
    return _dev_executed(out,evidence="native:HF002")


def _root_cause_adapter(packet:dict[str,Any])->dict[str,Any]:
    candidate=RootCandidate(
        "single-owner-control",
        "ROOT_GENERATOR",
        frozenset({"PROJECT_CONTROL_GAP"}),
        evidence=frozenset({"first-sweep-projectmanager-receipt"}),
        survives_representation_change=True,
        removal_breaks_recurrence=True,
    )
    out=run_root_cause_hf2(
        failure_class=("PROJECT_CONTROL_GAP",),
        candidates=(candidate,),
        basis_id="tool-system-every-tool",
    )
    return _dev_executed(out,evidence="native:RootCause")


def _trc_adapter(packet:dict[str,Any])->dict[str,Any]:
    q=Consequence(
        "tool-system-project-control",
        "VERIFY",
        "CURRENT",
        "PROJECT_LOCAL",
        "every-tool-sweep",
        "ANTI_LOSS",
    )
    out=run_tool_run_closure(
        tool_result={"finding":"project-control-complete"},
        pre_state={},
        post_state={},
        harvest_fn=lambda r,p,s:(q,),
        disposition_fn=lambda c,s:Disposition.REALIZE,
        realize_fn=lambda c,s:StageResult(s,"COMPLETED_UNVERIFIED",evidence=("realized",)),
        verify_fn=lambda c,s:StageResult(s,"VERIFIED",evidence=("verified",)),
        consume_fn=lambda c,s:StageResult(s,ConsumerState.CONSUMED.value,evidence=("consumed",)),
        harvest_basis="EVERY_TOOL_SWEEP",
        harvest_complete=True,
    )
    return _dev_executed(out,evidence="native:TRC")


def _rtc_adapter(packet:dict[str,Any])->dict[str,Any]:
    out=raise_the_ceiling({
        "candidates":[{
            "id":"native-every-tool-development-bindings",
            "strict_gain":True,
            "preserves":("anti-loss","single-owner","append-only"),
        }]
    })
    return _dev_executed(out,evidence="native:RTC")


def _bias_adapter(packet:dict[str,Any])->dict[str,Any]:
    target={"owner":"single","surface":"docs"}
    perturbations=(
        {"owner":"single","surface":"yaml"},
        {"owner":"single","surface":"markdown"},
    )
    out=run_bias_perturbation(
        target,perturbations,
        runner=lambda x:x["owner"],
        semantics_equivalent=lambda a,b:a["owner"]==b["owner"],
        result_equivalent=lambda a,b:a==b,
    )
    return _dev_executed(out,evidence="native:BiasPerturbation")


def _currentness_adapter(packet:dict[str,Any])->dict[str,Any]:
    out=assess_currentness(
        component="projects/tool-system",
        built_basis="current-main",
        latest_basis="current-main",
        protected=("one-owner","append-only","no-overwrite"),
        delta=(),
        evidence=("every-tool-sweep",),
        reverified=True,
    )
    return _dev_executed(out,evidence="native:CurrentnessAudit")


def _foundry_adapter(packet:dict[str,Any])->dict[str,Any]:
    candidate=CapabilitySpec(
        capability_id="DEV_ORGANIZATION_OBSERVER",
        capability_type=CapabilityType.BEHAVIOR,
        trigger="tool-system development sweep",
        input_contract="project summary",
        transform="observe -> compare -> report",
        output_contract="evidence-only development finding",
        success="finding consumed or typed OPEN",
        failure="OPEN",
        persistence="EPHEMERAL",
    )
    out=CapabilityFoundry().evaluate(
        candidate,
        functionally_subsumed=lambda a,b:False,
        material_goal_gain=lambda c:True,
        architecture_compatible=lambda c:True,
    )
    return _dev_executed(out,evidence="native:CapabilityFoundry")


def _emergent_adapter(packet:dict[str,Any])->dict[str,Any]:
    out=admit_emergent(ObjectCandidate(
        object_id="TOOL_UMBRELLA_ALIAS",
        object_type="SEMANTIC_OBJECT",
        load_bearing=True,
        known_equivalent="TERM:TOOL",
    ))
    return _dev_executed({"disposition":out},evidence="native:EmergentAdmission")


def _historical_adapter(packet:dict[str,Any])->dict[str,Any]:
    case=ReconstructionCase(
        historical_id="pre-package-tool-organization",
        successor_id="projects/tool-system",
        frozen_job="prevent document overwrite and loss",
        protected=("single-owner","append-only","open-preservation"),
        predecessor_result={"intent":"preserve"},
        successor_result={"intent":"preserve"},
        predecessor_witness="Sukkos authority/change-control pattern",
        successor_witness="every-tool project validation",
        context="tool-system organization",
    )
    return _dev_executed(compare_historical(case),evidence="native:HistoricalReconstruction")


def _zero_request_adapter(packet:dict[str,Any])->dict[str,Any]:
    out=zero_request_episode(
        ("projects/tool-system","runtime/tool_project_packages.py"),
        lambda corpus,binding:{
            "objects":len(corpus),
            "structural":("authority-registry","per-object-packages","regression"),
            "observation_only":binding.observation_only,
        },
    )
    return _dev_executed(out,evidence="native:ZeroRequest")


class _ToolSystemMultiProvider:
    def joint(self,objects,*,route_id):
        return RouteResult(
            route_id,"FULL_JOINT",tuple(o.object_id for o in objects),
            (RelationFinding("joint-1",tuple(o.object_id for o in objects),"COORDINATED_ANTI_LOSS",("joint",),("tool-system",)),),
            isolation_receipt="isolated-joint",
        )
    def pair(self,left,right,*,route_id):
        return RouteResult(route_id,"PAIR",(left.object_id,right.object_id),(),isolation_receipt="isolated-"+route_id)
    def synthesize_pairs(self,pair_routes):
        return RouteResult(
            "PAIR_SYNTH","PAIR_SYNTHESIS",
            ("REGISTRY","PACKAGES","VALIDATION"),
            (RelationFinding("synth-1",("REGISTRY","PACKAGES","VALIDATION"),"SHARED_DEPENDENCY",("pairs",),("tool-system",)),),
            isolation_receipt="pair-synthesis",
        )
    def challenge_reducibility(self,joint_route,pair_routes,pair_synthesis):
        return (ResidualJudgment("joint-1","HIGHER_ORDER_RESIDUAL",("whole-system interaction",)),)
    def triggered_views(self,objects,joint_route,pair_routes,pair_synthesis,residuals):
        return ()
    def analyze_view(self,request,objects):
        raise AssertionError("no view requested")
    def reconcile(self,pair_routes,pair_synthesis,joint_route,residuals,view_results):
        return (
            ReconciledFinding("joint-1","JOINT_ONLY",("higher-order anti-loss coupling",)),
            ReconciledFinding("synth-1","PAIRWISE_ONLY",("pair synthesis",)),
        )


def _multiobject_adapter(packet:dict[str,Any])->dict[str,Any]:
    objects=(
        FrozenObject("REGISTRY","REGISTRY","SYSTEM","current tool inventory"),
        FrozenObject("PACKAGES","PROJECT_STRUCTURE","SUBSYSTEM","per-object durable state"),
        FrozenObject("VALIDATION","VERIFICATION","INTERFACE","regression gate"),
    )
    out=run_multiobject(objects,_ToolSystemMultiProvider())
    return _dev_executed(out,evidence="native:MultiObject")


def _diagnosis_adapter(packet:dict[str,Any])->dict[str,Any]:
    out=diagnose({
        "failures":[{
            "id":"missing-project-control-coordinate",
            "material":True,
            "mechanism":"organization inherited earlier project pattern before ProjectManager 21-coordinate contract",
        }]
    })
    return _dev_executed(out,evidence="native:Diagnosis")


def _assert_adapter(packet:dict[str,Any])->dict[str,Any]:
    stages=AssertStages(
        assert_stage=lambda s:s,
        compare_stage=lambda s:s,
        resolve_stage=lambda s:s,
        here_stage=lambda s:s,
        inquire_stage=lambda s:s,
        reassert_stage=lambda s:s,
    )
    out=run_to_fixed_point(AssertState(),stages,max_rounds=3)
    return _dev_executed(out,evidence="native:ASSERT")


def _goal_adapter(packet:dict[str,Any])->dict[str,Any]:
    goal=GoalObject(
        X="Take-5 tool and ICC ecosystem",
        T="durably organized non-overwriting project system",
        I="current registry plus recovered ICC/IC inventory",
        Sigma="registry/package parity + owner integrity + regression validation",
    )
    candidate=GoalCandidate(
        "tool-system-goal",
        goal,
        constraints=("no semantic duplication","preserve OPEN","local change only"),
        evidence=("projects/tool-system/GOAL.md",),
        grounded=True,
        authority_typed=True,
        determinate_enough=True,
    )
    return _dev_executed(recover_goal((candidate,)),evidence="native:GOAL")


def _solution_adapter(packet:dict[str,Any])->dict[str,Any]:
    problem=Problem(
        observed=("historical overwrite/loss and dimension collision",),
        generators=("unowned mutable truth and destructive replacement",),
        required_effects=("single-owner-routing","append-only-history","regression-detection"),
        protected=("semantic-authority","OPEN-preservation"),
    )
    candidate=Candidate(
        id="owned-project-packages",
        proposed_attacks=problem.generators,
        proposed_effects=problem.required_effects,
        proposed_preservations=problem.protected,
        cost=1.0,
    )
    receipt=SolutionReceipt(
        candidate_id=candidate.id,
        source="every-tool-development-sweep",
        execution_stage="CONSUMED",
        observed_attacks=problem.generators,
        observed_effects=problem.required_effects,
        observed_preservations=problem.protected,
        verification_status="PASS",
        closure_status="CLOSED",
        evidence=("package-audit","full-validation","projectmanager-assessment"),
    )
    return _dev_executed(solve(problem,(candidate,),(receipt,)),evidence="native:SolutionToMyProblem")


def _prose_adapter(packet:dict[str,Any])->dict[str,Any]:
    evidence=ProseEvidence(
        semantic_preservation="PASS",
        earned_claim_strength="PASS",
        no_unsupported_inflation="PASS",
        evidence=("every-tool:semantic","every-tool:strength","every-tool:no-inflation"),
    )
    out=assess_prose(
        "The project preserves its protected prose contract.",
        ProseContract("every-tool"),
        evidence,
    )
    return _dev_executed(out,evidence="native:Prose")


def _desired_jane_adapter(packet:dict[str,Any])->dict[str,Any]:
    evidence=(
        DesireEvidence(
            "project_continuity","WANT","current-user-request",
            "Keep the whole tool project organized using durable project-control lessons without rewriting documents."
        ),
        DesireEvidence(
            "silent_rewrite","DO_NOT_WANT","current-user-request",
            "Do not rewrite documents across dimensions or lose prior work."
        ),
    )
    return _dev_executed(recover_desired_jane(evidence),evidence="native:DesiredJane")


def _question_adapter(packet:dict[str,Any])->dict[str,Any]:
    questions=(
        QuestionCandidate(
            "control-gap",
            "Are any native project-control coordinates missing or multiply owned?",
            1.0,0.9,1.0,1.0,0.2,0.1,
        ),
        QuestionCandidate(
            "cosmetic",
            "Could package headings be reformatted?",
            0.1,0.1,0.0,0.2,0.2,0.2,
        ),
    )
    return _dev_executed(select_question(questions),evidence="native:QuestionWorthAsking")


def _lambda_adapter(packet:dict[str,Any])->dict[str,Any]:
    candidate=EntryState(
        "organize-tool-system",
        "projects/tool-system",
        "observer-development",
        ("no-overwrite","one-owner"),
        "current-main",
        "validated-relative-closure",
    )
    out=reconstruct_lambda(
        (candidate,),
        consistent=lambda x:True,
        continuation_equivalent=lambda a,b:a==b,
        result_sensitive=lambda coordinate:coordinate in {"T","C","S"},
    )
    return _dev_executed(out,evidence="native:LambdaMath")


def _semantic_pipeline_adapter(packet:dict[str,Any])->dict[str,Any]:
    out=plan_black_box_resolution(
        "TOOL_SYSTEM_ORGANIZATION",
        residuals=("CURRENTNESS_OPEN","DEPENDENCY_OPEN"),
    )
    return _dev_executed(out,evidence="native:SemanticResolutionPipeline")


def _recursive_compiler_adapter(packet:dict[str,Any])->dict[str,Any]:
    root=CompilerNode(
        "whole","WHOLE",None,
        gates={"observer":True,"focused":True,"final_observer":True},
        protected_constraints=("NO_DOWNGRADE",),
    )
    child=CompilerNode(
        "section","SECTION","whole",
        gates={"observer":True,"focused":True,"final_observer":True},
        protected_constraints=("NO_DOWNGRADE",),
    )
    out=evaluate_global_closure(
        nodes=(root,child),
        edge_receipts={("whole","section"):True},
        constraint_receipts={
            ("whole","NO_DOWNGRADE"):True,
            ("section","NO_DOWNGRADE"):True,
        },
        admitted_delta_hashes={},
        realized_delta_hashes={},
        hf2_trace=({"disposition":"RELATIVE_CLOSE","delta":{}},),
    )
    return _dev_executed(out,evidence="native:RecursiveCompiler")


def development_adapters(summary:dict[str,Any])->dict[str,Any]:
    return {
        "ProjectManager":project_manager_adapter,
        "ImprovementCore":_improvement_core_adapter,
        "ICC128":_icc128_adapter,
        "MT":_mt_adapter,
        "MTA":_mta_adapter,
        "Architecture":_architecture_adapter,
        "PD":_pd_adapter,
        "PDAudit":_pdaudit_adapter,
        "GDOS":_gdos_adapter,
        "Discriminator":_discriminator_adapter,
        "Reconciler":_reconciler_adapter,
        "DelegatedExecutor":_delegated_executor_adapter,
        "HF001":_hf1_adapter,
        "HF002":_hf2_adapter,
        "RootCause":_root_cause_adapter,
        "TRC":_trc_adapter,
        "RTC":_rtc_adapter,
        "BiasPerturbation":_bias_adapter,
        "CurrentnessAudit":_currentness_adapter,
        "CapabilityFoundry":_foundry_adapter,
        "EmergentAdmission":_emergent_adapter,
        "HistoricalReconstruction":_historical_adapter,
        "ZeroRequest":_zero_request_adapter,
        "MultiObject":_multiobject_adapter,
        "Diagnosis":_diagnosis_adapter,
        "ASSERT":_assert_adapter,
        "GOAL":_goal_adapter,
        "SolutionToMyProblem":_solution_adapter,
        "Prose":_prose_adapter,
        "DesiredJane":_desired_jane_adapter,
        "QuestionWorthAsking":_question_adapter,
        "LambdaMath":_lambda_adapter,
        "SemanticResolutionPipeline":_semantic_pipeline_adapter,
        "RecursiveCompiler":_recursive_compiler_adapter,
    }


def maturity_summary()->dict[str,Any]:
    rows=audit_maturity()
    counts={}
    for row in rows:
        key=str(getattr(getattr(row,"disposition",None),"value",getattr(row,"disposition","UNKNOWN")))
        counts[key]=counts.get(key,0)+1
    return {"count":len(rows),"dispositions":counts}


def development_audits()->dict[str,Any]:
    identity=audit_current_portfolio_identity()
    invocation=audit_full_invocation_portfolio()
    transitions=audit_protected_transition_portfolio()
    manifests=audit_tool_identities(CONFIGURED_RUNS,OVERRIDES)
    reality=audit_tool_reality()
    system=run_audit(ROOT)
    packages=audit_materialized(ROOT)
    historical_replays=audit_historical_replays()
    reachability=audit_current_repertoire_reachability()
    cleanup=run_cleanup_campaign(ROOT)
    audit_architecture=audit_audits()
    return {
        "current_portfolio_identity":plain(identity),
        "full_invocation_portfolio":plain(invocation),
        "protected_transition_portfolio":plain(transitions),
        "tool_manifest_audit":plain(manifests),
        "tool_reality_audit":plain(reality),
        "tool_maturity":maturity_summary(),
        "system_audit":plain(system),
        "tool_project_package_audit":plain(packages),
        "historical_replay_audit":plain(historical_replays),
        "repertoire_reachability":plain(reachability),
        "system_cleanup_campaign":plain(cleanup),
        "audit_architecture":plain(audit_architecture),
    }


def run()->dict[str,Any]:
    summary=project_summary()
    packet={
        "target":"projects/tool-system",
        "purpose":"exhaustive development sweep of anti-loss organization",
        "capability_inputs":capability_inputs(summary),
        "learning_inputs":learning_inputs(summary),
        "project_summary":summary,
    }
    conductor=run_tool_conductor(
        packet,
        adapters=development_adapters(summary),
    )
    rows=conductor["results"]
    statuses={}
    for row in rows:
        statuses[row["status"]]=statuses.get(row["status"],0)+1
    pm=next(row for row in rows if row["tool_id"]=="ProjectManager")
    dev=development_audits()

    structural_failures=[]
    for name in ("current_portfolio_identity","full_invocation_portfolio","protected_transition_portfolio","repertoire_reachability"):
        status=str(dev[name].get("status",""))
        if status not in {"CLOSED_RELATIVE","PASS"}:
            structural_failures.append(f"{name}:{status}")
    if dev["historical_replay_audit"].get("status")!="PASS":
        structural_failures.append("historical_replay_audit:FAIL")
    if dev["system_cleanup_campaign"].get("status")!="CLOSED_RELATIVE":
        structural_failures.append("system_cleanup_campaign:OPEN")
    if dev["tool_project_package_audit"].get("status")!="CLOSED_RELATIVE":
        structural_failures.append("tool_project_package_audit:OPEN")
    if not dev["system_audit"].get("closed"):
        structural_failures.append("system_audit:OPEN")

    return {
        "campaign_id":"ICC_EVERY_TOOL_TOOL_SYSTEM_SWEEP_001_2026-09-27",
        "target":"projects/tool-system",
        "registered_tool_count":len(MATERIAL_TOOLS),
        "tool_conductor":{
            "status":conductor["status"],
            "tool_count":conductor["tool_count"],
            "status_counts":statuses,
            "open_tools":conductor["open_tools"],
            "portability_open_set":conductor["portability_open_set"],
            "results":plain(rows),
        },
        "project_manager_actual_project_assessment":plain(pm),
        "development_audits":dev,
        "structural_failures":structural_failures,
        "campaign_status":"OPEN" if structural_failures or pm["status"] in {"OPEN","BLOCKED","CONFLICT"} else "CLOSED_RELATIVE",
        "claim_boundary":{
            "synthetic_full_invocation_witness":"proves route/profile reachability, not domain semantic correctness",
            "tool_conductor_open":"named tools without required semantic bindings are not simulated",
            "effect_class":"EVIDENCE_ONLY",
        },
    }


def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--json-out")
    args=parser.parse_args()
    receipt=run()
    payload=json.dumps(plain(receipt),sort_keys=True,indent=2,default=str)
    if args.json_out:
        path=Path(args.json_out)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(payload+"\n",encoding="utf-8")
    compact={
        "campaign_id":receipt["campaign_id"],
        "campaign_status":receipt["campaign_status"],
        "registered_tool_count":receipt["registered_tool_count"],
        "tool_status_counts":receipt["tool_conductor"]["status_counts"],
        "open_tools":receipt["tool_conductor"]["open_tools"],
        "project_manager_status":receipt["project_manager_actual_project_assessment"]["status"],
        "project_manager_result":receipt["project_manager_actual_project_assessment"]["result"],
        "structural_failures":receipt["structural_failures"],
        "development_statuses":{
            k:(v.get("status") if isinstance(v,dict) and "status" in v else v.get("closed") if isinstance(v,dict) and "closed" in v else None)
            for k,v in receipt["development_audits"].items()
        },
    }
    print("EVERY_TOOL_SWEEP="+json.dumps(compact,sort_keys=True,default=str))


if __name__=="__main__":
    main()
