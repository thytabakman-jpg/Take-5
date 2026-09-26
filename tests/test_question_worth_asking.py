from question_worth_asking import QuestionCandidate, dominates, select_question

def q(i,rs,ig,du,a,c,r,b=False):
    return QuestionCandidate(i,i,rs,ig,du,a,c,r,b)

def test_dominant_question_wins():
    weak=q("weak",.3,.3,.3,.3,.5,.5)
    strong=q("strong",.8,.8,.8,.8,.2,.2)
    x=select_question([weak,strong])
    assert x.status=="SELECTED" and x.selected[0].question_id=="strong"

def test_dominated_question_not_frontier():
    weak=q("weak",.3,.3,.3,.3,.5,.5)
    strong=q("strong",.8,.8,.8,.8,.2,.2)
    assert dominates(strong,weak)
    assert [x.question_id for x in select_question([weak,strong]).frontier]==["strong"]

def test_tie_preserved():
    a=q("a",.5,.5,.5,.5,.2,.2)
    b=q("b",.5,.5,.5,.5,.2,.2)
    x=select_question([a,b])
    assert x.status=="TIE" and {y.question_id for y in x.selected}=={"a","b"}

def test_blocked_visible_not_selected():
    blocked=q("blocked",1,1,1,1,0,0,True)
    live=q("live",.2,.2,.2,.2,.2,.2)
    x=select_question([blocked,live])
    assert x.selected[0].question_id=="live"
    assert x.blocked[0].question_id=="blocked"

def test_all_blocked_open():
    x=select_question([q("b",1,1,1,1,0,0,True)])
    assert x.status=="OPEN" and not x.selected

def test_zero_cost_defined():
    x=select_question([q("free",.5,.5,.5,.5,0,0)])
    assert x.selected[0].worth==2.0

def test_empty():
    assert select_question([]).status=="EMPTY"
