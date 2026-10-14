"""Jane integrated interface over Take-5 control services.

Jane is the user-facing continuity interface/facade. The historical begin_turn
retains its IC-028 compatibility binding; begin_icc128_turn is the explicit
guarded ICC128 continuity handoff. Neither facade owns substantive selection
or authenticates external host currentness.
"""
from dataclasses import dataclass
from capability_router import coverage
from delegation_officer import plan_delegation
from entry_contract import bind_entry_contract, entry_is_bound
from jane_continuity import recover_continuity, controller_context
from icc128_entry_binding import bind_icc128_entry_contract
from jane_icc128_bridge import bind_jane_continuity

@dataclass(frozen=True)
class JanePacket:
    goal:str
    now:tuple
    changed:tuple=()
    open_items:tuple=()
    receipts:tuple=()

def begin_turn(user_text, *, target, job, basis, authority=frozenset(),
               boundary=None, explicit_mode=None, observer_risk=None,
               episode_id="chat"):
    """Bind the entry contract and controller lease before substantive work."""
    binding=bind_entry_contract(
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
    if not entry_is_bound(binding):
        raise RuntimeError("ENTRY_CONTRACT_NOT_BOUND")
    return binding

def capability_disposition(blocker, tags=(), *, licensed=None, registry=None):
    """Return current capability-coverage disposition for the live blocker."""
    return coverage(str(blocker), tags, licensed=licensed)

def delegate_work(work_items,max_items=4):
    return plan_delegation(work_items,max_items=max_items)

def human_view(packet):
    return {
        "goal":packet.goal,
        "now":packet.now,
        "changed":packet.changed,
        "open":packet.open_items,
        "receipt_count":len(packet.receipts),
    }


def recover_turn_continuity(currentness, *, protected_behaviors=(), open_coordinates=(),
                            capability_gaps=(), evidence_refs=()):
    """Recover typed supervisory continuity context for a new turn.

    This exposes durable entry-state reconstruction through Jane's normal interface
    without granting Jane substantive controller authority.
    """
    packet=recover_continuity(
        currentness,
        protected_behaviors=protected_behaviors,
        open_coordinates=open_coordinates,
        capability_gaps=capability_gaps,
        evidence_refs=evidence_refs,
    )
    return packet,controller_context(packet)


def begin_icc128_turn(user_text, *, target, job, basis, currentness,
                      authority=frozenset(), boundary=None, explicit_mode=None,
                      observer_risk=None, episode_id="icc128-jane",
                      protected_behaviors=(), open_coordinates=(),
                      capability_gaps=(), evidence_refs=(), rejection_memory=None):
    """Bind the current ICC128 entry only after Jane continuity is READY.

    This guarded facade is for callers requiring durable cross-turn continuity.
    It does not grant Jane substantive selection, authenticate external host
    ingress, or replace the historical begin_turn compatibility interface.
    """
    packet, _ = recover_turn_continuity(
        currentness,
        protected_behaviors=protected_behaviors,
        open_coordinates=open_coordinates,
        capability_gaps=capability_gaps,
        evidence_refs=evidence_refs,
    )
    if packet.status != "READY":
        raise RuntimeError(
            "JANE_CONTINUITY_OPEN:" + ",".join(packet.missing)
        )
    for name, expected in (("target", target), ("job", job), ("basis", basis)):
        if getattr(packet, name) != str(expected):
            raise RuntimeError("JANE_CONTINUITY_IDENTITY_MISMATCH:" + name)

    binding = bind_icc128_entry_contract(
        user_text, target=target, job=job, basis=basis,
        authority=authority, boundary=boundary,
        explicit_mode=explicit_mode, observer_risk=observer_risk,
        episode_id=episode_id,
    )
    if not entry_is_bound(binding):
        raise RuntimeError("ICC128_ENTRY_CONTRACT_NOT_BOUND")
    handoff = bind_jane_continuity(packet, rejection_memory=rejection_memory)
    if handoff.status != "READY":
        raise RuntimeError("JANE_ICC128_HANDOFF_NOT_READY")
    return binding, handoff
