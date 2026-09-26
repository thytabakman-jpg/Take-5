"""Zero-request upstream discovery for ImprovementCore.

Converts an addressable corpus into a governed observation-first seed for the
normal ImprovementCore controller. It does not solve the substantive problem
before controller entry. It creates only a typed discovery job from observed
structure.

The current path now also:
- selects CHEAP versus BROAD observation using the validated structural policy;
- carries the current relation-generator basis;
- admits direct reference relations under the typed relation kernel.

This makes the relation/calibration repair part of the normal entry path rather
than a detached analysis artifact.
"""
from dataclasses import dataclass
from typing import Any, Iterable

from autonomous_observer import observe_records
from improvement_core_route_calibration import broad_observe_records,select_route
from relation_kernel import (
    current_relation_basis,
    relation_candidates_from_records,
    licensed_ledger,
)
from zero_request_episode import zero_request_episode


@dataclass(frozen=True)
class UpstreamSeed:
    target: str
    job: str
    basis: str
    state_delta: dict[str, Any]
    observation_receipt: Any


def _relation_projection(records):
    basis=current_relation_basis()
    candidates=relation_candidates_from_records(records)
    licensed,unresolved,rejected=licensed_ledger(candidates,basis)
    def row(pair):
        c,a=pair
        return {
            "relation_id":c.relation_id,
            "arguments":c.arguments,
            "status":a.status.value,
            "reason":a.reason,
        }
    return {
        "basis_id":basis.basis_id,
        "generator_ids":basis.generator_ids,
        "licensed":tuple(row(x) for x in licensed),
        "open":tuple(row(x) for x in unresolved),
        "rejected":tuple(row(x) for x in rejected),
    }


def discover_upstream_seed(corpus: Iterable[Any]) -> UpstreamSeed:
    records=tuple(corpus)
    if not records:
        raise ValueError("ZERO_REQUEST_CORPUS_REQUIRED")

    calibration=select_route(records)
    observer=broad_observe_records if calibration.route=="BROAD" else observe_records
    episode=zero_request_episode(records, lambda items,binding: observer(items))
    if not episode.complete:
        raise RuntimeError("ZERO_REQUEST_OBSERVATION_INCOMPLETE")

    target="corpus:"+"|".join(str(i) for i in range(len(records)))
    state_delta={
        "upstream_discovery":{
            "status":"OBSERVED",
            "corpus_size":len(records),
            "observation":episode.result,
            "authority":"observe",
            "route":calibration.route,
            "route_reason":calibration.reason,
            "relation_state":_relation_projection(records),
        },
    }
    return UpstreamSeed(
        target=target,
        job="DISCOVER_MATERIAL_IMPROVEMENT_FRONTIER",
        basis="ZERO_REQUEST_OBSERVATION",
        state_delta=state_delta,
        observation_receipt=episode,
    )
