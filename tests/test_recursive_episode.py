from recursive_episode import (
    ClosureResult, RoundResult, Terminal, run_recursive_episode
)

def test_closure_runs_before_reentry_and_material_delta_continues():
    events=[]
    def round_fn(s):
        events.append(("round",s))
        return RoundResult(s+1,result_delta=s<1)
    def closure_fn(s,r):
        events.append(("close",r.value))
        return ClosureResult("CLOSED")
    def update_fn(s,r,c):
        events.append(("update",r.value))
        return r.value
    def terminal_fn(s,r,c):
        return Terminal.RELATIVE_CLOSE if s>=2 else Terminal.CONTINUE

    state,receipt=run_recursive_episode(
        0,round_fn=round_fn,closure_fn=closure_fn,update_fn=update_fn,
        terminal_fn=terminal_fn,max_rounds=4
    )
    assert state==2
    assert receipt.terminal==Terminal.RELATIVE_CLOSE
    assert events[:3]==[("round",0),("close",1),("update",1)]

def test_external_challenge_can_reopen_after_same_basis_close():
    challenge_used=[]
    def round_fn(s):
        return RoundResult(s,result_delta=False)
    def closure_fn(s,r):
        return ClosureResult("CLOSED")
    def update_fn(s,r,c):
        return s + (1 if r.result_delta else 0)
    def terminal_fn(s,r,c):
        return Terminal.RELATIVE_CLOSE
    def challenge_fn(s):
        challenge_used.append(True)
        return RoundResult(s+1,result_delta=True)

    state,receipt=run_recursive_episode(
        0,round_fn=round_fn,closure_fn=closure_fn,update_fn=update_fn,
        terminal_fn=terminal_fn,challenge_fn=challenge_fn,max_rounds=3
    )
    assert challenge_used
    assert receipt.external_challenge_used
    assert state>=1

def test_open_closure_stops_without_update():
    updated=[]
    def round_fn(s):
        return RoundResult("x",result_delta=True)
    def closure_fn(s,r):
        return ClosureResult("OPEN")
    def update_fn(s,r,c):
        updated.append(True)
        return s
    def terminal_fn(s,r,c):
        return Terminal.CONTINUE

    state,receipt=run_recursive_episode(
        0,round_fn=round_fn,closure_fn=closure_fn,update_fn=update_fn,
        terminal_fn=terminal_fn
    )
    assert state==0
    assert receipt.terminal==Terminal.OPEN
    assert not updated
