from zero_request_episode import zero_request_episode

def test_zero_request_runs_observation_only_and_consumes_result():
    seen={}
    def observer(corpus,binding):
        seen["obs"]=binding.observation_only
        seen["authority"]=binding.authority_out
        return {"objects":len(corpus),"structural":["boundary"]}
    r=zero_request_episode(["a","b"],observer)
    assert r.complete
    assert seen["obs"] is True
    assert seen["authority"]==frozenset({"observe"})
    assert r.result["structural"]==["boundary"]
    assert r.ledger.activation_complete("zero-request","DOS")
