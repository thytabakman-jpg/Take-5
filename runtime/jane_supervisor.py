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


def semantic_capture_obligation(
    state:JaneSupervisoryState,
    *,
    object_id:str,
    term:str,
    source:str,
    load_bearing:bool|None,
    package_current:bool,
    created_here:bool=False,
    math_complete_for_use:bool=False,
):
    """Create mandatory semantic-lifecycle work for a load-bearing object.

    Discovered terms may remain BLACK_BOX_OPEN with a durable package.
    Deliberately created tools/programs must not be treated as admission-ready
    while required mathematics for their advertised use remains unresolved.
    """
    # Unknown load-bearingness is a reason to capture, not a reason to prune.
    # This prevents the detector's own incompleteness from silently losing terms.
    if load_bearing is False:
        return None
    if package_current and (not created_here or math_complete_for_use):
        return None
    kind="CREATED_OBJECT_MATH_AND_PACKAGE" if created_here else "LOAD_BEARING_TERM_PACKAGE"
    alert={
        "kind":kind,
        "object_id":object_id,
        "term":term,
        "source":source,
        "status":"WORK_CANDIDATE",
        "load_bearing_status":"CONFIRMED" if load_bearing is True else "OPEN",
        "required":(
            "semantic_package",
            "mathematical_basis" if created_here else "typed_open_semantics",
        ),
    }
    state.alerts.append(alert)
    return alert
