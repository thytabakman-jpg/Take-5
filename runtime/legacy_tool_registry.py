"""Registry for immutable historical tools, separate from current tools."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class LegacyToolSpec:
    canonical_name: str
    aliases: frozenset[str]
    loader_module: str
    source_commit: str
    immutable: bool = True

ICC128_LEGACY = LegacyToolSpec(
    canonical_name="ICC128 Legacy",
    aliases=frozenset({
        "icc128 legacy",
        "activate icc128 legacy",
        "run icc128 legacy",
        "use icc128 legacy",
    }),
    loader_module="icc128_legacy",
    source_commit="e4c76c595b44a35fd9efc02cde8979e656ef54e8",
)

LEGACY_TOOLS = (ICC128_LEGACY,)

def resolve_legacy_tool(command: str) -> LegacyToolSpec | None:
    key = " ".join(str(command).strip().lower().split())
    for spec in LEGACY_TOOLS:
        if key == spec.canonical_name.lower() or key in spec.aliases:
            return spec
    return None
