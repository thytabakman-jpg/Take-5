from coordinate_registry import *

def test_equal_six_cardinality_does_not_make_same_coordinate():
    assert same_cardinality_is_not_equivalence(SCOPE,IOOC)
    assert same_cardinality_is_not_equivalence(MODE_FACE,TRANSITION_KIND)

def test_mode_faces_not_independent_product_factor():
    assert not product_factor_admissible(MODE_FACE)

def test_scope_is_admitted_coordinate():
    assert product_factor_admissible(SCOPE)
    assert SCOPE.canonical

def test_iooc_is_material_rival_not_yet_canonical():
    assert product_factor_admissible(IOOC)
    assert not IOOC.canonical

def test_bridge_basis_not_promoted_while_reducibility_open():
    assert not product_factor_admissible(BRIDGE_KIND)
