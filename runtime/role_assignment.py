"""Obligation-based role assignment records."""
from dataclasses import dataclass

@dataclass(frozen=True)
class RoleAssignmentRecord:
    obligation:str
    origin:str
    semantic_owner:str
    authority_owner:str
    executor:str
    verifier:str
    state_consumers:tuple
    status:str
    evidence:tuple=()

def valid_role_assignment(r):
    return bool(r.obligation and r.origin and r.semantic_owner and r.authority_owner and r.executor and r.verifier and r.status)
