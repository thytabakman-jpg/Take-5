from configured_run import ConfiguredRunSpec,validate_specs
from mode_centers import reconcile,discriminate,delegated_execute
from emergent_admission import ObjectCandidate,Admission,admit
from foundation_snapshot import self_contained

def test_configured_run_identity_requires_closure_and_reentry():
    s=ConfiguredRunSpec("MTA",True,True,True,"WHEN_STRONG_CLAIM")
    assert s.complete() and validate_specs([s])

def test_reconciler_preserves_common_conflict_and_provenance():
    r=reconcile([{"a":1,"b":2},{"a":1,"b":3}])
    assert r["common"]=={"a":1}
    assert "b" in r["conflicts"] and len(r["provenance"])==2

def test_discriminator_preserves_plural_and_open():
    assert discriminate([1,2,3],lambda x:x>1)["status"]=="PLURAL"
    assert discriminate([1,2],lambda x:x>9)["status"]=="OPEN"

def test_delegated_executor_returns_specialist_output_unmodified():
    r=delegated_execute(lambda x:{"specialist":x["x"]+1},{"x":1})
    assert r.output=={"specialist":2} and r.preserved

def test_emergent_object_cannot_claim_execution_without_binding():
    o=ObjectCandidate("NEW","PROGRAM",True,executable_claim=True,bound=False)
    assert admit(o)==Admission.OPEN

def test_takeover_foundation_has_no_predecessor_runtime_dependency():
    assert self_contained()
