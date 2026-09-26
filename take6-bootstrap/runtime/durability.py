"""Durability gate for Take-6 content-addressed evidence."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class ReplicaWitness:
    backend_id: str
    trust_domain: str
    verified_cids: frozenset[str]

@dataclass(frozen=True)
class DurabilityReceipt:
    cid: str
    independent_trust_domains: tuple[str, ...]
    replica_backends: tuple[str, ...]
    status: str

def verify_durable(
    cid: str,
    replicas: Iterable[ReplicaWitness],
    *,
    min_independent_trust_domains: int = 2,
) -> DurabilityReceipt:
    matched = [r for r in replicas if cid in r.verified_cids]
    domains = tuple(sorted({r.trust_domain for r in matched}))
    backends = tuple(sorted({r.backend_id for r in matched}))
    if len(domains) < min_independent_trust_domains:
        raise RuntimeError(
            "TAKE6_DURABILITY_REPLICATION_OPEN:"
            + cid
            + ":domains="
            + ",".join(domains)
        )
    return DurabilityReceipt(
        cid=cid,
        independent_trust_domains=domains,
        replica_backends=backends,
        status="PASS",
    )
