from controller_episode import run_episode

def test_controller_episode_complete_only_after_worker_return_consumed():
    def worker(binding):
        return {"program":binding.program_id,"target":binding.target_id}
    r=run_episode(episode="e1",program_id="C01",target_id="x",job="type",authority=frozenset({"observe"}),worker=worker)
    assert r.complete
    assert r.ledger.activation_complete("e1","C01")

def test_worker_failure_is_captured_but_not_activation_complete():
    def worker(binding):
        raise RuntimeError("boom")
    r=run_episode(episode="e2",program_id="C01",target_id="x",job="type",authority=frozenset({"observe"}),worker=worker)
    assert not r.complete
    assert r.result["error"]=="RuntimeError"
    assert not r.ledger.activation_complete("e2","C01")
