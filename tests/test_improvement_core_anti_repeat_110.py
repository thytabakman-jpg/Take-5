import sys
sys.path.insert(0,"runtime")

from improvement_core_learning_memory import LearningMemory
from improvement_core_recursive_manager import (
    ChildReturn,
    RecursiveImprovementCoreManager,
)


def _child(job):
    return ChildReturn(
        child_id=job.id,
        job_id=job.job["id"],
        execution_truth="FULL_MATCH",
        result={"ok":True},
        basis_id=job.basis_id,
    )


def test_negative_learning_survives_fresh_process_and_reopens_only_on_relevant_change(tmp_path):
    ledger=tmp_path/"learning.json"
    first=LearningMemory(durable_path=ledger,autosave=True)
    first.record(
        "route-a","basis-a","NO_GAIN",
        {"representation","evidence"},
        {"reason":"same continuation class"},
    )

    fresh=LearningMemory.from_durable(ledger,autosave=False)
    assert fresh.unchanged_rerun_blocked("route-a","basis-a",set())
    assert fresh.unchanged_rerun_blocked("route-a","basis-a",{"authority"})
    assert not fresh.unchanged_rerun_blocked(
        "route-a","basis-a",{"representation"}
    )


def test_learning_filter_removes_blocked_candidate_before_frontier_choice(tmp_path):
    ledger=tmp_path/"learning.json"
    memory=LearningMemory(durable_path=ledger,autosave=True)
    memory.record(
        "old-route","b0","NO_GAIN",{"evidence"},{"reason":"already tested"}
    )
    calls=[]

    def select(z,m):
        return [
            {
                "id":"old",
                "route_id":"old-route",
                "basis_id":"b0",
                "goal_gain":999,
                "dependency_footprint":["evidence"],
            },
            {
                "id":"fresh",
                "route_id":"fresh-route",
                "basis_id":"b0",
                "goal_gain":1,
                "dependency_footprint":["evidence"],
            },
        ]

    def child(job):
        calls.append(job.job["id"])
        return _child(job)

    def admit(ret,z,m):
        return "ADMIT",{"material_result_delta":True}

    def update(z,m,a,d):
        z=dict(z)
        z["terminal"]="COMPLETE"
        z["live_continuation"]=False
        return z,m

    mgr=RecursiveImprovementCoreManager(
        select,child,admit,update,learning_memory=memory
    )
    out=mgr.run(
        {"terminal":"CONTINUE","live_continuation":True,"basis_id":"b0"},
        {},
    )
    assert out["status"]=="COMPLETE"
    assert calls==["fresh"]
    assert out["traces"][0]["selected_job"]["id"]=="fresh"


def test_same_basis_semantic_no_effect_cycle_is_closed_and_persisted(tmp_path):
    ledger=tmp_path/"learning.json"
    memory=LearningMemory(durable_path=ledger,autosave=True)

    def select(z,m):
        return {
            "id":"audit-again",
            "route_id":"audit-again",
            "basis_id":"b0",
            "dependency_footprint":["representation"],
        }

    def admit(ret,z,m):
        return "NO_GAIN",{"certified_no_gain":True}

    def update(z,m,a,d):
        return {
            **z,
            "semantic_class":"SAME",
            "terminal":"CONTINUE",
            "live_continuation":True,
        },m

    mgr=RecursiveImprovementCoreManager(
        select,_child,admit,update,learning_memory=memory
    )
    out=mgr.run(
        {
            "semantic_class":"SAME",
            "terminal":"CONTINUE",
            "live_continuation":True,
            "basis_id":"b0",
        },
        {},
    )
    assert out["status"]=="OPEN"
    assert out["blocker"]=="IC_MANAGER_SEMANTIC_CYCLE_NO_GAIN"

    fresh=LearningMemory.from_durable(ledger,autosave=False)
    assert fresh.unchanged_rerun_blocked("audit-again","b0",set())
    assert any(
        r.disposition=="CYCLE_NO_GAIN"
        for r in fresh.records
        if r.route_id=="audit-again"
    )


def test_material_label_cannot_hide_protected_regression():
    def select(z,m):
        return {"id":"unsafe","route_id":"unsafe","basis_id":"b0"}

    def admit(ret,z,m):
        return "ADMIT",{"material_result_delta":True}

    def update(z,m,a,d):
        return {
            **z,
            "protected_behavior_ids":[],
            "terminal":"CONTINUE",
            "live_continuation":True,
        },m

    mgr=RecursiveImprovementCoreManager(select,_child,admit,update)
    try:
        mgr.run(
            {
                "protected_behavior_ids":["KEEP"],
                "terminal":"CONTINUE",
                "live_continuation":True,
                "basis_id":"b0",
            },
            {},
        )
    except RuntimeError as exc:
        assert "PROTECTED_REGRESSION" in str(exc)
    else:
        raise AssertionError("protected regression must reject strict progress")
