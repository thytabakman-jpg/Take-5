"""Typed Jane supervisory-relevance predicate.

Jane owns continuity supervision, not primary action selection.  This module
decides whether an admitted material delta touches a Jane-owned continuity
coordinate and therefore must be synchronized to Jane.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping


SUPERVISORY_PREFIXES = (
    "canonical",
    "current",
    "version",
    "provenance",
    "receipt",
    "open",
    "blocked",
    "conflict",
    "incomparable",
    "handoff",
    "frontier",
    "question",
    "authority",
    "controller",
    "target",
    "job",
    "basis",
    "frozen_math",
    "candidate_universe",
)


@dataclass(frozen=True)
class JaneRelevance:
    relevant: bool
    coordinates: tuple[str, ...]
    reason: str


def _changed_coordinates(delta: Any) -> tuple[str, ...]:
    if delta is None:
        return ()
    changed = getattr(delta, "changed", None)
    if changed is not None:
        return tuple(str(x) for x in changed)
    if isinstance(delta, Mapping):
        explicit = delta.get("changed")
        if explicit is not None and not isinstance(explicit, (str, bytes)):
            return tuple(str(x) for x in explicit)
        return tuple(str(x) for x in delta.keys())
    if isinstance(delta, Iterable) and not isinstance(delta, (str, bytes)):
        return tuple(str(x) for x in delta)
    return (str(delta),)


def supervisory_relevance(delta: Any, *, frozen_math=None, entry_binding=None) -> JaneRelevance:
    coordinates = _changed_coordinates(delta)
    relevant = tuple(
        c for c in coordinates
        if any(c.lower().startswith(prefix) for prefix in SUPERVISORY_PREFIXES)
    )
    if relevant:
        return JaneRelevance(True, relevant, "JANE_OWNED_CONTINUITY_COORDINATE")
    return JaneRelevance(False, (), "NO_JANE_OWNED_CONTINUITY_DELTA")


def is_supervisory_relevant(delta: Any, *, frozen_math=None, entry_binding=None) -> bool:
    return supervisory_relevance(
        delta,
        frozen_math=frozen_math,
        entry_binding=entry_binding,
    ).relevant
