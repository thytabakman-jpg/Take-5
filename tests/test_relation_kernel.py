from relation_kernel import (
    CURRENT_GENERATOR_BASIS,
    RelationAdmission,
    RelationBasis,
    RelationCandidate,
    RelationEvidence,
    RelationStatus,
    RelationType,
    admit_relation,
    empty_fiber_status,
    higher_order_reduction_status,
)

def basis(*,complete=False):
    return RelationBasis(
        "B1",
        {
            "DEPENDS_ON":RelationType("DEPENDS_ON",2,("OBJECT","OBJECT"),True),
            "JOINT_EFFECT":RelationType("JOINT_EFFECT",3,("OBJECT","OBJECT","OBJECT"),False),
        },
        CURRENT_GENERATOR_BASIS,
        coverage_complete_for_claim=complete,
    )

def ev():
    return (RelationEvidence("e1","TEST","fixture"),)

def test_relation_requires_declared_vocabulary_and_grounds():
    c=RelationCandidate("UNKNOWN",("a","b"),("OBJECT","OBJECT"),ev())
    assert admit_relation(c,basis()).status==RelationStatus.OPEN
    c2=RelationCandidate("DEPENDS_ON",("a","b"),("OBJECT","OBJECT"),())
    assert admit_relation(c2,basis()).status==RelationStatus.OPEN

def test_direction_is_not_silently_symmetrized():
    a=RelationCandidate("DEPENDS_ON",("a","b"),("OBJECT","OBJECT"),ev())
    b=RelationCandidate("DEPENDS_ON",("b","a"),("OBJECT","OBJECT"),ev())
    assert admit_relation(a,basis()).status==RelationStatus.LICENSED
    assert admit_relation(b,basis()).status==RelationStatus.LICENSED
    assert a.arguments!=b.arguments

def test_wrong_arity_or_type_is_rejected():
    wrong_arity=RelationCandidate("DEPENDS_ON",("a",),("OBJECT",),ev())
    assert admit_relation(wrong_arity,basis()).status==RelationStatus.REJECTED
    wrong_type=RelationCandidate("DEPENDS_ON",("a","b"),("OBJECT","TOOL"),ev())
    assert admit_relation(wrong_type,basis()).status==RelationStatus.REJECTED

def test_no_relation_requires_coverage_complete_basis():
    assert empty_fiber_status([],basis(complete=False))==RelationStatus.OPEN
    assert empty_fiber_status([],basis(complete=True))==RelationStatus.NO_LICENSED_RELATION

def test_higher_order_relation_not_pairwise_reduced_without_rule():
    assert higher_order_reduction_status(
        higher_arity_relation_present=True,
        licensed_reconstruction_rule_present=False,
    )=="OPEN"
