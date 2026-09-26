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
    semantic_object_id: str=""
    mathematical_basis: str=""
    math_required_coordinates: tuple[str,...]=()
    math_recovered_coordinates: tuple[str,...]=()

    def math_complete_for_use(self)->bool:
        required=set(self.math_required_coordinates)
        recovered=set(self.math_recovered_coordinates)
        return bool(self.mathematical_basis.strip()) and bool(required) and required <= recovered

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
        package_verifier: Callable[[str],bool] | None = None,
    )->FoundryResult:
        reasons=[]
        if candidate.grants_authority:
            return FoundryResult(candidate,FoundryDisposition.REJECT,("self_authorization_prohibited",))
        if not candidate.executable_contract_complete():
            return FoundryResult(candidate,FoundryDisposition.OPEN,("incomplete_execution_contract",))
        if candidate.capability_type in {CapabilityType.TOOL, CapabilityType.META_TOOL, CapabilityType.PROGRAM}:
            missing=[]
            if not candidate.semantic_object_id.strip():
                missing.append("semantic_object_id_missing")
            if not candidate.mathematical_basis.strip():
                missing.append("mathematical_basis_missing")
            if not candidate.math_required_coordinates:
                missing.append("required_math_coordinates_unspecified")
            elif not candidate.math_complete_for_use():
                missing.append("required_mathematics_unrecovered")
            package_ok = bool(package_verifier(candidate.semantic_object_id)) if package_verifier is not None else False
            if not package_ok:
                missing.append("semantic_package_missing_or_stale")
            if missing:
                return FoundryResult(candidate,FoundryDisposition.OPEN,tuple(missing))
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
