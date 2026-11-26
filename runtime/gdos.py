"""Native Goal-Decoupled Observation Sweep.

GDOS freezes one target, executes observers independently against copies of that
target with intervention/optimization suppressed by contract, and reconciles only
after all observations have been captured.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Iterable


def run_gdos(
    target: Any,
    *,
    observers: Iterable[Callable[[Any], Any]],
    reconcile_fn: Callable[[tuple[Any, ...]], Any],
):
    frozen=deepcopy(target)
    observations=[]
    observers=tuple(observers)
    if not observers:
        return {"status":"OPEN","frozen_target":frozen,"observations":(),
                "blocker":"GDOS_OBSERVER_INVENTORY_REQUIRED"}
    for index,observer in enumerate(observers):
        try:
            # Capture each result before a later observer can mutate a shared buffer.
            result=deepcopy(observer(deepcopy(frozen)))
        except Exception as exc:
            return {
                "status":"BLOCKED",
                "frozen_target":frozen,
                "observations":tuple(observations),
                "failed_observer":index,
                "error":f"{type(exc).__name__}:{exc}",
            }
        observations.append(result)

    captured=tuple(observations)
    try:
        reconciled=reconcile_fn(deepcopy(captured))
    except Exception as exc:
        return {
            "status":"BLOCKED",
            "frozen_target":frozen,
            "observations":captured,
            "blocker":"GDOS_RECONCILIATION_FAILED",
            "error":f"{type(exc).__name__}:{exc}",
        }
    return {
        "status":"EXECUTED",
        "frozen_target":frozen,
        "observations":captured,
        "reconciled":reconciled,
        "goal_conditioning":"SUPPRESSED_DURING_OBSERVATION",
        "mutation_policy":"INDEPENDENT_COPY_PER_OBSERVER",
    }
