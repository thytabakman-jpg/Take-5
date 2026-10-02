import sys
sys.path.insert(0,"runtime")

import pytest

pytest.importorskip("dbos")

from kernel053_dbos_backend import DBOSDurableBackend
from kernel053_durable_execution import execute_selected_operation


def test_dbos_same_episode_operation_id_is_idempotent(tmp_path):
    calls={"n":0}

    def generic(payload):
        calls["n"]+=1
        return {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":{"seen":payload["value"],"call":calls["n"]},
        }

    db=tmp_path/"kernel053.sqlite"
    backend=DBOSDurableBackend(
        operations={"generic":generic},
        system_database_url=f"sqlite:///{db}",
        application_name="kernel053-bakeoff",
        application_version="0.1.0",
        reset_database=True,
    )
    try:
        first=execute_selected_operation(
            backend,
            episode_id="episode-1",
            operation_id="generic:w1",
            payload={"value":7},
            invoke=lambda: (_ for _ in ()).throw(
                AssertionError("DBOS backend must use registered durable handler")
            ),
        )
        second=execute_selected_operation(
            backend,
            episode_id="episode-1",
            operation_id="generic:w1",
            payload={"value":7},
            invoke=lambda: (_ for _ in ()).throw(
                AssertionError("DBOS backend must use registered durable handler")
            ),
        )
        assert first.result==second.result
        assert calls["n"]==1
        assert first.backend=="DBOS"
        assert "workflow_id:kernel053:episode-1:generic:w1" in first.evidence
    finally:
        backend.close()


def test_dbos_distinct_operation_ids_execute_distinct_work(tmp_path):
    calls=[]

    def generic(payload):
        calls.append(payload["value"])
        return {"status":"EXECUTED","result":payload["value"]}

    backend=DBOSDurableBackend(
        operations={"generic":generic},
        system_database_url=f"sqlite:///{tmp_path/'kernel053.sqlite'}",
        application_name="kernel053-bakeoff-2",
        application_version="0.1.0",
        reset_database=True,
    )
    try:
        for work_id,value in (("w1",1),("w2",2)):
            execute_selected_operation(
                backend,
                episode_id="episode-2",
                operation_id=f"generic:{work_id}",
                payload={"value":value},
                invoke=lambda:None,
            )
        assert calls==[1,2]
    finally:
        backend.close()


def test_dbos_backend_refuses_unregistered_operation_type(tmp_path):
    backend=DBOSDurableBackend(
        operations={"generic":lambda p:p},
        system_database_url=f"sqlite:///{tmp_path/'kernel053.sqlite'}",
        application_name="kernel053-bakeoff-3",
        application_version="0.1.0",
        reset_database=True,
    )
    try:
        with pytest.raises(RuntimeError,match="OPERATION_TYPE_UNREGISTERED:tool"):
            execute_selected_operation(
                backend,
                episode_id="episode-3",
                operation_id="tool:PD",
                payload={},
                invoke=lambda:{"status":"EXECUTED"},
            )
    finally:
        backend.close()
