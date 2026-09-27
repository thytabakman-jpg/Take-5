"""Native Bias Perturbation tool.

Operational bias susceptibility is result sensitivity to a perturbation already
licensed as irrelevant to the protected semantics. Unlicensed perturbations stay
OPEN and are never counted as bias evidence.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Iterable


@dataclass(frozen=True)
class PerturbationResult:
    perturbation: Any
    semantics_irrelevant: bool
    result_changed: bool | None
    result: Any = None


def run_bias_perturbation(
    target: Any,
    perturbations: Iterable[Any],
    *,
    runner: Callable[[Any], Any],
    semantics_equivalent: Callable[[Any, Any], bool],
    result_equivalent: Callable[[Any, Any], bool],
):
    baseline_target=deepcopy(target)
    baseline_result=runner(deepcopy(baseline_target))
    rows=[]
    unresolved=[]
    sensitive=[]

    for perturbation in tuple(perturbations):
        candidate=deepcopy(perturbation)
        irrelevant=bool(semantics_equivalent(baseline_target,candidate))
        if not irrelevant:
            rows.append(PerturbationResult(candidate,False,None,None))
            unresolved.append(candidate)
            continue
        result=runner(deepcopy(candidate))
        changed=not bool(result_equivalent(baseline_result,result))
        rows.append(PerturbationResult(candidate,True,changed,result))
        if changed:
            sensitive.append(candidate)

    return {
        "status":"OPEN" if unresolved else "ACCEPT",
        "baseline_result":baseline_result,
        "results":tuple(rows),
        "bias_sensitive":tuple(sensitive),
        "unlicensed_or_unresolved":tuple(unresolved),
    }
