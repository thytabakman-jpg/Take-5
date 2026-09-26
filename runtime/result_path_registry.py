"""Authority registry for executable result paths.

Exactly one path is the default protected RESULT path. Alternate facades remain
available for comparison/regression but do not acquire result authority by existence.
The default user-visible emission path is fail-closed through the mandatory
mathematical glyph-color gate.
"""
from dataclasses import dataclass
from typing import Iterable

from mathematical_color_gate import (
    AssessedMathFragment,
    Fragment,
    MathFragment,
    TextFragment,
    ColorInvariantViolation,
    emit_user_visible,
)


@dataclass(frozen=True)
class ResultPath:
    name: str
    module: str
    authority: str
    role: str
    emission_gate: str | None = None


PATHS = (
    ResultPath(
        "math_first",
        "math_first_wrapper",
        "DEFAULT_RESULT_AUTHORITY",
        "CURRENT_DEFAULT",
        "mathematical_color_gate.emit_user_visible",
    ),
    ResultPath(
        "recursive_episode",
        "recursive_episode",
        "NO_DEFAULT_RESULT_AUTHORITY",
        "COMPARATOR",
        None,
    ),
    ResultPath(
        "inquiry_session",
        "inquiry_session",
        "NO_DEFAULT_RESULT_AUTHORITY",
        "COMPARATOR",
        None,
    ),
)


def default_result_path() -> ResultPath:
    xs = [p for p in PATHS if p.authority == "DEFAULT_RESULT_AUTHORITY"]
    if len(xs) != 1:
        raise RuntimeError("RESULT_PATH_AUTHORITY_NOT_UNIQUE")
    path = xs[0]
    if not path.emission_gate:
        raise RuntimeError("DEFAULT_RESULT_EMISSION_GATE_REQUIRED")
    return path


def result_path(name: str) -> ResultPath:
    return next(p for p in PATHS if p.name == name)


def emit_default_result(fragments: Iterable[Fragment]) -> str:
    """Canonical user-visible emission boundary for the default result path.

    Formal math may reach this authoritative boundary only after a complete-for-use
    assessment. Raw MathFragment values cannot self-certify recovery.
    """
    default_result_path()
    parts = tuple(fragments)
    for fragment in parts:
        if isinstance(fragment, MathFragment) and not isinstance(fragment, AssessedMathFragment):
            raise ColorInvariantViolation("UNASSESSED_MATH_AT_DEFAULT_RESULT_BOUNDARY")
        if not isinstance(fragment, (TextFragment, AssessedMathFragment)):
            raise ColorInvariantViolation("UNTYPED_DEFAULT_RESULT_FRAGMENT")
    return emit_user_visible(parts)
