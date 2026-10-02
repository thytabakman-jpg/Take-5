"""Kernel 053 Packetize boundary.

Packetize may package evidence and dependencies.  It cannot generate controller
question/work frontiers or select substantive work.
"""
from __future__ import annotations

from typing import Any, Mapping


FORBIDDEN_ACTIVE_FIELDS = frozenset({
    "question_frontier",
    "work_frontier",
    "selected_work",
    "selected_works",
    "selected_tools",
    "selected_tool_ids",
    "selected_tool",
    "selected_tool_id",
    "selected_action",
    "selected_job",
    "selected_next_candidate",
})


class PacketizeSelectionBlocked(RuntimeError):
    pass


def _material(value: Any) -> bool:
    if value is None:
        return False
    if value is False:
        return False
    if value in ((), [], {}, "", frozenset(), set()):
        return False
    return True


def validate_packetize_output(packet: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(packet, Mapping):
        raise PacketizeSelectionBlocked("PACKETIZE_MAPPING_REQUIRED")

    offenders = tuple(
        key for key in sorted(FORBIDDEN_ACTIVE_FIELDS)
        if key in packet and _material(packet[key])
    )
    if offenders:
        raise PacketizeSelectionBlocked(
            "PACKETIZE_SUBSTANTIVE_SELECTION_FORBIDDEN:" + ",".join(offenders)
        )
    return dict(packet)
