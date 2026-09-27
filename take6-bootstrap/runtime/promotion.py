"""Protected-behavior promotion gate for Take-6."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class PromotionReceipt:
    status: str
    missing_behaviors: tuple[str, ...]
    typed_open_behaviors: tuple[str, ...]
    authorized_deltas: tuple[str, ...]
    validations: tuple[str, ...]
    consequence_closed: bool
    predecessor_specification_status: str
    successor_specification_status: str
    source_frontier_cid: str

def verify_promotion(
    *,
    predecessor_protected: Iterable[str],
    successor_preserved: Iterable[str],
    authorized_deltas: Iterable[str] = (),
    typed_open: Iterable[str] = (),
    validations: Iterable[str] = (),
    required_validations: Iterable[str] = (),
    consequence_closed: bool,
    predecessor_specification_status: str = "OPEN",
    successor_specification_status: str = "OPEN",
    source_frontier_verified: bool = False,
    source_frontier_cid: str = "",
) -> PromotionReceipt:
    pred=set(map(str, predecessor_protected))
    kept=set(map(str, successor_preserved))
    auth=set(map(str, authorized_deltas))
    opened=set(map(str, typed_open))
    missing=tuple(sorted(pred-kept-auth-opened))
    vals=set(map(str, validations))
    req=set(map(str, required_validations))
    missing_validations=sorted(req-vals)
    predecessor_specification_status=str(predecessor_specification_status).upper()
    successor_specification_status=str(successor_specification_status).upper()

    if not source_frontier_verified or not str(source_frontier_cid).startswith("sha256:"):
        raise RuntimeError("TAKE6_PROMOTION_SOURCE_FRONTIER_UNVERIFIED")
    if predecessor_specification_status!="PASS" or successor_specification_status!="PASS":
        raise RuntimeError(
            "TAKE6_PROMOTION_SPECIFICATION_OPEN:"
            + predecessor_specification_status
            + ":"
            + successor_specification_status
        )
    if missing:
        raise RuntimeError("TAKE6_PROMOTION_SILENT_BEHAVIOR_LOSS:" + ",".join(missing))
    if missing_validations:
        raise RuntimeError("TAKE6_PROMOTION_VALIDATION_MISSING:" + ",".join(missing_validations))
    if not consequence_closed:
        raise RuntimeError("TAKE6_PROMOTION_CONSEQUENCE_CLOSURE_MISSING")

    status="OPEN" if opened else "PASS"
    return PromotionReceipt(
        status=status,
        missing_behaviors=(),
        typed_open_behaviors=tuple(sorted(opened)),
        authorized_deltas=tuple(sorted(auth)),
        validations=tuple(sorted(vals)),
        consequence_closed=True,
        predecessor_specification_status=predecessor_specification_status,
        successor_specification_status=successor_specification_status,
        source_frontier_cid=str(source_frontier_cid),
    )
