from endogenous_work import WorkItem,WorkKind,WorkStatus,activate,closure_status

def test_debt_is_typed_work_not_new_primitive():
    w=WorkItem("d1","repair drift",kind=WorkKind.DEBT,cost=2,risk=5,provenance=("legacy-debt",))
    assert w.kind is WorkKind.DEBT and w.provenance

def test_activation_requires_authority():
    w=WorkItem("x","do it",authority=("owner",))
    try:
        activate(w,"stranger")
        assert False
    except PermissionError:
        pass
    assert activate(w,"owner").status is WorkStatus.ACTIVE

def test_open_work_prevents_closure():
    w=WorkItem("t","transfer",kind=WorkKind.TRANSFER,target="P2")
    assert closure_status((w,),set()) is WorkStatus.ACTIVE


# Regression: identity/authority alone must not bypass backlog lifecycle state.
import pytest

@pytest.mark.parametrize("changes", [
    {"material": False},
    {"reachable": False},
    {"licensed": False},
    {"status": WorkStatus.BLOCKED},
    {"status": WorkStatus.PAUSED_OPEN},
    {"status": WorkStatus.CLOSED},
])
def test_activation_does_not_bypass_work_lifecycle(changes):
    work = WorkItem("item", "bounded backlog work", authority=("owner",), **changes)
    with pytest.raises(PermissionError):
        activate(work, "owner")
    assert work.status == changes.get("status", WorkStatus.CANDIDATE)


def test_activation_keeps_identity_and_is_idempotent_for_active_work():
    work = WorkItem("item", "bounded backlog work", authority=("owner",),
                    provenance=("source",), relations=("route",))
    active = activate(work, "owner")
    assert active.status is WorkStatus.ACTIVE
    assert active.work_id == work.work_id
    assert active.provenance == work.provenance
    assert active.relations == work.relations
    assert activate(active, "owner") == active
