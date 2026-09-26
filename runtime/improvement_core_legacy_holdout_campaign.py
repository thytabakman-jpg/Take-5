#!/usr/bin/env python3
"""Control holdouts and causal ablations for Legacy-loop candidate 131."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from improvement_core_legacy_candidate import run_legacy_candidate
from ic028_operator import GOAL_DIRECTED_STAGES


def base_state(work_items, **extra):
    s={
        "terminal":"CONTINUE",
        "admitted_continuation":True,
        "required_jobs":["solve"],
        "work_items":work_items,
    }
    s.update(extra)
    return s


def qgen(state,memory):
    return [{
        "question_id":f"q:{state.get('phase',0)}",
        "issue":state.get("issue","resolve live residual"),
        "obligations":["solve"],
    }]


def workgen(q,state,memory):
    return list(state["work_items"])


def run_formal_research():
    calls=[]
    state=base_state(
        [
            {"id":"counterexample_check","jobs":["solve"],"burden":1,"info_gain":5},
            {"id":"full_spectrum_audit","jobs":["solve"],"burden":8,"info_gain":5},
        ],
        task_and_job_well_typed=True,
        one_validated_capability_clearly_fits=True,
        consequence_bounded=True,
        no_material_rival_exposed=True,
        issue="test the smallest discriminating formal argument",
    )
    def execute(selected,state,memory):
        calls.append([x["id"] for x in selected])
        return [{"status":"EXECUTED","result":"counterexample separates candidates"}]
    def update(state,memory,delta):
        s=dict(state); s["terminal"]="COMPLETE"; s["admitted_continuation"]=False
        return s,dict(memory)
    out=run_legacy_candidate(
        state,{},generate_questions=qgen,generate_work=workgen,
        execute_work=execute,admit_results=lambda r,s,m:{"material_result_delta":True},
        update_state=update,
    )
    return {
        "domain":"formal_research",
        "status":out.status,
        "selected":calls,
        "activation":[x["activation_mode"] for x in out.selection_traces],
        "pass":out.status=="COMPLETE" and calls==[["counterexample_check"]],
    }


def run_artifact_reselection():
    calls=[]
    state=base_state(
        [
            {"id":"structure_probe","jobs":["solve"],"burden":3,"info_gain":8,"dependency_leverage":2},
            {"id":"copy_probe","jobs":["solve"],"burden":3,"info_gain":2,"dependency_leverage":8},
        ],
        multiple_material_packages_fit=True,
        phase=0,
        issue="determine whether structure or copy is the live artifact bottleneck",
    )
    def execute(selected,state,memory):
        calls.append([x["id"] for x in selected])
        return [{"status":"EXECUTED","phase":state["phase"],"selected":[x["id"] for x in selected]}]
    def admit(results,state,memory):
        return {"material_result_delta":True,"changed_representation":state["phase"]==0}
    def update(state,memory,delta):
        s=dict(state)
        if s["phase"]==0:
            s["phase"]=1
            s["multiple_material_packages_fit"]=False
            s["task_and_job_well_typed"]=True
            s["one_validated_capability_clearly_fits"]=True
            s["consequence_bounded"]=True
            s["no_material_rival_exposed"]=True
            s["work_items"]=[{"id":"finalize_structure","jobs":["solve"],"burden":1,"info_gain":5}]
            s["admitted_continuation"]=True
            s["terminal"]="CONTINUE"
        else:
            s["terminal"]="COMPLETE"
            s["admitted_continuation"]=False
        return s,dict(memory)
    out=run_legacy_candidate(
        state,{},generate_questions=qgen,generate_work=workgen,
        execute_work=execute,admit_results=admit,update_state=update,max_iterations=4,
    )
    modes=[x["activation_mode"] for x in out.selection_traces]
    return {
        "domain":"artifact_work",
        "status":out.status,
        "selected":calls,
        "activation":modes,
        "pass":out.status=="COMPLETE" and modes==["FIRE","CHEAP_DIRECT"] and calls[-1]==["finalize_structure"],
    }


def run_external_archive_boundary():
    state=base_state(
        [{"id":"acquire_archive","jobs":["solve"],"burden":1}],
        task_and_job_well_typed=True,
        one_validated_capability_clearly_fits=True,
        consequence_bounded=True,
        no_material_rival_exposed=True,
        issue="bind the unavailable master archive without inventing it",
    )
    def execute(selected,state,memory):
        return [{"status":"OPEN","execution_truth":"NOT_EXECUTED","blocker":"MASTER_ARCHIVE_NOT_ADDRESSABLE"}]
    out=run_legacy_candidate(
        state,{},generate_questions=qgen,generate_work=workgen,
        execute_work=execute,admit_results=lambda r,s,m:{},
        update_state=lambda s,m,d:(dict(s),dict(m)),
    )
    return {
        "domain":"external_archive_recovery",
        "status":out.status,
        "terminal":out.state.get("terminal"),
        "pass":out.status=="OPEN" and out.state.get("terminal")=="OPEN",
    }


def run_system_debug_fail_closed():
    state=base_state(
        [{"id":"root","jobs":["solve"],"burden":1,"tool_id":"RootCause"}],
        task_and_job_well_typed=True,
        one_validated_capability_clearly_fits=True,
        consequence_bounded=True,
        no_material_rival_exposed=True,
        issue="execute formal debugging tool through configured runtime",
    )
    out=run_legacy_candidate(
        state,{},generate_questions=qgen,generate_work=workgen,
        execute_work=None,admit_results=lambda r,s,m:{},
        update_state=lambda s,m,d:(dict(s),dict(m)),
        configured_tool_adapters={},
    )
    return {
        "domain":"system_debug",
        "status":out.status,
        "terminal":out.state.get("terminal"),
        "pass":out.status=="OPEN" and out.state.get("terminal")=="OPEN",
    }


def ablate_question_generation():
    state=base_state(
        [{"id":"x","jobs":["solve"],"burden":1}],
        task_and_job_well_typed=True,
        one_validated_capability_clearly_fits=True,
        consequence_bounded=True,
        no_material_rival_exposed=True,
    )
    try:
        run_legacy_candidate(
            state,{},generate_questions=lambda s,m:[],generate_work=workgen,
            execute_work=lambda x,s,m:[{"status":"EXECUTED"}],
            admit_results=lambda r,s,m:{},
            update_state=lambda s,m,d:(dict(s),dict(m)),
            max_iterations=1,
        )
    except RuntimeError as exc:
        return {"ablation":"question_generation","observed":str(exc),"pass":"LIVENESS_FAILURE" in str(exc)}
    return {"ablation":"question_generation","observed":"NO_FAILURE","pass":False}


def ablate_result_sensitive_update():
    state=base_state(
        [{"id":"stale_route","jobs":["solve"],"burden":1}],
        task_and_job_well_typed=True,
        one_validated_capability_clearly_fits=True,
        consequence_bounded=True,
        no_material_rival_exposed=True,
    )
    try:
        run_legacy_candidate(
            state,{},generate_questions=qgen,generate_work=workgen,
            execute_work=lambda x,s,m:[{"status":"EXECUTED"}],
            admit_results=lambda r,s,m:{"material_result_delta":True,"changed_representation":True},
            update_state=lambda s,m,d:({**s,"terminal":"CONTINUE","admitted_continuation":True},dict(m)),
            max_iterations=2,
        )
    except RuntimeError as exc:
        return {"ablation":"result_sensitive_update","observed":str(exc),"pass":"RESOURCE_BOUND" in str(exc)}
    return {"ablation":"result_sensitive_update","observed":"NO_FAILURE","pass":False}


def run(output):
    holdouts=[
        run_formal_research(),
        run_artifact_reselection(),
        run_external_archive_boundary(),
        run_system_debug_fail_closed(),
    ]
    ablations=[ablate_question_generation(),ablate_result_sensitive_update()]
    report={
        "candidate":"runtime/improvement_core_legacy_candidate.py",
        "current_improvecore_fixed_stage_count":len(GOAL_DIRECTED_STAGES),
        "holdouts":holdouts,
        "holdout_pass_count":sum(1 for x in holdouts if x["pass"]),
        "ablation":ablations,
        "ablation_pass_count":sum(1 for x in ablations if x["pass"]),
        "control_benchmark_status":"PASS" if all(x["pass"] for x in holdouts+ablations) else "FAIL",
        "semantic_effectiveness_status":"PARTIAL_EVIDENCE_ONLY",
        "promotion_status":"OPEN_PENDING_UNLIKE_OPEN_ENDED_SEMANTIC_HOLDOUTS",
    }
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps(report,indent=2,sort_keys=True))
    return report


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default=str(ROOT/"runtime/state/improvecore-legacy-holdouts-131/report.json"))
    args=p.parse_args()
    run(Path(args.output))

if __name__=="__main__":
    main()
