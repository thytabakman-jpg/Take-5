"""Candidate ICC128 entry binding for Kernel Math Contract 053.

The current generic entry contract still names IC-028.  This candidate preserves
its target/job/mode logic while binding the substantive controller identity to
ICC128 for 053 prototype episodes.
"""
from __future__ import annotations

from dataclasses import replace

from entry_contract import EntryBinding, bind_entry_contract


ICC128_CONTROLLER = "ICC128"


def bind_icc128_entry_contract(
    user_text,
    *,
    target,
    job,
    basis,
    authority=frozenset(),
    boundary=None,
    explicit_mode=None,
    observer_risk=None,
    episode_id="icc128-053",
):
    base = bind_entry_contract(
        user_text,
        target=target,
        job=job,
        basis=basis,
        authority=authority,
        boundary=boundary,
        explicit_mode=explicit_mode,
        observer_risk=observer_risk,
        episode_id=episode_id,
    )
    contract = replace(
        base.contract,
        controller=ICC128_CONTROLLER,
        receipt=f"{episode_id}:ENTRY_BOUND:{ICC128_CONTROLLER}:{base.contract.mode_profile.mode_id}",
    )
    lease = replace(base.lease, controller=ICC128_CONTROLLER)
    return EntryBinding(contract, lease)
