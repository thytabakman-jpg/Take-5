"""Fail-closed user-visible mathematical status emission.

Mathematical and formal-system objects are emitted as typed fragments carrying
their recovery state. Recovery state is semantic. Rendering is channel-specific.

No caller may hand-author color markup or drop status before emission.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Iterable, Sequence


class MathStatus(str, Enum):
    RECOVERED = "RECOVERED"
    UNRESOLVED = "UNRESOLVED"


class RenderMode(str, Enum):
    LATEX_COLOR = "LATEX_COLOR"
    STATUS_PREFIX = "STATUS_PREFIX"


@dataclass(frozen=True)
class RenderChannel:
    name: str
    mode: RenderMode


TAKE5_LATEX = RenderChannel("take5_latex", RenderMode.LATEX_COLOR)
PORTABLE_TEXT = RenderChannel("portable_text", RenderMode.STATUS_PREFIX)


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


def _status_prefix(status: MathStatus) -> str:
    return "🟢" if status is MathStatus.RECOVERED else "🔴"


def render_math(fragment: MathFragment, channel: RenderChannel = TAKE5_LATEX) -> str:
    latex = fragment.latex.strip()
    if not latex:
        raise ColorInvariantViolation("EMPTY_MATH_FRAGMENT")
    if not isinstance(fragment.status, MathStatus):
        raise ColorInvariantViolation("MATH_STATUS_REQUIRED")

    if channel.mode is RenderMode.LATEX_COLOR:
        color = "green" if fragment.status is MathStatus.RECOVERED else "red"
        return rf"\color{{{color}}}{{{latex}}}"

    if channel.mode is RenderMode.STATUS_PREFIX:
        return f"{_status_prefix(fragment.status)} {latex}"

    raise ColorInvariantViolation("UNSUPPORTED_RENDER_MODE")


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


def emit_user_visible(
    fragments: Iterable[Fragment],
    *,
    channel: RenderChannel = TAKE5_LATEX,
) -> str:
    """Render verified typed fragments through an explicit channel adapter.

    The status survives even when literal color is unavailable. Portable
    channels receive an unambiguous status prefix instead of raw markup.
    """
    parts = tuple(fragments)
    verify_fragments(parts)
    rendered: list[str] = []
    for fragment in parts:
        if isinstance(fragment, MathFragment):
            rendered.append(render_math(fragment, channel))
        else:
            rendered.append(fragment.text)
    return "".join(rendered)
