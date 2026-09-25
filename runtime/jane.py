"""Jane integrated interface over Take-5 control services.

Jane is a user-facing system role, not a new authority class.
"""
from dataclasses import dataclass
from capability_router import cover_capabilities
from delegation_officer import plan_delegation

@dataclass(frozen=True)
class JanePacket:
    goal:str
    now:tuple
    changed:tuple=()
    open_items:tuple=()
    receipts:tuple=()

def capability_disposition(blocker,registry=None):
    return cover_capabilities(blocker)

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
