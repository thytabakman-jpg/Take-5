"""Whole-system cleanup campaign.

This is an observation/audit composition, not a self-promoting repair engine.
It runs independent current audits together so a cleanup pass cannot mistake one
narrow green surface for whole-system closure.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path

from capability_preservation import evaluate_manifest
from current_portfolio_identity import audit_current_portfolio_identity
from full_invocation_portfolio import audit_full_invocation_portfolio
from protected_transition_portfolio import audit_protected_transition_portfolio
from repertoire_reachability import audit_current_repertoire_reachability
from system_audit import run_audit
from tool_maturity import audit_all
from tool_reality_audit import audit_tool_reality


@dataclass(frozen=True)
class CleanupCampaignReceipt:
    status:str
    system_closed:bool
    configured_identity_status:str
    protected_transition_status:str
    full_invocation_status:str
    reachability_status:str
    capability_preservation_status:str
    capability_preservation_open:tuple[str,...]
    tool_reality_status:str
    native_unrecovered:tuple[str,...]
    generic_only:tuple[str,...]
    capability_repair:tuple[str,...]


def _capability_preservation(repo_root:Path):
    path=repo_root/"integration"/"CAPABILITY_PRESERVATION_MANIFEST_100.json"
    if not path.exists():
        return "OPEN",("MANIFEST_MISSING",)
    payload=json.loads(path.read_text(encoding="utf-8"))
    results=evaluate_manifest(payload.get("capabilities",{}))
    open_ids=tuple(r.capability_id for r in results if not r.preserved)
    return ("PRESERVED" if results and not open_ids else "OPEN"),open_ids


def run_cleanup_campaign(root=None)->CleanupCampaignReceipt:
    repo_root=Path(root) if root is not None else Path(__file__).resolve().parents[1]
    system=run_audit(repo_root)
    configured=audit_current_portfolio_identity()
    pti=audit_protected_transition_portfolio()
    invocation=audit_full_invocation_portfolio()
    reachability=audit_current_repertoire_reachability()
    preservation_status,preservation_open=_capability_preservation(repo_root)
    reality=audit_tool_reality()
    maturity=audit_all()
    capability_repair=tuple(
        row.program_id for row in maturity
        if str(row.disposition.value)=="C_REPAIR"
    )

    blocking=(
        not system.closed
        or configured.status!="CLOSED_RELATIVE"
        or pti.status!="PASS"
        or invocation.status!="CLOSED_RELATIVE"
        or reachability.status!="CLOSED_RELATIVE"
        or preservation_status!="PRESERVED"
        or bool(capability_repair)
    )
    return CleanupCampaignReceipt(
        status="OPEN" if blocking or reality.status!="CLOSED_RELATIVE" else "CLOSED_RELATIVE",
        system_closed=system.closed,
        configured_identity_status=configured.status,
        protected_transition_status=pti.status,
        full_invocation_status=invocation.status,
        reachability_status=reachability.status,
        capability_preservation_status=preservation_status,
        capability_preservation_open=preservation_open,
        tool_reality_status=reality.status,
        native_unrecovered=tuple(reality.native_unrecovered),
        generic_only=tuple(reality.generic_only),
        capability_repair=capability_repair,
    )


if __name__=="__main__":
    print(asdict(run_cleanup_campaign()))
