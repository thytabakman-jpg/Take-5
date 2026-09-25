from work_views import MigratedWork,WorkClass,validate_work,queue_view,activation_allowed

def test_backlog_never_self_authorizes_or_activates():
    w=MigratedWork("b",WorkClass.BACKLOG,False,False,None,("Reaserch/BACKLOG.yaml",))
    assert validate_work(w)
    assert not activation_allowed(w,False)

def test_invalid_authoritative_backlog_is_rejected():
    w=MigratedWork("b",WorkClass.BACKLOG,False,True,None,("src",))
    assert not validate_work(w)

def test_queue_is_view_not_priority():
    a=MigratedWork("a",WorkClass.BACKLOG,False,False,None,("src",))
    b=MigratedWork("b",WorkClass.DEBT,False,False,None,("src",))
    assert queue_view((a,b),WorkClass.BACKLOG)==(a,)
    assert a.priority is None
