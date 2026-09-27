"""Jane -> current ICC128 continuity handoff.

Jane reconstructs continuity. ICC128 owns substantive selection.
This bridge prevents a label-only handoff by requiring a READY continuity
packet and producing explicit controller state and memory.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

@dataclass(frozen=True)
class ICC128Entry:
    state: dict[str, Any]
    memory: dict[str, Any]
    status: str

def bind_jane_continuity(packet, *, rejection_memory: Mapping[str,Any] | None = None) -> ICC128Entry:
    status=str(getattr(packet,"status","OPEN"))
    if status!="READY":
        missing=tuple(getattr(packet,"missing",()) or ())
        return ICC128Entry(
            state={
                "terminal":"OPEN",
                "selection_blocked":True,
                "continuity_missing":missing,
                "admitted_continuation":False,
            },
            memory=dict(rejection_memory or {}),
            status="OPEN",
        )

    state={
        "terminal":"CONTINUE",
        "admitted_continuation":True,
        "target":getattr(packet,"target",None),
        "job":getattr(packet,"job",None),
        "basis":getattr(packet,"basis",None),
        "canonical_version":getattr(packet,"canonical_version",None),
        "protected_behaviors":tuple(getattr(packet,"protected_behaviors",()) or ()),
        "open_coordinates":tuple(getattr(packet,"open_coordinates",()) or ()),
        "capability_gaps":tuple(getattr(packet,"capability_gaps",()) or ()),
        "evidence_refs":tuple(getattr(packet,"evidence_refs",()) or ()),
        "target_or_job_identity_open":False,
        "recurrence_or_prior_failure":bool(rejection_memory),
        "representation_result_sensitive":True,
        "state_delta_invalidates_prior_selection":bool(rejection_memory),
        "capability_or_tool_selection_is_itself_the_job":False,
    }
    memory=dict(rejection_memory or {})
    memory["jane_continuity"]={
        "canonical_version":state["canonical_version"],
        "evidence_refs":state["evidence_refs"],
        "protected_behaviors":state["protected_behaviors"],
        "open_coordinates":state["open_coordinates"],
        "capability_gaps":state["capability_gaps"],
    }
    return ICC128Entry(state=state,memory=memory,status="READY")
