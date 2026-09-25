"""Shared six-scope ontology and typed handoffs."""
from enum import Enum

class Scope(str,Enum):
    SYSTEM="SYSTEM"
    SUBSYSTEM="SUBSYSTEM"
    COMPONENT="COMPONENT"
    INTERFACE="INTERFACE"
    BOUNDARY_DECOMPOSITION="BOUNDARY_DECOMPOSITION"
    CROSS_LAYER="CROSS_LAYER"

class ScopeSpecies(str,Enum):
    CONTAINMENT="CONTAINMENT"
    RELATION="RELATION"
    TRANSPORT="TRANSPORT"

class Handoff(str,Enum):
    PROJECT="PROJECT"
    LIFT="LIFT"
    RELATE="RELATE"
    REDECOMPOSE="REDECOMPOSE"
    TRANSPORT="TRANSPORT"

def species(scope):
    if scope in {Scope.SYSTEM,Scope.SUBSYSTEM,Scope.COMPONENT}:
        return ScopeSpecies.CONTAINMENT
    if scope in {Scope.INTERFACE,Scope.BOUNDARY_DECOMPOSITION}:
        return ScopeSpecies.RELATION
    return ScopeSpecies.TRANSPORT

def required_handoff(source,target):
    if source==target:
        return None
    if target==Scope.BOUNDARY_DECOMPOSITION or source==Scope.BOUNDARY_DECOMPOSITION:
        return Handoff.REDECOMPOSE
    if source==Scope.CROSS_LAYER or target==Scope.CROSS_LAYER:
        return Handoff.TRANSPORT
    if target==Scope.INTERFACE or source==Scope.INTERFACE:
        return Handoff.RELATE
    containment=[Scope.SYSTEM,Scope.SUBSYSTEM,Scope.COMPONENT]
    return Handoff.PROJECT if containment.index(source)<containment.index(target) else Handoff.LIFT

def scope_projection_legal(preserves_identity,preserves_protected,preserves_provenance,preserves_open,external_dependencies_preserved):
    return all((preserves_identity,preserves_protected,preserves_provenance,preserves_open,external_dependencies_preserved))
