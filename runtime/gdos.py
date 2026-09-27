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
    for index,observer in enumerate(tuple(observers)):
        try:
            result=observer(deepcopy(frozen))
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
    reconciled=reconcile_fn(captured)
    return {
        "status":"EXECUTED",
        "frozen_target":frozen,
        "observations":captured,
        "reconciled":reconciled,
        "goal_conditioning":"SUPPRESSED_DURING_OBSERVATION",
        "mutation_policy":"INDEPENDENT_COPY_PER_OBSERVER",
    }
