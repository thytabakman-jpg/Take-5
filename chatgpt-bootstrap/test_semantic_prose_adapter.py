"""Fixture transport tests execute real native Prose, not a research audit."""
from pathlib import Path
import os,sys,json
import pytest
sys.path.insert(0,str(Path(os.environ['TAKE5_TEST_RUNTIME'])/'runtime'))
from direct_tool_command_gateway import execute_direct_tool_commands
from semantic_prose_adapter import bind_adapters

@pytest.fixture
def packet():return {'prose':{'text':'A test statement.','contract':{'contract_id':'fixture','constraints':['AFFIRMATIVE_FIRST']}}}

def test_unconfigured_fails_closed(packet,monkeypatch):
    monkeypatch.delenv('TAKE5_SEMANTIC_WORKER_CONFIG',raising=False)
    batch=execute_direct_tool_commands('run Prose',adapters=bind_adapters(packet))
    assert batch.status=='OPEN'

@pytest.fixture
def configured(tmp_path,monkeypatch):
    worker=tmp_path/'fixture.py'
    worker.write_text('''import json,sys\nr=json.load(sys.stdin); t=r['text']\nrows=[dict(projection_id=x,status='ANALYSED',analysis='fixture only',evidence=['fixture only'],source_spans=[dict(start=0,end=len(t),quote=t)]) for x in r['projection_ids']]\nprint(json.dumps(dict(worker_id='fixture',request_sha256=r['request_sha256'],target_sha256=r['target_sha256'],projections=rows,prose_evidence=dict(semantic_preservation='PASS',earned_claim_strength='PASS',no_unsupported_inflation='PASS',evidence=['fixture only']))))\n''')
    config=tmp_path/'config.json';config.write_text(json.dumps({'worker_id':'fixture','worker_command':[sys.executable,str(worker)]}))
    monkeypatch.setenv('TAKE5_SEMANTIC_WORKER_CONFIG',str(config))
    return worker

def test_fixture_reaches_real_native_prose(packet,configured):
    result=execute_direct_tool_commands('run Prose',adapters=bind_adapters(packet))
    assert result.status=='EXECUTED'
    e=result.executions[0]
    assert e.result['native_result']['status']=='PASS'
    assert e.recurrence_status=='RELATIVE_CLOSE'
    assert 'native:prose.assess_prose' in e.evidence
    assert len(e.result['semantic_coverage']['projections'])>=1008

def test_real_native_finding_not_suppressed(packet,configured):
    packet['prose']['text']='It is not merely a test.'
    result=execute_direct_tool_commands('run Prose',adapters=bind_adapters(packet))
    assert result.status=='EXECUTED'
    assert result.executions[0].result['native_result']['status']=='REPAIR_REQUIRED'

def test_bad_worker_identity(packet,configured):
    configured.write_text(configured.read_text().replace("worker_id='fixture'","worker_id='wrong'"))
    result=execute_direct_tool_commands('run Prose',adapters=bind_adapters(packet))
    assert result.status=='OPEN'
