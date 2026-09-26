"""Jane continuity recovery packet.

Jane's continuity job is to reconstruct enough durable entry state that a new turn
does not require the user to restate the system. Missing coordinates remain OPEN.
This module does not select substantive actions; it prepares supervisory context for
the controller that owns the episode.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping,Any

REQUIRED=("target","job","basis","canonical_version")

@dataclass(frozen=True)
class JaneContinuityPacket:
    target:str|None
    job:str|None
    basis:str|None
    canonical_version:str|None
    protected_behaviors:tuple[str,...]
    open_coordinates:tuple[str,...]
    capability_gaps:tuple[str,...]
    evidence_refs:tuple[str,...]
    missing:tuple[str,...]
    status:str

def recover_continuity(
    currentness:Mapping[str,Any],
    *,
    protected_behaviors=(),
    open_coordinates=(),
    capability_gaps=(),
    evidence_refs=(),
)->JaneContinuityPacket:
    values={k:currentness.get(k) for k in REQUIRED}
    missing=tuple(k for k,v in values.items() if not v)
    status="OPEN" if missing else "READY"
    return JaneContinuityPacket(
        target=values["target"],
        job=values["job"],
        basis=values["basis"],
        canonical_version=values["canonical_version"],
        protected_behaviors=tuple(protected_behaviors),
        open_coordinates=tuple(open_coordinates),
        capability_gaps=tuple(capability_gaps),
        evidence_refs=tuple(evidence_refs),
        missing=missing,
        status=status,
    )

def controller_context(packet:JaneContinuityPacket)->dict:
    """Project continuity evidence without claiming controller authority."""
    return {
        "target":packet.target,
        "job":packet.job,
        "basis":packet.basis,
        "canonical_version":packet.canonical_version,
        "protected_behaviors":packet.protected_behaviors,
        "open_coordinates":packet.open_coordinates,
        "capability_gaps":packet.capability_gaps,
        "evidence_refs":packet.evidence_refs,
        "continuity_status":packet.status,
        "continuity_missing":packet.missing,
    }
