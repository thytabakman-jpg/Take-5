import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from entry_contract import MODE_OBSERVE_DECOUPLED
from global_tool_execution import build_tool_execution_plan
from improvement_core_dispatch import dispatch_improvement_core
from ic028_operator import OBSERVER_FIRST_STAGES
from semantic_resolution_pipeline import plan_black_box_resolution
from tool_run_registry import CONFIGURED_RUNS


EVIDENCE_PATH=ROOT/"artifacts"/"improvecore"/"MT_EVIDENCE_PACKET_113_2026-09-26.json"


def _load_evidence():
    return json.loads(EVIDENCE_PATH.read_text())


def _handlers():
    handlers={}

    def default(stage):
        def fn(state):
            return {
                "state":{**state,"last_stage":stage},
                "material_delta":False,
                "supervisory_relevant":False,
            }
        return fn

    for stage in OBSERVER_FIRST_STAGES:
        handlers[stage]=default(stage)

    def observe(state):
        packet=state["mt_evidence"]
        return {
            "state":{
                **state,
                "observed_verified_ids":tuple(x["id"] for x in packet["verified_evidence"]),
                "observed_unresolved_ids":tuple(x["id"] for x in packet["unresolved_evidence"]),
                "input_role":packet["source_role"],
            },
            "material_delta":False,
        }

    def observe_reconcile(state):
        unresolved=tuple(state.get("observed_unresolved_ids",()))
        return {
            "state":{
                **state,
                "evidence_reconciled":True,
                "unresolved_count":len(unresolved),
                "verified_positive_claims_preserved":True,
            },
            "material_delta":False,
        }

    def observe_trc(state):
        return {
            "state":{
                **state,
                "licensed_transition":"EVIDENCE_TO_CONTROLLER_INFERENCE",
                "input_not_authoritative_plan":True,
            },
            "material_delta":False,
        }

    def recover_goal(state):
        return {
            "state":{
                **state,
                "governing_goal":"Determine the evidence-supported campaign status and choose any next work without treating the MT result as a draft or mandated plan.",
            },
            "material_delta":False,
        }

    def curiosity_pd(state):
        unresolved=state["mt_evidence"]["unresolved_evidence"]
        residuals=tuple(x["required_receipt"] for x in unresolved)
        return {
            "state":{
                **state,
                "problem_residuals":residuals,
                "problem_generator":"EXECUTION_TRUTH_RECEIPT_GAP" if residuals else None,
            },
            "material_delta":False,
        }

    def formalize(state):
        verified=tuple(x["id"] for x in state["mt_evidence"]["verified_evidence"])
        unresolved=tuple(x["id"] for x in state["mt_evidence"]["unresolved_evidence"])
        supported_status="VERIFY_REQUIRED" if unresolved else "COMPLETE_RELATIVE"
        return {
            "state":{
                **state,
                "evidence_classification":{
                    "verified":verified,
                    "unresolved":unresolved,
                    "supported_campaign_status":supported_status,
                },
            },
            "material_delta":False,
        }

    def plan_order(state):
        return {
            "state":{
                **state,
                "controller_work_order":(
                    "preserve_verified_claims",
                    "resolve_execution_truth_gap",
                    "retest_campaign_closure",
                ),
            },
            "material_delta":False,
        }

    def objectify(state):
        return {
            "state":{
                **state,
                "evidence_object":{
                    "target":"prior_campaign_closure",
                    "gap":"CAMPAIGN_SPECIFIC_ICC128_LEGACY_CONTROLLER_EXECUTION_RECEIPT_REQUIRED",
                    "input_role":"EVIDENCE",
                },
            },
            "material_delta":False,
        }

    def generate_work(state):
        unresolved={x["id"] for x in state["mt_evidence"]["unresolved_evidence"]}
        frontier=(
            {
                "id":"OBTAIN_CAMPAIGN_SPECIFIC_LEGACY_EXECUTION_RECEIPT",
                "covers":("U1","U2","U3"),
                "mutation":False,
                "purpose":"close the causal runtime->report->commit receipt chain",
            },
            {
                "id":"DOWNGRADE_LABEL_ONLY",
                "covers":(),
                "mutation":False,
                "purpose":"correct prose without resolving the execution gap",
            },
        )
        return {
            "state":{
                **state,
                "work_frontier":frontier,
                "live_unresolved":tuple(sorted(unresolved)),
            },
            "material_delta":False,
        }

    def select(state):
        live=set(state.get("live_unresolved",()))
        frontier=state["work_frontier"]
        ranked=sorted(
            frontier,
            key=lambda x:(len(live & set(x["covers"])),x["id"]),
            reverse=True,
        )
        selected=ranked[0]
        return {
            "state":{
                **state,
                "selected_evidence_work":selected,
                "selected_from_evidence_not_input_plan":True,
            },
            "material_delta":False,
        }

    def bind(state):
        return {
            "state":{
                **state,
                "bound_evidence_work":state["selected_evidence_work"]["id"],
            },
            "material_delta":False,
        }

    def execute(state):
        selected=state["selected_evidence_work"]
        return {
            "state":{
                **state,
                "execution_kind":"ANALYTICAL_EVIDENCE_EVALUATION",
                "licensed_next_work":selected["id"],
                "mutation_performed":False,
            },
            "material_delta":False,
        }

    def admit(state):
        unresolved=tuple(state["evidence_classification"]["unresolved"])
        return {
            "state":{
                **state,
                "improvement_core_decision":"REOPEN_PRIOR_CAMPAIGN_CLOSURE" if unresolved else "PRESERVE_COMPLETE_RELATIVE",
                "prior_campaign_supported_status":"VERIFY_REQUIRED" if unresolved else "COMPLETE_RELATIVE",
                "residual":"CAMPAIGN_SPECIFIC_ICC128_LEGACY_CONTROLLER_EXECUTION_RECEIPT_REQUIRED" if unresolved else None,
                "mt_input_admitted_as":"EVIDENCE_NOT_DRAFT",
            },
            "material_delta":True,
            "delta":{"kind":"EXECUTION_TRUTH_STRENGTHENED","scope":"prior_campaign_closure"},
        }

    def reconcile(state):
        return {
            "state":{
                **state,
                "reconciliation":{
                    "verified_positive_claims_preserved":True,
                    "unsupported_completion_inference_removed":True,
                    "new_architecture_admitted":False,
                },
            },
            "material_delta":False,
        }

    def propagate(state):
        return {
            "state":{
                **state,
                "affected_cone":("ICC128_LEGACY_CAMPAIGN_EXECUTION_TRUTH","CAMPAIGN_CLOSURE_STATUS"),
            },
            "material_delta":False,
        }

    def persist(state):
        return {
            "state":{
                **state,
                "persistence_disposition":"PERSIST_EVIDENCE_RUN_RECEIPT",
            },
            "material_delta":False,
        }

    def verify(state):
        ok=(
            state.get("input_role")=="EVIDENCE_NOT_DRAFT"
            and state.get("selected_from_evidence_not_input_plan") is True
            and state.get("prior_campaign_supported_status")=="VERIFY_REQUIRED"
            and state.get("mutation_performed") is False
            and state.get("reconciliation",{}).get("verified_positive_claims_preserved") is True
        )
        return {
            "state":{
                **state,
                "verification_status":"PASS" if ok else "FAIL",
            },
            "material_delta":False,
        }

    def complete(state):
        terminal=state.get("verification_status")=="PASS"
        return {
            "state":{
                **state,
                "improvement_core_run_status":"COMPLETE" if terminal else "OPEN",
                "live_continuation":False,
            },
            "terminal":terminal,
            "material_delta":False,
        }

    handlers.update({
        "OBSERVE":observe,
        "OBSERVE_RECONCILE":observe_reconcile,
        "OBSERVE_TRC":observe_trc,
        "RECOVER_GOAL":recover_goal,
        "CURIOSITY_PD":curiosity_pd,
        "FORMALIZE":formalize,
        "PLAN_ORDER":plan_order,
        "OBJECTIFY":objectify,
        "GENERATE_WORK":generate_work,
        "SELECT":select,
        "BIND":bind,
        "EXECUTE":execute,
        "ADMIT":admit,
        "RECONCILE":reconcile,
        "PROPAGATE_AFFECTED_CONE":propagate,
        "PERSIST":persist,
        "VERIFY":verify,
        "COMPLETE":complete,
    })
    handlers["REENTER"]=lambda state: {"state":state,"terminal":True}
    return handlers


def test_full_mt_evidence_plan_and_black_box_spine_are_current():
    plan=build_tool_execution_plan(CONFIGURED_RUNS["MT"])
    assert plan.complete
    assert plan.wrapper_required is True
    assert plan.mode=="OBSERVER"
    assert len(plan.cells)==36
    assert len(plan.questions)==792
    assert len(plan.cognitive)==144

    bb=plan_black_box_resolution("LEGACY_CAMPAIGN_EXECUTION_TRUTH")
    assert [x.tool_id for x in bb.stages]==[
        "PD","PDAudit","MTA","MT","PDAudit","C47"
    ]


def test_current_improvement_core_consumes_mt_as_evidence_not_draft():
    evidence=_load_evidence()
    resolution,out=dispatch_improvement_core(
        "ImproveCore observer mode. Use the MT results as evidence, not as a draft.",
        target="prior full-system Show-Me-the-Math campaign closure",
        job="evaluate MT evidence and determine licensed next work",
        basis="Take-5 main 6a1594ae8c92e8bb6ef173f51e68f1e30dd48154",
        state={"mt_evidence":evidence},
        handlers=_handlers(),
        explicit_mode=MODE_OBSERVE_DECOUPLED,
        observer_risk=True,
    )

    assert resolution.controller=="IC-028"
    assert out.status=="COMPLETE"
    assert out.receipt.initial_mode==MODE_OBSERVE_DECOUPLED
    assert out.result.terminal is True

    state=out.result.state
    assert state["mt_input_admitted_as"]=="EVIDENCE_NOT_DRAFT"
    assert state["selected_from_evidence_not_input_plan"] is True
    assert state["improvement_core_decision"]=="REOPEN_PRIOR_CAMPAIGN_CLOSURE"
    assert state["prior_campaign_supported_status"]=="VERIFY_REQUIRED"
    assert state["residual"]=="CAMPAIGN_SPECIFIC_ICC128_LEGACY_CONTROLLER_EXECUTION_RECEIPT_REQUIRED"
    assert state["licensed_next_work"]=="OBTAIN_CAMPAIGN_SPECIFIC_LEGACY_EXECUTION_RECEIPT"
    assert state["mutation_performed"] is False
    assert state["verification_status"]=="PASS"
    assert state["reconciliation"]["verified_positive_claims_preserved"] is True
    assert state["reconciliation"]["new_architecture_admitted"] is False

    stages=out.receipt.stages
    for required in (
        "OBSERVE","OBSERVE_RECONCILE","OBSERVE_TRC","RECOVER_GOAL",
        "CURIOSITY_PD","FORMALIZE","GENERATE_WORK","SELECT","BIND",
        "EXECUTE","ADMIT","RECONCILE","PERSIST","VERIFY","COMPLETE"
    ):
        assert required in stages
