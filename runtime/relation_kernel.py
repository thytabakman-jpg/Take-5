"""Basis-relative typed relation generation and admission.

This module closes the current ImprovementCore relation-basis ambiguity without
claiming open-world completeness.

A relation result is always relative to a declared RelationBasis. Unknown
vocabulary, insufficient evidence, or incomplete search remains OPEN. Empty
fibers become NO_LICENSED_RELATION only when the declared generator/evidence
basis is coverage-complete for the claim being made.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping


class RelationStatus(str, Enum):
    LICENSED="LICENSED"
    OPEN="OPEN"
    REJECTED="REJECTED"
    NO_LICENSED_RELATION="NO_LICENSED_RELATION"


@dataclass(frozen=True)
class RelationType:
    relation_id:str
    arity:int
    argument_types:tuple[str,...]=()
    directional:bool=True

    def valid(self)->bool:
        return bool(self.relation_id) and self.arity>=1 and (
            not self.argument_types or len(self.argument_types)==self.arity
        )


@dataclass(frozen=True)
class RelationEvidence:
    evidence_id:str
    grounds_type:str
    provenance:str


@dataclass(frozen=True)
class RelationCandidate:
    relation_id:str
    arguments:tuple[str,...]
    argument_types:tuple[str,...]
    evidence:tuple[RelationEvidence,...]=()
    admitted_tuple:bool=True


@dataclass(frozen=True)
class RelationBasis:
    basis_id:str
    vocabulary:Mapping[str,RelationType]
    generator_ids:tuple[str,...]
    coverage_complete_for_claim:bool=False

    def complete(self)->bool:
        return (
            bool(self.basis_id)
            and bool(self.vocabulary)
            and bool(self.generator_ids)
            and all(x.valid() for x in self.vocabulary.values())
        )


@dataclass(frozen=True)
class RelationAdmission:
    status:RelationStatus
    reason:str


CURRENT_GENERATOR_BASIS=(
    "DIRECT_TYPED",
    "DEPENDENCY",
    "PROVENANCE",
    "AUTHORITY",
    "COMPOSITION_RESIDUAL",
    "CROSS_LAYER",
    "EXTERNAL_COMPARATOR",
)

CURRENT_RELATION_VOCABULARY={
    "REFERENCES":RelationType("REFERENCES",2,("OBJECT","OBJECT"),True),
    "DEPENDS_ON":RelationType("DEPENDS_ON",2,("OBJECT","OBJECT"),True),
    "DERIVES_FROM":RelationType("DERIVES_FROM",2,("OBJECT","OBJECT"),True),
    "AUTHORIZES":RelationType("AUTHORIZES",2,("OBJECT","OBJECT"),True),
    "PART_OF":RelationType("PART_OF",2,("OBJECT","OBJECT"),True),
    "PRECEDES":RelationType("PRECEDES",2,("OBJECT","OBJECT"),True),
    "CONFLICTS_WITH":RelationType("CONFLICTS_WITH",2,("OBJECT","OBJECT"),False),
    "EQUIVALENT_TO":RelationType("EQUIVALENT_TO",2,("OBJECT","OBJECT"),False),
    "JOINT_EFFECT":RelationType("JOINT_EFFECT",3,("OBJECT","OBJECT","OBJECT"),False),
}


def current_relation_basis(*,coverage_complete_for_claim=False)->RelationBasis:
    return RelationBasis(
        "TAKE5_RELATION_BASIS_001",
        CURRENT_RELATION_VOCABULARY,
        CURRENT_GENERATOR_BASIS,
        coverage_complete_for_claim=coverage_complete_for_claim,
    )


def admit_relation(candidate:RelationCandidate,basis:RelationBasis)->RelationAdmission:
    if not basis.complete():
        return RelationAdmission(RelationStatus.OPEN,"RELATION_BASIS_INCOMPLETE")

    spec=basis.vocabulary.get(candidate.relation_id)
    if spec is None:
        return RelationAdmission(RelationStatus.OPEN,"RELATION_VOCABULARY_OPEN")

    if len(candidate.arguments)!=spec.arity:
        return RelationAdmission(RelationStatus.REJECTED,"ARITY_MISMATCH")

    if candidate.argument_types and len(candidate.argument_types)!=spec.arity:
        return RelationAdmission(RelationStatus.REJECTED,"ARGUMENT_TYPE_ARITY_MISMATCH")

    if spec.argument_types and candidate.argument_types:
        if tuple(candidate.argument_types)!=tuple(spec.argument_types):
            return RelationAdmission(RelationStatus.REJECTED,"ARGUMENT_TYPE_MISMATCH")

    if not candidate.admitted_tuple:
        return RelationAdmission(RelationStatus.REJECTED,"TUPLE_NOT_ADMITTED")

    if not candidate.evidence:
        return RelationAdmission(RelationStatus.OPEN,"GROUNDS_OPEN")

    if any(not e.evidence_id or not e.provenance for e in candidate.evidence):
        return RelationAdmission(RelationStatus.OPEN,"EVIDENCE_PROVENANCE_OPEN")

    return RelationAdmission(RelationStatus.LICENSED,"LICENSED_UNDER_DECLARED_BASIS")


def relation_candidates_from_records(records)->tuple[RelationCandidate,...]:
    """Extract the currently implemented direct REFERENCES relation family.

    The broader generator basis is declared above; generators not implemented on
    this input representation remain distinct future generator implementations.
    """
    rows=tuple(records)
    known={
        str(r.get("id"))
        for r in rows
        if isinstance(r,dict) and r.get("id") is not None
    }
    out=[]
    for i,r in enumerate(rows):
        if not isinstance(r,dict):
            continue
        source=str(r.get("id",i))
        for j,ref in enumerate(r.get("refs",())):
            target=str(ref)
            evidence=RelationEvidence(
                f"{source}:ref:{j}",
                "DECLARED_REFERENCE",
                f"corpus-record:{source}",
            )
            out.append(
                RelationCandidate(
                    "REFERENCES",
                    (source,target),
                    ("OBJECT","OBJECT"),
                    (evidence,),
                    admitted_tuple=(source in known and target in known),
                )
            )
    return tuple(out)


def licensed_ledger(candidates:Iterable[RelationCandidate],basis:RelationBasis):
    licensed=[]
    unresolved=[]
    rejected=[]
    for c in candidates:
        a=admit_relation(c,basis)
        row=(c,a)
        if a.status==RelationStatus.LICENSED:
            licensed.append(row)
        elif a.status==RelationStatus.REJECTED:
            rejected.append(row)
        else:
            unresolved.append(row)
    return tuple(licensed),tuple(unresolved),tuple(rejected)


def empty_fiber_status(candidates:Iterable[RelationCandidate],basis:RelationBasis)->RelationStatus:
    licensed,unresolved,_=licensed_ledger(candidates,basis)
    if licensed:
        return RelationStatus.LICENSED
    if unresolved:
        return RelationStatus.OPEN
    if basis.coverage_complete_for_claim:
        return RelationStatus.NO_LICENSED_RELATION
    return RelationStatus.OPEN


def higher_order_reduction_status(
    *,
    higher_arity_relation_present:bool,
    licensed_reconstruction_rule_present:bool,
)->str:
    """Do not infer pairwise reducibility without a licensed local-to-global rule."""
    if not higher_arity_relation_present:
        return "NOT_APPLICABLE"
    if not licensed_reconstruction_rule_present:
        return "OPEN"
    return "RECONSTRUCTION_TEST_REQUIRED"
