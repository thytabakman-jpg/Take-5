"""Fail-closed user-visible mathematical color emission gate.

Mathematical and formal-system objects are emitted as typed fragments carrying
their recovery state. The renderer owns the color projection; callers do not
hand-author HTML or drop status before emission.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Iterable, Sequence


class MathStatus(str, Enum):
    RECOVERED = "RECOVERED"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class TextFragment:
    text: str


@dataclass(frozen=True)
class MathFragment:
    latex: str
    status: MathStatus


Fragment = TextFragment | MathFragment


class ColorInvariantViolation(RuntimeError):
    pass


FORBIDDEN_RAW_MARKUP = ("<span", "</span>", "style=", "color:")
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


def render_math(fragment: MathFragment) -> str:
    latex = fragment.latex.strip()
    if not latex:
        raise ColorInvariantViolation("EMPTY_MATH_FRAGMENT")
    color = "green" if fragment.status is MathStatus.RECOVERED else "red"
    return rf"\color{{{color}}}{{{latex}}}"


def _raw_text_contains_load_bearing_math(text: str) -> bool:
    return bool(FORMAL_OBJECT_PATTERN.search(text) or MATH_SIGNAL_PATTERN.search(text))


def verify_fragments(fragments: Sequence[Fragment]) -> None:
    for fragment in fragments:
        if isinstance(fragment, MathFragment):
            if not isinstance(fragment.status, MathStatus):
                raise ColorInvariantViolation("MATH_STATUS_REQUIRED")
            if not fragment.latex.strip():
                raise ColorInvariantViolation("EMPTY_MATH_FRAGMENT")
            continue
        if isinstance(fragment, TextFragment):
            lowered = fragment.text.lower()
            if any(marker in lowered for marker in FORBIDDEN_RAW_MARKUP):
                raise ColorInvariantViolation("RAW_COLOR_MARKUP_FORBIDDEN")
            if _raw_text_contains_load_bearing_math(fragment.text):
                raise ColorInvariantViolation("UNTYPED_LOAD_BEARING_MATH")
            continue
        raise ColorInvariantViolation("UNTYPED_FRAGMENT")


def emit_user_visible(fragments: Iterable[Fragment]) -> str:
    """Render only verified typed fragments.

    Fail closed: load-bearing mathematics/formal-system names cannot travel as
    ordinary text. They must be MathFragment values with explicit recovery
    status, so status survives all the way to the visible renderer.
    """
    parts = tuple(fragments)
    verify_fragments(parts)
    rendered: list[str] = []
    for fragment in parts:
        if isinstance(fragment, MathFragment):
            rendered.append(render_math(fragment))
        else:
            rendered.append(fragment.text)
    return "".join(rendered)
