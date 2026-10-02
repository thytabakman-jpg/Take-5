"""Optional DBOS realization of Kernel 053 D_exec.

This module is intentionally optional.  Normal Take-5 runtime does not import it.
DBOS owns durable workflow/step mechanics only; ICC128 remains the substantive
controller.

Handlers are registered by stable operation type so recovery does not depend on
serializing a per-call closure.
"""
from __future__ import annotations

from typing import Any, Callable, Mapping

from dbos import DBOS, DBOSConfig, SetWorkflowID

from kernel053_durable_execution import DurableExecutionReceipt


_OPERATION_REGISTRY:dict[str,Callable[[Mapping[str,Any]],Any]]={}


@DBOS.step()
def _kernel053_registered_step(operation_type:str,payload:dict[str,Any]):
    handler=_OPERATION_REGISTRY.get(str(operation_type))
    if handler is None:
        raise RuntimeError(f"DBOS_KERNEL053_OPERATION_TYPE_UNREGISTERED:{operation_type}")
    return handler(dict(payload))


@DBOS.workflow()
def _kernel053_registered_workflow(operation_type:str,payload:dict[str,Any]):
    return _kernel053_registered_step(operation_type,dict(payload))


class DBOSDurableBackend:
    name="DBOS"

    def __init__(
        self,
        *,
        operations:Mapping[str,Callable[[Mapping[str,Any]],Any]],
        system_database_url:str="sqlite:///kernel053_dbos.sqlite",
        application_name:str="take5-kernel053",
        application_version:str="0.1.0",
        reset_database:bool=False,
        launch:bool=True,
    ):
        self.operations={str(k):v for k,v in operations.items()}
        if not self.operations:
            raise ValueError("DBOS_KERNEL053_OPERATION_REGISTRY_REQUIRED")
        for key,handler in self.operations.items():
            if not callable(handler):
                raise TypeError(f"DBOS_KERNEL053_HANDLER_NOT_CALLABLE:{key}")
            _OPERATION_REGISTRY[key]=handler

        if launch:
            DBOS.destroy()
            config:DBOSConfig={
                "name":str(application_name),
                "application_version":str(application_version),
                "system_database_url":str(system_database_url),
            }
            DBOS(config=config)
            if reset_database:
                DBOS.reset_system_database(truncate=True)
            DBOS.launch()

    @staticmethod
    def operation_type(operation_id:str)->str:
        raw=str(operation_id)
        if ":" not in raw:
            return raw
        return raw.split(":",1)[0]

    def execute(self,*,episode_id,operation_id,payload,invoke):
        operation_type=self.operation_type(str(operation_id))
        if operation_type not in self.operations:
            raise RuntimeError(
                f"DBOS_KERNEL053_OPERATION_TYPE_UNREGISTERED:{operation_type}"
            )
        workflow_id=f"kernel053:{episode_id}:{operation_id}"
        with SetWorkflowID(workflow_id):
            raw=_kernel053_registered_workflow(operation_type,dict(payload))

        if isinstance(raw,Mapping):
            status=str(raw.get("status","EXECUTED"))
            truth=str(raw.get("execution_truth","")) or (
                status if status in {"OPEN","BLOCKED","CONFLICT"}
                else "IMPLEMENTATION_EXECUTED"
            )
        else:
            status="EXECUTED"
            truth="IMPLEMENTATION_EXECUTED"

        return DurableExecutionReceipt(
            backend=self.name,
            episode_id=str(episode_id),
            operation_id=str(operation_id),
            status=status,
            execution_truth=truth,
            result=raw,
            evidence=(
                f"d_exec:{self.name}",
                f"workflow_id:{workflow_id}",
                f"operation_type:{operation_type}",
            ),
        )

    @staticmethod
    def close():
        DBOS.destroy()
