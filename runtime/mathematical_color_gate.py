"""Fail-closed user-visible mathematical color emission gate.

Mathematical objects are emitted as typed fragments carrying their recovery state.
The renderer owns the color projection; callers do not hand-author HTML or drop
the state before emission.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
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


def render_math(fragment: MathFragment) -> str:
    latex = fragment.latex.strip()
    if not latex:
        raise ColorInvariantViolation("EMPTY_MATH_FRAGMENT")
    color = "green" if fragment.status is MathStatus.RECOVERED else "red"
    return rf"\color{{{color}}}{{{latex}}}"


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
            continue
        raise ColorInvariantViolation("UNTYPED_FRAGMENT")


def emit_user_visible(fragments: Iterable[Fragment]) -> str:
    """Render only verified typed fragments.

    This boundary is deliberately fail-closed. A caller that owns load-bearing
    mathematics must provide MathFragment objects with explicit recovery state.
    The status therefore survives all the way to visible rendering.
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
