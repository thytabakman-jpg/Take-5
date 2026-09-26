"""Jane supervisory sidecar semantics.

Jane observes/projects continuity state and emits candidate work. It does not own
primary episode action selection while another controller holds the lease.
"""
from dataclasses import dataclass,field
from typing import Any
from state_commit import CommitReceipt,StateRole,require_role

@dataclass
class JaneSupervisoryState:
    canonical_version:str|None=None
    material_deltas:list=field(default_factory=list)
    alerts:list=field(default_factory=list)
    receipts:list=field(default_factory=list)

def update_after_admitted_delta(state:JaneSupervisoryState, delta:Any, *, commit_receipt:CommitReceipt, canonical_version=None, receipt=None):
    require_role(commit_receipt,StateRole.SUPERVISORY)
    state.material_deltas.append(delta)
    if canonical_version is not None:
        state.canonical_version=canonical_version
    state.receipts.append(commit_receipt)
    if receipt is not None:
        state.receipts.append(receipt)
    return state

def continuity_alert(state:JaneSupervisoryState, kind:str, detail:Any):
    alert={"kind":kind,"detail":detail,"status":"WORK_CANDIDATE"}
    state.alerts.append(alert)
    return alert

def operator_context(state:JaneSupervisoryState):
    return {
        "canonical_version":state.canonical_version,
        "recent_material_deltas":tuple(state.material_deltas[-20:]),
        "open_alerts":tuple(a for a in state.alerts if a.get("status")=="WORK_CANDIDATE"),
        "receipt_count":len(state.receipts),
    }
