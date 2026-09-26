"""Zero-request upstream discovery for ImprovementCore.

Converts an addressable corpus into a governed observation-first seed for the
normal ImprovementCore controller. It does not solve the substantive problem
before controller entry. It creates only a typed discovery job from observed
structure.
"""
from dataclasses import dataclass
from typing import Any, Iterable

from autonomous_observer import observe_records
from zero_request_episode import zero_request_episode


@dataclass(frozen=True)
class UpstreamSeed:
    target: str
    job: str
    basis: str
    state_delta: dict[str, Any]
    observation_receipt: Any


def discover_upstream_seed(corpus: Iterable[Any]) -> UpstreamSeed:
    records=tuple(corpus)
    if not records:
        raise ValueError("ZERO_REQUEST_CORPUS_REQUIRED")

    episode=zero_request_episode(records, lambda items,binding: observe_records(items))
    if not episode.complete:
        raise RuntimeError("ZERO_REQUEST_OBSERVATION_INCOMPLETE")

    target="corpus:"+"|".join(str(i) for i in range(len(records)))
    state_delta={
        "upstream_discovery":{
            "status":"OBSERVED",
            "corpus_size":len(records),
            "observation":episode.result,
            "authority":"observe",
        },
    }
    return UpstreamSeed(
        target=target,
        job="DISCOVER_MATERIAL_IMPROVEMENT_FRONTIER",
        basis="ZERO_REQUEST_OBSERVATION",
        state_delta=state_delta,
        observation_receipt=episode,
    )
