"""Fail-closed user-visible mathematical status emission.

Formal-object identity is owned by runtime/formal_object_registry.py. This module
owns status assessment, typed rendering, and response-boundary enforcement.

Authoritative claims such as CURRENT/CANONICAL/EXACT_CURRENT mathematics have
one additional requirement: recovery alone is insufficient.  They must carry a
passing formal-claim admission receipt proving identity/version/currentness,
authority, dependency admission, and composition typing.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Any, Iterable, Mapping, Sequence

from formal_object_registry import (
    FORMAL_OBJECT_ALIASES,
    aliases_by_length,
    canonical_formal_label as _canonical_formal_label,
)
from prose import AFFIRMATIVE_FIRST, ProseContract, audit_affirmative_first


class MathStatus(str, Enum):
    RECOVERED = "RECOVERED"
    UNRESOLVED = "UNRESOLVED"


RECOVERED_COORDINATE_STATUSES = frozenset({"RECOVERED", "ADMITTED", "VERIFIED"})


@dataclass(frozen=True)
class RecoveryAssessment:
    object_id: str
    job: str
    claim: str
    required_coordinates: tuple[str, ...]
    unresolved_coordinates: tuple[str, ...]
    complete_for_use: bool
    status: MathStatus
    authoritative_claim: bool = False
    authority_residuals: tuple[str, ...] = ()


def _formal_claim_green(receipt: Any) -> bool:
    return bool(receipt is not None and getattr(receipt, "green_licensed", False))


def _formal_claim_residuals(receipt: Any) -> tuple[str, ...]:
    if receipt is None:
        return ("FORMAL_CLAIM_RECEIPT_REQUIRED",)
    residuals = tuple(str(x) for x in getattr(receipt, "residuals", ()) if str(x))
    if residuals:
        return residuals
    status = str(getattr(receipt, "status", "") or "OPEN")
    return (f"FORMAL_CLAIM_NOT_ADMITTED:{status}",)


def assess_recovery(
    *,
    object_id: str,
    job: str,
    claim: str,
    required_coordinates: Sequence[str],
    coordinate_status: Mapping[str, str],
    authoritative_claim: bool = False,
    formal_claim_receipt: Any | None = None,
) -> RecoveryAssessment:
    required = tuple(required_coordinates)
    unresolved: list[str] = []
    authority_residuals: tuple[str, ...] = ()

    if not required:
        unresolved.append("REQUIRED_COORDINATES_UNSPECIFIED")
    for coordinate in required:
        if coordinate_status.get(coordinate, "MISSING") not in RECOVERED_COORDINATE_STATUSES:
            unresolved.append(coordinate)

    if authoritative_claim and not _formal_claim_green(formal_claim_receipt):
        authority_residuals = _formal_claim_residuals(formal_claim_receipt)
        unresolved.extend(
            f"AUTHORITY:{residual}" for residual in authority_residuals
        )

    complete_for_use = bool(required) and not unresolved
    status = MathStatus.RECOVERED if complete_for_use else MathStatus.UNRESOLVED
    return RecoveryAssessment(
        object_id=object_id,
        job=job,
        claim=claim,
        required_coordinates=required,
        unresolved_coordinates=tuple(unresolved),
        complete_for_use=complete_for_use,
        status=status,
        authoritative_claim=authoritative_claim,
        authority_residuals=authority_residuals,
    )


def assess_authoritative_recovery(
    *,
    object_id: str,
    job: str,
    claim: str,
    required_coordinates: Sequence[str],
    coordinate_status: Mapping[str, str],
    formal_claim_receipt: Any | None,
) -> RecoveryAssessment:
    """Assess a current/canonical/exact-current mathematical claim.

    This helper prevents callers from accidentally forgetting the authority gate
    when the claim itself is authoritative.
    """
    return assess_recovery(
        object_id=object_id,
        job=job,
        claim=claim,
        required_coordinates=required_coordinates,
        coordinate_status=coordinate_status,
        authoritative_claim=True,
        formal_claim_receipt=formal_claim_receipt,
    )


@dataclass(frozen=True)
class TextFragment:
    text: str


@dataclass(frozen=True)
class MathFragment:
    latex: str
    status: MathStatus


@dataclass(frozen=True)
class AssessedMathFragment:
    latex: str
    assessment: RecoveryAssessment

    @property
    def status(self) -> MathStatus:
        return self.assessment.status


Fragment = TextFragment | MathFragment | AssessedMathFragment


class ColorInvariantViolation(RuntimeError):
    pass


def _formal_pattern() -> re.Pattern:
    aliases=aliases_by_length()
    encoded="|".join(re.escape(x) for x in aliases)
    return re.compile(
        rf"(?<![A-Za-z0-9_])(?:{encoded}|ICC(?:[- _]?\d+)?)(?![A-Za-z0-9_])",
        re.IGNORECASE,
    )


FORMAL_OBJECT_PATTERN = _formal_pattern()
FORBIDDEN_RAW_MARKUP = ("<span", "</span>", "style=", "color:")
FORBIDDEN_FALLBACK_MARKERS = ("🟢", "🔴")
AUTHORITATIVE_TEXT_MARKERS = (
    "current",
    "canonical",
    "exact",
    "latest",
    "new math",
    "actual math",
)
MATH_SIGNAL_PATTERN = re.compile(
    r"(\\(?:color|boxed|Gamma|varphi|vdash|nvdash|neq|Rightarrow|implies|iff|land|lor|mu|operatorname)"
    r"|\$|[=≠→⇒⇔∧∨⊢⊬∈∉∀∃μΓφ])"
)
COLORED_FORMAL_LABEL_PATTERN = re.compile(
    r"\\color\{(?:green|red)\}\{\\operatorname\{[^{}]*(?:\{[-]\}[^{}]*)*\}\}",
    re.IGNORECASE,
)


def canonical_formal_label(label: str) -> str:
    try:
        return _canonical_formal_label(label)
    except KeyError as exc:
        raise ColorInvariantViolation("FORMAL_LABEL_NOT_REGISTERED") from exc


def render_math(fragment: MathFragment | AssessedMathFragment) -> str:
    latex = fragment.latex.strip()
    if not latex:
        raise ColorInvariantViolation("EMPTY_MATH_FRAGMENT")
    if not isinstance(fragment.status, MathStatus):
        raise ColorInvariantViolation("MATH_STATUS_REQUIRED")
    color = "green" if fragment.status is MathStatus.RECOVERED else "red"
    return rf"\color{{{color}}}{{{latex}}}"


def render_formal_label(label: str, status: MathStatus) -> str:
    canonical = canonical_formal_label(label)
    if not isinstance(status, MathStatus):
        raise ColorInvariantViolation("MATH_STATUS_REQUIRED")
    latex_label = canonical.replace("_", r"\_").replace("-", r"{-}")
    return render_math(MathFragment(rf"\operatorname{{{latex_label}}}", status))


def _raw_text_contains_load_bearing_math(text: str) -> bool:
    return bool(FORMAL_OBJECT_PATTERN.search(text) or MATH_SIGNAL_PATTERN.search(text))


def verify_fragments(fragments: Sequence[Fragment]) -> None:
    for fragment in fragments:
        if isinstance(fragment, (MathFragment, AssessedMathFragment)):
            if not isinstance(fragment.status, MathStatus):
                raise ColorInvariantViolation("MATH_STATUS_REQUIRED")
            if not fragment.latex.strip():
                raise ColorInvariantViolation("EMPTY_MATH_FRAGMENT")
            if (
                isinstance(fragment, AssessedMathFragment)
                and fragment.assessment.authoritative_claim
                and fragment.status is MathStatus.RECOVERED
                and fragment.assessment.authority_residuals
            ):
                raise ColorInvariantViolation(
                    "AUTHORITATIVE_GREEN_WITH_UNCLOSED_AUTHORITY"
                )
            continue
        if isinstance(fragment, TextFragment):
            lowered = fragment.text.lower()
            if any(marker in lowered for marker in FORBIDDEN_RAW_MARKUP):
                raise ColorInvariantViolation("RAW_COLOR_MARKUP_FORBIDDEN")
            if any(marker in fragment.text for marker in FORBIDDEN_FALLBACK_MARKERS):
                raise ColorInvariantViolation("STATUS_FALLBACK_FORBIDDEN")
            if _raw_text_contains_load_bearing_math(fragment.text):
                raise ColorInvariantViolation("UNTYPED_LOAD_BEARING_MATH")
            continue
        raise ColorInvariantViolation("UNTYPED_FRAGMENT")


def verify_rendered_output(rendered: str) -> None:
    if any(marker in rendered.lower() for marker in FORBIDDEN_RAW_MARKUP):
        raise ColorInvariantViolation("RAW_COLOR_MARKUP_FORBIDDEN")
    if any(marker in rendered for marker in FORBIDDEN_FALLBACK_MARKERS):
        raise ColorInvariantViolation("STATUS_FALLBACK_FORBIDDEN")


def verify_assistant_response(
    rendered: str,
    *,
    prose_contract: ProseContract | None = None,
) -> None:
    """Reject untyped formal identity and negative-first prose at final emission."""
    verify_rendered_output(rendered)
    masked = COLORED_FORMAL_LABEL_PATTERN.sub("", rendered)
    if FORMAL_OBJECT_PATTERN.search(masked):
        raise ColorInvariantViolation("UNTYPED_FORMAL_LABEL_AT_RESPONSE_BOUNDARY")

    contract = prose_contract or ProseContract(
        "assistant-response-boundary",
        constraints=(AFFIRMATIVE_FIRST,),
    )
    violations = audit_affirmative_first(rendered, contract)
    if violations:
        first = violations[0]
        raise ColorInvariantViolation(
            f"NEGATIVE_FIRST_PROSE_AT_RESPONSE_BOUNDARY:{first.code}:{first.excerpt}"
        )


def _infer_authoritative_emission(parts: Sequence[Fragment]) -> bool:
    text=" ".join(
        fragment.text.lower()
        for fragment in parts
        if isinstance(fragment,TextFragment)
    )
    return any(marker in text for marker in AUTHORITATIVE_TEXT_MARKERS)


def emit_user_visible(
    fragments: Iterable[Fragment],
    *,
    authoritative_claim: bool | None = None,
    formal_claim_receipt: Any | None = None,
    prose_contract: ProseContract | None = None,
) -> str:
    parts = tuple(fragments)
    verify_fragments(parts)

    authoritative=(
        _infer_authoritative_emission(parts)
        if authoritative_claim is None
        else bool(authoritative_claim)
    )
    has_green=any(
        isinstance(fragment,(MathFragment,AssessedMathFragment))
        and fragment.status is MathStatus.RECOVERED
        for fragment in parts
    )
    if authoritative and has_green and not _formal_claim_green(formal_claim_receipt):
        raise ColorInvariantViolation(
            "AUTHORITATIVE_FORMAL_CLAIM_RECEIPT_REQUIRED"
        )

    rendered: list[str] = []
    for fragment in parts:
        if isinstance(fragment, (MathFragment, AssessedMathFragment)):
            rendered.append(render_math(fragment))
        else:
            rendered.append(fragment.text)
    out = "".join(rendered)
    verify_assistant_response(out, prose_contract=prose_contract)
    return out
