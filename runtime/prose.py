"""PROSE — protected reader-facing prose acceptance.

PROSE owns a narrow job: determine whether a concrete prose realization satisfies
an explicit frozen prose contract while preserving separately evidenced semantic
commitments, earned claim strength, and no-inflation boundaries.

It does not decide factual truth and does not silently rewrite failed prose.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


AFFIRMATIVE_FIRST="AFFIRMATIVE_FIRST"
FIRST_MENTION_PERSON_DATES="FIRST_MENTION_PERSON_DATES"
NUMERIC_YEAR_DATES_ONLY="NUMERIC_YEAR_DATES_ONLY"
ORDERED_ANCHORS="ORDERED_ANCHORS"
READER_LOAD="READER_LOAD"
SUPPORTED_CONSTRAINTS=frozenset({
    AFFIRMATIVE_FIRST,
    FIRST_MENTION_PERSON_DATES,
    NUMERIC_YEAR_DATES_ONLY,
    ORDERED_ANCHORS,
    READER_LOAD,
})


@dataclass(frozen=True)
class ProseContract:
    contract_id:str
    constraints:tuple[str,...]=(AFFIRMATIVE_FIRST,NUMERIC_YEAR_DATES_ONLY)
    allowed_negative_spans:tuple[str,...]=()
    person_dates:tuple[tuple[str,str],...]=()
    ordered_anchors:tuple[str,...]=()


@dataclass(frozen=True)
class ProseEvidence:
    semantic_preservation:str="OPEN"
    earned_claim_strength:str="OPEN"
    no_unsupported_inflation:str="OPEN"
    evidence:tuple[str,...]=()
    reader_load:str="OPEN"
    reader_load_evidence:tuple[str,...]=()


@dataclass(frozen=True)
class ProseViolation:
    constraint_id:str
    code:str
    start:int
    end:int
    excerpt:str


@dataclass(frozen=True)
class ProseAssessment:
    status:str
    contract_id:str
    violations:tuple[ProseViolation,...]
    unsupported_constraints:tuple[str,...]
    residuals:tuple[str,...]
    evidence:tuple[str,...]


class ProseAcceptanceError(RuntimeError):
    pass


_NEGATIVE_FIRST_PATTERNS=(
    (
        "NOT_MERELY",
        re.compile(
            r"\b(?:does|do|did|is|are|was|were|has|have|had|can|could|would|will)?"
            r"\s*not\s+merely\b[^.!?\n]{0,220}",
            re.IGNORECASE,
        ),
    ),
    (
        "NOT_BUT",
        re.compile(
            r"\b(?:does|do|did|is|are|was|were|has|have|had|can|could|would|will)"
            r"\s+not\b[^.!?\n]{0,220}\bbut\b[^.!?\n]{0,220}",
            re.IGNORECASE,
        ),
    ),
    (
        "NOT_RATHER",
        re.compile(
            r"\bnot\b[^.!?\n]{0,220}\brather\b[^.!?\n]{0,220}",
            re.IGNORECASE,
        ),
    ),
    (
        "NEGATIVE_THEN_POSITIVE_SENTENCE",
        re.compile(
            r"\b(?:does|do|did|is|are|was|were|has|have|had|can|could|would|will)"
            r"\s+not\b[^.!?\n]{0,220}[.!?]\s+"
            r"(?:It|This|That|They|He|She|The\s+[A-Z][A-Za-z-]*)\b",
            re.IGNORECASE,
        ),
    ),
)

_CENTURY_LABEL_PATTERNS=(
    (
        "NUMERIC_CENTURY_LABEL",
        re.compile(
            r"\b(?:[1-9]|1\d|20|21)(?:st|nd|rd|th)\s*[- ]?\s*centur(?:y|ies)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "WORD_CENTURY_LABEL",
        re.compile(
            r"\b(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|"
            r"tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|"
            r"seventeenth|eighteenth|nineteenth|twentieth|twenty[- ]first)"
            r"\s*[- ]?\s*centur(?:y|ies)\b",
            re.IGNORECASE,
        ),
    ),
)

_YEAR_TOKEN=re.compile(r"(?<!\d)\d{1,4}(?!\d)")


def audit_numeric_year_dates(text:str)->tuple[ProseViolation,...]:
    value=str(text or "")
    violations=[]
    for code,pattern in _CENTURY_LABEL_PATTERNS:
        for match in pattern.finditer(value):
            violations.append(ProseViolation(
                constraint_id=NUMERIC_YEAR_DATES_ONLY,
                code=code,
                start=match.start(),
                end=match.end(),
                excerpt=match.group(0),
            ))
    return tuple(sorted(violations,key=lambda x:(x.start,x.end,x.code)))


def _valid_numeric_person_date(date:str)->bool:
    value=str(date or "").strip()
    if not value:
        return False
    if audit_numeric_year_dates(value):
        return False
    return bool(_YEAR_TOKEN.search(value))



def _allowed(text:str, start:int, end:int, contract:ProseContract)->bool:
    lowered=str(text).casefold()
    for raw in contract.allowed_negative_spans:
        span=str(raw).strip().casefold()
        if not span:
            continue
        offset=0
        while True:
            idx=lowered.find(span,offset)
            if idx<0:
                break
            span_end=idx+len(span)
            if idx<=end and span_end>=start:
                return True
            offset=idx+1
    return False


def audit_affirmative_first(text:str, contract:ProseContract)->tuple[ProseViolation,...]:
    value=str(text or "")
    violations=[]
    seen=set()
    for code,pattern in _NEGATIVE_FIRST_PATTERNS:
        for match in pattern.finditer(value):
            excerpt=match.group(0).strip()
            if not excerpt or _allowed(value,match.start(),match.end(),contract):
                continue
            key=(match.start(),match.end(),code)
            if key in seen:
                continue
            seen.add(key)
            violations.append(ProseViolation(
                constraint_id=AFFIRMATIVE_FIRST,
                code=code,
                start=match.start(),
                end=match.end(),
                excerpt=excerpt,
            ))
    return tuple(sorted(violations,key=lambda x:(x.start,x.end,x.code)))


def audit_first_mention_person_dates(text:str, contract:ProseContract):
    value=str(text or "")
    violations=[]
    residuals=[]
    for raw_name,raw_date in contract.person_dates:
        name=str(raw_name).strip()
        date=str(raw_date).strip()
        if not name:
            continue
        match=re.search(r"(?<!\w)"+re.escape(name)+r"(?!\w)",value)
        if match is None:
            continue
        if not date:
            residuals.append(f"PERSON_DATE_UNRESOLVED:{name}")
            continue
        if not _valid_numeric_person_date(date):
            code=(
                "PERSON_DATE_CENTURY_LABEL_FORBIDDEN"
                if audit_numeric_year_dates(date)
                else "PERSON_DATE_NUMERIC_YEAR_REQUIRED"
            )
            violations.append(ProseViolation(
                constraint_id=NUMERIC_YEAR_DATES_ONLY,
                code=code,
                start=match.start(),
                end=match.end(),
                excerpt=f"{name} ({date})",
            ))
            continue
        expected=f" ({date})"
        if value[match.end():match.end()+len(expected)]!=expected:
            violations.append(ProseViolation(
                constraint_id=FIRST_MENTION_PERSON_DATES,
                code="FIRST_MENTION_DATE_MISSING",
                start=match.start(),
                end=match.end(),
                excerpt=match.group(0),
            ))
    return tuple(violations),tuple(residuals)


def audit_ordered_anchors(text:str, contract:ProseContract)->tuple[ProseViolation,...]:
    """Require supplied exact anchors to occur in the declared order."""
    value=str(text or "")
    anchors=tuple(str(x) for x in contract.ordered_anchors if str(x))
    violations=[]
    cursor=0
    for anchor in anchors:
        pos=value.find(anchor,cursor)
        if pos>=0:
            cursor=pos+len(anchor)
            continue
        anywhere=value.find(anchor)
        violations.append(ProseViolation(
            constraint_id=ORDERED_ANCHORS,
            code=("ORDERED_ANCHOR_OUT_OF_ORDER" if anywhere>=0 else "ORDERED_ANCHOR_MISSING"),
            start=max(anywhere,0),
            end=(anywhere+len(anchor) if anywhere>=0 else 0),
            excerpt=anchor,
        ))
    return tuple(violations)


def assess_prose(
    text:str,
    contract:ProseContract,
    evidence:ProseEvidence|None=None,
)->ProseAssessment:
    requested=tuple(dict.fromkeys(str(x) for x in contract.constraints if str(x)))
    unsupported=tuple(sorted(set(requested)-SUPPORTED_CONSTRAINTS))

    violations=()
    residuals=()
    if AFFIRMATIVE_FIRST in requested:
        violations=violations+audit_affirmative_first(text,contract)
    if NUMERIC_YEAR_DATES_ONLY in requested:
        violations=violations+audit_numeric_year_dates(text)
    if FIRST_MENTION_PERSON_DATES in requested:
        date_violations,date_residuals=audit_first_mention_person_dates(text,contract)
        violations=violations+date_violations
        residuals=residuals+date_residuals
    if ORDERED_ANCHORS in requested:
        if not tuple(str(x) for x in contract.ordered_anchors if str(x)):
            residuals=residuals+("ORDERED_ANCHORS_REQUIRED",)
        else:
            violations=violations+audit_ordered_anchors(text,contract)

    if unsupported:
        return ProseAssessment(
            "OPEN",contract.contract_id,violations,unsupported,
            residuals+tuple(f"UNSUPPORTED_CONSTRAINT:{x}" for x in unsupported),(),
        )

    reader_load_evidence=()
    if READER_LOAD in requested:
        if evidence is None:
            residuals=residuals+("READER_LOAD_RECEIPT_REQUIRED",)
        else:
            reader_load_status=str(evidence.reader_load or "OPEN").upper()
            reader_load_evidence=tuple(
                str(x) for x in evidence.reader_load_evidence if str(x)
            )
            if reader_load_status=="BLOCKED":
                return ProseAssessment(
                    "BLOCKED",contract.contract_id,violations,(),
                    residuals+("READER_LOAD:BLOCKED",),
                    tuple(evidence.evidence)+reader_load_evidence,
                )
            if reader_load_status in {"FAIL","REPAIR_REQUIRED"}:
                violations=violations+(ProseViolation(
                    constraint_id=READER_LOAD,
                    code="READER_LOAD_REPAIR_REQUIRED",
                    start=0,
                    end=min(len(str(text or "")),220),
                    excerpt=(
                        "; ".join(reader_load_evidence)
                        or str(text or "")[:220]
                    ),
                ),)
            elif reader_load_status!="PASS":
                residuals=residuals+(f"READER_LOAD:{reader_load_status}",)
            elif not reader_load_evidence:
                residuals=residuals+("READER_LOAD_EVIDENCE_REQUIRED",)

    if violations:
        return ProseAssessment(
            "REPAIR_REQUIRED",contract.contract_id,violations,(),
            residuals+("PROTECTED_PROSE_CONSTRAINT_VIOLATED",),
            tuple(evidence.evidence)+reader_load_evidence if evidence is not None else (),
        )

    if residuals:
        return ProseAssessment(
            "OPEN",contract.contract_id,(),(),residuals,
            tuple(evidence.evidence)+reader_load_evidence if evidence is not None else (),
        )

    if evidence is None:
        return ProseAssessment(
            "OPEN",contract.contract_id,(),(),(
                "SEMANTIC_PRESERVATION_RECEIPT_REQUIRED",
                "EARNED_CLAIM_STRENGTH_RECEIPT_REQUIRED",
                "NO_UNSUPPORTED_INFLATION_RECEIPT_REQUIRED",
            ),(),
        )

    statuses={
        "semantic_preservation":str(evidence.semantic_preservation).upper(),
        "earned_claim_strength":str(evidence.earned_claim_strength).upper(),
        "no_unsupported_inflation":str(evidence.no_unsupported_inflation).upper(),
    }
    if "BLOCKED" in statuses.values():
        return ProseAssessment(
            "BLOCKED",contract.contract_id,(),(),tuple(
                f"{k.upper()}:{v}" for k,v in statuses.items() if v!="PASS"
            ),tuple(evidence.evidence),
        )
    residuals=tuple(
        f"{k.upper()}:{v}" for k,v in statuses.items() if v!="PASS"
    )
    if residuals or not evidence.evidence:
        if not evidence.evidence:
            residuals=residuals+("PROSE_EVIDENCE_REQUIRED",)
        return ProseAssessment(
            "OPEN",contract.contract_id,(),(),residuals,tuple(evidence.evidence),
        )

    return ProseAssessment(
        "PASS",contract.contract_id,(),(),(),tuple(evidence.evidence),
    )


def require_prose_admissible(
    text:str,
    contract:ProseContract,
    evidence:ProseEvidence,
)->ProseAssessment:
    assessment=assess_prose(text,contract,evidence)
    if assessment.status!="PASS":
        codes=",".join(v.code for v in assessment.violations)
        residual=",".join(assessment.residuals)
        raise ProseAcceptanceError(
            f"PROSE_NOT_ADMISSIBLE:{contract.contract_id}:{assessment.status}:"
            f"violations={codes}:residuals={residual}"
        )
    return assessment


def receipt_dict(assessment:ProseAssessment)->dict:
    return {
        "tool":"Prose",
        "contract_id":assessment.contract_id,
        "status":assessment.status,
        "violations":tuple(v.code for v in assessment.violations),
        "residuals":assessment.residuals,
        "evidence":assessment.evidence,
    }
