from adaptive_response_selector import ResponseCandidate, ResponseState, choose, update_rejection

def c(cid, fmt="math-only", exact=True, complete=True, unsupported=0, drift=0, extra=0):
    return ResponseCandidate(cid,"target-equation",fmt,exact,complete,unsupported,drift,extra)

def test_shortest_admissible_wins():
    z=ResponseState("target-equation","math-only")
    out=choose((c("long",extra=40),c("short",extra=0)),z)
    assert tuple(x.candidate_id for x in out)==("short",)

def test_wrong_format_is_inadmissible():
    z=ResponseState("target-equation","math-only")
    assert choose((c("prose",fmt="report"),),z)==()

def test_abstraction_drift_is_inadmissible():
    z=ResponseState("target-equation","math-only")
    assert choose((c("drift",drift=1),),z)==()

def test_rejection_memory_blocks_repeat():
    z=update_rejection(ResponseState("target-equation","math-only"),candidate_id="bad")
    assert choose((c("bad"),),z)==()

def test_rejected_format_blocks_repackaged_failure():
    z=update_rejection(ResponseState("target-equation","math-only"),format_id="math-only")
    assert choose((c("renamed"),),z)==()
