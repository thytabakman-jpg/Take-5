"""Fail-closed capability preservation checks.

A capability is not preserved merely because its name or documentation survives.
Operational preservation requires a recoverable chain from identity through future
consumption/reentry.

For an operational capability c:

Pres(c) = I ∧ S ∧ R ∧ Q ∧ X ∧ E ∧ C ∧ V

I identity is recoverable
S semantics/job contract is recoverable
R capability remains reachable from normal control
Q selection/routing basis is recoverable
X execution binding exists
E material effect/admission semantics are recoverable
C a consumer/reentry path exists
V recovery/verification witness exists

Non-operational semantic objects may explicitly waive X only when the waiver is typed
and the remaining coordinates are present. Unknown is OPEN, never silently preserved.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Any

REQUIRED_OPERATIONAL=(
    "identity","semantics","reachability","selection",
    "execution","effect","consumer","recovery",
)
REQUIRED_SEMANTIC=(
    "identity","semantics","reachability","selection",
    "effect","consumer","recovery",
)

@dataclass(frozen=True)
class PreservationResult:
    capability_id:str
    disposition:str
    missing:tuple[str,...]
    present:tuple[str,...]

    @property
    def preserved(self)->bool:
        return self.disposition=="PRESERVED"

def _present(value:Any)->bool:
    if value is None:
        return False
    if isinstance(value,str):
        return bool(value.strip())
    if isinstance(value,(tuple,list,set,frozenset,dict)):
        return bool(value)
    return bool(value)

def evaluate_capability(
    capability_id:str,
    witness:Mapping[str,Any],
    *,
    operational:bool=True,
)->PreservationResult:
    required=REQUIRED_OPERATIONAL if operational else REQUIRED_SEMANTIC
    present=tuple(k for k in required if _present(witness.get(k)))
    missing=tuple(k for k in required if k not in present)
    if missing:
        return PreservationResult(capability_id,"OPEN",missing,present)
    return PreservationResult(capability_id,"PRESERVED",(),present)

def evaluate_manifest(manifest:Mapping[str,Mapping[str,Any]]):
    results=[]
    for capability_id,witness in manifest.items():
        operational=bool(witness.get("operational",True))
        results.append(evaluate_capability(capability_id,witness,operational=operational))
    return tuple(results)

def lost_capabilities(manifest:Mapping[str,Mapping[str,Any]])->tuple[str,...]:
    return tuple(
        r.capability_id for r in evaluate_manifest(manifest)
        if not r.preserved
    )
