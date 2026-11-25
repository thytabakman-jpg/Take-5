#!/usr/bin/env python3
"""Read-only launcher for Take-5's authoritative packet runner, not a semantic adapter.
Records actual subprocess invocation, target/packet digests and observed receipts.
The host must establish packet-to-target semantic provenance and current Git SHA.
"""
import argparse, hashlib, json, subprocess, sys, uuid
from datetime import datetime, timezone
from pathlib import Path

DOCUMENT_PROVIDER_TOOLS = frozenset({'GDOS','Discriminator','BiasPerturbation','Architecture','MultiObject','GOAL','CurrentnessAudit','Reconciler','MT','Diagnosis','RTC','ASSERT','TRC'})
DOCUMENT_PROVIDER_FIELDS = frozenset({'sources','expected_ids','matrix','threshold','open_coordinates'})
MATRIX_FIELDS = frozenset({'axes','raw','transfer_fnv','declared_counts','exclusive_axis'})
THRESHOLD_FIELDS = frozenset({'values','lower','upper','baseline_probes','declared_pair_count','proof','proof_fnv'})
ADAPTER_URL = 'https://github.com/thytabakman-jpg/Take-5/blob/chatgpt-runtime-bootstrap/chatgpt-bootstrap/document_adapters.py'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def git_blob_sha(p):
    raw=p.read_bytes()
    return hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()

def resolve_adapter(runner, supplied, expected, packet, record):
    required=sorted(expected & DOCUMENT_PROVIDER_TOOLS)
    if supplied is not None:
        path=supplied.resolve()
        record['adapter_selection']='explicit native adapter'
    elif required:
        path=runner.resolve().parent/'document_adapters.py'
        record['adapter_selection']='authoritative sibling document adapter'
    else:
        record['adapter_selection']='built-in packet bindings only'
        return None
    record['adapter_path']=str(path)
    record['adapter_required_tools']=required
    record['authoritative_document_adapter_url']=ADAPTER_URL
    if not path.is_file():
        raise RuntimeError(f'REQUIRED_NATIVE_ADAPTER_MISSING: {path}; source: {ADAPTER_URL}; tools: {required}')
    record['adapter_git_blob_sha']=git_blob_sha(path)
    record['adapter_sha256']=sha(path)
    if path.name=='document_adapters.py' and required:
        absent=sorted(DOCUMENT_PROVIDER_FIELDS-set(packet))
        if not absent:
            for key, fields in [('matrix',MATRIX_FIELDS),('threshold',THRESHOLD_FIELDS)]:
                value=packet[key]
                if not isinstance(value,dict): absent.append(key+':mapping required')
                else: absent.extend(key+'.'+x for x in sorted(fields-set(value)))
        if absent:
            raise RuntimeError(f'NATIVE_ADAPTER_INPUT_CONTRACT_UNSATISFIED: {path}; tools: {required}; missing or invalid: {absent}; no fabricated input permitted')
    return path
def write(p, obj): p.write_text(json.dumps(obj, indent=2, default=str)+'\n')
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('bootstrap-receipt','runner','packet','target','output-dir'):
        p.add_argument('--'+k,required=True,type=Path)
    p.add_argument('--current-commit',required=True)
    p.add_argument('--target-id',required=True)
    p.add_argument('--mode',choices=['recommendation-only','repair'],required=True)
    p.add_argument('--adapter-module',type=Path)
    p.add_argument('--coverage-trust-config',type=Path,help='Trusted local deployment configuration (not target or packet data)')
    p.add_argument('--expected-tools',required=True,help='Comma-separated canonical applicable tool IDs for this packet')
    a=p.parse_args(); out=a.output_dir.resolve()/uuid.uuid4().hex; out.mkdir(parents=True,exist_ok=False)
    record={'started_at':datetime.now(timezone.utc).isoformat(),'target_id':a.target_id,'target_sha256':sha(a.target),'packet_sha256':sha(a.packet),'mode':a.mode,'current_commit':a.current_commit,'status':'NOT_ATTEMPTED','semantic_coverage':'NOT_CERTIFIED','target_binding':'byte identity only; semantic provenance requires separate evidence'}
    manifest=out/'execution.json'
    try:
        boot=json.loads(a.bootstrap_receipt.read_text()); runtime=Path(boot['runtime_path']).resolve()
        smoke=boot['smoke']; assert boot['status']=='BOOTSTRAP_VERIFIED' and boot['source_commit']==a.current_commit==runtime.name and runtime.is_dir() and smoke['returncode']==0 and smoke['registry_returncode']==0, 'runtime verification or current revision mismatch'
        record['bootstrap_receipt_sha256']=sha(a.bootstrap_receipt)
        record['bootstrap_tests']=smoke['stdout']; record['bootstrap_provenance']='verified receipt supplied for matching runtime; not a claim tests were rerun by this launcher'
        receipt=out/'native.json'
        cmd=[sys.executable,str(a.runner.resolve()),'--runtime',str(runtime),'--packet',str(a.packet.resolve()),'--receipt',str(receipt)]
        expected={x.strip() for x in a.expected_tools.split(',') if x.strip()}
        packet=json.loads(a.packet.read_text())
        adapter=resolve_adapter(a.runner,a.adapter_module,expected,packet,record)
        if adapter: cmd+=['--adapter-module',str(adapter)]
        record['command']=cmd; record['runner_sha256']=sha(a.runner); record['status']='ATTEMPTED'; write(manifest,record)
        proc=subprocess.run(cmd,capture_output=True,text=True,timeout=180)
        (out/'stdout.txt').write_text(proc.stdout); (out/'stderr.txt').write_text(proc.stderr)
        record['returncode']=proc.returncode
        if not receipt.exists(): raise RuntimeError('No native receipt produced; see subprocess logs')
        r=json.loads(receipt.read_text())
        if r.get('source_commit')!=a.current_commit or r.get('packet_sha256')!=record['packet_sha256']: raise RuntimeError('Native receipt identity mismatch')
        if adapter:
            provider=r.get('adapter_module') or {}
            if provider.get('sha256')!=record['adapter_sha256'] or Path(provider.get('path','')).resolve()!=adapter:
                raise RuntimeError('NATIVE_ADAPTER_RECEIPT_IDENTITY_MISMATCH')
            record['adapter_binding_verified']=True
        record['receipt_sha256']=sha(receipt); record['tools']=[]
        for tool in r.get('tool_ids',[]):
            rows=[e for result in r.get('results',[]) for e in result.get('executions',[]) if e.get('tool_id')==tool]
            for e in rows:
                b=e.get('binding') or {}; advanced=(b.get('invocation_profile')=='FULL_CONFIGURED_HF2_V1' and b.get('geometry')=='D36_C' and b.get('cell_count')==36 and b.get('question_count')==792 and b.get('cognitive_count')==144 and b.get('wrapper_required') is True and b.get('mode')=='OBSERVER' and b.get('recurrence_engine')==('SELF' if tool=='HF002' else 'HF002'))
                native_evidence=[x for x in e.get('evidence',[]) if isinstance(x,str) and x.startswith('native:')]
                record['tools'].append({'tool':tool,'advanced_binding':advanced,'native_evidence':native_evidence,'execution_truth':e.get('execution_truth'),'status':e.get('status'),'recurrence_status':e.get('recurrence_status'),'recurrence_rounds':e.get('recurrence_rounds'),'full_semantic_coverage':'NOT_CERTIFIED'})
            if not rows:
                batches=[x for x in r.get('results',[]) if tool in (x.get('state',{}).get('direct_tool_ids') or []) or x.get('tool_id')==tool]
                record['tools'].append({'tool':tool,'status':'NO_EXECUTION_ROW','native_evidence':[], 'gateway_dispositions':[{'status':x.get('status'),'blocker':x.get('blocker')} for x in batches]})
        # Only an independent, configured reviewer can admit actual per-projection native evidence.
        # The default path remains fail-closed; bounded receipts cannot be certified.
        if a.coverage_trust_config:
            from semantic_coverage import verify_coverage
            trust_path=a.coverage_trust_config.resolve()
            trust=json.loads(trust_path.read_text())
            command=trust.get('review_command')
            if not isinstance(command,list) or not command or not all(isinstance(x,str) and x for x in command):
                raise RuntimeError('TRUSTED_COVERAGE_REVIEW_COMMAND_REQUIRED')
            cert=out/'coverage-attestation.json'
            review=subprocess.run(command+['--native-receipt',str(receipt),'--target',str(a.target.resolve()),'--packet',str(a.packet.resolve()),'--source-commit',a.current_commit,'--output',str(cert)],capture_output=True,text=True,timeout=180)
            (out/'coverage-review-stdout.txt').write_text(review.stdout)
            (out/'coverage-review-stderr.txt').write_text(review.stderr)
            if review.returncode or not cert.is_file(): raise RuntimeError('INDEPENDENT_COVERAGE_REVIEW_FAILED')
            if sha(receipt)!=record['receipt_sha256'] or sha(a.packet)!=record['packet_sha256'] or sha(a.target)!=record['target_sha256']: raise RuntimeError('FROZEN_EXECUTION_EVIDENCE_CHANGED_DURING_REVIEW')
            verified=verify_coverage(runtime=runtime,native_receipt=receipt,target=a.target,packet=a.packet,expected_tools=expected,commit=a.current_commit,certificate=cert,trust_config=trust_path)
            record['coverage_attestation']=verified
            record['semantic_coverage']='CERTIFIED'
            for row in record['tools']:
                if row['tool'] in verified['projections_by_tool']:
                    row['full_semantic_coverage']='CERTIFIED'
                    row['verified_projection_count']=verified['projections_by_tool'][row['tool']]
        record['target_unchanged']=sha(a.target)==record['target_sha256']
        expected={x.strip() for x in a.expected_tools.split(',') if x.strip()}
        observed=set(r.get('tool_ids',[]))
        blockers=[]
        if not expected or expected!=observed: blockers.append(f'TOOL_INVENTORY_MISMATCH: expected={sorted(expected)} observed={sorted(observed)}')
        if proc.returncode: blockers.append(f'NATIVE_RUNNER_EXIT:{proc.returncode}')
        if not record['target_unchanged']: blockers.append('TARGET_CHANGED_DURING_READ_ONLY_EXECUTION')
        for tool in sorted(expected):
            rows=[e for e in record['tools'] if e['tool']==tool]
            if not rows: blockers.append(f'{tool}:MISSING_EXECUTION_ROW'); continue
            for e in rows:
                if not e.get('advanced_binding'): blockers.append(f'{tool}:ADVANCED_BINDING_UNVERIFIED')
                if not e.get('native_evidence'): blockers.append(f'{tool}:NATIVE_EXECUTION_UNVERIFIED')
                if e.get('recurrence_status') not in ('RELATIVE_CLOSE','SELF_CLOSE'): blockers.append(f'{tool}:RECURRENCE_UNVERIFIED')
                # The authoritative packet runner explicitly scopes its receipt to bounded
                # execution. No full semantic coverage certificate schema is established.
                # Never infer such a certificate from a host-provided label or plan counts.
                if e.get('full_semantic_coverage')!='CERTIFIED': blockers.append(f'{tool}:FULL_SEMANTIC_COVERAGE_UNVERIFIED')
        record['blockers']=list(dict.fromkeys(blockers))
        record['status']='PD-SAR_FAILED' if blockers else 'STRICT_NATIVE_VERIFIED'
        record['completion']='FAILED_CLOSED' if blockers else 'STRICT_GATE_PASSED' 
    except Exception as e:
        record['error']=str(e); record['prior_status']=record['status']; record['status']='PD-SAR_FAILED'; record['completion']='FAILED_CLOSED'
    finally:
        write(manifest,record); print(manifest); print(json.dumps(record,indent=2))
    return int(record['status']!='STRICT_NATIVE_VERIFIED' or not record.get('target_unchanged'))
if __name__=='__main__': sys.exit(main())
