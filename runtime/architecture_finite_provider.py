"""Admission of explicit source-located finite architecture observations.

This provider checks representation and evidence references, not the truth of
host-supplied observations. It owns no Git mutation or tool-selection authority.
"""
from architecture_finite import Observation, FiniteContract, run_finite_architecture


def _text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('FINITE_ARCHITECTURE_NONEMPTY_TEXT_REQUIRED')
    return value


def _texts(value, *, unique=False, nonempty=False):
    if not isinstance(value, list) or (nonempty and not value):
        raise ValueError('FINITE_ARCHITECTURE_TEXT_LIST_REQUIRED')
    out = tuple(_text(x) for x in value)
    if unique and len(set(out)) != len(out):
        raise ValueError('FINITE_ARCHITECTURE_DUPLICATE_COORDINATE')
    return out


def prepare_finite_architecture(spec, sources):
    admitted = {(s['path'], s['sha']) for s in sources}
    if not isinstance(spec, dict):
        raise ValueError('FINITE_ARCHITECTURE_MAPPING_REQUIRED')

    def evidence(ref):
        if not isinstance(ref, dict):
            raise ValueError('FINITE_ARCHITECTURE_EVIDENCE_REQUIRED')
        path, sha = _text(ref['source_path']), _text(ref['source_sha'])
        if (path, sha) not in admitted:
            raise ValueError('FINITE_ARCHITECTURE_SOURCE_NOT_ADMITTED')
        return f"{path}@{sha}:{_text(ref['locator'])}:{_text(ref['basis'])}"

    components = _texts(spec['components'], unique=True, nonempty=True)
    obligations = frozenset(_texts(spec['obligations'], unique=True, nonempty=True))
    baselines = _texts(spec['baseline_ids'], unique=True, nonempty=True)
    raw = spec['observations']
    if not isinstance(raw, list) or not raw:
        raise ValueError('FINITE_ARCHITECTURE_OBSERVATIONS_REQUIRED')
    rows = []
    for r in raw:
        if not isinstance(r, dict):
            raise ValueError('FINITE_ARCHITECTURE_OBSERVATION_MAPPING_REQUIRED')
        rows.append(Observation(_text(r['id']), _text(r['context']), _texts(r['state']),
            frozenset(_texts(r['satisfied'], unique=True)), _texts(r['protected']), evidence(r['evidence'])))
    ids = {r.identity for r in rows}
    if len(ids) != len(rows) or not set(baselines) <= ids:
        raise ValueError('FINITE_ARCHITECTURE_OBSERVATION_INVENTORY_INVALID')
    raw_candidates = spec.get('candidates', [])
    if not isinstance(raw_candidates, list):
        raise ValueError('FINITE_ARCHITECTURE_CANDIDATES_LIST_REQUIRED')
    candidates = []
    for r in raw_candidates:
        if not isinstance(r, dict):
            raise ValueError('FINITE_ARCHITECTURE_CANDIDATE_MAPPING_REQUIRED')
        selected = _texts(r['observation_ids'], unique=True, nonempty=True)
        if not set(selected) <= ids:
            raise ValueError('FINITE_ARCHITECTURE_CANDIDATE_OBSERVATION_UNKNOWN')
        candidates.append((_text(r['id']), selected))
    generate = spec.get('generate_observed_candidates', False)
    if type(generate) is not bool:
        raise ValueError('FINITE_ARCHITECTURE_GENERATION_FLAG_INVALID')
    if generate and candidates:
        raise ValueError('FINITE_ARCHITECTURE_MIXED_CANDIDATE_MODES')
    contract = FiniteContract(components, obligations, baselines, evidence(spec['authority']), tuple(candidates), generate)
    return tuple(rows), contract


def invoke_finite_architecture(prepared):
    try:
        return run_finite_architecture(*prepared)
    except ValueError as exc:
        disposition = 'CONFLICT' if str(exc) == 'FINITE_ARCHITECTURE_OBSERVATION_CONFLICT' else 'BLOCKED'
        return {'status': disposition, 'blocker': str(exc), 'result': None}
