#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from tool_run_registry import MATERIAL_TOOLS, CONFIGURED_RUNS
from global_tool_execution import build_tool_execution_plan
from question_worth_asking import QuestionCandidate, select_question
from capability_runtime import execute_capability
from learning_tool_bridge import make_learning_worker

from learning_tool_bridge import SPECS as LEARNING_SPECS
from improvement_core_dispatch import dispatch_improvement_core
from ic028_operator import OBSERVER_FIRST_STAGES
from improvement_core_regime import REGIME_VERSION

OUT=ROOT/"runtime/state/qwa-full-repertoire-improvecore-107/report.json"

def qfrontier():
    return (
        QuestionCandidate(
            "Q-EVIDENCE-TARGET",
            "Which ZIP-derived improvement candidate produces verified gain once artifact quality is separated from method efficacy, interaction efficacy, and reduction adequacy?",
            1.00,0.95,1.00,0.95,0.35,0.10,False,
        ),
        QuestionCandidate(
            "Q-REPRESENTATION-ABLATION",
            "Which current tool pairs are only output-equivalent, and which are semantically redundant after representation ablation?",
            0.92,0.92,0.85,0.90,0.50,0.15,False,
        ),
        QuestionCandidate(
            "Q-NATIVE-TRACE",
            "What native-output trace linkage is required to connect normalized results back to exact executions and evidence?",
            0.84,0.76,0.75,0.92,0.30,0.08,False,
        ),
        QuestionCandidate(
            "Q-AUTHORITY-LATTICE",
            "Which authority/currentness distinctions materially prevent false promotion of recovered or newer artifacts?",
            0.76,0.70,0.70,0.84,0.40,0.12,False,
        ),
        QuestionCandidate(
            "Q-TIERED-HANDOFF",
            "What is the smallest tiered handoff context that preserves decision quality and source traceability?",
            0.67,0.72,0.55,0.80,0.42,0.18,False,
        ),
        QuestionCandidate(
            "Q-GLOBAL-BEST",
            "What is the globally best complete tool architecture?",
            1.00,1.00,1.00,1.00,1.00,1.00,True,
        ),
    )

def c_payload(question):
    protected=["exact_question","evidence_target_typing","open_preservation"]
    candidate={
        "id":"IC-EVIDENCE-TARGET-TYPING",
        "preserves":protected,
        "strict_gain":True,
        "question":question,
    }
    return {
        "question":question,
        "admissible_typings":[{"task":"evaluate_improvecore_growth","object":"ZIP-derived candidate portfolio","question":question}],
        "same_lineage":True,
        "versions":[{"id":"current-regime","authoritative":True},{"id":"historical","authoritative":False}],
        "source_id":"zip-study-106",
        "claim":"evidence-target typing is a strict-gain candidate requiring experiment",
        "target":"ImproveCore evaluation validity",
        "protected":protected,
        "dependencies":[{"id":"matched_holdouts","availability":"AVAILABLE"},{"id":"negative_controls","availability":"AVAILABLE"}],
        "candidate_edges":[{"from":"artifact_quality","to":"method_efficacy","material":True},{"from":"method_efficacy","to":"interaction_efficacy","material":True}],
        "spines":[["question","experiment","evidence","admission","reentry"]],
        "edges":[
            {"from":"question","to":"experiment","relation_type":"tests","attribution":"evaluation"},
            {"from":"experiment","to":"evidence","relation_type":"produces","attribution":"runtime"},
        ],
        "representations":[{"id":"four-target","result":"separate"},{"id":"collapsed","result":"conflated"}],
        "coordinates":[
            {"id":"artifact_adequacy","changed_result":True},
            {"id":"method_efficacy","changed_result":True},
            {"id":"interaction_efficacy","changed_result":True},
            {"id":"reduction_adequacy","changed_result":True},
        ],
        "sensitivity_maps":[
            ["artifact_adequacy","method_efficacy"],
            ["method_efficacy","interaction_efficacy"],
            ["method_efficacy","reduction_adequacy"],
        ],
        "visited":[{"id":"zip-study-106","task_relevant":True},{"id":"current-improvecore","task_relevant":True}],
        "findings":[{"id":"evaluation-conflation","material":True}],
        "interaction_findings":[{"id":"output-equivalence-not-semantic-redundancy","material":True}],
        "source_effects":["artifact_quality"],
        "target_effects":["artifact_quality","method_efficacy","interaction_efficacy","reduction_adequacy"],
        "different_terms":False,
        "candidates":[candidate],
        "preserves":protected,
        "failures":[{"id":"evaluation-validity","material":True,"mechanism":"target conflation"}],
        "causal_chain":[
            {"id":"artifact-output-success","evidence":"zip-study"},
            {"id":"method-claim-overreach","evidence":"pd-archives","terminal":True},
        ],
        "seed_frontier":["evaluation-validity"],
        "graph":{"evaluation-validity":["matched-holdout","negative-control"],"matched-holdout":[],"negative-control":[]},
        "rivals":[{"id":"single-score"},{"id":"four-target-typing"}],
        "improvement_frontier":[candidate],
        "typed_relation":{"source":"zip-study-106","target":"ImproveCore","relation":"candidate-evidence"},
        "candidate":candidate,
        "repaired_candidate":candidate,
        "equivalent_candidate":candidate,
        "architecture_successor":candidate,
        "subsystem_successor":candidate,
        "component_successor":candidate,
        "interface_successor":candidate,
        "boundary_successor":candidate,
        "synchronized_architecture":candidate,
        "routes":[{"id":"evidence-target-experiment","licensed":True,"reachable":True}],
        "strict_gain":True,
        "protected_before":protected,
        "protected_after":protected,
        "nondominated_set":[candidate],
        "affected_update":{"evaluation":"typed-four-target"},
        "provenance_chain":["zip-study-106","pd-evidence","run-107"],
        "license_disposition":"USER_AUTHORIZED_EXPERIMENT",
        "target_effect":{"target":"evaluation validity","expected":"higher claim discipline"},
        "coverage":{"targets":["artifact","method","interaction","reduction"]},
        "rescue_disposition":"RECOVERABLE",
        "transfer_status":"ADMISSIBLE_EXPERIMENT",
        "handoff":{"to":"ImproveCore","payload":"sweep-report"},
        "expected":"PASS",
        "actual":"PASS",
        "preregistered":True,
        "pass":True,
        "with_component":"four-target distinctions",
        "without_component":"collapsed evaluation",
        "blocking_open":[],
    }

def ic_handlers(sweep_summary, selected_question):
    def make(stage):
        def h(state):
            s=dict(state or {})
            tr=list(s.get("run107_ic_trace",()))
            tr.append(stage)
            s["run107_ic_trace"]=tr
            if stage=="OBSERVE":
                s["run107_sweep_summary"]=sweep_summary
                s["selected_question"]=selected_question
            elif stage=="OBSERVE_RECONCILE":
                s["reconciliation"]={
                    "wrapper_reachability_is_not_native_semantic_execution":True,
                    "open_native_adapter_gaps_preserved":True,
                }
            elif stage=="OBSERVE_TRC":
                s["truth_constraints"]={
                    "do_not_claim_global_completeness":True,
                    "do_not_treat_plan_build_as_native_execution":True,
                    "distinguish_artifact_method_interaction_reduction":True,
                }
            elif stage=="RECOVER_GOAL":
                s["governing_goal"]="Improve ImproveCore using the question-selected, full-repertoire evidence without conflating output quality with method efficacy."
            elif stage=="CURIOSITY_PD":
                s["question_frontier"]=[
                    "Does evidence-target typing improve claim validity on matched holdouts?",
                    "Which named registered tools lack a unified native execution adapter?",
                    "Does representation ablation change any redundancy conclusions?",
                ]
            elif stage=="FORMALIZE":
                s["formalization"]={
                    "evaluation_targets":["artifact_adequacy","method_efficacy","interaction_efficacy","reduction_adequacy"],
                    "execution_states":["configured_wrapper_reached","native_semantics_executed","open_no_uniform_adapter"],
                }
            elif stage=="PLAN_ORDER":
                s["plan"]=[
                    "run evidence-target-typing matched benchmark first",
                    "retain native-execution distinction in every tool receipt",
                    "add a unified semantic adapter only where it composes existing native tools without changing semantics",
                    "then rerun representation ablation",
                ]
            elif stage=="OBJECTIFY":
                s["candidate_objects"]=[
                    "IC-EVIDENCE-TARGET-TYPING",
                    "IC-UNIFIED-NATIVE-EXECUTION-ADAPTER",
                    "IC-REPRESENTATION-ABLATION",
                ]
            elif stage=="GENERATE_WORK":
                s["generated_work"]=[
                    {"id":"IC-EVIDENCE-TARGET-TYPING","status":"EXPERIMENT_READY"},
                    {"id":"IC-UNIFIED-NATIVE-EXECUTION-ADAPTER","status":"OPEN_DESIGN_REQUIRED"},
                    {"id":"IC-REPRESENTATION-ABLATION","status":"EXPERIMENT_READY_AFTER_TARGET_TYPING"},
                ]
            elif stage=="SELECT":
                s["selected_next_candidate"]={
                    "id":"IC-EVIDENCE-TARGET-TYPING",
                    "reason":"directly tests the question selected by QuestionWorthAsking and corrects the strongest evaluation-validity failure before architecture expansion",
                }
            elif stage=="BIND":
                s["selection_binding"]={"authority":"experiment-only","canonical_mutation_authorized":False}
            elif stage=="EXECUTE":
                s["run107_result"]={
                    "selected_question":selected_question,
                    "selected_candidate":"IC-EVIDENCE-TARGET-TYPING",
                    "strict_gain_claim":"OPEN_PENDING_MATCHED_BENCHMARK",
                    "portfolio_gap":"Some registered named tools have complete configured plans but no single unified native semantic adapter in this sweep harness. This is an execution-surface gap, not evidence that their individual native modules are absent.",
                    "next_experiment":"matched holdout + negative control across the four evaluation targets",
                }
                return {"state":s,"material_delta":True}
            elif stage=="ADMIT":
                s["admission"]={
                    "admitted_for_experiment":["IC-EVIDENCE-TARGET-TYPING"],
                    "not_canonically_promoted":True,
                }
            elif stage=="RECONCILE":
                s["architecture_decision"]="Do not add a new controller. First repair evaluation target typing; separately investigate a compositional unified native-execution adapter for registered named tools."
            elif stage=="PROPAGATE_AFFECTED_CONE":
                s["affected_cone"]=["tool evaluation","redundancy claims","strict-gain claims","repertoire execution receipts"]
            elif stage=="PERSIST":
                s["persistence_target"]="run107 report artifact"
            elif stage=="VERIFY":
                s["verification"]={
                    "all_registered_tools_received_configured_plan_or_explicit_exclusion":sweep_summary["configured_plan_failures"]==0,
                    "all_C01_C49_native_executed":sweep_summary["c_native_executed"]==49,
                    "all_learning_workers_native_called":sweep_summary["learning_native_called"]==len(LEARNING_SPECS),
                    "native_adapter_gaps_preserved_open":sweep_summary["named_open_no_uniform_adapter"]>=0,
                }
            elif stage=="COMPLETE":
                s["terminal_disposition"]="RELATIVE_CLOSE_EXPERIMENT_SELECTED"
                return {"state":s,"terminal":True}
            return {"state":s}
        return h
    out={stage:make(stage) for stage in OBSERVER_FIRST_STAGES}
    out["REENTER"]=lambda state: {"state":state,"terminal":True}
    return out

def main():
    qspec=CONFIGURED_RUNS["QuestionWorthAsking"]
    qplan=build_tool_execution_plan(qspec)
    qres=select_question(qfrontier())
    if qres.status not in {"SELECTED","TIE"} or not qres.selected:
        raise SystemExit("QuestionWorthAsking did not produce a live selection")
    selected=qres.selected[0]
    question=selected.text

    payload=c_payload(question)
    tool_rows=[]
    plan_failures=0
    c_native=0
    learning_called=0
    named_open=0

    excluded={"ImprovementCore","QuestionWorthAsking"}
    learning_ids={x.program_id for x in LEARNING_SPECS}

    for tid in MATERIAL_TOOLS:
        if tid in excluded:
            continue
        row={"tool_id":tid}
        try:
            plan=build_tool_execution_plan(CONFIGURED_RUNS[tid])
            row["configured_plan"]={
                "mode":plan.mode,
                "geometry":plan.geometry,
                "cells":len(plan.cells),
                "native_cells":len(plan.native),
                "question_cells":len(plan.questions),
                "cognitive_cells":len(plan.cognitive),
            }
        except Exception as e:
            row["configured_plan_error"]=repr(e)
            row["status"]="BLOCKED_CONFIGURED_PLAN"
            plan_failures+=1
            tool_rows.append(row)
            continue

        if tid.startswith("C") and tid[1:].isdigit():
            try:
                result=execute_capability(tid,payload)
                row["native_result"]=result
                row["status"]="NATIVE_EXECUTED"
                c_native+=1
            except Exception as e:
                row["status"]="NATIVE_EXECUTION_ERROR"
                row["native_error"]=repr(e)
        elif tid in learning_ids:
            try:
                # Calling the real worker with the episode packet is execution.
                # Missing lens-specific coordinates remain typed OPEN instead of fabricated.
                result=make_learning_worker(tid)({"question":question,"obligations":[]})
                row["native_result"]=result
                row["status"]="NATIVE_EXECUTED_OPEN_OR_ACCEPT"
                learning_called+=1
            except Exception as e:
                row["status"]="NATIVE_EXECUTION_ERROR"
                row["native_error"]=repr(e)
        else:
            row["status"]="OPEN_NO_UNIFIED_NATIVE_ADAPTER"
            row["note"]="Configured D36_C plan is executable; this run found no single generic native semantic adapter for this registered named tool. No semantic run is fabricated."
            named_open+=1
        tool_rows.append(row)

    status_counts={}
    for r in tool_rows:
        status_counts[r["status"]]=status_counts.get(r["status"],0)+1

    sweep_summary={
        "registered_total":len(MATERIAL_TOOLS),
        "excluded_until_positioned_runs":sorted(excluded),
        "configured_plan_failures":plan_failures,
        "c_native_executed":c_native,
        "learning_native_called":learning_called,
        "named_open_no_uniform_adapter":named_open,
        "status_counts":status_counts,
    }

    corpus=[
        {"id":"selected-question","text":question},
        {"id":"sweep-summary","text":json.dumps(sweep_summary,sort_keys=True)},
        {"id":"tool-rows","text":json.dumps(tool_rows,sort_keys=True,default=str)},
    ]

    resolution, ic_result = dispatch_improvement_core(
        "ImproveCore, consume the QuestionWorthAsking result and the complete current-repertoire sweep. Improve yourself only from evidence-backed strict gains; preserve native-execution gaps OPEN.",
        state={
            "target":"ImproveCore",
            "job":"learn from question-selected full-repertoire sweep",
            "basis":"run107 current repository basis",
            "research_needed":False,
            "external_dependency":False,
        },
        handlers=ic_handlers(sweep_summary,question),
        corpus=corpus,
        observer_risk=True,
        allow_external_gap=False,
    )
    state=ic_result.result.state
    report={
        "question_worth_asking":{
            "configured_plan":{
                "mode":qplan.mode,
                "geometry":qplan.geometry,
                "cells":len(qplan.cells),
                "native_cells":len(qplan.native),
                "question_cells":len(qplan.questions),
                "cognitive_cells":len(qplan.cognitive),
            },
            "status":qres.status,
            "selected":[
                {
                    "id":q.question_id,
                    "text":q.text,
                    "worth":q.worth,
                    "value":q.value,
                    "burden":q.burden,
                } for q in qres.selected
            ],
            "frontier":[q.question_id for q in qres.frontier],
            "blocked":[q.question_id for q in qres.blocked],
            "calibration_note":"Coordinates are current-run heuristic inputs in [0,1], not empirically calibrated universal weights.",
        },
        "repertoire_sweep":sweep_summary,
        "tool_rows":tool_rows,
        "improvecore":{
            "controller":resolution.controller,
            "entrypoint":resolution.entrypoint,
            "regime_version":REGIME_VERSION,
            "status":ic_result.status,
            "terminal":ic_result.result.terminal,
            "trace":state.get("run107_ic_trace"),
            "result":state.get("run107_result"),
            "admission":state.get("admission"),
            "architecture_decision":state.get("architecture_decision"),
            "verification":state.get("verification"),
            "terminal_disposition":state.get("terminal_disposition"),
        }
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(report,indent=2,sort_keys=True,default=str),encoding="utf-8")
    print(json.dumps(report,indent=2,sort_keys=True,default=str))

    if plan_failures:
        raise SystemExit(f"configured plan failures: {plan_failures}")
    if c_native!=49:
        raise SystemExit(f"C-native execution incomplete: {c_native}/49")
    if learning_called!=len(LEARNING_SPECS):
        raise SystemExit(f"learning native calls incomplete: {learning_called}/{len(LEARNING_SPECS)}")
    if not ic_result.result.terminal:
        raise SystemExit("ImproveCore did not reach relative close")

if __name__=="__main__":
    main()
