"""Mandatory controller consultation through ToolConductor.

The consultation contract is coverage-relative: every registered factor must
receive exactly one conductor-level disposition. Individual OPEN/BLOCKED factor
states remain evidence and do not by themselves fail the parent controller.

The active controller's adapter is removed from the nested conductor
environment so an ImprovementCore or ICC128 invocation cannot recursively spawn
itself through ToolConductor.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from portable_tool_conductor import consult_tool_conductor
from tool_run_registry import MATERIAL_TOOLS


@dataclass(frozen=True)
class ControllerToolConductorReceipt:
    active_controller: str
    status: str
    blocker: str | None
    conductor_status: str
    tool_count: int
    expected_tool_count: int
    emitted_tool_ids: tuple[str, ...]
    open_tools: tuple[str, ...]
    results: tuple[dict[str, Any], ...]

    @property
    def coverage_complete(self) -> bool:
        return self.status == "COMPLETE"

    def payload(self) -> dict[str, Any]:
        return {
            "active_controller": self.active_controller,
            "status": self.status,
            "blocker": self.blocker,
            "conductor_status": self.conductor_status,
            "coverage_complete": self.coverage_complete,
            "tool_count": self.tool_count,
            "expected_tool_count": self.expected_tool_count,
            "emitted_tool_ids": self.emitted_tool_ids,
            "open_tools": self.open_tools,
            "results": self.results,
        }


def consult_registered_repertoire(
    packet: Mapping[str, Any] | None,
    *,
    active_controller: str,
    adapters: Mapping[str, Callable] | None = None,
    conductor_runner: Callable[..., dict[str, Any]] = consult_tool_conductor,
) -> ControllerToolConductorReceipt:
    """Run the ToolConductor consultation surface and verify exact registered-repertoire coverage."""
    source = dict(packet or {})
    nested_adapters = {
        str(tool_id): adapter
        for tool_id, adapter in dict(adapters or {}).items()
        if str(tool_id) != str(active_controller)
    }

    try:
        raw = conductor_runner(source, adapters=nested_adapters)
    except Exception as exc:
        return ControllerToolConductorReceipt(
            active_controller=str(active_controller),
            status="OPEN",
            blocker=f"TOOL_CONDUCTOR_EXECUTION_FAILED:{type(exc).__name__}:{exc}",
            conductor_status="OPEN",
            tool_count=0,
            expected_tool_count=len(MATERIAL_TOOLS),
            emitted_tool_ids=(),
            open_tools=(),
            results=(),
        )

    results = tuple(
        dict(row) for row in tuple(raw.get("results", ()))
        if isinstance(row, Mapping)
    )
    emitted = tuple(str(row.get("tool_id", "")) for row in results)
    expected = tuple(str(x) for x in MATERIAL_TOOLS)

    blocker = None
    if int(raw.get("tool_count", len(results))) != len(expected):
        blocker = "TOOL_CONDUCTOR_TOOL_COUNT_MISMATCH"
    elif len(results) != len(expected):
        blocker = "TOOL_CONDUCTOR_RESULT_COUNT_MISMATCH"
    elif emitted != expected:
        blocker = "TOOL_CONDUCTOR_REGISTERED_ORDER_OR_IDENTITY_MISMATCH"
    elif len(set(emitted)) != len(expected):
        blocker = "TOOL_CONDUCTOR_DUPLICATE_FACTOR"
    elif any(not str(row.get("status", "")) for row in results):
        blocker = "TOOL_CONDUCTOR_UNTYPED_FACTOR_DISPOSITION"

    open_tools = tuple(
        str(row.get("tool_id"))
        for row in results
        if str(row.get("status", "")) in {"OPEN", "BLOCKED", "CONFLICT"}
    )

    return ControllerToolConductorReceipt(
        active_controller=str(active_controller),
        status="COMPLETE" if blocker is None else "OPEN",
        blocker=blocker,
        conductor_status=str(raw.get("status", "OPEN")),
        tool_count=len(results),
        expected_tool_count=len(expected),
        emitted_tool_ids=emitted,
        open_tools=open_tools,
        results=results,
    )


def attach_consultation(
    state: Any,
    receipt: ControllerToolConductorReceipt,
) -> Any:
    if not isinstance(state, dict):
        return state
    history = tuple(state.get("tool_conductor_consultation_history", ()))
    summary = {
        "active_controller": receipt.active_controller,
        "status": receipt.status,
        "blocker": receipt.blocker,
        "conductor_status": receipt.conductor_status,
        "tool_count": receipt.tool_count,
        "expected_tool_count": receipt.expected_tool_count,
        "open_tools": receipt.open_tools,
    }
    return {
        **state,
        "tool_conductor_consultation": receipt.payload(),
        "tool_conductor_coverage_status": receipt.status,
        "tool_conductor_consultation_history": history + (summary,),
    }
