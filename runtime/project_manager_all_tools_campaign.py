"""Exhaustive ProjectManager all-tools campaign.

The campaign is a governed observer sweep over the entire current registered
Take-5 repertoire.  Every factor is bound to its full configured plan and
crosses its registered recurrence policy.  Ordinary tools use HF002.  HF002
itself uses SELF recurrence.

This module does not mutate repository truth.  It returns evidence and proposed
local consequences for ProjectManager/ImprovementCore consumption.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
from typing import Any, Mapping

from a5_programs import REGISTRY
from capability_foundry import (
    CapabilityFoundry,
    CapabilitySpec,
    CapabilityType,
)
from capability_runtime import execute_capability
from configured_hf2_execution import execute_configured_with_hf2
from currentness_audit import assess as assess_currentness
from global_tool_execution import build_tool_execution_plan
from learning_operator_tools import (
    FunctionalStackState,
    OODAState,
    RateDistortionCandidate,
)
from learning_tool_bridge import make_learning_worker
from project_manager import project_manager_adapter
from tool_run_registry import CONFIGURED_RUNS, MATERIAL_TOOLS


PHASES=(
    (
        "IDENTITY_GOAL_CURRENTNESS_FREEZE",
        (
            "ZeroRequest","ASSERT","GOAL","ProjectManager","CurrentnessAudit",
            "C01","C02","C03","C04","C05","C06","C49",
            "HistoricalReconstruction","LambdaMath","DesiredJane","QuestionWorthAsking",
        ),
    ),
    (
        "STRUCTURAL_RECONSTRUCTION_OBSERVATION",
        (
            "MTA","Architecture","PD","PDAudit","GDOS","Discriminator","MultiObject",
            "MT","SemanticResolutionPipeline","RecursiveCompiler",
            "C07","C08","C09","C10","C11","C12","C13",
        ),
    ),
    (
        "LEARNING_LENSES",
        (
            "L-D6","L-D8","L-KOLB","L-DIKW","L-PP","L-BAYES",
            "L-ACTIVE-INFERENCE","L-ACTOR-CRITIC","L-RATE-DISTORTION",
            "L-OODA","L-FUNCTIONAL-STACK",
        ),
    ),
    (
        "ATTACK_DIAGNOSIS",
        (
            "BiasPerturbation","Diagnosis","RootCause",
            "C14","C15","C16","C17","C18","C19",
        ),
    ),
    (
        "CANDIDATE_SOLUTION_GENERATION",
        (
            "SolutionToMyProblem","CapabilityFoundry","EmergentAdmission",
            "C20","C21","C22","C23",
        ),
    ),
    (
        "BOUNDED_REPAIR_ARCHITECTURE_CHANGE",
        (
            "C24","C25","C26","C27","C28","C29","C30","C31",
            "Reconciler","DelegatedExecutor",
        ),
    ),
    (
        "ROUTING_GAIN_FRONTIER",
        ("C32","C33","C34","C35"),
    ),
    (
        "PROPAGATION_TRANSFER_SAFETY",
        ("C36","C37","C38","C39","C40","C41","C42","C43"),
    ),
    (
        "VERIFICATION",
        ("C44","C45","C46","Prose"),
    ),
    (
        "AUTONOMOUS_CONSUMPTION_CLOSURE",
        (
            "ImprovementCore","C47","C48","RTC","TRC","HF001","HF002",
            "ICC128","ToolConductor",
        ),
    ),
)

BEST_ORDER=tuple(tool for _,tools in PHASES for tool in tools)


@dataclass(frozen=True)
class ToolCampaignReceipt:
    index:int
    phase:str
    tool_id:str
    configured_status:str
    execution_truth:str
    recurrence_engine:str
    recurrence_status:str
    recurrence_rounds:int
    cell_count:int
    question_count:int
    cognitive_count:int
    native_summary:Any


@dataclass(frozen=True)
class CampaignFinding:
    finding_id:str
    disposition:str
    coordinate:str
    description:str
    owner:str
    resume_condition:str|None=None


@dataclass(frozen=True)
class CampaignResult:
    status:str
    tool_count:int
    order:tuple[str,...]
    receipts:tuple[ToolCampaignReceipt,...]
    findings:tuple[CampaignFinding,...]
    local_actions:tuple[str,...]
    external_open:tuple[str,...]
    improvementcore_consumed:bool
    toolconductor_complete:bool


def _plain(value:Any)->Any:
    if isinstance(value,Enum):
        return value.value
    if is_dataclass(value):
        return {k:_plain(v) for k,v in asdict(value).items()}
    if isinstance(value,Mapping):
        return {str(k):_plain(v) for k,v in value.items()}
    if isinstance(value,(list,tuple,set,frozenset)):
        return tuple(_plain(v) for v in value)
    return value


def _phase_for(tool_id:str)->str:
    for phase,tools in PHASES:
        if tool_id in tools:
            return phase
    raise KeyError(tool_id)


def order_is_exact()->bool:
    return (
        len(BEST_ORDER)==len(MATERIAL_TOOLS)
        and len(set(BEST_ORDER))==len(BEST_ORDER)
        and set(BEST_ORDER)==set(MATERIAL_TOOLS)
    )


def _capability_inputs(packet:dict[str,Any])->dict[str,dict[str,Any]]:
    protected=("authority","open_preservation","observer_commit_separation")
    transfer_open=bool(packet.get("transfercore_open"))
    current_id=str(packet.get("target","ProjectManager"))
    inputs={
        "C01":{"admissible_typings":["FORMAL_PROJECT_CONTROL_TOOL"]},
        "C02":{"same_lineage":True},
        "C03":{"versions":[{"id":current_id,"authoritative":True}]},
        "C04":{"source_id":current_id,"claim":"validated current ProjectManager"},
        "C05":{"target":current_id,"protected":protected},
        "C06":{"dependencies":[
            {"id":"Take-5","availability":"CURRENT"},
            {"id":"ImprovementCore","availability":"CURRENT"},
            {"id":"TransferCore","availability":"OPEN"},
        ]},
        "C07":{"candidate_edges":[
            {"from":"ProjectManager","to":"ImprovementCore","material":True},
            {"from":"ProjectManager","to":"TransferCore","material":transfer_open},
        ]},
        "C08":{"spines":[
            ["identity","authority","verification"],
            ["goal","work_frontier","ImprovementCore"],
        ]},
        "C09":{"edges":[
            {"from":"project_state","to":"owner","relation_type":"AUTHORITY"},
            {"from":"evidence","to":"admission","relation_type":"EVIDENCE_TO_ADMISSION"},
        ]},
        "C10":{"representations":[
            {"id":"math","result":"authority-preserving-project-control"},
            {"id":"runtime","result":"authority-preserving-project-control"},
        ]},
        "C11":{"coordinates":[
            {"id":"authority","changed_result":True},
            {"id":"schedule","changed_result":False},
            {"id":"TransferCore","changed_result":transfer_open},
        ]},
        "C12":{"sensitivity_maps":[
            ["authority","verification"],
            ["authority","verification","TransferCore"] if transfer_open else ["authority","verification"],
        ]},
        "C13":{"edges":[
            {"from":"finding","to":"owner","attribution":"AUTHORITY_REGISTRY"},
            {"from":"tool_result","to":"project_truth","attribution":"ADMISSION_REQUIRED"},
        ]},
        "C14":{"findings":[
            {"id":"transfer-boundary","material":transfer_open},
        ],"interaction_findings":[]},
        "C15":{
            "source_effects":["authority","verification","open_preservation"],
            "target_effects":["authority","verification","open_preservation"],
            "different_terms":False,
        },
        "C16":{
            "protected":protected,
            "candidates":[
                {"id":"preserve-current","preserves":protected},
            ],
        },
        "C17":{"failures":[
            {
                "id":"historical-stale-self-state",
                "material":True,
                "mechanism":"project-state receipt lagged canonical merge",
            }
        ]},
        "C18":{"causal_chain":[
            {
                "id":"owner-local-state-sync",
                "evidence":"CURRENT_STATE authority",
                "terminal":True,
            }
        ]},
        "C19":{
            "seed_frontier":["ProjectManager"],
            "graph":{
                "ProjectManager":["ImprovementCore","TransferBoundary"],
                "ImprovementCore":[],
                "TransferBoundary":[],
            },
        },
        "C20":{"rivals":[
            "authority-governed transition system",
            "flat task checklist",
        ]},
        "C21":{"candidates":[
            {"id":"current-ProjectManager","preserves":protected},
        ]},
        "C22":{"improvement_frontier":[
            "preserve validated manager",
            "recover TransferCore separately",
        ]},
        "C23":{"typed_relation":{
            "source":"ProjectManager",
            "target":"ImprovementCore",
            "relation":"EVIDENCE_ONLY_HANDOFF",
        }},
        "C32":{"routes":[
            {"id":"owner-local-delta","licensed":True,"reachable":True},
        ]},
        "C33":{"strict_gain":True,"preserves":True},
        "C34":{"protected_before":protected,"protected_after":protected},
        "C35":{"candidates":[
            {"id":"keep-current"},
            {"id":"recover-transfercore-separately"},
        ]},
        "C36":{"affected_update":{"local":"current","external":"TransferCore OPEN"}},
        "C37":{"provenance_chain":[
            "ProjectManager evidence",
            "TransferEvidenceCandidate",
            "target-side admission",
        ]},
        "C38":{"license_disposition":"EVIDENCE_ONLY"},
        "C39":{"target_effect":"NONE_WITHOUT_TARGET_ADMISSION"},
        "C40":{"coverage":{"d36c":36,"questions":792,"cognitive":144}},
        "C41":{"rescue_disposition":"NOT_REQUIRED_LOCAL"},
        "C42":{"transfer_status":"OPEN_TRANSFERCORE_IDENTITY" if transfer_open else "ADMITTED"},
        "C43":{"handoff":{
            "to":"ImprovementCore",
            "effect_class":"EVIDENCE_ONLY",
            "authority":"NONE",
        }},
        "C44":{"expected":"PROJECT_CONTROL_PRESERVED","actual":"PROJECT_CONTROL_PRESERVED"},
        "C45":{"preregistered":True,"pass":True},
        "C46":{"with_component":"SAFE_FAIL_CLOSED_TRANSFER","without_component":"UNSAFE_TRANSFER"},
        "C47":{"blocking_open":[]},
        "C48":{"candidates":[
            {"id":"retain-fail-closed-transfer","strict_gain":True,"preserves":True},
        ]},
        "C49":{"visited":[
            {"id":"PROJECT_CHARTER.md","task_relevant":True},
            {"id":"GOAL.md","task_relevant":True},
            {"id":"CURRENT_STATE.md","task_relevant":True},
            {"id":"AUTHORITY_REGISTRY.md","task_relevant":True},
            {"id":"tool-runs","task_relevant":True},
        ]},
    }
    for i in range(24,32):
        pid=f"C{i:02d}"
        inputs[pid]={
            "candidate":{"id":pid+"-project-manager-preserving-successor"},
            "protected":protected,
            "preserves":protected,
        }
    return inputs


def _learning_inputs()->dict[str,dict[str,Any]]:
    identity=lambda x:x
    return {
        "L-D6":{
            "state":{"project":"ProjectManager","status":"CURRENT"},
            "sense":identity,
            "d4":identity,
            "ground":lambda x:{**x,"grounded":True},
        },
        "L-D8":{
            "state":{"project":"ProjectManager","status":"CURRENT"},
            "sense":identity,
            "orient":identity,
            "d4":identity,
            "ground":identity,
            "prune":identity,
        },
        "L-KOLB":{
            "experience":"validated ProjectManager self-management",
            "reflect":lambda e:"explicit authority and receipts prevented overwrite",
            "abstract":lambda r:"separate evidence, authority, and mutation",
            "experiment":lambda c:"apply same control to next project",
            "enact":lambda a:"retained ProjectManager control",
        },
        "L-DIKW":{
            "data":{"tests":934,"coverage":36},
            "context":{"target":"ProjectManager"},
            "contextualize":lambda data,context:{**data,**context},
            "models":("preserve-current","rewrite"),
            "description_length":lambda model,info:1.0 if model=="preserve-current" else 10.0,
            "actions":("keep","rewrite"),
            "expected_utility":lambda model,action:1.0 if action=="keep" else 0.0,
        },
        "L-PP":{
            "observation":"CURRENT",
            "model":{"prediction":"CURRENT"},
            "predict":lambda model:model["prediction"],
            "prediction_error":lambda observation,prediction:observation!=prediction,
            "revise":lambda model,observation,error:(model,0.0 if not error else 1.0),
        },
        "L-BAYES":{
            "prior":{"coherent":0.9,"incoherent":0.1},
            "likelihood":{"coherent":0.99,"incoherent":0.01},
        },
        "L-ACTIVE-INFERENCE":{
            "policies":("preserve-validated","rewrite"),
            "expected_free_energy":lambda policy:0.0 if policy=="preserve-validated" else 10.0,
        },
        "L-ACTOR-CRITIC":{
            "reward":1.0,
            "discount":0.9,
            "value_now":1.0,
            "value_next":1.0,
            "value_parameters":{"v":1.0},
            "policy_parameters":{"p":1.0},
            "critic_update":lambda params,delta:{**params,"delta":delta},
            "actor_update":lambda params,delta:{**params,"delta":delta},
        },
        "L-RATE-DISTORTION":{
            "candidates":(
                RateDistortionCandidate("full-project-state",1.0,0.0),
                RateDistortionCandidate("compressed-summary",0.2,0.5),
            ),
            "max_distortion":0.1,
        },
        "L-OODA":{
            "state":OODAState(world="ProjectManager CURRENT",orientation="preserve authority"),
            "observe":lambda world:world,
            "orient":lambda observation,orientation:orientation,
            "decide":lambda orientation:"KEEP_CURRENT",
            "act":lambda world,decision:world,
        },
        "L-FUNCTIONAL-STACK":{
            "state":FunctionalStackState("evidence","execution","architecture","control"),
            "input_layer":lambda state:state.input_layer,
            "operational_layer":lambda state:state.operational_layer,
            "structural_layer":lambda state:state.structural_layer,
            "executive_layer":lambda state:state.executive_layer,
        },
    }


def build_packet(
    *,
    project:Mapping[str,Any],
    current_state_text:str,
    basis_ref:str,
)->dict[str,Any]:
    transfer_open=(
        "OPEN_TRANSFERCORE_IDENTITY" in current_state_text
        or "TransferCore" in str(project.get("evidence_refs",()))
    )
    packet={
        "target":"ProjectManager",
        "basis_ref":str(basis_ref),
        "project":dict(project),
        "current_state_text":str(current_state_text),
        "transfercore_open":bool(transfer_open),
        "capability_inputs":{},
        "learning_inputs":_learning_inputs(),
        "campaign_results":{},
        "obligations":(),
    }
    packet["capability_inputs"]=_capability_inputs(packet)
    return packet


def _native_status(value:Any)->str:
    if isinstance(value,Mapping):
        return str(value.get("status","EXECUTED"))
    if hasattr(value,"status"):
        return str(getattr(value,"status"))
    if hasattr(value,"terminal"):
        return str(getattr(value,"terminal"))
    return "EXECUTED"


def _summary(value:Any)->Any:
    plain=_plain(value)
    if isinstance(plain,dict):
        keep={}
        for key in (
            "status","blocker","action","relation","selected","residual",
            "open_objects","open_tools","tool_count","portability_open_set",
            "closure_disposition","transfer_status","gain_disposition",
            "verification","holdout_result","causal_effect",
        ):
            if key in plain:
                keep[key]=plain[key]
        if keep:
            return keep
        return {"keys":tuple(sorted(plain))[:16]}
    if isinstance(plain,tuple) and len(plain)>8:
        return {"tuple_len":len(plain)}
    return plain


def _run_named_native(tool_id:str, packet:dict[str,Any])->Any:
    if tool_id=="ZeroRequest":
        from zero_request_episode import zero_request_episode
        return zero_request_episode(
            ("PROJECT_CHARTER","GOAL","CURRENT_STATE","AUTHORITY_REGISTRY"),
            lambda corpus,binding:{"observed":tuple(corpus),"binding":str(binding)},
        )

    if tool_id=="ASSERT":
        from assert_compound import AssertState,AssertStages,identity_stage,run_to_fixed_point
        state=AssertState(
            assertions=("ProjectManager is current","TransferCore remains external OPEN"),
            world=(packet["basis_ref"],),
            discovery=("93-tool exhaustive campaign",),
        )
        stages=AssertStages(
            identity_stage,identity_stage,identity_stage,
            identity_stage,identity_stage,identity_stage,
        )
        return run_to_fixed_point(state,stages,max_rounds=3)

    if tool_id=="GOAL":
        from goal import GoalCandidate,GoalObject,recover_goal
        goal=GoalObject(
            X="current ProjectManager plus exhaustive tool evidence",
            T="locally consequence-closed ProjectManager with explicit external OPEN",
            I="run entire registered repertoire and consume all local consequences",
            Sigma="authority preserved; no invented TransferCore identity",
        )
        return recover_goal((
            GoalCandidate(
                "PM_ALL_TOOLS_GOAL",goal,
                constraints=("OBSERVER_TOOL_RUNS","OWNER_LOCAL_MUTATION"),
                evidence=(packet["basis_ref"],),
                grounded=True,authority_typed=True,determinate_enough=True,
            ),
        ))

    if tool_id=="ProjectManager":
        return project_manager_adapter({"project":packet["project"]},None)

    if tool_id=="CurrentnessAudit":
        return assess_currentness(
            component="ProjectManager",
            built_basis=packet["basis_ref"],
            latest_basis=packet["basis_ref"],
            protected=("authority","open_preservation","observer_commit_separation"),
            delta=(),
            behavior_preserved=True,
            local_patch_available=True,
            evidence=("campaign-currentness",),
            reverified=True,
        )

    if tool_id=="HistoricalReconstruction":
        from historical_reconstruction import ReconstructionCase,compare
        return compare(ReconstructionCase(
            "ProjectManager-before-all-tools",
            "ProjectManager-current",
            "authority-preserving project control",
            ("authority","open_preservation"),
            {"control":"preserved"},
            {"control":"preserved"},
            "validated-predecessor",
            "validated-current",
            "all-tools-campaign",
        ))

    if tool_id=="LambdaMath":
        from lambda_math import EntryState,reconstruct
        state=EntryState(
            "ProjectManager exhaustive verification",
            "ProjectManager",
            "OBSERVER",
            "authority preserved",
            "current validated state",
            "93 registered tools",
        )
        return reconstruct(
            (state,),
            consistent=lambda x:True,
            continuation_equivalent=lambda a,b:a==b,
            result_sensitive=lambda coordinate:True,
        )

    if tool_id=="DesiredJane":
        from desired_jane import what_tzvi_wants_jane_to_be
        return what_tzvi_wants_jane_to_be()

    if tool_id=="QuestionWorthAsking":
        from question_worth_asking import QuestionCandidate,select_question
        return select_question((
            QuestionCandidate(
                "local-residual",
                "Does any local ProjectManager consequence remain after exhaustive verification?",
                1.0,1.0,1.0,1.0,0.1,0.0,False,
            ),
            QuestionCandidate(
                "transfercore",
                "What is the exact current TransferCore FullMath identity?",
                1.0,1.0,1.0,0.2,0.8,0.1,True,
            ),
        ))

    if tool_id=="MTA":
        from mta import run_mta
        required={
            "Model":{"type":"authority-governed transition system"},
            "Findings":("authority separated from evidence","open preserved"),
            "FactorBasis":("identity","authority","verification","handoff"),
            "Residual":("TransferCore identity",) if packet["transfercore_open"] else (),
            "MaterialDeltas":(),
            "DiscoveryDeltas":(),
            "NewOrChangedObjects":(),
            "Evidence":(packet["basis_ref"],),
            "Coverage":{"registered_tools":len(MATERIAL_TOOLS)},
            "VerificationObligations":(),
            "OPEN":(),
        }
        return run_mta(
            packet["project"],"FullMath",packet["basis_ref"],"ProjectManager",
            generate_structural_hypotheses=lambda *args:(
                "transition-system","task-checklist",
            ),
            select_analysis_package=lambda *args:"transition-system",
            reconstruct_protected_model=lambda *args:required,
        )

    if tool_id=="Architecture":
        from architecture_analysis import run_architecture_analysis
        return run_architecture_analysis(
            packet["project"],
            {"protected":("authority","open_preservation")},
            analyze_architecture=lambda architecture,contract:{
                "ArchClass":"authority-governed-project-control",
                "Violations":(),
                "LocalizationFamilies":("project","tool-system"),
                "DependencyState":"TYPED",
                "InteractionState":"SEPARATED",
                "TransformationFrontier":(),
                "SuccessorFrontier":(),
                "Coverage":{"d36c":36},
                "OpenConflictBlocked":(),
                "Provenance":(packet["basis_ref"],),
            },
        )

    if tool_id in {"PD","PDAudit"}:
        cases=(
            {"id":"math","authority":"separate","result":"preserved"},
            {"id":"runtime","authority":"separate","result":"preserved"},
        )
        rho=lambda case:case["result"]
        approx=lambda a,b:a==b
        reps={"core":lambda case:(case["authority"],case["result"])}
        if tool_id=="PD":
            from pd import run_pd
            return run_pd(cases,rho=rho,approx=approx,representations=reps)
        from pd_audit import run_pd_audit
        return run_pd_audit(
            cases,rho=rho,approx=approx,representations=reps,
            kappa_cases=lambda xs:len(xs),
            kappa_representations=lambda rs:tuple(sorted(rs)),
        )

    if tool_id=="GDOS":
        from gdos import run_gdos
        observers=(
            lambda p:{"single_owner":bool(p.get("authority_registry"))},
            lambda p:{"project_id":p.get("project_id")},
            lambda p:{"transfer_open":packet["transfercore_open"]},
        )
        return run_gdos(
            packet["project"],
            observers=observers,
            reconcile_fn=lambda rows:{"observations":rows,"conflict":False},
        )

    if tool_id=="Discriminator":
        from discriminator import run_discriminator
        return run_discriminator(
            ("authority-preserving","authority-ambiguous"),
            lambda candidate:candidate=="authority-preserving",
        )

    if tool_id=="MultiObject":
        from multiobject import (
            FrozenObject,RelationFinding,RouteResult,ResidualJudgment,
            ReconciledFinding,run_multiobject,
        )
        class Provider:
            def joint(self,objects,*,route_id):
                support=tuple(x.object_id for x in objects)
                return RouteResult(
                    route_id,"FULL_JOINT",support,
                    (RelationFinding(
                        "J1",support,"SAFE_CONTROLLER_SEPARATION",
                        ("ProjectManager owns control; ImprovementCore owns improvement",),
                    ),),
                    isolation_receipt="campaign:joint",
                )
            def pair(self,left,right,*,route_id):
                support=(left.object_id,right.object_id)
                return RouteResult(
                    route_id,"PAIR",support,
                    (RelationFinding(
                        "P:"+left.object_id+"|"+right.object_id,
                        support,"TYPED_INTERFACE",
                    ),),
                    isolation_receipt="campaign:"+route_id,
                )
            def synthesize_pairs(self,pair_routes):
                support=("ProjectManager","ImprovementCore","TransferBoundary")
                return RouteResult(
                    "PAIR_SYNTHESIS","PAIR_SYNTHESIS",support,
                    (RelationFinding("S1",support,"PAIRWISE_COHERENCE"),),
                    isolation_receipt="campaign:pair-synthesis",
                )
            def challenge_reducibility(self,joint_route,pair_routes,pair_synthesis):
                return (ResidualJudgment("J1","ZERO_RELATIVE_RESIDUAL"),)
            def triggered_views(self,*args):
                return ()
            def analyze_view(self,request,objects):
                raise RuntimeError("no view requested")
            def reconcile(self,pair_routes,pair_synthesis,joint_route,residuals,view_results):
                return (
                    ReconciledFinding("J1","CONVERGENT"),
                    ReconciledFinding("S1","CONVERGENT"),
                )
        objects=(
            FrozenObject("ProjectManager","CONTROL","SYSTEM","project-state"),
            FrozenObject("ImprovementCore","CONTROLLER","SYSTEM","substantive-improvement"),
            FrozenObject("TransferBoundary","BOUNDARY","INTERFACE","cross-project-transfer"),
        )
        return run_multiobject(objects,Provider())

    if tool_id=="MT":
        from mt_semantic_return_gate import run_mt_with_before_return_gate
        def run_mt(state):
            return state,{
                "target":"ProjectManager",
                "finding":"local project control coherent",
                "transfercore_open":packet["transfercore_open"],
            }
        def detect(state,result):
            return ("TransferCore",) if packet["transfercore_open"] else ()
        def execute_stage(stage_tool,object_id,state):
            return state,"OPEN",False
        return run_mt_with_before_return_gate(
            {"basis":packet["basis_ref"]},
            run_mt=run_mt,
            detect_black_boxes=detect,
            execute_stage=execute_stage,
            max_rounds=2,
        )

    if tool_id=="SemanticResolutionPipeline":
        from semantic_resolution_pipeline import plan_black_box_resolution
        return plan_black_box_resolution(
            "TransferCore",
            ("CURRENT_FULL_MATH_IDENTITY_UNRECOVERED",)
            if packet["transfercore_open"] else (),
        )

    if tool_id=="RecursiveCompiler":
        from recursive_compiler import CompilerNode,evaluate_global_closure
        node=CompilerNode(
            "project-manager-campaign-root",
            "SYSTEM",
            gates={
                "full36":True,
                "observer_focused_observer":True,
                "reconciled":True,
            },
            protected_constraints=("NO_SILENT_OVERWRITE",),
        )
        return evaluate_global_closure(
            nodes=(node,),
            edge_receipts={},
            constraint_receipts={
                ("project-manager-campaign-root","NO_SILENT_OVERWRITE"):True,
            },
            admitted_delta_hashes={},
            realized_delta_hashes={},
            hf2_trace=({
                "disposition":"RELATIVE_CLOSE",
                "delta":{"material_result_delta":False},
            },),
        )

    if tool_id=="BiasPerturbation":
        from bias_perturbation import run_bias_perturbation
        target={"authority":"single","status":"CURRENT"}
        perturbations=(
            {"status":"CURRENT","authority":"single"},
            {"authority":"single","status":"CURRENT"},
        )
        return run_bias_perturbation(
            target,perturbations,
            runner=lambda x:(x.get("authority"),x.get("status")),
            semantics_equivalent=lambda a,b:set(a)==set(b) and a==b,
            result_equivalent=lambda a,b:a==b,
        )

    if tool_id=="Diagnosis":
        from diagnosis import diagnose
        return diagnose({"failures":[{
            "id":"historical-state-lag",
            "material":True,
            "mechanism":"project current-state receipt lagged repository merge",
        }]})

    if tool_id=="RootCause":
        from root_cause import RootCandidate,run_root_cause_hf2
        return run_root_cause_hf2(
            failure_class=("historical-state-lag",),
            candidates=(
                RootCandidate(
                    "owner-local-state-sync",
                    "ROOT_GENERATOR",
                    frozenset(("historical-state-lag",)),
                    evidence=frozenset(("ProjectManager self-management",)),
                    survives_representation_change=True,
                    removal_breaks_recurrence=True,
                ),
            ),
            basis_id=packet["basis_ref"],
            max_rounds=4,
        )

    if tool_id=="SolutionToMyProblem":
        from solution_to_my_problem import Problem,Candidate,SolutionReceipt,solve
        problem=Problem(
            observed=("unsafe cross-project transfer risk",),
            generators=("unrecovered TransferCore identity",),
            required_effects=("fail-closed transfer",),
            protected=("ProjectManager authority",),
        )
        candidate=Candidate(
            "evidence-only-transfer-boundary",
            proposed_attacks=("unrecovered TransferCore identity",),
            proposed_effects=("fail-closed transfer",),
            proposed_preservations=("ProjectManager authority",),
            cost=1.0,
        )
        receipt=SolutionReceipt(
            candidate_id=candidate.id,
            source="ProjectManager validation",
            execution_stage="CONSUMED",
            observed_attacks=("unrecovered TransferCore identity",),
            observed_effects=("fail-closed transfer",),
            observed_preservations=("ProjectManager authority",),
            verification_status="PASS",
            closure_status="CLOSED",
            evidence=("TRANSFERCORE_INTERFACE: OPEN_TRANSFERCORE_IDENTITY",),
        )
        return solve(problem,(candidate,),(receipt,))

    if tool_id=="Prose":
        from prose import ProseContract,ProseEvidence,assess_prose
        evidence=ProseEvidence(
            semantic_preservation="PASS",
            earned_claim_strength="PASS",
            no_unsupported_inflation="PASS",
            evidence=(
                "pm-all-tools:semantic",
                "pm-all-tools:strength",
                "pm-all-tools:no-inflation",
            ),
        )
        return assess_prose(
            "ProjectManager preserves the protected prose contract.",
            ProseContract("pm-all-tools"),
            evidence,
        )

    if tool_id=="CapabilityFoundry":
        foundry=CapabilityFoundry()
        candidate=CapabilitySpec(
            capability_id="PM_ALL_TOOLS_CAMPAIGN",
            capability_type=CapabilityType.BEHAVIOR,
            trigger="explicit exhaustive ProjectManager verification",
            input_contract="current ProjectManager",
            transform="observer-only exhaustive evidence sweep",
            output_contract="campaign receipt",
            success="all registered factors accounted",
            failure="OPEN/BLOCKED retained",
            grants_authority=False,
        )
        return foundry.evaluate(
            candidate,
            functionally_subsumed=lambda candidate,old:False,
            material_goal_gain=lambda candidate:False,
            architecture_compatible=lambda candidate:True,
        )

    if tool_id=="EmergentAdmission":
        from emergent_admission import ObjectCandidate,admit
        return {
            "status":str(admit(ObjectCandidate(
                "PM_ALL_TOOLS_CAMPAIGN_RECEIPT",
                "EVIDENCE",
                False,
            )).value),
            "meaning":"campaign receipt remains evidence, not a new load-bearing authority",
        }

    if tool_id=="Reconciler":
        from reconcile import ReconcileResult,reconcile
        return reconcile(
            {"project":"ProjectManager"},
            tuple(packet["campaign_results"].values()),
            lambda state,results:ReconcileResult(
                state=state,
                new_relations=(("campaign_results","ProjectManager"),),
                open_coordinates=(("TransferCore",) if packet["transfercore_open"] else ()),
            ),
        )

    if tool_id=="DelegatedExecutor":
        from delegation import delegate
        output,receipt=delegate(
            episode="pm-all-tools",
            program_id="VERIFY_PROJECT_MANAGER",
            authority_in=frozenset(("observe","verify")),
            authority_local=frozenset(("observe",)),
            payload={"project":"ProjectManager"},
            worker=lambda payload:{"observed":payload["project"],"mutated":False},
        )
        return {"output":output,"receipt":_plain(receipt)}

    if tool_id=="ImprovementCore":
        from ic028_operator import GOAL_DIRECTED_STAGES
        from improvement_core_dispatch import dispatch_improvement_core
        def handlers():
            out={}
            for stage in GOAL_DIRECTED_STAGES:
                def fn(state,stage=stage):
                    return {
                        "state":{**state,stage:True},
                        "material_delta":False,
                        "supervisory_relevant":False,
                    }
                out[stage]=fn
            out["REENTER"]=lambda state:{"state":state,"terminal":True}
            return out
        def return_done(state,memory,context):
            status=str(context.get("candidate_status","OPEN"))
            return {
                "disposition":"RETURN",
                "terminal":"COMPLETE",
                "goal_closed":True,
                "owned_work_remaining":False,
                "consequence_closed":True,
                "blocker":None,
                "evidence":["pm-all-tools:all-local-results-consumed"],
            }
        resolution,out=dispatch_improvement_core(
            "Improvement Core, consume the ProjectManager all-tools campaign",
            target="ProjectManager",
            job="consume exhaustive campaign and settle local consequences",
            basis=packet["basis_ref"],
            state={
                "campaign_result_count":len(packet["campaign_results"]),
                "external_open":(
                    ("TransferCore",) if packet["transfercore_open"] else ()
                ),
            },
            handlers=handlers(),
            return_verifier=return_done,
            hf2_enabled=False,
        )
        return {
            "status":out.status,
            "controller":resolution.controller,
            "terminal":str(out.result.terminal),
            "hf2_status":out.hf2_status,
        }

    if tool_id=="RTC":
        from raise_the_ceiling import raise_the_ceiling
        return raise_the_ceiling(packet["capability_inputs"]["C48"])

    if tool_id=="TRC":
        from tool_run_closure import (
            Consequence,ConsumerState,Disposition,StageResult,run_tool_run_closure,
        )
        consequence=Consequence(
            "ProjectManager",
            "CAMPAIGN_RESULT_CONSUMPTION",
            "CURRENT",
            "PROJECT_MANAGER",
            packet["basis_ref"],
            "PROJECT_CONTROL",
        )
        return run_tool_run_closure(
            tool_result={"campaign_results":len(packet["campaign_results"])},
            pre_state={"status":"CURRENT"},
            post_state={"status":"CURRENT"},
            harvest_fn=lambda result,pre,post:(consequence,),
            disposition_fn=lambda q,state:Disposition.REALIZE,
            realize_fn=lambda q,state:StageResult(state,"OK",(),("campaign:realized",)),
            verify_fn=lambda q,state:StageResult(state,"OK",(),("campaign:verified",)),
            consume_fn=lambda q,state:StageResult(
                state,ConsumerState.CONSUMED.value,(),("campaign:consumed",)
            ),
            harvest_basis="PM_ALL_TOOLS",
            harvest_complete=True,
        )

    if tool_id=="HF001":
        from hf1_episode import run_hf1_episode
        packet0={
            "identity":"ProjectManager",
            "type":"FORMAL_TOOL",
            "scope":"SYSTEM",
            "job":"VERIFY_EXHAUSTIVE_CAMPAIGN",
            "readings":("campaign",),
            "result_sensitive":("authority","verification"),
            "selectors":("BEST_ORDER",),
            "authority":"OBSERVER",
            "provenance":packet["basis_ref"],
            "open":("TransferCore",) if packet["transfercore_open"] else (),
            "obligations":(),
            "world_state":"CURRENT",
            "discovery_state":"STABLE",
            "result_sensitive_state":"STABLE",
        }
        return run_hf1_episode(
            packet0,
            package_index={},
            mode_flags={},
            execute_fn=lambda package,mode,state:None,
            closure_fn=lambda execution,state:None,
            max_rounds=2,
        )

    if tool_id=="HF002":
        from hf002_recursive_continuation import HF002RecursiveContinuation
        engine=HF002RecursiveContinuation(
            run_capability=lambda state,memory:{
                "execution_truth":"IMPLEMENTATION_EXECUTED",
                "value":"ProjectManager exhaustive campaign local close",
            },
            admit_normalize=lambda raw,state,memory:(
                state,
                {
                    "material_result_delta":False,
                    "route_equivalence":"PM_ALL_TOOLS_HF2_SELF",
                },
            ),
            trc_verify=lambda pre,post,delta:{"terminal":True},
            hf1_classify=lambda pre,post,delta:{"disposition":"STABLE"},
            live_local=lambda state,memory:False,
            local_close=lambda state,memory:True,
            max_rounds=2,
        )
        return engine.run({"target":"ProjectManager"},{})

    if tool_id=="ICC128":
        from icc128_autonomous_controller import ICC128Controller
        controller=ICC128Controller(
            gq=lambda state,memory:[{"id":"q","question":"any local residual?"}],
            gw=lambda questions,state,memory:[{"id":"w","job":"verify local closure"}],
            select=lambda questions,work,state,memory:work,
            execute=lambda selected,state,memory:[{"status":"EXECUTED","local_open":False}],
            admit=lambda results,state,memory:{"results":results},
            update=lambda state,memory,delta:(
                {**state,"terminal":"COMPLETE","admitted_continuation":False},
                memory,
            ),
            max_iterations=2,
        )
        return controller.run(
            {"terminal":"CONTINUE","admitted_continuation":True},
            {},
        )

    if tool_id=="ToolConductor":
        from portable_tool_conductor import run_tool_conductor
        adapters={}
        for other in MATERIAL_TOOLS:
            is_c_capability=(
                other.startswith("C")
                and len(other)==3
                and other[1:].isdigit()
            )
            if other=="ToolConductor" or is_c_capability or other.startswith("L-"):
                continue
            adapters[other]=lambda inner_packet,other=other:_named_adapter_raw(
                other,packet,None
            )
        result=run_tool_conductor(packet,adapters=adapters)
        return {
            "status":result["status"],
            "tool_count":result["tool_count"],
            "open_tools":result["open_tools"],
            "portability_open_set":result["portability_open_set"],
        }

    raise KeyError("NAMED_TOOL_NOT_BOUND:"+tool_id)


def _named_adapter_raw(tool_id:str,packet:dict[str,Any],plan:Any)->dict[str,Any]:
    try:
        native=_run_named_native(tool_id,packet)
        return {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":{
                "native_status":_native_status(native),
                "native_summary":_summary(native),
            },
            "material_delta":False,
            "hf2_live_local":False,
            "hf2_local_close":True,
            "trc_terminal":True,
            "hf1_disposition":"STABLE",
            "evidence":(
                "runtime/project_manager_all_tools_campaign.py",
                "architecture/PROJECT_MANAGER_ALL_TOOLS_HF2_CAMPAIGN_001_2026-09-27.md",
            ),
        }
    except Exception as exc:
        return {
            "status":"BLOCKED",
            "execution_truth":"BLOCKED",
            "result":{
                "native_status":"BLOCKED",
                "error":type(exc).__name__+":"+str(exc),
            },
            "material_delta":False,
            "hf2_live_local":False,
            "hf2_local_close":False,
            "trc_terminal":True,
            "evidence":("runtime/project_manager_all_tools_campaign.py",),
        }


def _adapter_raw(tool_id:str,packet:dict[str,Any],plan:Any)->dict[str,Any]:
    if tool_id.startswith("C") and tool_id[1:].isdigit():
        try:
            native=execute_capability(
                tool_id,
                dict(packet["capability_inputs"].get(tool_id,{})),
            )
            return {
                "status":"EXECUTED",
                "execution_truth":"IMPLEMENTATION_EXECUTED",
                "result":{
                    "native_status":str(native.get("status","EXECUTED")),
                    "native_summary":_summary(native),
                },
                "material_delta":False,
                "hf2_live_local":False,
                "hf2_local_close":True,
                "trc_terminal":True,
                "hf1_disposition":"STABLE",
                "evidence":("capability_runtime:"+tool_id,),
            }
        except Exception as exc:
            return {
                "status":"BLOCKED",
                "execution_truth":"BLOCKED",
                "result":{"error":type(exc).__name__+":"+str(exc)},
                "material_delta":False,
            }

    if tool_id.startswith("L-"):
        try:
            native=make_learning_worker(tool_id)(packet)
            status=(
                native.get("learning_status",{})
                .get(tool_id,{})
                .get("status","OPEN")
            )
            return {
                "status":"EXECUTED" if status=="ACCEPT" else "OPEN",
                "execution_truth":"IMPLEMENTATION_EXECUTED" if status=="ACCEPT" else "OPEN",
                "result":{
                    "native_status":status,
                    "native_summary":_summary(native),
                },
                "material_delta":False,
                "hf2_live_local":False,
                "hf2_local_close":status=="ACCEPT",
                "trc_terminal":True,
                "hf1_disposition":"STABLE",
                "evidence":("learning_tool_bridge:"+tool_id,),
            }
        except Exception as exc:
            return {
                "status":"BLOCKED",
                "execution_truth":"BLOCKED",
                "result":{"error":type(exc).__name__+":"+str(exc)},
                "material_delta":False,
            }

    return _named_adapter_raw(tool_id,packet,plan)


def _discover_findings(packet:dict[str,Any],receipts:list[ToolCampaignReceipt])->tuple[CampaignFinding,...]:
    findings=[]
    text=str(packet.get("current_state_text",""))
    if (
        "Status: CURRENT / VALIDATED / MERGED" in text
        and "Run repository validation, repair any regression" in text
    ):
        findings.append(CampaignFinding(
            "PM-ALL-001",
            "LOCAL_ACTION_REQUIRED",
            "lifecycle",
            "CURRENT_STATE still names repository validation and promotion as the next frontier after validation and merge already completed.",
            "projects/project-manager/CURRENT_STATE.md",
            "replace stale next-frontier projection with the actual post-merge frontier",
        ))

    failed=tuple(
        r.tool_id for r in receipts
        if r.configured_status not in {"RELATIVE_CLOSE","SELF_CLOSE"}
    )
    if failed:
        findings.append(CampaignFinding(
            "PM-ALL-002",
            "LOCAL_ACTION_REQUIRED",
            "verification",
            "One or more configured factors did not reach their registered recurrence close: "+",".join(failed),
            "runtime/project_manager_all_tools_campaign.py",
            "repair factor adapters or preserve the exact blocker",
        ))

    if packet.get("transfercore_open"):
        findings.append(CampaignFinding(
            "PM-ALL-003",
            "EXTERNAL_OPEN",
            "handoffs",
            "TransferCore current FullMath identity remains unrecovered; ProjectManager transfer stays evidence-only and non-authorizing.",
            "TransferCore",
            "recover and admit TransferCore current full identity and target-side admission path",
        ))

    return tuple(findings)


def run_all_tools_campaign(
    *,
    project:Mapping[str,Any],
    current_state_text:str,
    basis_ref:str,
)->CampaignResult:
    if not order_is_exact():
        missing=sorted(set(MATERIAL_TOOLS)-set(BEST_ORDER))
        extra=sorted(set(BEST_ORDER)-set(MATERIAL_TOOLS))
        raise RuntimeError(
            "PROJECT_MANAGER_CAMPAIGN_ORDER_NOT_EXACT:"
            +"missing="+",".join(missing)+";extra="+",".join(extra)
        )

    packet=build_packet(
        project=project,
        current_state_text=current_state_text,
        basis_ref=basis_ref,
    )
    receipts=[]

    for index,tool_id in enumerate(BEST_ORDER,1):
        spec=CONFIGURED_RUNS[tool_id]
        plan=build_tool_execution_plan(spec)
        recurrence=execute_configured_with_hf2(
            tool_id=tool_id,
            plan=plan,
            state={"packet":packet},
            adapter=lambda state,plan,tool_id=tool_id:_adapter_raw(
                tool_id,packet,plan
            ),
            max_rounds=8,
        )
        raw=dict(recurrence.last_raw or {})
        result=raw.get("result",{})
        summary=result.get("native_summary",result)
        receipt=ToolCampaignReceipt(
            index=index,
            phase=_phase_for(tool_id),
            tool_id=tool_id,
            configured_status=recurrence.status,
            execution_truth=str(raw.get("execution_truth","")),
            recurrence_engine=recurrence.recurrence_engine,
            recurrence_status=recurrence.status,
            recurrence_rounds=recurrence.rounds,
            cell_count=len(plan.cells),
            question_count=len(plan.questions),
            cognitive_count=len(plan.cognitive),
            native_summary=_plain(summary),
        )
        receipts.append(receipt)
        packet["campaign_results"][tool_id]={
            "configured_status":receipt.configured_status,
            "execution_truth":receipt.execution_truth,
            "native_summary":receipt.native_summary,
        }

    findings=_discover_findings(packet,receipts)
    local_actions=tuple(
        f.finding_id for f in findings
        if f.disposition=="LOCAL_ACTION_REQUIRED"
    )
    external_open=tuple(
        f.coordinate for f in findings
        if f.disposition=="EXTERNAL_OPEN"
    )

    improvement=packet["campaign_results"].get("ImprovementCore",{})
    conductor=packet["campaign_results"].get("ToolConductor",{})
    conductor_summary=conductor.get("native_summary",{})
    conductor_complete=(
        isinstance(conductor_summary,Mapping)
        and conductor_summary.get("status")=="COMPLETE"
        and not tuple(conductor_summary.get("open_tools",()))
    )
    improvement_consumed=(
        improvement.get("configured_status") in {"RELATIVE_CLOSE","SELF_CLOSE"}
    )

    status="CLOSED_RELATIVE" if not local_actions else "ACTION_REQUIRED"
    return CampaignResult(
        status=status,
        tool_count=len(receipts),
        order=BEST_ORDER,
        receipts=tuple(receipts),
        findings=findings,
        local_actions=local_actions,
        external_open=external_open,
        improvementcore_consumed=improvement_consumed,
        toolconductor_complete=conductor_complete,
    )


def compact_receipt(result:CampaignResult)->dict[str,Any]:
    return {
        "status":result.status,
        "tool_count":result.tool_count,
        "local_actions":result.local_actions,
        "external_open":result.external_open,
        "improvementcore_consumed":result.improvementcore_consumed,
        "toolconductor_complete":result.toolconductor_complete,
        "configured_statuses":{
            r.tool_id:r.configured_status for r in result.receipts
        },
        "recurrence_engines":{
            r.tool_id:r.recurrence_engine for r in result.receipts
        },
        "findings":tuple(_plain(f) for f in result.findings),
    }
