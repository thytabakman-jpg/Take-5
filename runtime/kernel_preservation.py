"""Executable Take-Two-style kernel preservation membrane.

This guard does not decide what substantive change to make. It enforces the compact
kernel law around consequential state changes.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class KernelChange:
    consequential:bool
    observed_before:bool
    typed:bool
    authority:bool
    transition_declared:bool
    verified_after:bool
    open_state_preserved:bool

@dataclass(frozen=True)
class KernelChangeVerdict:
    legal:bool
    reasons:tuple[str,...]

def admit_change(change:KernelChange)->KernelChangeVerdict:
    if not change.consequential:
        return KernelChangeVerdict(True,())
    checks=(
        ("OBSERVATION_REQUIRED",change.observed_before),
        ("TYPE_REQUIRED",change.typed),
        ("AUTHORITY_REQUIRED",change.authority),
        ("TYPED_TRANSITION_REQUIRED",change.transition_declared),
        ("VERIFICATION_REQUIRED",change.verified_after),
        ("OPEN_STATE_PRESERVATION_REQUIRED",change.open_state_preserved),
    )
    reasons=tuple(name for name,ok in checks if not ok)
    return KernelChangeVerdict(not reasons,reasons)
