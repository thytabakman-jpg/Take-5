"""Capability Foundry: nonproduction capability-generation guard for Take-5."""
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Iterable

class CapabilityType(str, Enum):
    BEHAVIOR="BEHAVIOR"
    TOOL="TOOL"
    BOUNDARY="BOUNDARY"
    META_TOOL="META_TOOL"
    PROGRAM="PROGRAM"

class FoundryDisposition(str, Enum):
    ADMISSION_REQUEST="ADMISSION_REQUEST"
    SUBSUME="SUBSUME"
    OPEN="OPEN"
    REJECT="REJECT"

@dataclass(frozen=True)
class CapabilitySpec:
    capability_id: str
    capability_type: CapabilityType
    trigger: str
    input_contract: str
    transform: str
    output_contract: str
    success: str
    failure: str
    dependencies: tuple[str,...]=()
    persistence: str="EPHEMERAL"
    grants_authority: bool=False

    def executable_contract_complete(self)->bool:
        return all([
            self.trigger.strip(),
            self.input_contract.strip(),
            self.transform.strip(),
            self.output_contract.strip(),
            self.success.strip(),
            self.failure.strip(),
        ])

@dataclass(frozen=True)
class FoundryResult:
    candidate: CapabilitySpec
    disposition: FoundryDisposition
    reasons: tuple[str,...]

class CapabilityFoundry:
    """Generates typed candidates; it never admits or authorizes them."""

    def __init__(self, existing: Iterable[CapabilitySpec]=()):
        self.existing={c.capability_id:c for c in existing}

    def evaluate(
        self,
        candidate: CapabilitySpec,
        *,
        functionally_subsumed: Callable[[CapabilitySpec,CapabilitySpec],bool],
        material_goal_gain: Callable[[CapabilitySpec],bool],
        architecture_compatible: Callable[[CapabilitySpec],bool],
    )->FoundryResult:
        reasons=[]
        if candidate.grants_authority:
            return FoundryResult(candidate,FoundryDisposition.REJECT,("self_authorization_prohibited",))
        if not candidate.executable_contract_complete():
            return FoundryResult(candidate,FoundryDisposition.OPEN,("incomplete_execution_contract",))
        for old in self.existing.values():
            if functionally_subsumed(candidate,old):
                return FoundryResult(candidate,FoundryDisposition.SUBSUME,(f"subsumed_by:{old.capability_id}",))
        if not material_goal_gain(candidate):
            reasons.append("no_material_goal_gain")
        if not architecture_compatible(candidate):
            reasons.append("architecture_incompatible")
        if reasons:
            return FoundryResult(candidate,FoundryDisposition.OPEN,tuple(reasons))
        return FoundryResult(candidate,FoundryDisposition.ADMISSION_REQUEST,("candidate_ready_for_independent_admission",))
