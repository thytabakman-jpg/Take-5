"""Dependency-cone propagation primitive for Take-6."""
from __future__ import annotations
from collections import deque
from typing import Mapping, Iterable

def affected_cone(
    seeds: Iterable[str],
    reverse_dependencies: Mapping[str, Iterable[str]],
) -> tuple[str, ...]:
    seen = set(str(x) for x in seeds)
    q = deque(sorted(seen))
    while q:
        node = q.popleft()
        for dep in sorted(str(x) for x in reverse_dependencies.get(node, ())):
            if dep not in seen:
                seen.add(dep)
                q.append(dep)
    return tuple(sorted(seen))

def require_consequence_dispositions(
    cone: Iterable[str],
    dispositions: Mapping[str, str],
) -> None:
    allowed = {"COVERED", "NO_EFFECT", "OPEN", "BLOCKED", "CONFLICT", "SUPERSEDED"}
    missing = []
    invalid = []
    for item in sorted(set(str(x) for x in cone)):
        if item not in dispositions:
            missing.append(item)
        elif dispositions[item] not in allowed:
            invalid.append(item + ":" + str(dispositions[item]))
    if missing:
        raise RuntimeError("TAKE6_AFFECTED_CONE_UNDISPOSITIONED:" + ",".join(missing))
    if invalid:
        raise RuntimeError("TAKE6_AFFECTED_CONE_BAD_DISPOSITION:" + ",".join(invalid))
