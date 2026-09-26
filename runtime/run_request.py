"""User-facing run-command resolution.

Ordinary "run TOOL" means the current configured run, not the bare semantic
primitive. Bare/core execution requires explicit user wording.

The resolver also types the legacy overloaded "36" shell. MT's default full
geometry is D36_C = Scope x ModeFace.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re

from tool_run_registry import CONFIGURED_RUNS


class Geometry(str, Enum):
    D36_C = "D36_C"   # Scope x ModeFace
    D36_H = "D36_H"   # SourceScope x TargetScope
    D216 = "D216"     # SourceScope x TargetScope x ModeFace
    D288 = "D288"     # SourceScope x TargetScope x FullMode


@dataclass(frozen=True)
class RunRequest:
    tool_id: str
    configured: bool
    wrapper_required: bool
    geometry: Geometry | None
    recursive: bool
    closure_required: bool
    reentry_required: bool
    semantic_before_return: bool


ALIASES = {
    "mt": "MT",
    "mta": "MTA",
    "pd": "PD",
    "pd audit": "PDAudit",
    "pdaudit": "PDAudit",
    "assert": "ASSERT",
    "goal": "GOAL",
    "root cause": "Diagnosis",
}

DEFAULT_GEOMETRY = {
    "MT": Geometry.D36_C,
    "PD": Geometry.D36_C,
    "PDAudit": Geometry.D36_C,
}


def _normalize_tool(text: str) -> str:
    lowered = " ".join(text.lower().strip().split())
    if lowered in ALIASES:
        return ALIASES[lowered]
    for alias, tool in sorted(ALIASES.items(), key=lambda x: -len(x[0])):
        if re.search(rf"\b{re.escape(alias)}\b", lowered):
            return tool
    raise KeyError("TOOL_NOT_RESOLVED")


def resolve_run_request(text: str) -> RunRequest:
    """Resolve user wording into the protected execution contract.

    Default:
      run TOOL / TOOL this -> configured recursive run + wrapper + typed geometry

    Escape hatch:
      bare TOOL / core TOOL -> semantic primitive only
    """
    tool = _normalize_tool(text)
    lowered = text.lower()
    explicit_bare = bool(re.search(r"\b(?:bare|core)\b", lowered))

    if explicit_bare:
        return RunRequest(
            tool_id=tool,
            configured=False,
            wrapper_required=False,
            geometry=None,
            recursive=False,
            closure_required=False,
            reentry_required=False,
            semantic_before_return=False,
        )

    spec = CONFIGURED_RUNS.get(tool)
    if spec is None:
        raise KeyError(f"CONFIGURED_RUN_NOT_REGISTERED:{tool}")

    return RunRequest(
        tool_id=tool,
        configured=True,
        wrapper_required=True,
        geometry=DEFAULT_GEOMETRY.get(tool),
        recursive=spec.recursive,
        closure_required=spec.closure_required,
        reentry_required=spec.reentry_required,
        semantic_before_return=(tool=="MT"),
    )
