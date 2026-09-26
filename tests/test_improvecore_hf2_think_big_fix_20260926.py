import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from entry_contract import MODE_GOAL_DIRECTED
from execution_claim_integrity import (
    ExecutionClaimLevel,
    ExecutionClaimReceipt,
    assess_execution_claim,
)
from hf002_recursive_continuation import HF002RecursiveContinuation
from ic028_operator import GOAL_DIRECTED_STAGES
from icc128_legacy_portable import CONTINUE, Controller, take5_activation_closed
import icc128_legacy_reporting as reporting
from improvement_core_learning_memory import LearningMemory
from improvement_core_knowledge_ledger import KnowledgeLedger
from improvement_core_regime import run_improvement_core_regime


def _legacy_controller():
    def gq(state,memory):
        if state.get("step",0)>=1:
            return []
        return [{
            "question_id":"q1",
            "question":"Does the execution claim have a causal runtime witness?",
            "live_candidate_answers":["yes","no"],
            "enabling_discovery_or_distinction":"runtime/report provenance",
            "unresolved_structure":"execution claim integrity",
            "downstream_dependency":"Legacy closure",
        }]

    def gw(questions,state,memory):
        if not questions:
            return []
        return [{
            "work_id":"w1",
            "question_id":"q1",
            "probe_or_test":"cross Controller.run then consume exact result into report",
            "candidate_answers_discriminated":["causal","narrative-only"],
            "expected_search_space_effect":"close one provenance gap",
            "required_inputs_or_sources":[],
            "execution_or_semantic_route":"runtime",
        }]

    def select(questions,work,state,memory):
        return work[:1]

    def execute(selected,state,memory):
        return [{
            "work_id":row["work_id"],
            "finding":"controller runtime crossed",
        } for row in selected]

    def admit(results,state,memory):
        return {
            "results":results,
            "material_result_delta":bool(results),
        }

    def update(state,memory,delta):
        nxt=dict(state)
        mem=dict(memory)
        nxt["step"]=1
        nxt["terminal"]="COMPLETE"
        nxt["admitted_continuation"]=False
        nxt["unresolved"]=False
        mem["runtime_delta"]=delta
        return nxt,mem

    return Controller(gq,gw,select,execute,admit,update)


def _probe_execution_claim_gate():
    incomplete=ExecutionClaimReceipt(
        object_id="campaign-artifact",
        claim_id="probe-incomplete",
        claimed_level=ExecutionClaimLevel.EXECUTED,
        evidence={
            "identity":"id",
            "plan":"plan",
            "dispatch":"dispatch",
        },
    )
    fail_closed=assess_execution_claim(incomplete)
    assert fail_closed.status=="OPEN"
    assert fail_closed.missing_coordinates==("execution",)

    controller=_legacy_controller()
    initial={
        "step":0,
        "terminal":CONTINUE,
        "admitted_continuation":True,
        "unresolved":True,
    }
    run_result,report,execution_receipt=reporting.run_and_build_attested_learning_report(
        run_id="think-big-attested",
        controller_run=controller.run,
        initial_state=initial,
        initial_memory={},
        plan_evidence="HF2-ImprovementCore-selected execution-claim integrity gate",
    )
    assert run_result["status"]=="COMPLETE"
    assert len(run_result["traces"])==1
    assert report["execution_claim_status"]=="VERIFIED"
    assert report["execution_claim"]["claimed_level"]=="CONSUMED"

    bare=reporting.require_github_receipt(
        run_id="think-big-attested",
        report_sha256=reporting.report_sha256(report),
        repository="thytabakman-jpg/Take-5",
        path="artifacts/icc128-legacy-learning/think-big-attested.json",
        commit_sha="test-commit",
    )
    assert reporting.closure_allowed(bare) is False

    attested=reporting.require_attested_github_receipt(
        report=report,
        execution_receipt=execution_receipt,
        repository="thytabakman-jpg/Take-5",
        path="artifacts/icc128-legacy-learning/think-big-attested.json",
        commit_sha="test-commit",
    )
    assert reporting.closure_allowed(attested) is True
    assert attested.execution_receipt.level() is ExecutionClaimLevel.VERIFIED

    assert not take5_activation_closed({
        "repository":"thytabakman-jpg/Take-5",
        "path":"artifacts/icc128-legacy-learning/x.json",
        "commit_sha":"abc",
        "report_sha256":"def",
    })
    assert take5_activation_closed({
        "repository":"thytabakman-jpg/Take-5",
        "path":"artifacts/icc128-legacy-learning/x.json",
        "commit_sha":"abc",
        "report_sha256":"def",
        "execution_claim_level":"VERIFIED",
        "execution_claim_evidence_sha256":"ghi",
    })

    return {
        "incomplete_claim":"OPEN",
        "causal_controller_run":"COMPLETE",
        "attested_legacy_closure":"VERIFIED",
        "bare_report_closure":"REJECTED",
        "portable_activation_requires_execution_claim":True,
    }


def _action_handlers(phase):
    handlers={}

    def passthrough(stage):
        def fn(state):
            return {
                "state":{**state,"last_stage":stage},
                "material_delta":False,
            }
        return fn

    for stage in GOAL_DIRECTED_STAGES:
        handlers[stage]=passthrough(stage)

    def recover_goal(state):
        return {
            "state":{
                **state,
                "command":"Think big, fix this.",
                "recovered_goal":"Close the broadest repository-owned execution-truth seam without duplicating PTI or pretending to own universal host interception.",
            },
            "material_delta":False,
        }

    def curiosity_pd(state):
        return {
            "state":{
                **state,
                "problem_generator":"UNATTESTED_EXECUTION_CLAIMS_OUTSIDE_CONFIGURED_PTI",
            },
            "material_delta":False,
        }

    def formalize(state):
        return {
            "state":{
                **state,
                "action_phase":"IMPLEMENT" if phase==0 else "VERIFY_REENTRY",
                "protected_existing_invariant":"PTI",
                "external_boundary":"UNIVERSAL_HOST_INTERCEPTION:EXTERNAL_NOT_OWNED",
            },
            "material_delta":False,
        }

    def generate_work(state):
        candidates=(
            {
                "id":"EXECUTION_CLAIM_INTEGRITY_GATE",
                "coverage":3,
                "owned":True,
                "duplicates_pti":False,
            },
            {
                "id":"LEGACY_ONLY_RECEIPT_PATCH",
                "coverage":1,
                "owned":True,
                "duplicates_pti":False,
            },
            {
                "id":"DUPLICATE_CONFIGURED_PTI",
                "coverage":2,
                "owned":True,
                "duplicates_pti":True,
            },
            {
                "id":"UNIVERSAL_HOST_INTERCEPTION",
                "coverage":4,
                "owned":False,
                "duplicates_pti":False,
            },
        )
        return {
            "state":{**state,"action_candidates":candidates},
            "material_delta":False,
        }

    def select(state):
        admissible=[
            row for row in state["action_candidates"]
            if row["owned"] and not row["duplicates_pti"]
        ]
        selected=max(admissible,key=lambda row:(row["coverage"],row["id"]))
        return {
            "state":{
                **state,
                "selected_fix":selected["id"],
                "selection_basis":"MAX_REPOSITORY_OWNED_COVERAGE_WITH_PTI_PRESERVATION",
            },
            "material_delta":False,
        }

    def execute(state):
        probe=_probe_execution_claim_gate()
        return {
            "state":{
                **state,
                "implementation_probe":probe,
                "host_applied_selected_implementation":True,
                "implementation_surface":(
                    "runtime/execution_claim_integrity.py",
                    "runtime/icc128_legacy_reporting.py",
                    "runtime/icc128_legacy_portable.py",
                ),
            },
            "material_delta":phase==0,
            "delta":{
                "execution_truth_strengthened":phase==0,
                "resolved_open":phase==0,
            },
        }

    def admit(state):
        return {
            "state":{
                **state,
                "fix_admission":"ADMIT",
                "repository_owned_seam":"CLOSED_RELATIVE" if phase>=1 else "IMPLEMENTED_VERIFY_REQUIRED",
                "hf2_improvementcore_binding":"EXPERIMENTAL_CAMPAIGN_BINDING_VALIDATED",
            },
            "material_delta":phase==0,
            "delta":{
                "execution_truth_strengthened":phase==0,
                "resolved_open":phase==0,
            },
        }

    def reconcile(state):
        return {
            "state":{
                **state,
                "reconciliation":{
                    "pti_preserved":True,
                    "universal_host_boundary_preserved":True,
                    "bare_report_no_longer_closes_legacy":True,
                    "causal_execution_attestation_required":True,
                },
            },
            "material_delta":False,
        }

    def verify(state):
        probe=state["implementation_probe"]
        ok=(
            state.get("selected_fix")=="EXECUTION_CLAIM_INTEGRITY_GATE"
            and probe["incomplete_claim"]=="OPEN"
            and probe["causal_controller_run"]=="COMPLETE"
            and probe["attested_legacy_closure"]=="VERIFIED"
            and probe["bare_report_closure"]=="REJECTED"
            and state["reconciliation"]["pti_preserved"] is True
            and state["reconciliation"]["universal_host_boundary_preserved"] is True
        )
        return {
            "state":{**state,"action_verification":"PASS" if ok else "FAIL"},
            "material_delta":False,
        }

    def complete(state):
        terminal=state.get("action_verification")=="PASS"
        return {
            "state":{
                **state,
                "live_continuation":False,
                "action_ic_terminal":terminal,
            },
            "terminal":terminal,
            "material_delta":False,
        }

    handlers.update({
        "RECOVER_GOAL":recover_goal,
        "CURIOSITY_PD":curiosity_pd,
        "FORMALIZE":formalize,
        "GENERATE_WORK":generate_work,
        "SELECT":select,
        "EXECUTE":execute,
        "ADMIT":admit,
        "RECONCILE":reconcile,
        "VERIFY":verify,
        "COMPLETE":complete,
    })
    handlers["REENTER"]=lambda state: {"state":state,"terminal":True}
    return handlers


def _run_action_ic(state,memory):
    phase=int(state.get("hf2_action_round",0))
    out=run_improvement_core_regime(
        "Improvement Core. Think big, fix this.",
        target="whole current Take-5 system after observer HF2 campaign",
        job="implement and verify the broadest repository-owned repair",
        basis="HF2_IC_THINK_BIG_FIX_20260926",
        state=state,
        handlers=_action_handlers(phase),
        explicit_mode=MODE_GOAL_DIRECTED,
        observer_risk=False,
        learning_memory=LearningMemory(),
        knowledge_ledger=KnowledgeLedger(),
    )
    assert out.status=="COMPLETE"
    return {
        "execution_truth":"IMPLEMENTATION_EXECUTED",
        "state":dict(out.result.state),
        "phase":phase,
        "ic_status":out.status,
        "ic_stages":out.receipt.stages,
    }


def _action_admit_normalize(raw,state,memory):
    phase=int(raw["phase"])
    normalized=dict(raw["state"])
    normalized["hf2_action_round"]=phase+1
    material=phase==0
    delta={
        "material_result_delta":material,
        "resolved_open":material,
        "route_equivalence":f"IC_THINK_BIG_PHASE_{phase}",
    }
    return normalized,delta


def test_think_big_fix_runs_improvementcore_under_hf2_and_closes_owned_seam():
    initial={
        "hf2_action_round":0,
        "observer_candidate":"EXECUTION_CLAIM_INTEGRITY_GATE",
        "pti_internal_configured_path":"CLOSED_RELATIVE",
        "repository_owned_artifact_attestation_gap":"OPEN",
        "universal_host_interception":"EXTERNAL_NOT_OWNED",
    }

    hf2=HF002RecursiveContinuation(
        run_capability=_run_action_ic,
        admit_normalize=_action_admit_normalize,
        trc_verify=lambda before,after,delta:{"terminal":True},
        hf1_classify=lambda before,after,delta:{"disposition":"STABLE"},
        live_local=lambda state,memory:int(state.get("hf2_action_round",0))<2,
        local_close=lambda state,memory:(
            int(state.get("hf2_action_round",0))>=2
            and state.get("repository_owned_seam")=="CLOSED_RELATIVE"
            and state.get("action_verification")=="PASS"
        ),
        max_rounds=5,
    )

    out=hf2.run(initial,{})
    assert out["status"]=="RELATIVE_CLOSE"
    assert len(out["trace"])==2
    assert [row["disposition"] for row in out["trace"]]==[
        "REAPPLY_C","RELATIVE_CLOSE"
    ]

    final=out["state"]
    assert final["command"]=="Think big, fix this."
    assert final["selected_fix"]=="EXECUTION_CLAIM_INTEGRITY_GATE"
    assert final["repository_owned_seam"]=="CLOSED_RELATIVE"
    assert final["action_verification"]=="PASS"
    assert final["reconciliation"]["pti_preserved"] is True
    assert final["reconciliation"]["universal_host_boundary_preserved"] is True
    assert final["hf2_improvementcore_binding"]=="EXPERIMENTAL_CAMPAIGN_BINDING_VALIDATED"
