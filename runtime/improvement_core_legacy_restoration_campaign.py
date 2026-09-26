#!/usr/bin/env python3
"""ImprovementCore Legacy-restoration campaign 130.

Actual current ImprovementCore dispatcher run with default HF002 recurrence.
The campaign is successor-sensitive: before candidate implementation it selects the
smallest strict-gain runtime; after implementation it audits the successor and moves
to the next material promotion residual rather than rediscovering the same repair.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from improvement_core_dispatch import dispatch_improvement_core
from ic028_operator import GOAL_DIRECTED_STAGES

BENCH=ROOT/"integration/IC128_LEGACY_BEHAVIOR_BENCHMARK_129.yaml"
OPERATOR=ROOT/"runtime/ic028_operator.py"
HF2=ROOT/"runtime/improvement_core_hf2_default.py"
LEGACY=ROOT/"legacy/icc128-legacy/snapshot/runtime/icc128_autonomous_controller.py"
RHO=ROOT/"legacy/icc128-legacy/snapshot/runtime/rho128_policy.py"
RHO_CONTRACT=ROOT/"legacy/icc128-legacy/snapshot/contracts/ICC128_RHO_POLICY_CURRENT.yaml"
CANDIDATE=ROOT/"runtime/improvement_core_legacy_candidate.py"
CANDIDATE_TESTS=ROOT/"tests/test_improvement_core_legacy_candidate.py"
RESTORED=ROOT/"runtime/improvement_core_legacy_restored.py"
RESTORED_TESTS=ROOT/"tests/test_improvement_core_legacy_restored.py"
CONTROL_RECEIPT=ROOT/"artifacts/improvecore/LEGACY_CANDIDATE_CONTROL_HOLDOUT_131_2026-09-26.md"
SEMANTIC_RECEIPT=ROOT/"artifacts/improvecore/LEGACY_RESTORED_SEMANTIC_HOLDOUT_132_2026-09-26.md"

def read(p): return p.read_text(encoding="utf-8")

def evidence_snapshot():
    operator=read(OPERATOR)
    rho=read(RHO)
    legacy=read(LEGACY)
    benchmark=read(BENCH)
    candidate=CANDIDATE.exists()
    candidate_text=read(CANDIDATE) if candidate else ""
    tests=CANDIDATE_TESTS.exists()
    tests_text=read(CANDIDATE_TESTS) if tests else ""
    restored=RESTORED.exists()
    restored_text=read(RESTORED) if restored else ""
    restored_tests=RESTORED_TESTS.exists()
    restored_tests_text=read(RESTORED_TESTS) if restored_tests else ""
    control_receipt=read(CONTROL_RECEIPT) if CONTROL_RECEIPT.exists() else ""
    semantic_receipt=read(SEMANTIC_RECEIPT) if SEMANTIC_RECEIPT.exists() else ""
    return {
        "fixed_goal_directed_stage_train":"GOAL_DIRECTED_STAGES=(" in operator,
        "goal_stage_count":len(GOAL_DIRECTED_STAGES),
        "legacy_loop_present":"G_Q -> G_W -> S -> E -> A -> U -> G_Q" in legacy,
        "cheap_direct_present":'"CHEAP_DIRECT"' in rho,
        "do_not_run_everything":"do_not_run_everything_by_default" in read(RHO_CONTRACT),
        "result_sensitive_reselection":"needs_reselection" in rho,
        "benchmark_cheap_direct":"id: CHEAP_DIRECT_PATH" in benchmark,
        "benchmark_endogenous":"id: ENDOGENOUS_QUESTION_GENERATION" in benchmark,
        "benchmark_reselection":"id: RESULT_SENSITIVE_RESELECTION" in benchmark,
        "benchmark_no_premature":"id: NO_PREMATURE_TERMINALITY" in benchmark,
        "benchmark_holdouts":"unlike_domains_minimum: 4" in benchmark,
        "benchmark_ablation":"causal_ablation:" in benchmark and "required: true" in benchmark,
        "current_hf2_default":"run_improvement_core_with_hf2" in read(HF2),
        "candidate_present":candidate,
        "candidate_tests_present":tests,
        "candidate_reuses_legacy":"icc128_legacy.activate()" in candidate_text,
        "candidate_uses_current_tool_bridge":"execute_bound_tools" in candidate_text,
        "candidate_entry_contract":"bind_entry_contract" in restored_text,
        "candidate_external_acquisition":"acquire_external" in restored_text,
        "candidate_knowledge_ledger":"KnowledgeLedger" in restored_text,
        "candidate_outer_hf2":"HF002RecursiveContinuation" in restored_text,
        "restored_wrapper_present":restored,
        "restored_tests_present":restored_tests,
        "restored_observer_guard":"OBSERVER_PREPARE_REQUIRED" in restored_text,
        "restored_external_gap_test":"test_external_gap_survives_candidate_completion" in restored_tests_text,
        "restored_hf2_test":"test_outer_hf2_reapplies_same_capability_when_local_frontier_live" in restored_tests_text,
        "candidate_cheap_direct_test":"test_cheap_direct_executes_one_minimal_package" in tests_text,
        "candidate_plurality_test":"test_deep_route_preserves_nondominated_plurality" in tests_text,
        "candidate_reselection_test":"test_material_delta_records_reselection_requirement" in tests_text,
        "candidate_liveness_test":"test_live_inquiry_cannot_silently_terminate" in tests_text,
        "candidate_fail_closed_test":"test_missing_configured_tool_adapter_preserves_open" in tests_text,
        "control_holdout_pass":"4/4 PASS" in control_receipt and "2/2 PASS" in control_receipt,
        "semantic_holdout_pass":"4/4 PASS" in semantic_receipt and "HOST_MODEL_SUPPLIED_SEMANTIC_FRONTIER + REPOSITORY_CONTROL_EXECUTION" in semantic_receipt,
        "semantic_evidence_nonindependent":"not independent-agent replication" in semantic_receipt.lower(),
    }

def handlers():
    snap=evidence_snapshot()

    def make(stage):
        def h(state):
            s=dict(state or {})
            trace=list(s.get("campaign_stage_trace",()))
            trace.append(stage)
            s["campaign_stage_trace"]=trace
            phase=int(s.get("campaign_phase",10 if snap["candidate_present"] else 0))

            if stage=="RECOVER_GOAL":
                s["goal"]="restore Legacy behavioral control law without discarding current protections"
            elif stage=="CURIOSITY_PD":
                s["live_distinctions"]=(
                    "implemented control mechanics versus demonstrated semantic effectiveness",
                    "candidate runtime versus current user-facing promotion",
                    "internal restoration residual versus external master-archive availability",
                ) if snap["candidate_present"] else (
                    "fixed stage train versus state-relative controller routing",
                    "Legacy semantic loop versus modern protection envelope",
                    "active context versus durable recovery corpus",
                )
            elif stage=="FORMALIZE":
                s["protected_target"]=(
                    "G_Q","G_W","S","E","A","U","G_Q",
                    "CHEAP_DIRECT","RESULT_SENSITIVE_RESELECTION",
                    "OPEN_BLOCKED_CONFLICT","EXECUTION_TRUTH",
                )
            elif stage=="PLAN_ORDER":
                s["campaign_rule"]="one strict-gain residual per HF2 successor"
            elif stage=="OBSERVE":
                s["evidence_snapshot"]=snap
            elif stage=="OBJECTIFY":
                s["objects"]=(
                    "candidate runtime",
                    "Legacy behavior benchmark 129",
                    "current ImprovementCore user-facing path",
                    "master archive external evidence boundary",
                )
            elif stage=="GENERATE_WORK":
                if phase==0:
                    s["work_frontier"]=("diagnose_control_law_delta",)
                elif phase==1:
                    s["work_frontier"]=(
                        "LEGACY_LOOP_MODERN_GUARDS",
                        "SKIP_FLAGS_ONLY",
                        "FROZEN_LEGACY_WHOLESALE",
                    )
                elif phase==2:
                    s["work_frontier"]=("IMPLEMENT_ADAPTIVE_LEGACY_CORE_CANDIDATE",)
                elif phase==10:
                    s["work_frontier"]=("AUDIT_IMPLEMENTED_CANDIDATE",)
                elif phase==11:
                    s["work_frontier"]=(
                        "RUN_HETEROGENEOUS_BEHAVIORAL_HOLDOUTS",
                        "PROMOTE_IMMEDIATELY",
                        "REDESIGN_AGAIN",
                    )
                elif phase==12:
                    s["work_frontier"]=(
                        "INTEGRATE_MODERN_GUARD_WRAPPER",
                        "RUN_CONTROL_HOLDOUTS",
                        "RUN_SEMANTIC_HOLDOUTS",
                        "ASSESS_REPOSITORY_PROMOTION_BOUNDARY",
                    )
                elif phase==13:
                    s["work_frontier"]=(
                        "ADD_GOVERNED_RESTORED_DISPATCH",
                        "REPLACE_CURRENT_DISPATCH_WITHOUT_HOST_BINDING",
                        "REDESIGN_CONTROLLER_AGAIN",
                    )
                else:
                    s["work_frontier"]=()
            elif stage=="SELECT":
                choices={
                    0:"diagnose_control_law_delta",
                    1:"LEGACY_LOOP_MODERN_GUARDS",
                    2:"IMPLEMENT_ADAPTIVE_LEGACY_CORE_CANDIDATE",
                    10:"AUDIT_IMPLEMENTED_CANDIDATE",
                    11:"RUN_HETEROGENEOUS_BEHAVIORAL_HOLDOUTS",
                    12:"RESOLVE_CURRENT_PROMOTION_RESIDUAL",
                    13:"ADD_GOVERNED_RESTORED_DISPATCH",
                }
                s["selected_work"]=choices.get(phase,"NONE")
            elif stage=="BIND":
                s["binding"]="repository evidence at workflow commit"
            elif stage=="EXECUTE":
                if phase==0:
                    s["diagnosis"]={
                        "defect":"CURRENT_OPERATOR_DOES_NOT_EXPRESS_LEGACY_STATE_RELATIVE_CHEAP_DIRECT_CONTROL",
                        "fixed_stage_train":snap["fixed_goal_directed_stage_train"],
                        "stage_count":snap["goal_stage_count"],
                        "legacy_cheap_direct":snap["cheap_direct_present"],
                        "legacy_reselection":snap["result_sensitive_reselection"],
                    }
                    s["campaign_phase"]=1
                    return {"state":s,"material_delta":True}
                if phase==1:
                    s["candidate_decision"]={
                        "selected":"LEGACY_LOOP_MODERN_GUARDS",
                        "reject":{
                            "SKIP_FLAGS_ONLY":"does not restore endogenous inquiry/reselection",
                            "FROZEN_LEGACY_WHOLESALE":"discards modern protections",
                        },
                    }
                    s["campaign_phase"]=2
                    return {"state":s,"material_delta":True}
                if phase==2:
                    s["implementation_target"]="runtime/improvement_core_legacy_candidate.py"
                    s["campaign_phase"]=3
                    return {"state":s,"material_delta":True}
                if phase==10:
                    checks={
                        "runtime_present":snap["candidate_present"],
                        "tests_present":snap["candidate_tests_present"],
                        "reuses_frozen_legacy":snap["candidate_reuses_legacy"],
                        "uses_current_tool_bridge":snap["candidate_uses_current_tool_bridge"],
                        "entry_contract":snap["candidate_entry_contract"],
                        "external_acquisition":snap["candidate_external_acquisition"],
                        "knowledge_ledger":snap["candidate_knowledge_ledger"],
                        "outer_hf2":snap["candidate_outer_hf2"],
                        "restored_wrapper_present":snap["restored_wrapper_present"],
                        "restored_tests_present":snap["restored_tests_present"],
                        "observer_guard":snap["restored_observer_guard"],
                        "external_gap_test":snap["restored_external_gap_test"],
                        "outer_hf2_test":snap["restored_hf2_test"],
                        "cheap_direct_test":snap["candidate_cheap_direct_test"],
                        "plurality_test":snap["candidate_plurality_test"],
                        "reselection_test":snap["candidate_reselection_test"],
                        "liveness_test":snap["candidate_liveness_test"],
                        "fail_closed_test":snap["candidate_fail_closed_test"],
                    }
                    s["successor_audit"]=checks
                    s["candidate_static_complete"]=all(checks.values())
                    s["campaign_phase"]=11
                    return {"state":s,"material_delta":True}
                if phase==11:
                    if not s.get("candidate_static_complete",False):
                        selected_next="INTEGRATE_MODERN_GUARD_WRAPPER"
                        reason="selected LEGACY_LOOP_MODERN_GUARDS architecture is not fully realized"
                    elif not snap["control_holdout_pass"]:
                        selected_next="RUN_CONTROL_HOLDOUTS"
                        reason="implemented control law lacks declared heterogeneous control/ablation receipt"
                    elif not snap["semantic_holdout_pass"]:
                        selected_next="RUN_SEMANTIC_HOLDOUTS"
                        reason="control mechanics pass but unlike semantic routing evidence is still absent"
                    else:
                        selected_next="ASSESS_REPOSITORY_PROMOTION_BOUNDARY"
                        reason="implementation, control holdouts, ablations, modern guards, and multi-domain semantic routing all pass on their declared evidence classes"
                    s["promotion_decision"]={
                        "status":"OPEN",
                        "reason":reason,
                        "selected_next":selected_next,
                        "evidence_class_boundary":{
                            "semantic_holdouts_nonindependent":snap["semantic_evidence_nonindependent"],
                            "universal_host_model_binding":"NOT_REPOSITORY_OWNED",
                        },
                        "reject":{
                            "PROMOTE_WITHOUT_HOST_BINDING":"repository cannot manufacture open-ended semantic generation",
                            "REDESIGN_AGAIN":"no failing controller witness currently licenses another redesign",
                        },
                    }
                    s["campaign_phase"]=12
                    return {"state":s,"material_delta":True}
                if phase==12:
                    selected_next=s.get("promotion_decision",{}).get("selected_next")
                    if selected_next=="INTEGRATE_MODERN_GUARD_WRAPPER":
                        s["implementation_target"]={
                            "new_runtime":"runtime/improvement_core_legacy_restored.py",
                            "wraps":"runtime/improvement_core_legacy_candidate.py",
                            "required_services":["entry_contract","external_acquisition","knowledge_ledger","HF002"],
                        }
                    elif selected_next=="RUN_CONTROL_HOLDOUTS":
                        s["implementation_target"]="runtime/improvement_core_legacy_holdout_campaign.py"
                    elif selected_next=="RUN_SEMANTIC_HOLDOUTS":
                        s["implementation_target"]="runtime/improvement_core_legacy_semantic_holdouts_132.py"
                    elif selected_next=="ASSESS_REPOSITORY_PROMOTION_BOUNDARY":
                        s["promotion_boundary"]={
                            "repository_restored_controller":"ADMISSION_READY",
                            "semantic_provider_contract":"REQUIRED",
                            "automatic_universal_chat_host_binding":"EXTERNAL_NOT_OWNED",
                            "selected_next":"ADD_GOVERNED_RESTORED_DISPATCH",
                            "rule":"route to restored controller when an explicit semantic provider is bound; never silently substitute the fixed-stage controller under a restored-execution claim",
                        }
                    s["campaign_phase"]=13
                    return {"state":s,"material_delta":True}
                if phase==13:
                    if s.get("promotion_boundary",{}).get("selected_next")=="ADD_GOVERNED_RESTORED_DISPATCH":
                        s["implementation_target"]={
                            "new_runtime":"runtime/improvement_core_restored_dispatch.py",
                            "semantic_provider":"explicit required host binding",
                            "fallback":"typed OPEN when restored semantics are requested but provider is unavailable",
                            "compatibility":"existing fixed-stage dispatch remains available as legacy compatibility/debug surface until host binding is universal",
                        }
                    s["campaign_phase"]=14
                    return {"state":s,"material_delta":True}
                s["hf2_disable_local_recurrence"]=True
                return {"state":s,"material_delta":False}
            elif stage=="ADMIT":
                s["admission"]="ADMIT_STRICT_GAIN_ONLY"
            elif stage=="RECONCILE":
                if int(s.get("campaign_phase",0))>=14:
                    s["remaining_residual"]="implement governed restored dispatch; universal automatic host semantic binding remains external"
                elif int(s.get("campaign_phase",0))>=13:
                    s["remaining_residual"]="repository promotion boundary / semantic host binding"
                elif int(s.get("campaign_phase",0))>=3 and not snap["candidate_present"]:
                    s["remaining_residual"]="implement candidate runtime"
            elif stage=="PROPAGATE_AFFECTED_CONE":
                s["affected_cone"]=(
                    "user-facing controller routing",
                    "Legacy behavioral benchmark",
                    "configured execution protection",
                    "HF2 recurrence",
                )
            elif stage=="PERSIST":
                s["persist"]="workflow execution receipt"
            elif stage=="VERIFY":
                s["verification"]={
                    "legacy_reference_recovered":all([
                        snap["legacy_loop_present"],snap["cheap_direct_present"],
                        snap["result_sensitive_reselection"]
                    ]),
                    "current_hf2_present":snap["current_hf2_default"],
                    "benchmark_bound":all([
                        snap["benchmark_cheap_direct"],snap["benchmark_endogenous"],
                        snap["benchmark_reselection"],snap["benchmark_no_premature"],
                    ]),
                }
            elif stage=="COMPLETE":
                return {"state":s,"terminal":True}
            return {"state":s}
        return h

    out={stage:make(stage) for stage in GOAL_DIRECTED_STAGES}
    out["REENTER"]=lambda state:{"state":state,"terminal":True}
    return out

def run(output:Path):
    snap=evidence_snapshot()
    initial_phase=10 if snap["candidate_present"] else 0
    _,result=dispatch_improvement_core(
        "ImproveCore, restore the Legacy behavior and keep rerunning with HF2 while material residuals remain",
        target="ImprovementCore Legacy behavioral restoration target 129",
        job="restore Legacy controller behavior with modern safeguards",
        basis="Take-5 current + frozen ICC128 Legacy evidence",
        state={"campaign_phase":initial_phase},
        handlers=handlers(),
        explicit_mode="GOAL_DIRECTED",
        allow_external_gap=False,
        hf2_enabled=True,
        hf2_max_rounds=8,
    )
    report={
        "controller":result.receipt.controller,
        "status":result.status,
        "blocker":result.blocker,
        "hf2_status":result.hf2_status,
        "hf2_rounds":len(result.hf2_trace),
        "hf2_trace":list(result.hf2_trace),
        "final_state":result.result.state,
    }
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2,sort_keys=True,default=str),encoding="utf-8")
    print(json.dumps(report,indent=2,sort_keys=True,default=str))
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default=str(ROOT/"runtime/state/improvecore-legacy-restoration-130/report.json"))
    a=p.parse_args()
    run(Path(a.output))

if __name__=="__main__":
    main()
