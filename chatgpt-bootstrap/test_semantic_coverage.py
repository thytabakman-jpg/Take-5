"""Engineering tests only. Synthetic signed receipts do not certify research."""
import copy
import json
import os
from pathlib import Path
import sys
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from semantic_coverage import verify_coverage, CoverageBlocked, canonical, digest, projection_ids

RUNTIME=Path(os.environ['TAKE5_TEST_RUNTIME'])
sys.path.insert(0,str(RUNTIME/'runtime'))
from global_tool_execution import build_tool_execution_plan
from tool_run_registry import CONFIGURED_RUNS
from improvement_core_tool_bridge import ConfiguredToolBinding

@pytest.fixture
def sample(tmp_path):
    target=tmp_path/'target.md';target.write_text('An explicit test sentence.')
    packet=tmp_path/'packet.json';packet.write_text('{}')
    native=tmp_path/'native.json'; cert=tmp_path/'certificate.json'; trust=tmp_path/'trust.json'
    worker, reviewer = Ed25519PrivateKey.generate(), Ed25519PrivateKey.generate()
    def pub(k):return k.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw).hex()
    trust.write_text(json.dumps({'worker_id':'test-worker','reviewer_id':'test-reviewer','worker_public_key':pub(worker),'reviewer_public_key':pub(reviewer)}))
    plan=build_tool_execution_plan(CONFIGURED_RUNS['PD'])
    rows=[{'projection_id':p,'status':'ANALYSED','analysis':'fixture only','evidence':['test only'],'source_spans':[{'start':0,'end':len(target.read_text()),'quote':target.read_text()}]} for p in sorted(projection_ids(plan))]
    execution={'tool_id':'PD','status':'EXECUTED','execution_truth':'IMPLEMENTATION_EXECUTED','recurrence_status':'RELATIVE_CLOSE','binding':ConfiguredToolBinding('PD',plan).summary,'evidence':['native:pd.run_pd'],'result':{'native_result':{},'semantic_coverage':{'target_sha256':digest(target),'worker_id':'test-worker','projections':rows}}}
    receipt={'source_commit':RUNTIME.name,'packet_sha256':digest(packet),'tool_ids':['PD'],'results':[{'status':'EXECUTED','executions':[execution]}]}
    def sign():
        native.write_text(json.dumps(receipt))
        payload={'schema':'TAKE5_SEMANTIC_COVERAGE_V1','worker_id':'test-worker','reviewer_id':'test-reviewer','review_status':'VERIFIED','independence_basis':'test keys only','review_method':'fixture only','source_commit':RUNTIME.name,'target_sha256':digest(target),'packet_sha256':digest(packet),'native_receipt_sha256':digest(native),'tool_ids':['PD']}
        cert.write_text(json.dumps({'payload':payload,'worker_signature':worker.sign(canonical(payload)).hex(),'reviewer_signature':reviewer.sign(canonical(payload)).hex()}))
    def verify():return verify_coverage(runtime=RUNTIME,native_receipt=native,target=target,packet=packet,expected_tools={'PD'},commit=RUNTIME.name,certificate=cert,trust_config=trust)
    sign()
    return execution, rows, sign, verify, target, cert, trust, native

def test_full_signed_fixture(sample):
    assert sample[3]() ['status']=='ATTESTED_COVERAGE_VERIFIED'

def test_missing_projection(sample):
    sample[1].pop();sample[2]()
    with pytest.raises(CoverageBlocked,match='PROJECTION_COVERAGE_INCOMPLETE'):sample[3]()

def test_duplicate_projection(sample):
    sample[1].append(copy.deepcopy(sample[1][0]));sample[2]()
    with pytest.raises(CoverageBlocked,match='PROJECTION_UNKNOWN_OR_DUPLICATE'):sample[3]()

def test_quote_mismatch(sample):
    sample[1][0]['source_spans'][0]['quote']='wrong';sample[2]()
    with pytest.raises(CoverageBlocked,match='SOURCE_QUOTATION_MISMATCH'):sample[3]()

def test_document_gap(sample):
    for row in sample[1]: row['source_spans']=[{'start':0,'end':2,'quote':'An'}]
    sample[2]()
    with pytest.raises(CoverageBlocked,match='DOCUMENT_SEMANTIC_SPAN_GAP'):sample[3]()

def test_open_native_run(sample):
    sample[0]['recurrence_status']='OPEN';sample[2]()
    with pytest.raises(CoverageBlocked,match='NATIVE_EXECUTION_NOT_CLOSED'):sample[3]()

def test_bounded_native_result(sample):
    del sample[0]['result']['semantic_coverage'];sample[2]()
    with pytest.raises(CoverageBlocked,match='NATIVE_SEMANTIC_EVIDENCE_MISSING'):sample[3]()

def test_tampered_target(sample):
    sample[4].write_text('changed')
    with pytest.raises(CoverageBlocked,match='COVERAGE_ATTESTATION_BINDING_MISMATCH'):sample[3]()

def test_forged_signature(sample):
    path=sample[5];data=json.loads(path.read_text());data['reviewer_signature']='00'*64;path.write_text(json.dumps(data))
    with pytest.raises(CoverageBlocked,match='ATTESTATION_SIGNATURE_INVALID'):sample[3]()

def test_same_key(sample):
    path=sample[6];data=json.loads(path.read_text());data['reviewer_public_key']=data['worker_public_key'];path.write_text(json.dumps(data))
    with pytest.raises(CoverageBlocked,match='REVIEWER_NOT_INDEPENDENT'):sample[3]()

def test_receipt_tamper(sample):
    sample[7].write_text(sample[7].read_text()+' ')
    with pytest.raises(CoverageBlocked,match='COVERAGE_ATTESTATION_BINDING_MISMATCH'):sample[3]()
