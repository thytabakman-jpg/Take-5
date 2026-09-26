"""Fail-closed user-visible mathematical status emission.

Mathematical and formal-system objects are emitted as typed fragments carrying
their recovery state. Recovery state is semantic. Rendering is channel-specific.

No caller may hand-author color markup or drop status before emission.
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
    """Return a binary complete-for-use verdict for this exact job and claim.

    GREEN/RECOVERED is permitted only when the entire mathematics required by
    this exact use is figured out. Any missing, partial, ambiguous, conflicting,
    open, blocked, or merely proposed required coordinate returns NO/UNRESOLVED.
    """
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


FORBIDDEN_RAW_MARKUP = ("<span", "</span>", "style=", "color:")
FORBIDDEN_FALLBACK_MARKERS = ("🟢", "🔴")
FORMAL_OBJECT_PATTERN = re.compile(
    r"(?i)(?<![A-Za-z0-9_])("
    r"ASSERT|COMPARE|RESOLVE|HERE|INQUIRE|REASSERT|ROOT[ _-]?CAUSE|GOAL|"
    r"ARCHITECT|WRAPPER|JANE|MT|PD|ICC(?:[- _]?\d+)?"
    r")(?![A-Za-z0-9_])"
)
MATH_SIGNAL_PATTERN = re.compile(
    r"(\\(?:color|boxed|Gamma|varphi|vdash|nvdash|neq|Rightarrow|implies|iff|land|lor|mu|operatorname)"
    r"|\$|[=≠→⇒⇔∧∨⊢⊬∈∉∀∃μΓφ])"
)


def render_math(fragment: MathFragment | AssessedMathFragment) -> str:
    latex = fragment.latex.strip()
    if not latex:
        raise ColorInvariantViolation("EMPTY_MATH_FRAGMENT")
    if not isinstance(fragment.status, MathStatus):
        raise ColorInvariantViolation("MATH_STATUS_REQUIRED")

    color = "green" if fragment.status is MathStatus.RECOVERED else "red"
    return rf"\color{{{color}}}{{{latex}}}"


def render_formal_label(label: str, status: MathStatus) -> str:
    """Render a formal-system name as a colored mathematical glyph.

    This is the supported chat-safe path for labels such as ASSERT, GOAL,
    WRAPPER, PD, MT, and ICC-128. Raw HTML is never an admissible substitute.
    """
    normalized = label.strip()
    if not normalized:
        raise ColorInvariantViolation("EMPTY_FORMAL_LABEL")
    if not isinstance(status, MathStatus):
        raise ColorInvariantViolation("MATH_STATUS_REQUIRED")
    if not FORMAL_OBJECT_PATTERN.fullmatch(normalized):
        raise ColorInvariantViolation("FORMAL_LABEL_NOT_REGISTERED")
    latex_label = normalized.replace(" ", r"\,").replace("-", r"{-}")
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


def emit_user_visible(fragments: Iterable[Fragment]) -> str:
    """Render verified typed fragments using mandatory glyph-level LaTeX color."""
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
