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
from protected_transition_portfolio import audit_protected_transition_portfolio
from system_audit import run_audit
from tool_manifest import OVERRIDES
from tool_manifest_audit import audit_tool_identities
from tool_maturity import audit_all as audit_maturity
from tool_project_packages import audit_materialized
from tool_reality_audit import audit_tool_reality
from tool_run_registry import CONFIGURED_RUNS, MATERIAL_TOOLS
from learning_operator_tools import FunctionalStackState,OODAState,RateDistortionCandidate


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
        "scope":"PROJECT_CHARTER.md",
        "authority":"AUTHORITY_REGISTRY.md",
        "deliverables":"WBS.md",
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
        "handoffs":"TWO_36_SURFACES.md",
    }
    coordinates={}
    authority={}
    for coordinate,file_name in owner_candidates.items():
        if (PROJECT_ROOT/file_name).is_file():
            coordinates[coordinate]={"status":"CURRENT","owner":file_name}
            authority[coordinate]=file_name
    return {
        "project_id":"take5-tool-system",
        "coordinates":coordinates,
        "authority_registry":authority,
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
    return {
        "current_portfolio_identity":plain(identity),
        "full_invocation_portfolio":plain(invocation),
        "protected_transition_portfolio":plain(transitions),
        "tool_manifest_audit":plain(manifests),
        "tool_reality_audit":plain(reality),
        "tool_maturity":maturity_summary(),
        "system_audit":plain(system),
        "tool_project_package_audit":plain(packages),
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
        adapters={"ProjectManager":project_manager_adapter},
    )
    rows=conductor["results"]
    statuses={}
    for row in rows:
        statuses[row["status"]]=statuses.get(row["status"],0)+1
    pm=next(row for row in rows if row["tool_id"]=="ProjectManager")
    dev=development_audits()

    structural_failures=[]
    for name in ("current_portfolio_identity","full_invocation_portfolio","protected_transition_portfolio"):
        status=str(dev[name].get("status",""))
        if status not in {"CLOSED_RELATIVE","PASS"}:
            structural_failures.append(f"{name}:{status}")
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
