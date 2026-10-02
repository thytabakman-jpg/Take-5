"""Pluggable D_exec boundary for Kernel 053.

The backend may provide execution durability, replay and lifecycle mechanics.  It
receives already-selected work and therefore has no substantive selection authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping, Protocol


@dataclass(frozen=True)
class DurableExecutionReceipt:
    backend: str
    episode_id: str
    operation_id: str
    status: str
    execution_truth: str
    result: Any
    evidence: tuple[str, ...]


class DurableExecutionBackend(Protocol):
    name: str

    def execute(
        self,
        *,
        episode_id: str,
        operation_id: str,
        payload: Mapping[str, Any],
        invoke: Callable[[], Any],
    ) -> DurableExecutionReceipt: ...


class Take5InlineBackend:
    """Baseline backend: current in-process Take-5 execution, no durability claim."""

    name = "TAKE5_INLINE"

    def execute(self, *, episode_id, operation_id, payload, invoke):
        raw = invoke()
        if isinstance(raw, Mapping):
            status = str(raw.get("status", "EXECUTED"))
            truth = str(raw.get("execution_truth", "")) or (
                status if status in {"OPEN", "BLOCKED", "CONFLICT"}
                else "IMPLEMENTATION_EXECUTED"
            )
        else:
            status = "EXECUTED"
            truth = "IMPLEMENTATION_EXECUTED"
        return DurableExecutionReceipt(
            backend=self.name,
            episode_id=str(episode_id),
            operation_id=str(operation_id),
            status=status,
            execution_truth=truth,
            result=raw,
            evidence=(f"d_exec:{self.name}", f"operation:{operation_id}"),
        )


def execute_selected_operation(
    backend: DurableExecutionBackend,
    *,
    episode_id: str,
    operation_id: str,
    payload: Mapping[str, Any],
    invoke: Callable[[], Any],
) -> DurableExecutionReceipt:
    if not operation_id:
        raise ValueError("D_EXEC_OPERATION_ID_REQUIRED")
    return backend.execute(
        episode_id=str(episode_id),
        operation_id=str(operation_id),
        payload=dict(payload),
        invoke=invoke,
    )
