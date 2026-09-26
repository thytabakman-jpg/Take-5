import sys
sys.path.insert(0,"runtime")

from improvement_core_knowledge_ledger import KnowledgeLedger
from improvement_core_legacy_restored import run_improvement_core_legacy_restored


def _q(state,memory):
    if state.get("terminal") in {"COMPLETE","OPEN","BLOCKED","CONFLICT"}:
        return []
    return [{"question_id":"q","issue":"solve","obligations":["solve"]}]


def _w(q,state,memory):
    return list(state["work_items"])


def _state(**extra):
    out={
        "terminal":"CONTINUE",
        "admitted_continuation":True,
        "required_jobs":["solve"],
        "task_and_job_well_typed":True,
        "one_validated_capability_clearly_fits":True,
        "consequence_bounded":True,
        "no_material_rival_exposed":True,
        "work_items":[{"id":"cheap","jobs":["solve"],"burden":1}],
    }
    out.update(extra)
    return out


def _execute(selected,state,memory):
    return [{"status":"EXECUTED","execution_truth":"IMPLEMENTATION_EXECUTED"}]


def _admit(results,state,memory):
    return {"material_result_delta":True}


def _complete(state,memory,delta):
    s=dict(state)
    s["terminal"]="COMPLETE"
    s["admitted_continuation"]=False
    return s,dict(memory)


def test_wrapper_binds_entry_captures_knowledge_and_closes_hf2():
    ledger=KnowledgeLedger()
    out=run_improvement_core_legacy_restored(
        "ImproveCore solve this",
        target="x",job="solve",basis="b",
        state=_state(),memory={},
        generate_questions=_q,generate_work=_w,
        execute_work=_execute,admit_results=_admit,update_state=_complete,
        knowledge_ledger=ledger,
        hf2_enabled=True,
    )
    assert out.status=="COMPLETE"
    assert out.hf2_status=="RELATIVE_CLOSE"
    assert "ENTRY_BOUND:IC-028" in out.entry_receipt
    assert len(out.knowledge_summary)>=1
    assert out.state["terminal"]=="COMPLETE"


def test_observer_mode_fails_closed_without_observer_prepare():
    out=run_improvement_core_legacy_restored(
        "ImproveCore in observer mode",
        target="x",job="inspect",basis="b",
        state=_state(),memory={},
        generate_questions=_q,generate_work=_w,
        execute_work=_execute,admit_results=_admit,update_state=_complete,
        knowledge_ledger=KnowledgeLedger(),
    )
    assert out.status=="BLOCKED"
    assert out.blocker=="OBSERVER_PREPARE_REQUIRED"


def test_external_gap_survives_candidate_completion():
    out=run_improvement_core_legacy_restored(
        "ImproveCore solve this",
        target="x",job="solve",basis="b",
        state=_state(external_dependency=True),memory={},
        generate_questions=_q,generate_work=_w,
        execute_work=_execute,admit_results=_admit,update_state=_complete,
        external_adapters={},
        allow_external_gap=True,
        knowledge_ledger=KnowledgeLedger(),
    )
    assert out.status=="OPEN"
    assert out.blocker=="EXTERNAL_ACQUISITION_GAP"


def test_outer_hf2_reapplies_same_capability_when_local_frontier_live():
    calls={"updates":0}
    def update(state,memory,delta):
        calls["updates"]+=1
        s=dict(state)
        s["terminal"]="COMPLETE"
        s["admitted_continuation"]=False
        s["hf2_live_local"]=calls["updates"]==1
        return s,dict(memory)

    out=run_improvement_core_legacy_restored(
        "ImproveCore solve this",
        target="x",job="solve",basis="b",
        state=_state(),memory={},
        generate_questions=_q,generate_work=_w,
        execute_work=_execute,admit_results=_admit,update_state=update,
        knowledge_ledger=KnowledgeLedger(),
        hf2_enabled=True,
        hf2_max_rounds=4,
    )
    assert out.status=="COMPLETE"
    assert out.hf2_status=="RELATIVE_CLOSE"
    assert len(out.hf2_trace)==2
    assert out.hf2_trace[0]["disposition"]=="REAPPLY_C"


def test_wrapper_preserves_missing_configured_tool_adapter_as_open():
    state=_state(work_items=[
        {"id":"formal","jobs":["solve"],"burden":1,"tool_id":"RootCause"},
    ])
    out=run_improvement_core_legacy_restored(
        "ImproveCore solve this",
        target="x",job="solve",basis="b",
        state=state,memory={},
        generate_questions=_q,generate_work=_w,
        execute_work=None,admit_results=lambda r,s,m:{},
        update_state=lambda s,m,d:(dict(s),dict(m)),
        configured_tool_adapters={},
        knowledge_ledger=KnowledgeLedger(),
    )
    assert out.status=="OPEN"
    assert out.state["terminal"]=="OPEN"
