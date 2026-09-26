import sys
sys.path.insert(0,"runtime")

from improvement_core_legacy_candidate import run_legacy_candidate


def _questions(state,memory):
    n=int(state.get("iteration",0))
    if state.get("terminal") in {"COMPLETE","OPEN","BLOCKED","CONFLICT"}:
        return []
    return [{"question_id":f"q{n}","issue":"next","obligations":["solve"]}]


def _work(questions,state,memory):
    return list(state["work_items"])


def _admit(results,state,memory):
    delta={"material_result_delta":True}
    if results:
        delta["result_status"]=results[0].get("status","EXECUTED")
    return delta


def _update_complete_after_one(state,memory,delta):
    nxt=dict(state)
    nxt["iteration"]=int(nxt.get("iteration",0))+1
    nxt["terminal"]="COMPLETE"
    nxt["admitted_continuation"]=False
    return nxt,dict(memory)


def test_cheap_direct_executes_one_minimal_package():
    calls=[]
    state={
        "terminal":"CONTINUE",
        "admitted_continuation":True,
        "required_jobs":["solve"],
        "task_and_job_well_typed":True,
        "one_validated_capability_clearly_fits":True,
        "consequence_bounded":True,
        "no_material_rival_exposed":True,
        "work_items":[
            {"id":"cheap","jobs":["solve"],"burden":1,"info_gain":3},
            {"id":"heavy","jobs":["solve"],"burden":9,"info_gain":3},
        ],
    }
    def execute(selected,state,memory):
        calls.append([x["id"] for x in selected])
        return [{"status":"EXECUTED","execution_truth":"IMPLEMENTATION_EXECUTED"}]

    out=run_legacy_candidate(
        state,{},
        generate_questions=_questions,
        generate_work=_work,
        execute_work=execute,
        admit_results=_admit,
        update_state=_update_complete_after_one,
    )
    assert out.status=="COMPLETE"
    assert calls==[["cheap"]]
    assert out.selection_traces[0]["activation_mode"]=="CHEAP_DIRECT"


def test_deep_route_preserves_nondominated_plurality():
    calls=[]
    state={
        "terminal":"CONTINUE",
        "admitted_continuation":True,
        "required_jobs":["solve"],
        "multiple_material_packages_fit":True,
        "work_items":[
            {"id":"info","jobs":["solve"],"burden":5,"info_gain":10,"dependency_leverage":1},
            {"id":"leverage","jobs":["solve"],"burden":5,"info_gain":1,"dependency_leverage":10},
        ],
    }
    def execute(selected,state,memory):
        calls.append({x["id"] for x in selected})
        return [{"status":"EXECUTED","execution_truth":"IMPLEMENTATION_EXECUTED"}]

    out=run_legacy_candidate(
        state,{},
        generate_questions=_questions,
        generate_work=_work,
        execute_work=execute,
        admit_results=_admit,
        update_state=_update_complete_after_one,
    )
    assert calls==[{"info","leverage"}]
    assert out.selection_traces[0]["activation_mode"]=="FIRE"


def test_material_delta_records_reselection_requirement():
    state={
        "terminal":"CONTINUE",
        "admitted_continuation":True,
        "required_jobs":["solve"],
        "task_and_job_well_typed":True,
        "one_validated_capability_clearly_fits":True,
        "consequence_bounded":True,
        "no_material_rival_exposed":True,
        "work_items":[{"id":"cheap","jobs":["solve"],"burden":1}],
    }
    def admit(results,state,memory):
        return {"material_result_delta":True,"changed_representation":True}
    out=run_legacy_candidate(
        state,{},
        generate_questions=_questions,
        generate_work=_work,
        execute_work=lambda selected,state,memory:[{"status":"EXECUTED"}],
        admit_results=admit,
        update_state=_update_complete_after_one,
    )
    assert out.memory["rho_reselection_required"] is True


def test_live_inquiry_cannot_silently_terminate():
    state={
        "terminal":"CONTINUE",
        "admitted_continuation":True,
        "required_jobs":["solve"],
        "task_and_job_well_typed":True,
        "one_validated_capability_clearly_fits":True,
        "consequence_bounded":True,
        "no_material_rival_exposed":True,
        "work_items":[{"id":"cheap","jobs":["solve"],"burden":1}],
    }
    def update(state,memory,delta):
        nxt=dict(state)
        nxt["iteration"]=1
        nxt["terminal"]="CONTINUE"
        nxt["admitted_continuation"]=False
        return nxt,dict(memory)

    try:
        run_legacy_candidate(
            state,{},
            generate_questions=_questions,
            generate_work=_work,
            execute_work=lambda selected,state,memory:[{"status":"EXECUTED"}],
            admit_results=_admit,
            update_state=update,
        )
    except RuntimeError as exc:
        assert "ICC128_REENTRY_FAILURE" in str(exc)
    else:
        raise AssertionError("expected liveness failure")


def test_missing_configured_tool_adapter_preserves_open():
    state={
        "terminal":"CONTINUE",
        "admitted_continuation":True,
        "required_jobs":["solve"],
        "task_and_job_well_typed":True,
        "one_validated_capability_clearly_fits":True,
        "consequence_bounded":True,
        "no_material_rival_exposed":True,
        "work_items":[
            {"id":"formal","jobs":["solve"],"burden":1,"tool_id":"RootCause"},
        ],
    }
    def update(state,memory,delta):
        return dict(state),dict(memory)

    out=run_legacy_candidate(
        state,{},
        generate_questions=_questions,
        generate_work=_work,
        execute_work=None,
        admit_results=lambda results,state,memory:{},
        update_state=update,
        configured_tool_adapters={},
    )
    assert out.status=="OPEN"
    assert out.state["terminal"]=="OPEN"
