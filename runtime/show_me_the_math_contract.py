"""Operational contract for the request "show me the math".

This is a request/job contract, not a formal tool. It checks whether a supplied
mathematical package is recursively reconstructible without hidden conversation
or repository dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

SHOW_MATH_PHRASES=(
    "show me the math",
    "show the math",
    "show me the full math",
    "show me the full math equation",
    "give me the actual math",
    "show me the actual math",
)

REQUIRED_PACKAGE_FIELDS=(
    "full_math",
    "run_spec",
    "definitions",
    "load_bearing_symbols",
    "initialization",
    "runtime_primitives",
    "persistence",
    "protected_behavior",
    "equivalence_tests",
)

@dataclass(frozen=True)
class ShowMathAssessment:
    complete: bool
    missing_fields: tuple[str,...]
    unresolved_symbols: tuple[str,...]
    unavailable_primitives: tuple[str,...]
    hidden_dependencies: tuple[str,...]

def is_show_me_the_math_request(text: str) -> bool:
    normalized=" ".join(str(text).lower().split())
    return any(p in normalized for p in SHOW_MATH_PHRASES)

def _deps(definitions: Mapping[str,Any], symbol: str) -> tuple[str,...]:
    row=definitions.get(symbol)
    if not isinstance(row,Mapping):
        return ()
    deps=row.get("dependencies",())
    return tuple(str(x) for x in deps)

def assess_show_math_package(package: Mapping[str,Any]) -> ShowMathAssessment:
    missing=tuple(k for k in REQUIRED_PACKAGE_FIELDS if k not in package)
    definitions=package.get("definitions",{})
    roots=tuple(str(x) for x in package.get("load_bearing_symbols",()))
    primitives=package.get("runtime_primitives",{})

    unresolved=set()
    unavailable=set()
    hidden=set()
    seen=set()
    frontier=list(roots)

    while frontier:
        symbol=frontier.pop()
        if symbol in seen:
            continue
        seen.add(symbol)

        if symbol in definitions:
            frontier.extend(_deps(definitions,symbol))
            continue

        primitive=primitives.get(symbol)
        if isinstance(primitive,Mapping):
            typed=bool(primitive.get("typed_contract"))
            available=bool(primitive.get("available"))
            if not typed:
                unresolved.add(symbol)
            if not available:
                unavailable.add(symbol)
            continue

        unresolved.add(symbol)
        hidden.add(symbol)

    complete=not (missing or unresolved or unavailable or hidden)
    return ShowMathAssessment(
        complete=complete,
        missing_fields=missing,
        unresolved_symbols=tuple(sorted(unresolved)),
        unavailable_primitives=tuple(sorted(unavailable)),
        hidden_dependencies=tuple(sorted(hidden)),
    )

def status_for_symbol(package: Mapping[str,Any], symbol: str) -> str:
    scoped=dict(package)
    scoped["load_bearing_symbols"]=(symbol,)
    return "GREEN" if assess_show_math_package(scoped).complete else "RED"
