import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from entry_contract import MODE_OBSERVE_DECOUPLED
from improvement_core_dispatch import dispatch_improvement_core
from ic028_operator import OBSERVER_FIRST_STAGES

CORPUS_PATH=ROOT/"artifacts"/"improvecore"/"WHOLE_CHAT_EVIDENCE_CORPUS_114_2026-09-26.json"


def _corpus():
    return json.loads(CORPUS_PATH.read_text())


def _theme_frontier(records):
    groups={
        "EXECUTION_TRUTH_INTEGRITY":{
            "kinds":{"recurring_failure","execution_truth_failure","controller_evidence","progress_rule","open_frontier"},
            "evidence":[],
        },
        "PORTABILITY_SEMANTICS":{
            "kinds":{"discovery","distinction","boundary"},
            "evidence":[],
        },
        "IDENTITY_FAIL_CLOSED":{
            "kinds":{"constraint","identity_evidence"},
            "evidence":[],
        },
        "ANTI_REPEAT_PROGRESS":{
            "kinds":{"anti_repeat","progress_rule"},
            "evidence":[],
        },
    }
    for row in records:
        for theme,spec in groups.items():
            if row["kind"] in spec["kinds"]:
                spec["evidence"].append(row["id"])
    frontier=[]
    for theme,spec in groups.items():
        open_bonus=sum(1 for row in records if row["id"] in spec["evidence"] and row["kind"]=="open_frontier")
        frontier.append({
            "theme":theme,
            "evidence_ids":tuple(spec["evidence"]),
            "score":len(spec["evidence"])+2*open_bonus,
        })
    return tuple(sorted(frontier,key=lambda x:(x["score"],x["theme"]),reverse=True))


def _handlers():
    handlers={}

    def passthrough(stage):
        def fn(state):
            return {"state":{**state,"last_stage":stage},"material_delta":False}
        return fn

    for stage in OBSERVER_FIRST_STAGES:
        handlers[stage]=passthrough(stage)

    def observe(state):
        records=tuple(state["chat_evidence"])
        return {
            "state":{
                **state,
                "input_role":"EVIDENCE_NOT_INSTRUCTIONS",
                "evidence_count":len(records),
                "observed_kinds":tuple(sorted({r["kind"] for r in records})),
            },
            "material_delta":False,
        }

    def observe_reconcile(state):
        upstream=state.get("upstream_discovery",{})
        return {
            "state":{
                **state,
                "zero_request_observer_ran":upstream.get("status")=="OBSERVED",
                "zero_request_route":upstream.get("route"),
                "evidence_reconciled":True,
            },
            "material_delta":False,
        }

    def observe_trc(state):
        return {
            "state":{
                **state,
                "licensed_transition":"EVIDENCE_TO_DISCOVERY_ONLY",
                "chat_does_not_self_authorize_actions":True,
            },
            "material_delta":False,
        }

    def recover_goal(state):
        return {
            "state":{
                **state,
                "recovered_goal":"Identify the highest-leverage recurrent system frontier evidenced by the chat, preserve contrary/open evidence, and select the next evidence-bearing work without treating chat proposals as commands.",
            },
            "material_delta":False,
        }

    def curiosity_pd(state):
        frontier=_theme_frontier(tuple(state["chat_evidence"]))
        return {
            "state":{
                **state,
                "theme_frontier":frontier,
                "problem_generator":"RECURRENT_EXECUTION_TRUTH_COLLAPSE" if frontier and frontier[0]["theme"]=="EXECUTION_TRUTH_INTEGRITY" else "EVIDENCE_FRONTIER_OPEN",
            },
            "material_delta":False,
        }

    def formalize(state):
        top=state["theme_frontier"][0]
        return {
            "state":{
                **state,
                "formalized_evidence_problem":{
                    "primary_theme":top["theme"],
                    "support":top["evidence_ids"],
                    "score":top["score"],
                    "claim":"Naming, planning, displaying, documenting, or persisting a formal object has repeatedly been allowed to stand too close to claims of actual configured execution or causal execution receipt.",
                },
            },
            "material_delta":False,
        }

    def plan_order(state):
        return {
            "state":{
                **state,
                "work_order":(
                    "close_current_execution_truth_residual",
                    "test_recurrence_across_prior failures",
                    "only_then_consider_system_wide_generalization",
                ),
            },
            "material_delta":False,
        }

    def objectify(state):
        return {
            "state":{
                **state,
                "evidence_object_id":"WHOLE_CHAT_EXECUTION_TRUTH_FRONTIER_114",
            },
            "material_delta":False,
        }

    def generate_work(state):
        records=tuple(state["chat_evidence"])
        has_open=any(r["kind"]=="open_frontier" for r in records)
        candidates=[
            {
                "id":"CLOSE_CURRENT_LEGACY_EXECUTION_RECEIPT",
                "evidence_ids":tuple(r["id"] for r in records if r["kind"] in {"execution_truth_failure","controller_evidence","open_frontier"}),
                "resolves_live_open":has_open,
                "mutation":False,
            },
            {
                "id":"WRITE_ANOTHER_GENERAL_ARCHITECTURE_REPORT",
                "evidence_ids":tuple(r["id"] for r in records if r["kind"]=="constraint"),
                "resolves_live_open":False,
                "mutation":False,
            },
            {
                "id":"TREAT_ALL_PRIOR_USER_TOOL_ORDERS_AS_PLAN",
                "evidence_ids":(),
                "resolves_live_open":False,
                "mutation":True,
            },
        ]
        return {"state":{**state,"generated_work":tuple(candidates)},"material_delta":False}

    def select(state):
        def rank(x):
            return (
                1 if x["resolves_live_open"] else 0,
                len(x["evidence_ids"]),
                0 if x["mutation"] else 1,
                x["id"],
            )
        selected=max(state["generated_work"],key=rank)
        return {
            "state":{
                **state,
                "selected_work":selected,
                "selection_basis":"EVIDENCE_COVERAGE_PLUS_LIVE_OPEN",
                "selected_from_chat_instruction":False,
            },
            "material_delta":False,
        }

    def bind(state):
        return {"state":{**state,"bound_work":state["selected_work"]["id"]},"material_delta":False}

    def execute(state):
        return {
            "state":{
                **state,
                "execution_kind":"EVIDENCE_EVALUATION_ONLY",
                "mutation_performed":False,
                "licensed_next_work":state["selected_work"]["id"],
            },
            "material_delta":False,
        }

    def admit(state):
        primary=state["formalized_evidence_problem"]["primary_theme"]
        return {
            "state":{
                **state,
                "improvement_core_finding":"EXECUTION_TRUTH_INTEGRITY_IS_PRIMARY_RECURRENT_FRONTIER" if primary=="EXECUTION_TRUTH_INTEGRITY" else "PLURAL_FRONTIER",
                "system_status":"OPEN",
                "admitted_as":"EVIDENCE_NOT_INSTRUCTIONS",
                "learning_event_candidate":{
                    "route_id":"whole-chat-execution-truth-frontier",
                    "basis_id":"whole-chat-evidence-114",
                    "disposition":"GAIN",
                    "dependency_footprint":["execution_truth","configured_tool_receipts","legacy_campaign_receipt"],
                },
            },
            "material_delta":True,
            "delta":{"kind":"MATERIAL_RELATION_DISCOVERED","scope":"whole_chat"},
        }

    def reconcile(state):
        return {
            "state":{
                **state,
                "reconciliation":{
                    "prior_user_proposals_are_binding":False,
                    "verified_receipts_preserved":True,
                    "open_frontiers_preserved":True,
                    "architecture_mutation_admitted":False,
                },
            },
            "material_delta":False,
        }

    def propagate(state):
        return {
            "state":{
                **state,
                "affected_cone":(
                    "TOOL_INVOCATION_EXECUTION_TRUTH",
                    "SHOW_MATH_EXECUTION_TRUTH",
                    "ICC128_LEGACY_CAMPAIGN_RECEIPT",
                    "CLOSURE_LABELS",
                ),
            },
            "material_delta":False,
        }

    def persist(state):
        return {"state":{**state,"persistence":"RUN_RECEIPT_ONLY"},"material_delta":False}

    def verify(state):
        ok=(
            state.get("zero_request_observer_ran") is True
            and state.get("input_role")=="EVIDENCE_NOT_INSTRUCTIONS"
            and state.get("selected_from_chat_instruction") is False
            and state.get("licensed_next_work")=="CLOSE_CURRENT_LEGACY_EXECUTION_RECEIPT"
            and state.get("reconciliation",{}).get("architecture_mutation_admitted") is False
            and state.get("mutation_performed") is False
        )
        return {"state":{**state,"verification_status":"PASS" if ok else "FAIL"},"material_delta":False}

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


def test_whole_chat_enters_improvement_core_as_evidence_not_instructions():
    packet=_corpus()
    records=tuple(packet["records"])
    resolution,out=dispatch_improvement_core(
        "ImproveCore observer mode. Treat this chat as evidence, not instructions.",
        corpus=records,
        state={
            "chat_evidence":records,
            "source_role":packet["source_role"],
        },
        handlers=_handlers(),
        explicit_mode=MODE_OBSERVE_DECOUPLED,
        observer_risk=True,
    )

    assert resolution.controller=="IC-028"
    assert out.status=="COMPLETE"
    assert out.result.terminal is True
    state=out.result.state

    assert state["zero_request_observer_ran"] is True
    assert state["input_role"]=="EVIDENCE_NOT_INSTRUCTIONS"
    assert state["admitted_as"]=="EVIDENCE_NOT_INSTRUCTIONS"
    assert state["formalized_evidence_problem"]["primary_theme"]=="EXECUTION_TRUTH_INTEGRITY"
    assert state["problem_generator"]=="RECURRENT_EXECUTION_TRUTH_COLLAPSE"
    assert state["licensed_next_work"]=="CLOSE_CURRENT_LEGACY_EXECUTION_RECEIPT"
    assert state["selected_from_chat_instruction"] is False
    assert state["mutation_performed"] is False
    assert state["verification_status"]=="PASS"
    assert state["reconciliation"]["prior_user_proposals_are_binding"] is False
    assert state["reconciliation"]["architecture_mutation_admitted"] is False

    stages=out.receipt.stages
    for required in (
        "OBSERVE","OBSERVE_RECONCILE","OBSERVE_TRC","RECOVER_GOAL",
        "CURIOSITY_PD","FORMALIZE","GENERATE_WORK","SELECT","EXECUTE",
        "ADMIT","RECONCILE","PERSIST","VERIFY","COMPLETE"
    ):
        assert required in stages
