"""Fail-closed bootstrap gate for every ICC wrapper execution.

Protected order:
    full wrapped ASSERT in observer mode
    -> full wrapped GOAL in observer mode
    -> ICC work

This module does not implement ASSERT or GOAL semantics. It validates that the
current configured wrapped tools actually ran, in observer mode, in the required
order, and that their results were captured and consumed before ICC proceeds.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class ToolRunReceipt:
    tool_id: str
    configured: bool
    wrapper_required: bool
    observer_mode: bool
    executed: bool
    result_captured: bool
    consumed: bool
    result: Any = None


@dataclass(frozen=True)
class ICCBootstrapReceipt:
    assert_receipt: ToolRunReceipt
    goal_receipt: ToolRunReceipt
    complete: bool
    trace: tuple[str, ...]


class ICCBootstrapBlocked(RuntimeError):
    pass


def _validate_tool_receipt(receipt: ToolRunReceipt, expected_tool: str) -> None:
    if receipt.tool_id != expected_tool:
        raise ICCBootstrapBlocked(f"BOOTSTRAP_WRONG_TOOL:{expected_tool}")
    if not receipt.configured:
        raise ICCBootstrapBlocked(f"BOOTSTRAP_BARE_TOOL_FORBIDDEN:{expected_tool}")
    if not receipt.wrapper_required:
        raise ICCBootstrapBlocked(f"BOOTSTRAP_WRAPPER_REQUIRED:{expected_tool}")
    if not receipt.observer_mode:
        raise ICCBootstrapBlocked(f"BOOTSTRAP_OBSERVER_MODE_REQUIRED:{expected_tool}")
    if not receipt.executed:
        raise ICCBootstrapBlocked(f"BOOTSTRAP_NOT_EXECUTED:{expected_tool}")
    if not receipt.result_captured:
        raise ICCBootstrapBlocked(f"BOOTSTRAP_RESULT_NOT_CAPTURED:{expected_tool}")
    if not receipt.consumed:
        raise ICCBootstrapBlocked(f"BOOTSTRAP_RESULT_NOT_CONSUMED:{expected_tool}")


def run_icc_bootstrap(
    target: Any,
    binding: Any,
    *,
    assert_observer_fn: Callable[[Any, Any], ToolRunReceipt],
    goal_observer_fn: Callable[[Any, Any, Any], ToolRunReceipt],
) -> ICCBootstrapReceipt:
    """Run and certify the mandatory ICC bootstrap.

    ASSERT sees the incoming target. GOAL sees the same target plus the captured
    ASSERT result. No ICC caller receives a complete receipt unless both current
    configured wrapped tools executed successfully in observer mode.
    """
    assert_receipt = assert_observer_fn(target, binding)
    _validate_tool_receipt(assert_receipt, "ASSERT")

    goal_receipt = goal_observer_fn(target, assert_receipt.result, binding)
    _validate_tool_receipt(goal_receipt, "GOAL")

    return ICCBootstrapReceipt(
        assert_receipt=assert_receipt,
        goal_receipt=goal_receipt,
        complete=True,
        trace=("ASSERT_OBSERVER", "GOAL_OBSERVER"),
    )


def require_icc_bootstrap(receipt: ICCBootstrapReceipt) -> ICCBootstrapReceipt:
    if not isinstance(receipt, ICCBootstrapReceipt):
        raise ICCBootstrapBlocked("ICC_BOOTSTRAP_RECEIPT_REQUIRED")
    if not receipt.complete:
        raise ICCBootstrapBlocked("ICC_BOOTSTRAP_INCOMPLETE")
    if receipt.trace != ("ASSERT_OBSERVER", "GOAL_OBSERVER"):
        raise ICCBootstrapBlocked("ICC_BOOTSTRAP_ORDER_INVALID")
    _validate_tool_receipt(receipt.assert_receipt, "ASSERT")
    _validate_tool_receipt(receipt.goal_receipt, "GOAL")
    return receipt
