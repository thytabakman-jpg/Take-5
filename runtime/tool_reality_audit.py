"""Strong whole-portfolio tool-reality audit.

This audit intentionally joins claims that narrower audits keep separate:
configured identity, explicit tool-specific identity reconstruction, and recovered
native executable realization. A strong whole-system closure claim is licensed
only when all three agree.

Environment-bound native programs count as recovered programs. They remain
explicitly environment-dependent rather than being misclassified as absent.
"""
from __future__ import annotations

from dataclasses import dataclass

from current_portfolio_identity import audit_current_portfolio_identity
from portable_tool_conductor import compilation_witness
from tool_manifest import OVERRIDES
from tool_manifest_audit import audit_tool_identities
from tool_run_registry import CONFIGURED_RUNS


@dataclass(frozen=True)
class ToolRealityAudit:
    status: str
    configured_identity_status: str
    explicit_manifest_status: str
    native_execution_status: str
    checked: int
    generic_only: tuple[str, ...]
    native_unrecovered: tuple[str, ...]
    environment_bound: tuple[str, ...]


def audit_tool_reality() -> ToolRealityAudit:
    configured = audit_current_portfolio_identity()
    manifests = audit_tool_identities(CONFIGURED_RUNS, OVERRIDES)

    native_unrecovered = []
    environment_bound = []
    for tool_id in CONFIGURED_RUNS:
        witness = compilation_witness(tool_id)
        if witness.entrypoint is None:
            native_unrecovered.append(tool_id)
        elif witness.required_environment:
            environment_bound.append(tool_id)

    configured_status = configured.status
    manifest_status = manifests.status
    native_status = "CLOSED_RELATIVE" if not native_unrecovered else "OPEN"

    strong_closed = (
        configured_status == "CLOSED_RELATIVE"
        and manifest_status == "CLOSED_RELATIVE"
        and native_status == "CLOSED_RELATIVE"
    )

    return ToolRealityAudit(
        status="CLOSED_RELATIVE" if strong_closed else "OPEN",
        configured_identity_status=configured_status,
        explicit_manifest_status=manifest_status,
        native_execution_status=native_status,
        checked=len(CONFIGURED_RUNS),
        generic_only=tuple(manifests.generic_only),
        native_unrecovered=tuple(native_unrecovered),
        environment_bound=tuple(environment_bound),
    )
