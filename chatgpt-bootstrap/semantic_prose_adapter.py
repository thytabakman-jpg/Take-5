"""Optional native Prose binding for a separately provisioned semantic worker.

No worker is bundled. No packet-supplied command, network call, self-signing,
synthetic semantic assessment, or automatic coverage promotion is permitted.
"""
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import subprocess
from prose import ProseContract, ProseEvidence, assess_prose
from semantic_coverage import canonical, projection_ids, verify_rows


def bind_adapters(packet):
    def invoke(current, plan):
        def opened(reason):
            return {'status':'OPEN','execution_truth':'OPEN','material_delta':False,'blocker':reason}
        config_path = os.environ.get('TAKE5_SEMANTIC_WORKER_CONFIG')
        if not config_path:
            return opened('SEMANTIC_WORKER_NOT_PROVISIONED')
        spec = packet.get('prose')
        if not isinstance(spec,dict) or not isinstance(spec.get('text'),str) or not spec['text'].strip():
            return opened('PROSE_TEXT_AND_CONTRACT_REQUIRED')
        text = spec['text']
        contract = ProseContract(**spec['contract'])
        text_sha = hashlib.sha256(text.encode('utf-8')).hexdigest()
        config = json.loads(Path(config_path).read_text())
        command = config.get('worker_command')
        if not isinstance(command,list) or not command or not all(isinstance(x,str) and x for x in command) or not config.get('worker_id'):
            return opened('SEMANTIC_WORKER_CONFIGURATION_INVALID')
        expected = projection_ids(plan)
        request = {'schema':'TAKE5_PROSE_WORKER_V1','tool_id':'Prose','target_sha256':text_sha,'text':text,'contract':asdict(contract),'projection_ids':sorted(expected),'mode':'OBSERVER'}
        request_sha = hashlib.sha256(canonical(request)).hexdigest()
        request['request_sha256'] = request_sha
        proc = subprocess.run(command,input=json.dumps(request,ensure_ascii=False),text=True,capture_output=True,timeout=120)
        if proc.returncode:
            return opened('SEMANTIC_WORKER_EXECUTION_FAILED')
        response = json.loads(proc.stdout)
        if response.get('worker_id')!=config['worker_id'] or response.get('request_sha256')!=request_sha or response.get('target_sha256')!=text_sha:
            return opened('SEMANTIC_WORKER_RESPONSE_IDENTITY_MISMATCH')
        rows = response.get('projections')
        verify_rows(rows,expected,text)
        evidence = ProseEvidence(**response['prose_evidence'])
        required = [evidence.semantic_preservation,evidence.earned_claim_strength,evidence.no_unsupported_inflation]
        if 'READER_LOAD' in contract.constraints:
            required.append(evidence.reader_load)
            if not evidence.reader_load_evidence:return opened('READER_LOAD_EVIDENCE_REQUIRED')
        if 'PLAIN_LANGUAGE' in contract.constraints:
            required.append(evidence.plain_language)
            if not evidence.plain_language_evidence:return opened('PLAIN_LANGUAGE_EVIDENCE_REQUIRED')
        if not evidence.evidence or any(str(x).upper() not in ('PASS','FAIL','REPAIR_REQUIRED') for x in required):
            return opened('PROSE_SEMANTIC_JUDGMENTS_UNRESOLVED')
        result = assess_prose(text,contract,evidence=evidence)
        # A native defect is a finding, not an execution failure. Preserve any
        # unresolved semantic residual rather than declaring a successful run.
        closed = result.status=='PASS' or (result.status=='REPAIR_REQUIRED' and set(result.residuals)=={'PROTECTED_PROSE_CONSTRAINT_VIOLATED'} and all(str(x).upper()=='PASS' for x in required[:3]))
        return {'status':'EXECUTED' if closed else ('BLOCKED' if result.status=='BLOCKED' else 'OPEN'),
                'execution_truth':'IMPLEMENTATION_EXECUTED' if closed else ('BLOCKED' if result.status=='BLOCKED' else 'OPEN'),
                'result':{'native_result':asdict(result),'semantic_coverage':{'target_sha256':text_sha,'worker_id':config['worker_id'],'projections':rows},'worker_request_sha256':request_sha,'worker_response_sha256':hashlib.sha256(canonical(response)).hexdigest(),'worker_evidence':asdict(evidence)},
                'evidence':['native:prose.assess_prose','worker-request:'+request_sha],
                'material_delta':False,'blocker':None if closed else 'PROSE_NATIVE_ASSESSMENT_UNRESOLVED'}
    return {'Prose':invoke}
