"""ImprovementCore attachment for RootCause.

RootCause owns local causal discrimination under HF2. ImprovementCore owns
admission into the larger controller state, cross-capability replanning, and
global terminality.
"""
from __future__ import annotations
from dataclasses import asdict
from typing import Iterable

from root_cause import RootCandidate, run_root_cause_hf2
from improvement_core_recursive_manager import ChildReturn


def run_root_cause_child(
    *,
    job_id:str,
    child_id:str,
    failure_class:Iterable[str],
    candidates:Iterable[RootCandidate],
    basis_id:str,
)->ChildReturn:
    result=run_root_cause_hf2(
        failure_class=failure_class,
        candidates=candidates,
        basis_id=basis_id,
    )
    if result.status=="RELATIVE_CLOSE":
        truth="FULL_MATCH"
    elif result.status in {"OPEN","BLOCKED","CONFLICT"}:
        truth=result.status
    else:
        truth="SEMANTICALLY_APPLIED"
    return ChildReturn(
        child_id=child_id,
        job_id=job_id,
        execution_truth=truth,
        result={
            "tool":"RootCause",
            "local_status":result.status,
            "root_candidates":result.root_candidates,
            "rejected_candidates":result.rejected_candidates,
            "unresolved":result.unresolved,
            "rounds":result.rounds,
            "parent_handoff":result.parent_handoff,
            "trace":result.trace,
        },
        basis_id=basis_id,
    )
