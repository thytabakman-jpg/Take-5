"""Jane integrated interface over Take-5 control services.

Jane is the user-facing interface/facade. Conversation entry is bound here
before substantive controller work so controller identity and initial mode do
not drift inside the host layer.
"""
from dataclasses import dataclass
from capability_router import coverage
from delegation_officer import plan_delegation
from entry_contract import bind_entry_contract, entry_is_bound

@dataclass(frozen=True)
class JanePacket:
    goal:str
    now:tuple
    changed:tuple=()
    open_items:tuple=()
    receipts:tuple=()

def begin_turn(user_text, *, target, job, basis, authority=frozenset(),
               boundary=None, explicit_mode=None, episode_id="chat"):
    """Bind the entry contract and controller lease before substantive work."""
    binding=bind_entry_contract(
        user_text,
        target=target,
        job=job,
        basis=basis,
        authority=authority,
        boundary=boundary,
        explicit_mode=explicit_mode,
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
