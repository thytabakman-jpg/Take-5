"""Native Discriminator tool.

Discriminator applies one explicit predicate to a frozen candidate set and
preserves plural or empty results rather than manufacturing a winner.
"""
from __future__ import annotations

from typing import Callable, Iterable, Any


def run_discriminator(candidates: Iterable[Any], predicate: Callable[[Any], bool]):
    frozen=tuple(candidates)
    survivors=tuple(x for x in frozen if predicate(x))
    if len(survivors)==1:
        status="UNIQUE"
    elif not survivors:
        status="OPEN"
    else:
        status="PLURAL"
    return {
        "status":status,
        "candidates":frozen,
        "survivors":survivors,
    }
