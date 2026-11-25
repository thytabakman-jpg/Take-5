"""Fail-closed semantic-coverage admission for Take-5 native packet receipts.

This verifies evidence identity, exact projection coverage and separately trusted
attestations. It does not supply a semantic worker or establish scholarly truth.
Private source, evidence and signing keys stay outside the repository.
"""
import hashlib
import json
from pathlib import Path
import sys
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


class CoverageBlocked(ValueError):
    pass


def require(ok, code):
    if not ok:
        raise CoverageBlocked(code)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def projection_ids(plan):
    def key(kind, name, cell):
        return ':'.join((kind, name, cell.scope.value, cell.mode_face.value))
    return ({key('CELL', 'D36_C', c) for c in plan.cells}
            | {key('NATIVE', name, c) for name, c in plan.native}
            | {key('QUESTION', name, c) for name, c in plan.questions}
            | {key('COGNITIVE', name, c) for name, c in plan.cognitive})


def verify_signature(payload, signature, public_key):
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key)).verify(
            bytes.fromhex(signature), canonical(payload))
    except Exception as exc:
        raise CoverageBlocked('ATTESTATION_SIGNATURE_INVALID') from exc


def verify_rows(rows, expected, text):
    require(isinstance(rows, list), 'PROJECTION_ROWS_REQUIRED')
    seen, ranges = set(), []
    for row in rows:
        identity = row.get('projection_id')
        require(identity in expected and identity not in seen, 'PROJECTION_UNKNOWN_OR_DUPLICATE')
        seen.add(identity)
        require(row.get('status') in ('ANALYSED', 'NOT_APPLICABLE'), 'PROJECTION_UNRESOLVED')
        require(isinstance(row.get('analysis'), str) and bool(row['analysis'].strip()), 'PROJECTION_ANALYSIS_REQUIRED')
        evidence = row.get('evidence')
        require(isinstance(evidence, list) and bool(evidence) and all(isinstance(x, str) and x.strip() for x in evidence), 'PROJECTION_EVIDENCE_REQUIRED')
        spans = row.get('source_spans')
        require(isinstance(spans, list) and bool(spans), 'PROJECTION_SOURCE_SPANS_REQUIRED')
        for span in spans:
            start, end, quote = span['start'], span['end'], span['quote']
            require(type(start) is int and type(end) is int and 0 <= start < end <= len(text), 'SOURCE_SPAN_INVALID')
            require(quote == text[start:end], 'SOURCE_QUOTATION_MISMATCH')
            ranges.append((start, end))
    require(seen == expected, 'PROJECTION_COVERAGE_INCOMPLETE')
    end = 0
    for lo, hi in sorted(ranges):
        require(lo <= end or not text[end:lo].strip(), 'DOCUMENT_SEMANTIC_SPAN_GAP')
        end = max(end, hi)
    require(not text[end:].strip(), 'DOCUMENT_SEMANTIC_SPAN_GAP')
    return len(seen)


def verify_coverage(*, runtime, native_receipt, target, packet, expected_tools, commit, certificate, trust_config):
    """Verify exact native results and signed external evidence; never self-certify.

    trust_config must be provisioned by a trusted deployment, not the packet author.
    Signatures authenticate attestations, not the actual intellectual correctness.
    The independent reviewer must examine the real native projection evidence.
    """
    runtime = Path(runtime).resolve()
    require(runtime.name == commit, 'RUNTIME_IDENTITY_MISMATCH')
    sys.path.insert(0, str(runtime / 'runtime'))
    from global_tool_execution import build_tool_execution_plan
    from tool_run_registry import CONFIGURED_RUNS
    trust = json.loads(Path(trust_config).read_text())
    cert = json.loads(Path(certificate).read_text())
    payload = cert['payload']
    require(payload.get('schema') == 'TAKE5_SEMANTIC_COVERAGE_V1', 'COVERAGE_SCHEMA_INVALID')
    require(payload.get('worker_id') == trust['worker_id'] and payload.get('reviewer_id') == trust['reviewer_id'], 'ATTESTATION_IDENTITY_MISMATCH')
    require(trust['worker_id'] != trust['reviewer_id'] and trust['worker_public_key'] != trust['reviewer_public_key'], 'REVIEWER_NOT_INDEPENDENT')
    verify_signature(payload, cert['worker_signature'], trust['worker_public_key'])
    verify_signature(payload, cert['reviewer_signature'], trust['reviewer_public_key'])
    require(payload.get('review_status') == 'VERIFIED' and bool(str(payload.get('independence_basis', '')).strip()) and bool(str(payload.get('review_method', '')).strip()), 'INDEPENDENT_REVIEW_UNVERIFIED')
    identities = {'source_commit': commit, 'target_sha256': digest(target), 'packet_sha256': digest(packet), 'native_receipt_sha256': digest(native_receipt)}
    require(all(payload.get(k) == v for k, v in identities.items()), 'COVERAGE_ATTESTATION_BINDING_MISMATCH')
    require(set(payload.get('tool_ids', [])) == set(expected_tools), 'ATTESTED_TOOL_INVENTORY_MISMATCH')
    receipt = json.loads(Path(native_receipt).read_text())
    require(receipt.get('source_commit') == commit and receipt.get('packet_sha256') == identities['packet_sha256'], 'NATIVE_RECEIPT_BINDING_MISMATCH')
    require(set(receipt.get('tool_ids', [])) == set(expected_tools), 'NATIVE_TOOL_INVENTORY_MISMATCH')
    text = Path(target).read_bytes().decode('utf-8')
    require(bool(text.strip()), 'EMPTY_TARGET')
    results = {}
    for tool in sorted(expected_tools):
        batches = [b for b in receipt.get('results', []) if any(e.get('tool_id') == tool for e in b.get('executions', []))]
        require(len(batches) == 1 and batches[0].get('status') == 'EXECUTED', 'NATIVE_BATCH_UNVERIFIED:' + tool)
        executions = [e for e in batches[0]['executions'] if e.get('tool_id') == tool]
        require(len(executions) == 1, 'NATIVE_EXECUTION_AMBIGUOUS:' + tool)
        e = executions[0]
        require(e.get('status') in ('EXECUTED', 'COMPLETE', 'CLOSED', 'CLOSED_RELATIVE', 'RELATIVE_CLOSE', 'FULL_MATCH') and e.get('execution_truth') in ('IMPLEMENTATION_EXECUTED', 'SEMANTICALLY_APPLIED', 'FULL_MATCH') and e.get('recurrence_status') in ('RELATIVE_CLOSE', 'SELF_CLOSE'), 'NATIVE_EXECUTION_NOT_CLOSED:' + tool)
        require(any(isinstance(x, str) and x.startswith('native:') for x in e.get('evidence', [])), 'NATIVE_ENTRYPOINT_EVIDENCE_REQUIRED:' + tool)
        plan = build_tool_execution_plan(CONFIGURED_RUNS[tool])
        binding = e.get('binding', {})
        require(plan.complete and binding.get('invocation_profile') == plan.invocation_profile and binding.get('geometry') == plan.geometry and binding.get('mode') == plan.mode and binding.get('wrapper_required') is True and binding.get('recurrence_engine') == plan.recurrence_engine and binding.get('cell_count') == len(plan.cells) and binding.get('question_count') == len(plan.questions) and binding.get('cognitive_count') == len(plan.cognitive) and set(binding.get('native_layers', [])) == {n for n, _ in plan.native}, 'NATIVE_PLAN_MISMATCH:' + tool)
        result = e.get('result')
        require(isinstance(result, dict) and 'native_result' in result and result['native_result'] is not None and 'semantic_coverage' in result, 'NATIVE_SEMANTIC_EVIDENCE_MISSING:' + tool)
        coverage = result['semantic_coverage']
        require(coverage.get('target_sha256') == identities['target_sha256'] and coverage.get('worker_id') == trust['worker_id'], 'SEMANTIC_WORKER_BINDING_MISMATCH:' + tool)
        results[tool] = verify_rows(coverage.get('projections'), projection_ids(plan), text)
    return {'status': 'ATTESTED_COVERAGE_VERIFIED', 'projections_by_tool': results, 'certificate_sha256': digest(certificate), 'reviewer_id': trust['reviewer_id'], **identities}
