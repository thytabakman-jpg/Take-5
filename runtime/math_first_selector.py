"""Exact math-first package selection for Improvement Core.

Implements the architecture decision:
choose the least-cost applicable package whose union of declared coverage
contains every live execution obligation.

This module is additive.  Existing HF selection remains the default unless a
caller explicitly supplies this selector.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping


@dataclass(frozen=True)
class ToolContract:
    program_id: str
    covers: frozenset[str]
    cost: float = 1.0
    input_type: str = "ANY"
    output_type: str = "ANY"
    applicable: bool | Callable[[Any], bool] = True
    licensed: bool = True

    def is_applicable(self, context: Any = None) -> bool:
        value = self.applicable(context) if callable(self.applicable) else self.applicable
        return bool(value) and bool(self.licensed)


@dataclass(frozen=True)
class PackageSelection:
    status: str
    package: tuple[str, ...]
    total_cost: float
    covered: frozenset[str]
    uncovered: frozenset[str]


def _better(candidate, incumbent):
    """Order by total cost, then package size, then stable lexical identity."""
    if incumbent is None:
        return True
    c_cost, c_ids = candidate
    i_cost, i_ids = incumbent
    return (c_cost, len(c_ids), c_ids) < (i_cost, len(i_ids), i_ids)


def select_min_cost_cover(
    obligations: Iterable[str],
    contracts: Iterable[ToolContract],
    *,
    context: Any = None,
) -> PackageSelection:
    """Exact finite weighted set cover over the live obligation set.

    Dynamic programming tracks only reachable covered subsets, so tool count
    may be large while the usual small live obligation frontier remains cheap.
    """
    target = frozenset(obligations)
    if not target:
        return PackageSelection("CLOSED", (), 0.0, frozenset(), frozenset())

    usable = []
    for contract in contracts:
        if contract.cost < 0:
            raise ValueError("tool cost must be nonnegative")
        cover = frozenset(contract.covers) & target
        if cover and contract.is_applicable(context):
            usable.append((contract, cover))

    # covered-set -> (cost, ordered package ids)
    dp: dict[frozenset[str], tuple[float, tuple[str, ...]]] = {
        frozenset(): (0.0, ())
    }
    for contract, cover in usable:
        nxt = dict(dp)
        for already, (cost, ids) in dp.items():
            combined = already | cover
            proposal = (cost + float(contract.cost), tuple(sorted(ids + (contract.program_id,))))
            if _better(proposal, nxt.get(combined)):
                nxt[combined] = proposal
        dp = nxt

    if target not in dp:
        best_covered = max(
            dp,
            key=lambda covered: (len(covered), -dp[covered][0], tuple(sorted(covered))),
        )
        cost, ids = dp[best_covered]
        return PackageSelection(
            "OPEN",
            ids,
            cost,
            best_covered,
            target - best_covered,
        )

    cost, ids = dp[target]
    return PackageSelection("SELECTED", ids, cost, target, frozenset())


def contracts_from_packet(
    package_index: Mapping[str, Iterable[str]],
    packet: Mapping[str, Any] | None = None,
) -> tuple[ToolContract, ...]:
    """Build typed contracts from existing package coverage plus optional metadata.

    packet["tool_contracts"] may override per-program cost/applicability/types:
      {
        "C02": {
          "cost": 0.5,
          "applicable": True,
          "licensed": True,
          "input_type": "...",
          "output_type": "...",
          "covers": ["..."]
        }
      }

    packet["licensed_tools"], when present, is an additional episode-level gate.
    """
    packet = {} if packet is None else packet
    metadata = packet.get("tool_contracts", {}) or {}
    licensed_tools = packet.get("licensed_tools")
    licensed_set = None if licensed_tools is None else set(licensed_tools)

    out = []
    for pid, default_cover in package_index.items():
        meta = metadata.get(pid, {}) or {}
        cover = meta.get("covers", default_cover)
        licensed = bool(meta.get("licensed", True))
        if licensed_set is not None:
            licensed = licensed and pid in licensed_set
        out.append(
            ToolContract(
                program_id=str(pid),
                covers=frozenset(cover),
                cost=float(meta.get("cost", 1.0)),
                input_type=str(meta.get("input_type", "ANY")),
                output_type=str(meta.get("output_type", "ANY")),
                applicable=meta.get("applicable", True),
                licensed=licensed,
            )
        )
    return tuple(out)


def select_min_cost_package(obligations, package_index, packet=None):
    result = select_min_cost_cover(
        obligations,
        contracts_from_packet(package_index, packet),
        context=packet,
    )
    return result.package if result.status == "SELECTED" else ()
