import pytest
from evidence_ledger import EvidenceLedger

def test_availability_does_not_count_as_activation():
    l=EvidenceLedger(); l.register_identity("C01",program="C01")
    assert not l.readiness()["activation_evidence"]

def test_full_activation_counts():
    l=EvidenceLedger()
    l.record_activation(episode="e",program_id="C01",selected=True,bound=True,dispatched=True,started=True,executed=True,captured=True,consumed=True,evidence_ref="ci")
    assert l.activation_complete("e","C01")

def test_unconsumed_does_not_count():
    l=EvidenceLedger()
    l.record_activation(episode="e",program_id="C01",selected=True,bound=True,dispatched=True,started=True,executed=True,captured=True,consumed=False)
    assert not l.activation_complete("e","C01")

def test_historical_requires_witnesses():
    l=EvidenceLedger()
    l.record_reconstruction(historical_id="CAP001",successor_id="C01",frozen_job="j",predecessor_witness="",successor_witness="s",relation="same-result",disposition="PASS")
    assert not l.historically_reconstructed("CAP001")

def test_historical_pass_with_complete_witness():
    l=EvidenceLedger()
    l.record_reconstruction(historical_id="CAP001",successor_id="C01",frozen_job="j",predecessor_witness="p",successor_witness="s",relation="same-result",disposition="PASS")
    assert l.historically_reconstructed("CAP001")

def test_failed_validation_blocks_readiness_axis():
    l=EvidenceLedger(); l.validate("holdout","FAIL","x")
    assert not l.readiness()["no_failed_required_validation"]
