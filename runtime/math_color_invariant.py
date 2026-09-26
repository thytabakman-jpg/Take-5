"""Claim-relative Mathematical Color Invariant.

GREEN is earned only when every coordinate required by the current job/claim is
sufficiently recovered. Otherwise the verdict is RED.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple

RED_STATUSES = frozenset({
    "MISSING",
    "PARTIAL",
    "AMBIGUOUS",
    "CONFLICT",
    "OPEN",
    "BLOCKED",
    "ONLY_NAMED",
    "CANDIDATE_ONLY",
    "IMPLEMENTED_BUT_NOT_SEMANTICALLY_COMPLETE",
    "SEMANTICALLY_DEFINED_BUT_NOT_BOUND_WHEN_BINDING_IS_REQUIRED",
    "UNVERIFIED_WHEN_VERIFICATION_IS_REQUIRED",
})

GREEN_STATUSES = frozenset({
    "RECOVERED",
    "ADMITTED",
    "VERIFIED",
})


@dataclass(frozen=True)
class ColorVerdict:
    object_id: str
    job: str
    claim: str
    required_coordinates: Tuple[str, ...]
    unresolved_coordinates: Tuple[str, ...]
    color: str


def color_verdict(
    *,
    object_id: str,
    job: str,
    claim: str,
    required_coordinates: Tuple[str, ...],
    coordinate_status: Mapping[str, str],
) -> ColorVerdict:
    required = tuple(required_coordinates)
    unresolved = []

    if not required:
        unresolved.append("REQUIRED_COORDINATES_UNSPECIFIED")

    for coordinate in required:
        status = coordinate_status.get(coordinate, "MISSING")
        if status not in GREEN_STATUSES:
            unresolved.append(coordinate)

    color = "GREEN" if required and not unresolved else "RED"

    return ColorVerdict(
        object_id=object_id,
        job=job,
        claim=claim,
        required_coordinates=required,
        unresolved_coordinates=tuple(unresolved),
        color=color,
    )
