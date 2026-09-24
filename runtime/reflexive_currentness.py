"""Reflexive currentness: audit the governing architecture basis before component currentness."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ArchitectureBasis:
    basis_id:str
    system_identity:str
    controller_role:str
    closure_law:str
    state_model:str

def basis_delta(built,latest):
    fields=("system_identity","controller_role","closure_law","state_model")
    return tuple(f for f in fields if getattr(built,f)!=getattr(latest,f))

def component_audit_allowed(built,latest):
    return not basis_delta(built,latest)

def current_basis():
    return ArchitectureBasis(
        "EWG-ARCH-001",
        "ENDOGENOUS_WORK_GENERATING_RESEARCH_SYSTEM",
        "IMPROVEMENT_CORE_IS_POLICY_CONTROLLER_INSIDE_WORK_LIFECYCLE",
        "CLOSED_IFF_NO_FRESH_WORK_AND_NO_OPEN_AND_HISTORY_CERTIFIED",
        "CONVERSATION_INTERFACE_NE_RESEARCH_PROCESS_NE_RESEARCH_STATE",
    )
