import sys
sys.path.insert(0,"runtime")

from improvement_core_knowledge_ledger import KnowledgeLedger
from improvement_core_restored_dispatch import (
    RestoredSemanticProvider,
    dispatch_improvement_core_restored,
)


def provider(calls=None):
    calls=calls if calls is not None else []

    def generate_questions(state,memory):
        calls.append("G_Q")
        if state.get("terminal") in {"COMPLETE","OPEN","BLOCKED","CONFLICT"}:
            return []
        return [{"question_id":"q","issue":"solve","obligations":["solve"]}]

    def generate_work(questions,state,memory):
        calls.append("G_W")
        return [{"id":"cheap","jobs":["solve"],"burden":1}]

    def execute_work(selected,state,memory):
        calls.append("E")
        return [{"status":"EXECUTED","execution_truth":"SEMANTIC_PROVIDER_EXECUTED"}]

    def admit_results(results,state,memory):
        calls.append("A")
        return {"material_result_delta":True}

    def update_state(state,memory,delta):
        calls.append("U")
        nxt=dict(state)
        nxt["terminal"]="COMPLETE"
        nxt["admitted_continuation"]=False
        return nxt,dict(memory)

    def verify_return(state,memory,context):
        calls.append("R")
        status=str(context.get("candidate_status","OPEN"))
        return {
            "disposition":"RETURN",
            "terminal":status,
            "goal_closed":status=="COMPLETE",
            "owned_work_remaining":False,
            "consequence_closed":True,
            "blocker":context.get("candidate_blocker"),
            "evidence":["test:restored-dispatch-whole-job"],
        }

    return RestoredSemanticProvider(
        generate_questions=generate_questions,
        generate_work=generate_work,
        execute_work=execute_work,
        admit_results=admit_results,
        update_state=update_state,
        verify_return=verify_return,
        provider_id="test-provider",
    )


def initial_state():
    return {
        "terminal":"CONTINUE",
        "admitted_continuation":True,
        "required_jobs":["solve"],
        "task_and_job_well_typed":True,
        "one_validated_capability_clearly_fits":True,
        "consequence_bounded":True,
        "no_material_rival_exposed":True,
    }


def test_missing_semantic_provider_fails_open_without_fixed_stage_fallback():
    out=dispatch_improvement_core_restored(
        "ImproveCore solve this",
        target="x",job="solve",basis="b",
        state=initial_state(),
        semantic_provider=None,
    )
    assert out.status=="OPEN"
    assert out.blocker=="RESTORED_SEMANTIC_PROVIDER_REQUIRED"
    assert out.result is None
    assert out.resolution.provider_id is None
    assert out.resolution.entrypoint.endswith("dispatch_improvement_core_restored")


def test_bound_semantic_provider_executes_restored_controller():
    calls=[]
    out=dispatch_improvement_core_restored(
        "ImproveCore solve this",
        target="x",job="solve",basis="b",
        state=initial_state(),
        semantic_provider=provider(calls),
        knowledge_ledger=KnowledgeLedger(),
    )
    assert out.status=="COMPLETE"
    assert out.blocker is None
    assert out.result is not None
    assert out.result.hf2_status=="RELATIVE_CLOSE"
    assert out.resolution.provider_id=="test-provider"
    assert calls==["G_Q","G_W","E","A","U","R"]


def test_partial_entry_coordinates_fail_open():
    out=dispatch_improvement_core_restored(
        "ImproveCore solve this",
        target="x",job=None,basis="b",
        state=initial_state(),
        semantic_provider=provider(),
    )
    assert out.status=="OPEN"
    assert out.blocker=="RESTORED_PARTIAL_ENTRY_COORDINATES"


def test_zero_request_without_corpus_fails_open():
    out=dispatch_improvement_core_restored(
        "ImproveCore",
        state={},
        semantic_provider=provider(),
    )
    assert out.status=="OPEN"
    assert out.blocker=="RESTORED_CORPUS_REQUIRED_FOR_UPSTREAM_DISCOVERY"


def test_observer_mode_stays_fail_closed_when_provider_has_no_observer_binding():
    out=dispatch_improvement_core_restored(
        "ImproveCore in observer mode",
        target="x",job="inspect",basis="b",
        state=initial_state(),
        semantic_provider=provider(),
        knowledge_ledger=KnowledgeLedger(),
    )
    assert out.status=="BLOCKED"
    assert out.blocker=="OBSERVER_PREPARE_REQUIRED"



def test_incomplete_semantic_provider_without_return_verifier_fails_open():
    p=provider()
    p_without_return=type("IncompleteProvider",(),{
        "generate_questions":p.generate_questions,
        "generate_work":p.generate_work,
        "execute_work":p.execute_work,
        "admit_results":p.admit_results,
        "update_state":p.update_state,
        "provider_id":"incomplete-provider",
    })()
    out=dispatch_improvement_core_restored(
        "ImproveCore solve this",
        target="x",job="solve",basis="b",
        state=initial_state(),
        semantic_provider=p_without_return,
    )
    assert out.status=="OPEN"
    assert "verify_return" in out.blocker
