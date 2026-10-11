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


from endogenous_work import select_work

@pytest.mark.parametrize("status", [WorkStatus.PAUSED_OPEN, WorkStatus.BLOCKED, WorkStatus.CLOSED])
def test_select_work_never_selects_paused_or_terminal_items(status):
    work = WorkItem("paused", "deferred", authority=("owner",), status=status)
    assert select_work([work]).selected == ()


def test_select_work_retains_candidate_and_active():
    candidate = WorkItem("candidate", "new task", status=WorkStatus.CANDIDATE)
    active = WorkItem("active", "continuing task", status=WorkStatus.ACTIVE)
    assert select_work([candidate, active]).selected == (candidate, active)


@pytest.mark.parametrize("status,expected", [
    (WorkStatus.BLOCKED, WorkStatus.BLOCKED),
    (WorkStatus.PAUSED_OPEN, WorkStatus.PAUSED_OPEN),
    (WorkStatus.CANDIDATE, WorkStatus.ACTIVE),
    (WorkStatus.ACTIVE, WorkStatus.ACTIVE),
    (WorkStatus.CLOSED, WorkStatus.CLOSED),
])
def test_closure_status_respects_remaining_work_lifecycle(status, expected):
    work = WorkItem("entry", "still owned", status=status)
    assert closure_status((work,), ()) is expected


def test_runnable_work_remains_active_despite_other_blocked_entries():
    blocked = WorkItem("blocked", "pending", status=WorkStatus.BLOCKED)
    candidate = WorkItem("candidate", "runnable", status=WorkStatus.CANDIDATE)
    assert closure_status((blocked, candidate), ()) is WorkStatus.ACTIVE


def test_explicit_blocked_episode_still_overrides_runnable_work():
    work = WorkItem("active", "work", status=WorkStatus.ACTIVE)
    assert closure_status((work,), (), blocked=True) is WorkStatus.BLOCKED


def test_discharge_and_open_coordinates_preserve_previous_terminal_rules():
    work = WorkItem("done", "complete")
    assert closure_status((work,), ("done",)) is WorkStatus.CLOSED
    assert closure_status((work,), ("done",), open_coordinates=("review",)) is WorkStatus.PAUSED_OPEN
