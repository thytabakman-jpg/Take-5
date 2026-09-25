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
