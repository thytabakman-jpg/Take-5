"""Fail-closed user-visible mathematical status emission.

Formal-system objects are registered centrally and rendered as typed LaTeX
fragments carrying a binary recovery state. A response-boundary audit can then
reject registered formal labels that escape as plain text.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Iterable, Mapping, Sequence


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


def assess_recovery(
    *,
    object_id: str,
    job: str,
    claim: str,
    required_coordinates: Sequence[str],
    coordinate_status: Mapping[str, str],
) -> RecoveryAssessment:
    required = tuple(required_coordinates)
    unresolved: list[str] = []

    if not required:
        unresolved.append("REQUIRED_COORDINATES_UNSPECIFIED")

    for coordinate in required:
        if coordinate_status.get(coordinate, "MISSING") not in RECOVERED_COORDINATE_STATUSES:
            unresolved.append(coordinate)

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


# One canonical registry for user-visible formal labels.
# Aliases normalize to one mathematical object identity.
FORMAL_OBJECT_ALIASES = {
    "ASSERT":"ASSERT",
    "COMPARE":"COMPARE",
    "RESOLVE":"RESOLVE",
    "HERE":"HERE",
    "INQUIRE":"INQUIRE",
    "REASSERT":"REASSERT",
    "ROOT CAUSE":"ROOT_CAUSE",
    "ROOT-CAUSE":"ROOT_CAUSE",
    "ROOT_CAUSE":"ROOT_CAUSE",
    "GOAL":"GOAL",
    "ARCHITECT":"ARCHITECT",
    "WRAPPER":"WRAPPER",
    "JANE":"JANE",
    "MT":"MT",
    "PD":"PD",
    "IMPROVECORE":"IMPROVECORE",
    "IMPROVE CORE":"IMPROVECORE",
    "IMPROVEMENTCORE":"IMPROVECORE",
    "IMPROVEMENT CORE":"IMPROVECORE",
    "HF1":"HF1",
    "HF-1":"HF1",
    "HF001":"HF1",
    "HF-001":"HF1",
}

_STATIC_ALIASES = sorted(FORMAL_OBJECT_ALIASES, key=len, reverse=True)
_STATIC_PATTERN = "|".join(re.escape(x) for x in _STATIC_ALIASES)
FORMAL_OBJECT_PATTERN = re.compile(
    rf"(?i)(?<![A-Za-z0-9_])(?:{_STATIC_PATTERN}|ICC(?:[- _]?\d+)?)(?![A-Za-z0-9_])"
)

FORBIDDEN_RAW_MARKUP = ("<span", "</span>", "style=", "color:")
FORBIDDEN_FALLBACK_MARKERS = ("🟢", "🔴")
MATH_SIGNAL_PATTERN = re.compile(
    r"(\(?:color|boxed|Gamma|varphi|vdash|nvdash|neq|Rightarrow|implies|iff|land|lor|mu|operatorname)"
    r"|\$|[=≠→⇒⇔∧∨⊢⊬∈∉∀∃μΓφ])"
)
COLORED_FORMAL_LABEL_PATTERN = re.compile(
    r"\\color\{(?:green|red)\}\{\\operatorname\{[^{}]+\}\}",
    re.IGNORECASE,
)


def canonical_formal_label(label: str) -> str:
    normalized = " ".join(label.strip().upper().split())
    if re.fullmatch(r"ICC(?:[- _]?\d+)?", normalized, flags=re.IGNORECASE):
        return normalized.replace(" ", "-").replace("_", "-")
    canonical = FORMAL_OBJECT_ALIASES.get(normalized)
    if canonical is None:
        raise ColorInvariantViolation("FORMAL_LABEL_NOT_REGISTERED")
    return canonical


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


def verify_assistant_response(rendered: str) -> None:
    """Fail closed when a registered formal label escapes outside typed color.

    This is intentionally narrower than a full LaTeX parser. It closes the
    recurring label-bypass failure while preserving ordinary prose.
    """
    verify_rendered_output(rendered)
    masked = COLORED_FORMAL_LABEL_PATTERN.sub("", rendered)
    if FORMAL_OBJECT_PATTERN.search(masked):
        raise ColorInvariantViolation("UNTYPED_FORMAL_LABEL_AT_RESPONSE_BOUNDARY")


def emit_user_visible(fragments: Iterable[Fragment]) -> str:
    parts = tuple(fragments)
    verify_fragments(parts)
    rendered: list[str] = []
    for fragment in parts:
        if isinstance(fragment, (MathFragment, AssessedMathFragment)):
            rendered.append(render_math(fragment))
        else:
            rendered.append(fragment.text)
    out = "".join(rendered)
    verify_rendered_output(out)
    return out
