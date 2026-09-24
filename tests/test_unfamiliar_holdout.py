from autonomous_observer import observe_records
from zero_request_episode import zero_request_episode

# Frozen after the generic observer was committed. Domain content was not used to design the observer.
HOLDOUT=[
 {"id":"M-17","name":"Aster","version":1,"refs":["M-18"]},
 {"id":"M-18","name":"Beryl","version":1,"refs":[]},
 {"id":"M-18","name":"Cairn","version":1,"refs":["M-99"]},
 {"id":"M-20","name":"Aster","version":2,"refs":[]},
]

def test_unfamiliar_record_holdout_discovers_three_independent_structural_defects():
    r=zero_request_episode(HOLDOUT,lambda corpus,binding: observe_records(corpus))
    assert r.complete
    types=[x["type"] for x in r.result["findings"]]
    assert types.count("DUPLICATE_ID")==1
    assert types.count("UNRESOLVED_REF")==1
    assert types.count("VERSION_PLURALITY")==1
    assert r.ledger.activation_complete("zero-request","DOS")
