#!/usr/bin/env python3
"""ImprovementCore Legacy-restoration campaign 130.

This is an actual current ImprovementCore dispatcher run with default HF002 recurrence.
Each HF2 successor pass examines the same restoration target after the prior pass changed
semantic state. The workflow is read-only with respect to repository files; it emits the
selected strict-gain implementation target as an execution receipt for host admission.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from improvement_core_dispatch import dispatch_improvement_core
from ic028_operator import GOAL_DIRECTED_STAGES

TARGET=ROOT/"architecture/IMPROVEMENT_CORE_LEGACY_RESTORATION_TARGET_129.md"
BENCH=ROOT/"integration/IC128_LEGACY_BEHAVIOR_BENCHMARK_129.yaml"
CURRENT=ROOT/"integration/CURRENT_IMPROVEMENT_CORE.md"
OPERATOR=ROOT/"runtime/ic028_operator.py"
HF2=ROOT/"runtime/improvement_core_hf2_default.py"
LEGACY=ROOT/"legacy/icc128-legacy/snapshot/runtime/icc128_autonomous_controller.py"
RHO=ROOT/"legacy/icc128-legacy/snapshot/runtime/rho128_policy.py"

def read(p): return p.read_text(encoding="utf-8")

def evidence_snapshot():
    operator=read(OPERATOR)
    rho=read(RHO)
    legacy=read(LEGACY)
    benchmark=read(BENCH)
    return {
        "fixed_goal_directed_stage_train":"GOAL_DIRECTED_STAGES=(" in operator,
        "goal_stage_count":len(GOAL_DIRECTED_STAGES),
        "legacy_loop_present":"G_Q -> G_W -> S -> E -> A -> U -> G_Q" in legacy,
        "cheap_direct_present":'"CHEAP_DIRECT"' in rho,
        "do_not_run_everything":"do_not_run_everything_by_default" in read(ROOT/"legacy/icc128-legacy/snapshot/contracts/ICC128_RHO_POLICY_CURRENT.yaml"),
        "result_sensitive_reselection":"needs_reselection" in rho,
        "benchmark_cheap_direct":"id: CHEAP_DIRECT_PATH" in benchmark,
        "benchmark_endogenous":"id: ENDOGENOUS_QUESTION_GENERATION" in benchmark,
        "benchmark_reselection":"id: RESULT_SENSITIVE_RESELECTION" in benchmark,
        "benchmark_no_premature":"id: NO_PREMATURE_TERMINALITY" in benchmark,
        "current_hf2_default":"run_improvement_core_with_hf2" in read(HF2),
    }

def handlers():
    snap=evidence_snapshot()

    def make(stage):
        def h(state):
            s=dict(state or {})
            trace=list(s.get("campaign_stage_trace",()))
            trace.append(stage)
            s["campaign_stage_trace"]=trace

            if stage=="RECOVER_GOAL":
                s["goal"]="restore Legacy behavioral control law without discarding current protections"
            elif stage=="CURIOSITY_PD":
                s["live_distinctions"]=(
                    "fixed stage train versus state-relative controller routing",
                    "Legacy semantic loop versus modern protection envelope",
                    "active context versus durable recovery corpus",
                )
            elif stage=="FORMALIZE":
                s["protected_target"]=(
                    "G_Q","G_W","S","E","A","U","G_Q",
                    "CHEAP_DIRECT","RESULT_SENSITIVE_RESELECTION",
                )
            elif stage=="PLAN_ORDER":
                s["campaign_rule"]="one strict-gain residual per HF2 successor"
            elif stage=="OBSERVE":
                s["evidence_snapshot"]=snap
            elif stage=="OBJECTIFY":
                s["objects"]=(
                    "runtime/ic028_operator.py",
                    "legacy ICC128 controller",
                    "legacy rho128 policy",
                    "current HF2 envelope",
                    "Legacy behavior benchmark 129",
                )
            elif stage=="GENERATE_WORK":
                phase=int(s.get("campaign_phase",0))
                if phase==0:
                    s["work_frontier"]=("diagnose_control_law_delta",)
                elif phase==1:
                    s["work_frontier"]=(
                        "wrap frozen Legacy inquiry loop with modern protection services",
                        "patch fixed stage train with skip flags only",
                        "replace modern protections with frozen Legacy wholesale",
                    )
                elif phase==2:
                    s["work_frontier"]=("specify_minimal_candidate_runtime_and_tests",)
                else:
                    s["work_frontier"]=()
            elif stage=="SELECT":
                phase=int(s.get("campaign_phase",0))
                if phase==0:
                    s["selected_work"]="diagnose_control_law_delta"
                elif phase==1:
                    s["selected_work"]="LEGACY_LOOP_MODERN_GUARDS"
                elif phase==2:
                    s["selected_work"]="IMPLEMENT_ADAPTIVE_LEGACY_CORE_CANDIDATE"
                else:
                    s["selected_work"]="NONE"
            elif stage=="BIND":
                s["binding"]="repository evidence at workflow commit"
            elif stage=="EXECUTE":
                phase=int(s.get("campaign_phase",0))
                if phase==0:
                    s["diagnosis"]={
                        "fixed_stage_train":snap["fixed_goal_directed_stage_train"],
                        "stage_count":snap["goal_stage_count"],
                        "legacy_cheap_direct":snap["cheap_direct_present"],
                        "legacy_reselection":snap["result_sensitive_reselection"],
                        "defect":"CURRENT_OPERATOR_DOES_NOT_EXPRESS_LEGACY_STATE_RELATIVE_CHEAP_DIRECT_CONTROL",
                    }
                    s["campaign_phase"]=1
                    return {"state":s,"material_delta":True}
                if phase==1:
                    s["candidate_decision"]={
                        "selected":"LEGACY_LOOP_MODERN_GUARDS",
                        "reject":{
                            "SKIP_FLAGS_ONLY":"does not restore endogenous question/work/reselection loop",
                            "FROZEN_LEGACY_WHOLESALE":"would discard modern protection and recovery gains",
                        },
                        "reason":"smallest architecture preserving both historical controller law and current safeguards",
                    }
                    s["campaign_phase"]=2
                    return {"state":s,"material_delta":True}
                if phase==2:
                    s["implementation_target"]={
                        "new_runtime":"runtime/improvement_core_legacy_candidate.py",
                        "reuse":[
                            "legacy/icc128-legacy/snapshot/runtime/icc128_autonomous_controller.py",
                            "legacy/icc128-legacy/snapshot/runtime/rho128_policy.py",
                            "runtime/improvement_core_tool_bridge.py",
                            "runtime/improvement_core_knowledge_ledger.py",
                            "runtime/improvement_core_hf2_default.py",
                        ],
                        "required_tests":[
                            "cheap direct executes one minimal package",
                            "deep route preserves nondominated plurality",
                            "material delta causes reselection",
                            "live inquiry prevents premature terminality",
                            "configured tool execution remains fail-closed",
                            "modern OPEN/BLOCKED/CONFLICT preserved",
                        ],
                        "promotion":"candidate only until heterogeneous behavioral holdouts pass",
                    }
                    s["campaign_phase"]=3
                    return {"state":s,"material_delta":True}
                s["campaign_phase"]=3
                s["hf2_disable_local_recurrence"]=True
                return {"state":s,"material_delta":False}
            elif stage=="ADMIT":
                s["admission"]="ADMIT_STRICT_GAIN_TARGET_ONLY"
            elif stage=="RECONCILE":
                s["remaining_residual"]=(
                    "implement and validate candidate runtime"
                    if int(s.get("campaign_phase",0))<3 else
                    "candidate implementation now licensed; archive ingestion waits for actual master archive"
                )
            elif stage=="PROPAGATE_AFFECTED_CONE":
                s["affected_cone"]=(
                    "user-facing controller routing",
                    "Legacy behavioral benchmark",
                    "configured execution protection",
                    "HF2 successor recurrence",
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
                        snap["benchmark_reselection"],snap["benchmark_no_premature"]
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
    _,result=dispatch_improvement_core(
        "ImproveCore, restore the Legacy behavior and keep rerunning with HF2 while material residuals remain",
        target="ImprovementCore Legacy behavioral restoration target 129",
        job="restore Legacy controller behavior with modern safeguards",
        basis="Take-5 current + frozen ICC128 Legacy evidence",
        state={"campaign_phase":0},
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
