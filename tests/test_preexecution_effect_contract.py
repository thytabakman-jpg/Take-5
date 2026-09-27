import sys
sys.path.insert(0,"runtime")

from improvement_core_recursive_manager import (
    ChildReturn,
    RecursiveImprovementCoreManager,
)
from improvement_core_legacy_candidate import run_legacy_candidate


def _valid_spec():
    return {
        "object_id":"TOOL:X",
        "basis_id":"b0",
        "identification_status":"IDENTIFIED",
        "required_coordinates":["native","protected"],
        "resolved_coordinates":["native","protected"],
    }


def test_recursive_manager_blocks_untyped_callback_before_run_child():
    calls=[]

    def select(z,m):
        return {
            "id":"j1",
            "basis_id":"b0",
            "operation_class":"VERIFY",
        }

    def child(job):
        calls.append(job.job["id"])
        raise AssertionError("untyped callback must not run")

    mgr=RecursiveImprovementCoreManager(
        select,
        child,
        lambda *args:("OPEN",{}),
        lambda z,m,a,d:(z,m),
    )
    out=mgr.run(
        {"terminal":"CONTINUE","live_continuation":True,"basis_id":"b0"},
        {},
    )
    assert out["status"]=="OPEN"
    assert out["blocker"]=="EXECUTION_ADMISSION_OPEN:EFFECT_CLASS_REQUIRED"
    assert calls==[]


def test_recursive_manager_blocks_transform_before_callback_when_spec_open():
    calls=[]

    def select(z,m):
        return {
            "id":"j1",
            "basis_id":"b0",
            "operation_class":"IMPROVE",
            "execution_effect_class":"TARGET_TRANSFORM",
        }

    def child(job):
        calls.append(job.job["id"])
        raise AssertionError("unlicensed transform must not run")

    mgr=RecursiveImprovementCoreManager(
        select,
        child,
        lambda *args:("OPEN",{}),
        lambda z,m,a,d:(z,m),
    )
    out=mgr.run(
        {"terminal":"CONTINUE","live_continuation":True,"basis_id":"b0"},
        {},
    )
    assert out["status"]=="OPEN"
    assert "SPECIFICATION_PACKET_REQUIRED" in out["blocker"]
    assert calls==[]


def test_recursive_manager_runs_licensed_target_transform():
    calls=[]

    def select(z,m):
        return {
            "id":"j1",
            "route_id":"j1",
            "basis_id":"b0",
            "operation_class":"IMPROVE",
            "execution_effect_class":"TARGET_TRANSFORM",
            "object_specification":_valid_spec(),
        }

    def child(job):
        calls.append(job.job["id"])
        return ChildReturn(
            child_id=job.id,
            job_id=job.job["id"],
            execution_truth="IMPLEMENTATION_EXECUTED",
            result={"changed":True},
            basis_id=job.basis_id,
        )

    def admit(ret,z,m):
        return "ADMIT",{
            "material_result_delta":True,
            "obligation_states":["CLOSED"],
        }

    def update(z,m,a,d):
        return {
            **z,
            "terminal":"COMPLETE",
            "live_continuation":False,
        },m

    mgr=RecursiveImprovementCoreManager(select,child,admit,update)
    out=mgr.run(
        {"terminal":"CONTINUE","live_continuation":True,"basis_id":"b0"},
        {},
    )
    assert out["status"]=="COMPLETE"
    assert calls==["j1"]
    assert out["traces"][0]["strict_progress"] is True


def _legacy_questions(state,memory):
    if state.get("terminal") in {"COMPLETE","OPEN","BLOCKED","CONFLICT"}:
        return []
    return [{"question_id":"q","issue":"next","obligations":["solve"]}]


def _legacy_work(questions,state,memory):
    return list(state["work_items"])


def _legacy_state(item):
    return {
        "terminal":"CONTINUE",
        "admitted_continuation":True,
        "required_jobs":["solve"],
        "task_and_job_well_typed":True,
        "one_validated_capability_clearly_fits":True,
        "consequence_bounded":True,
        "no_material_rival_exposed":True,
        "work_items":[item],
    }


def _legacy_update(state,memory,delta):
    nxt=dict(state)
    nxt["terminal"]="COMPLETE"
    nxt["admitted_continuation"]=False
    return nxt,dict(memory)


def test_legacy_generic_transform_is_blocked_before_execute_work():
    calls=[]

    def execute(selected,state,memory):
        calls.append(tuple(x["id"] for x in selected))
        raise AssertionError("unlicensed legacy transform must not run")

    out=run_legacy_candidate(
        _legacy_state({
            "id":"mutate",
            "jobs":["solve"],
            "burden":1,
            "operation_class":"IMPROVE",
            "execution_effect_class":"TARGET_TRANSFORM",
        }),
        {},
        generate_questions=_legacy_questions,
        generate_work=_legacy_work,
        execute_work=execute,
        admit_results=lambda results,state,memory:{},
        update_state=lambda s,m,d:(dict(s),dict(m)),
    )
    assert out.status=="OPEN"
    assert calls==[]
    assert "SPECIFICATION_PACKET_REQUIRED" in out.traces[0]["results"][0]["blocker"]


def test_legacy_generic_licensed_transform_can_execute():
    calls=[]

    def execute(selected,state,memory):
        calls.append(tuple(x["id"] for x in selected))
        return [{
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
        }]

    out=run_legacy_candidate(
        _legacy_state({
            "id":"mutate",
            "jobs":["solve"],
            "burden":1,
            "operation_class":"IMPROVE",
            "execution_effect_class":"TARGET_TRANSFORM",
            "object_specification":_valid_spec(),
        }),
        {},
        generate_questions=_legacy_questions,
        generate_work=_legacy_work,
        execute_work=execute,
        admit_results=lambda results,state,memory:{"material_result_delta":True},
        update_state=_legacy_update,
    )
    assert out.status=="COMPLETE"
    assert calls==[("mutate",)]
