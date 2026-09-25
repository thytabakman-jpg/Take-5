from scope_ontology import Scope,ScopeSpecies,Handoff,species,required_handoff

def test_six_scopes_factor_three_two_one():
    assert sum(species(s)==ScopeSpecies.CONTAINMENT for s in Scope)==3
    assert sum(species(s)==ScopeSpecies.RELATION for s in Scope)==2
    assert sum(species(s)==ScopeSpecies.TRANSPORT for s in Scope)==1

def test_boundary_is_redecomposition_not_zoom():
    assert required_handoff(Scope.COMPONENT,Scope.BOUNDARY_DECOMPOSITION)==Handoff.REDECOMPOSE

def test_cross_layer_is_transport():
    assert required_handoff(Scope.SYSTEM,Scope.CROSS_LAYER)==Handoff.TRANSPORT

def test_upward_containment_is_lift_not_projection():
    assert required_handoff(Scope.COMPONENT,Scope.SYSTEM)==Handoff.LIFT

def test_downward_containment_is_projection():
    assert required_handoff(Scope.SYSTEM,Scope.COMPONENT)==Handoff.PROJECT
