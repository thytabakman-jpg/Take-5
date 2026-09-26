import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from entry_contract import MODE_OBSERVE_DECOUPLED
from hf002_recursive_continuation import HF002RecursiveContinuation
from ic028_operator import OBSERVER_FIRST_STAGES
from improvement_core_learning_memory import LearningMemory
from improvement_core_knowledge_ledger import KnowledgeLedger
from improvement_core_regime import run_improvement_core_regime


def _observer_handlers(phase):
    handlers={}

    def passthrough(stage):
        def fn(state):
            return {
                "state":{**state,"last_stage":stage},
                "material_delta":False,
            }
        return fn

    for stage in OBSERVER_FIRST_STAGES:
        handlers[stage]=passthrough(stage)

    def observe(state):
        return {
            "state":{
                **state,
                "observer_mode_verified":True,
                "mutation_allowed":False,
            },
            "material_delta":False,
        }

    def recover_goal(state):
        return {
            "state":{
                **state,
                "recovered_goal":"Find the smallest live execution-truth seam without duplicating already-validated PTI and without crossing the external host authority boundary.",
            },
            "material_delta":False,
        }

    def formalize(state):
        if phase==0:
            finding="PTI_ALREADY_CLOSES_CONFIGURED_TOOL_PATH"
            live="LOCATE_REMAINING_EXECUTION_TRUTH_SEAM"
        elif phase==1:
            finding="NON_CONFIGURED_EXECUTION_CLAIM_SEAM"
            live="SEPARATE_REPOSITORY_OWNED_FROM_EXTERNAL_HOST_RESIDUAL"
        else:
            finding="REPOSITORY_OWNED_ARTIFACT_ATTESTATION_GAP"
            live=None
        return {
            "state":{
                **state,
                "observer_finding":finding,
                "live_local_frontier":live,
            },
            "material_delta":False,
        }

    def generate_work(state):
        if phase==0:
            frontier=(
                "COMPARE_RECURRENT_FAILURE_TO_PTI",
                "INVENT_SECOND_CONFIGURED_RECEIPT_SYSTEM",
            )
        elif phase==1:
            frontier=(
                "TRACE_CAMPAIGN_AND_LEGACY_ARTIFACT_CLAIMS",
                "TRY_TO_FIX_UNIVERSAL_HOST_INTERCEPTION",
            )
        else:
            frontier=(
                "EXECUTION_CLAIM_INTEGRITY_GATE",
                "LEGACY_ONLY_PATCH",
                "UNIVERSAL_HOST_INTERCEPTION",
            )
        return {
            "state":{**state,"observer_work_frontier":frontier},
            "material_delta":False,
        }

    def select(state):
        if phase==0:
            selected="COMPARE_RECURRENT_FAILURE_TO_PTI"
        elif phase==1:
            selected="TRACE_CAMPAIGN_AND_LEGACY_ARTIFACT_CLAIMS"
        else:
            selected="EXECUTION_CLAIM_INTEGRITY_GATE"
        return {
            "state":{
                **state,
                "observer_selected":selected,
                "selection_is_observational":True,
            },
            "material_delta":False,
        }

    def execute(state):
        return {
            "state":{
                **state,
                "observer_execution":"SEMANTIC_ANALYSIS_ONLY",
                "mutation_performed":False,
            },
            "material_delta":False,
        }

    def admit(state):
        if phase==0:
            relation={
                "configured_path":"PTI_CLOSED_RELATIVE",
                "outside_configured_path":"UNRESOLVED",
            }
        elif phase==1:
            relation={
                "repository_owned":"CAMPAIGN_AND_LEGACY_EXECUTION_CLAIMS",
                "external_not_owned":"UNIVERSAL_HOST_INTERCEPTION",
            }
        else:
            relation={
                "recommended_candidate":"EXECUTION_CLAIM_INTEGRITY_GATE",
                "must_reuse":"PTI_NOT_DUPLICATE_IT",
                "hf2_ic_binding":"EXPERIMENTAL_CAMPAIGN_BINDING_ONLY",
            }
        return {
            "state":{
                **state,
                "observer_relation":relation,
            },
            "material_delta":phase<2,
            "delta":{
                "material_relation_delta":phase<2,
                "changed_representation":phase<2,
            },
        }

    def verify(state):
        ok=(
            state.get("observer_mode_verified") is True
            and state.get("mutation_performed") is False
            and state.get("selection_is_observational") is True
        )
        return {
            "state":{**state,"observer_verification":"PASS" if ok else "FAIL"},
            "material_delta":False,
        }

    def complete(state):
        terminal=state.get("observer_verification")=="PASS"
        return {
            "state":{
                **state,
                "live_continuation":False,
                "observer_ic_terminal":terminal,
            },
            "terminal":terminal,
            "material_delta":False,
        }

    handlers.update({
        "OBSERVE":observe,
        "RECOVER_GOAL":recover_goal,
        "FORMALIZE":formalize,
        "GENERATE_WORK":generate_work,
        "SELECT":select,
        "EXECUTE":execute,
        "ADMIT":admit,
        "VERIFY":verify,
        "COMPLETE":complete,
    })
    handlers["REENTER"]=lambda state: {"state":state,"terminal":True}
    return handlers


def _run_observer_ic(state,memory):
    phase=int(state.get("hf2_observer_round",0))
    out=run_improvement_core_regime(
        "Improvement Core observer mode on the whole system with HF2.",
        target="whole conversation plus current Take-5 system",
        job="recover live system frontier without mutation",
        basis="HF2_IC_OBSERVER_CAMPAIGN_20260926",
        state=state,
        handlers=_observer_handlers(phase),
        explicit_mode=MODE_OBSERVE_DECOUPLED,
        observer_risk=True,
        learning_memory=LearningMemory(),
        knowledge_ledger=KnowledgeLedger(),
    )
    assert out.status=="COMPLETE"
    return {
        "execution_truth":"SEMANTICALLY_APPLIED",
        "state":dict(out.result.state),
        "phase":phase,
        "ic_status":out.status,
        "ic_stages":out.receipt.stages,
    }


def _observer_admit_normalize(raw,state,memory):
    phase=int(raw["phase"])
    normalized=dict(raw["state"])
    normalized["hf2_observer_round"]=phase+1
    material=phase<2
    delta={
        "material_discovery_delta":material,
        "changed_representation":material,
        "route_equivalence":f"IC_OBSERVER_PHASE_{phase}",
    }
    return normalized,delta


def test_observer_improvementcore_runs_under_explicit_hf2_recurrence():
    initial={
        "hf2_observer_round":0,
        "pti_internal_configured_path":"CLOSED_RELATIVE",
        "legacy_campaign_execution_provenance":"OPEN",
        "universal_host_interception":"EXTERNAL_NOT_OWNED",
        "hf2_improvementcore_promoted":False,
    }

    hf2=HF002RecursiveContinuation(
        run_capability=_run_observer_ic,
        admit_normalize=_observer_admit_normalize,
        trc_verify=lambda before,after,delta:{"terminal":True},
        hf1_classify=lambda before,after,delta:{"disposition":"STABLE"},
        live_local=lambda state,memory:int(state.get("hf2_observer_round",0))<3,
        local_close=lambda state,memory:(
            int(state.get("hf2_observer_round",0))>=3
            and state.get("observer_finding")=="REPOSITORY_OWNED_ARTIFACT_ATTESTATION_GAP"
        ),
        max_rounds=6,
    )

    out=hf2.run(initial,{})
    assert out["status"]=="RELATIVE_CLOSE"
    assert len(out["trace"])==3
    assert [x["disposition"] for x in out["trace"]]==[
        "REAPPLY_C","REAPPLY_C","RELATIVE_CLOSE"
    ]

    final=out["state"]
    assert final["mutation_performed"] is False
    assert final["observer_verification"]=="PASS"
    assert final["observer_finding"]=="REPOSITORY_OWNED_ARTIFACT_ATTESTATION_GAP"
    assert final["observer_selected"]=="EXECUTION_CLAIM_INTEGRITY_GATE"
    assert final["observer_relation"]["must_reuse"]=="PTI_NOT_DUPLICATE_IT"
    assert final["observer_relation"]["hf2_ic_binding"]=="EXPERIMENTAL_CAMPAIGN_BINDING_ONLY"
