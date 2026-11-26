"""Read-only Take-5 host adapters for explicitly admitted finite or structured document evidence.
No network, hidden model, private-repository writes or automatic semantic PASS.
All closures are relative to the packet; no full D36/Q22 semantic coverage claim.
"""
from collections import Counter, defaultdict
from dataclasses import asdict, replace
from itertools import combinations
import hashlib
import json


# I. Built-in provider bindings (finite PD/PDAudit and syntactic Prose).
# Explicit module bindings remain opt-in.
def builtin_adapters(packet, digest):
    def pd_adapter(tool):
        def invoke(current, plan):
            spec = packet.get("pd_frame")
            if not spec:
                return {"status":"OPEN", "blocker":"PD_FRAME_REQUIRED",
                        "adapter_provenance":{"native_invocation":"NOT_INVOKED","provider_binding":tool}}
            rows = tuple(spec["cases"])
            names = spec["representations"]
            if not rows or not names or not all(row.get("id") for row in rows):
                raise ValueError("EXPLICIT_PD_CASES_AND_COORDINATES_REQUIRED")
            if len({row["id"] for row in rows}) != len(rows):
                raise ValueError("DUPLICATE_PD_CASE_ID")
            if any(not isinstance(fields,list) or not fields for fields in names.values()):
                raise ValueError("PD_REPRESENTATION_FIELDS_REQUIRED")
            # Result labels and coordinate assignments are inputs, not generated evidence.
            args = dict(rho=lambda x:x["result"], approx=lambda a,b:a==b,
                        representations={name:(lambda x, keys=tuple(fields):tuple(x["coordinates"][k] for k in keys))
                                         for name,fields in names.items()})
            if tool == "PD":
                from pd import run_pd as fn
            else:
                from pd_audit import run_pd_audit as fn
            if tool=="PDAudit":
                args.update(kappa_cases=lambda xs:{"case_count":len(xs)},
                            kappa_representations=lambda reps:{"representation_names":list(reps)})
            out = fn(rows, **args)
            return {"status":out["status"], "result":out, "execution_truth":"IMPLEMENTATION_EXECUTED" if out["status"]=="RELATIVE_CLOSE" else "OPEN",
                    "material_delta":False, "evidence":[f"native:{fn.__module__}.{fn.__name__}",f"packet-sha256:{digest}"],
                    "blocker":out.get("blocker"),
                    "adapter_provenance":{"native_invocation":"RETURNED","provider_binding":tool,
                                          "semantic_coverage":"BOUNDED_NOT_CERTIFIED"}}
        return invoke

    def prose_adapter(current,plan):
        spec=packet.get("prose")
        if not spec:
            return {"status":"OPEN","blocker":"PROSE_TEXT_AND_CONTRACT_REQUIRED",
                    "adapter_provenance":{"native_invocation":"NOT_INVOKED","provider_binding":"Prose"}}
        # Semantic PASS evidence is intentionally not constructed from user labels.
        # A separately reviewed semantic-evidence adapter may be explicitly bound.
        from prose import ProseContract, assess_prose
        contract=ProseContract(**spec["contract"])
        out=assess_prose(spec["text"],contract,evidence=None)
        return {"status":"BLOCKED" if out.status=="BLOCKED" else "OPEN",
                "execution_truth":"BLOCKED" if out.status=="BLOCKED" else "OPEN",
                "result":asdict(out), "material_delta":False,
                "evidence":["native:prose.assess_prose",f"packet-sha256:{digest}"],
                "blocker":"PROSE_SEMANTIC_EVIDENCE_NOT_BOUND",
                "adapter_provenance":{"native_invocation":"RETURNED","provider_binding":"Prose",
                                      "semantic_coverage":"BOUNDED_NOT_CERTIFIED"}}

    return {"PD":pd_adapter("PD"),"PDAudit":pd_adapter("PDAudit"),"Prose":prose_adapter}


# II. Shared packet identity and provider admission.
# Relocation candidate (not moved): compare Git object hashing with the existing
# runtime_bootstrap.py identity utilities; preserve document-source versus
# runtime-artifact verification boundaries.
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def fnv(value):
    h=2166136261
    for ch in value:
        h=((h^ord(ch))*16777619)&0xffffffff
    return f'{h:08x}'


# Admission is per tool, not per packet family. All existing finite-model
# algorithms and the public bind_adapters(packet) mapping remain intact.
_INPUT_GROUPS = {
    'GDOS': ('matrix',), 'Discriminator': ('threshold',),
    'BiasPerturbation': ('matrix',), 'Architecture': ('matrix',),
    'MultiObject': ('matrix',), 'GOAL': ('matrix', 'threshold'),
    'CurrentnessAudit': (), 'Reconciler': ('threshold',),
    'MT': ('matrix', 'threshold'), 'Diagnosis': ('threshold',),
    'RTC': ('threshold',), 'ASSERT': ('matrix', 'threshold'), 'TRC': (),
}


def bind_adapters(packet):
    """Return independent bindings for the original registered tool set."""
    def binding(tool, groups):
        def invoke(current, plan):
            try:
                admitted = _bind_admitted_adapters(packet, tool, groups)
            except KeyError as exc:
                return {'status':'OPEN','execution_truth':'OPEN',
                        'blocker':f'DOCUMENT_INPUT_REQUIRED:{exc.args[0]}',
                        'material_delta':False,'evidence':[f'packet:{digest(packet)}'],
                        'scope':'BOUNDED_EXPLICIT_INPUT; NO_NATIVE_INVOCATION',
                        'adapter_provenance':{'native_invocation':'NOT_INVOKED','provider_binding':tool}}
            except (ValueError, TypeError, IndexError) as exc:
                return {'status':'BLOCKED','execution_truth':'BLOCKED',
                        'blocker':f'DOCUMENT_INPUT_INVALID:{exc}',
                        'material_delta':False,'evidence':[f'packet:{digest(packet)}'],
                        'scope':'BOUNDED_EXPLICIT_INPUT; NO_NATIVE_INVOCATION',
                        'adapter_provenance':{'native_invocation':'NOT_INVOKED','provider_binding':tool}}
            result=admitted[tool](current, plan)
            # Every admitted native route returns only after the native call.
            # Preserve invocation evidence independently of the gateway disposition.
            result['adapter_provenance']={
                'native_invocation':'RETURNED',
                'provider_binding':tool,
                'source_references':[{'path':s['path'],'sha':s['sha']} for s in packet['sources']],
                'semantic_coverage':'BOUNDED_NOT_CERTIFIED',
            }
            return result
        return invoke
    return {tool:binding(tool, groups) for tool, groups in _INPUT_GROUPS.items()}


# III. Structured document evidence admission.
# Keep the shared source/evidence contract separate from native tool semantics.
def _git_blob_sha(value):
    return isinstance(value,str) and len(value) in (40,64) and all(c in "0123456789abcdef" for c in value)


def _structured_inputs(packet, tool, sources):
    """Validate the host's declared evidence, not the truth of its interpretation."""
    key, inventory = ('diagnosis','failures') if tool=='Diagnosis' else ('rtc','candidates')
    spec=packet[key]
    if not isinstance(spec,dict):
        raise ValueError(f'{key}:EXPECTED_OBJECT')
    admitted=set()
    for source in sources:
        path,sha=source['path'],source['sha']
        if not isinstance(path,str) or not path.strip() or not _git_blob_sha(sha):
            raise ValueError('FROZEN_SOURCE_PATH_AND_BLOB_SHA_REQUIRED')
        admitted.add((path,sha))

    def require_evidence(container, field):
        refs=container[field]
        if not isinstance(refs,list):
            raise ValueError(f'{field}:EXPECTED_LIST')
        if not refs:
            raise KeyError(field)
        for ref in refs:
            if not isinstance(ref,dict):
                raise ValueError(f'{field}:EXPECTED_EVIDENCE_OBJECT')
            path,sha=ref['source_path'],ref['source_sha']
            if not isinstance(path,str) or not isinstance(sha,str) or (path,sha) not in admitted:
                raise ValueError(f'{field}:UNKNOWN_SOURCE_REVISION')
            for name in ('locator','basis'):
                if not isinstance(ref[name],str) or not ref[name].strip():
                    raise ValueError(f'{field}:{name}:NONEMPTY_TEXT_REQUIRED')

    require_evidence(spec,'inventory_evidence')
    rows=spec[inventory]
    if not isinstance(rows,list):
        raise ValueError(f'{inventory}:EXPECTED_LIST')
    seen=set()
    for row in rows:
        if not isinstance(row,dict):
            raise ValueError(f'{inventory}:EXPECTED_ROW_OBJECT')
        ident=row['id']
        if not isinstance(ident,str) or not ident.strip() or ident in seen:
            raise ValueError(f'{inventory}:UNIQUE_ROW_ID_REQUIRED')
        seen.add(ident)
        require_evidence(row,'evidence')
        if tool=='Diagnosis':
            if 'material' in row and type(row['material']) is not bool:
                raise ValueError('material:BOOLEAN_REQUIRED')
            mechanism=row.get('mechanism')
            if mechanism is not None:
                if not isinstance(mechanism,str) or not mechanism.strip():
                    raise ValueError('mechanism:TEXT_OR_NULL_REQUIRED')
                require_evidence(row,'mechanism_evidence')
        else:
            for field,evidence_field in (('strict_gain','gain_evidence'),('preserves','preservation_evidence')):
                value=row.get(field)
                if value is not None:
                    if type(value) is not bool:
                        raise ValueError(f'{field}:BOOLEAN_OR_NULL_REQUIRED')
                    require_evidence(row,evidence_field)
    return spec


# IV. Architecture graph provider.
# Relocation candidate (not moved): generic graph diagnostics may belong with
# runtime/architecture_analysis.py if its native contract admits them; graph
# packet parsing and source binding remain host integration responsibilities.
def _cyclic_components(dependencies):
    """Return cyclic strongly connected components, including self-loops.

    Iterative reachability avoids recursion limits and ignores dangling targets,
    which are reported separately by the graph analyzer.
    """
    reach = {}
    for start in dependencies:
        visited = set()
        pending = [start]
        while pending:
            node = pending.pop()
            if node in visited or node not in dependencies:
                continue
            visited.add(node)
            pending.extend(dependencies[node])
        reach[start] = visited
    remaining = set(dependencies)
    components = []
    while remaining:
        start = min(remaining)
        component = sorted(node for node in reach[start] if start in reach[node])
        remaining.difference_update(component)
        if len(component) > 1 or start in dependencies[start]:
            components.append(component)
    return components


def _graph_adapter(packet, sources):
    """Analyze declared, source-located graph facts; never infer semantic completeness."""
    def nonempty(value):
        return isinstance(value,str) and bool(value.strip())
    def ids(value, field):
        if not isinstance(value,list) or not all(nonempty(x) for x in value) or len(set(value))!=len(value):
            raise ValueError(f'{field}:UNIQUE_TEXT_IDS_REQUIRED')
        return value
    admitted={}
    for source in sources:
        path,sha=source['path'],source['sha']
        if not nonempty(path) or not _git_blob_sha(sha) or path in admitted:
            raise ValueError('GRAPH_SOURCE_PATH_AND_UNIQUE_BLOB_REQUIRED')
        admitted[path]=sha
    spec=packet['architecture_graph']
    if not isinstance(spec,dict):
        raise ValueError('ARCHITECTURE_GRAPH_OBJECT_REQUIRED')
    expected=set(ids(spec['expected_units'],'expected_units'))
    rows=spec['units']
    if not expected:
        raise ValueError('GRAPH_EXPECTED_UNITS_REQUIRED')
    if not isinstance(rows,list):
        raise ValueError('GRAPH_UNITS_LIST_REQUIRED')
    purity=spec.get('check_unit_job_purity',False)
    if type(purity) is not bool:
        raise ValueError('GRAPH_PURITY_FLAG_BOOLEAN_REQUIRED')
    seen=set()
    for row in rows:
        if not isinstance(row,dict):
            raise ValueError('GRAPH_UNIT_OBJECT_REQUIRED')
        ident=row['id']
        if not nonempty(ident) or ident in seen:
            raise ValueError('GRAPH_UNIQUE_UNIT_ID_REQUIRED')
        seen.add(ident)
        if not nonempty(row['source']) or not _git_blob_sha(row['sha']) or admitted.get(row['source'])!=row['sha']:
            raise ValueError('GRAPH_UNKNOWN_SOURCE_REVISION')
        if not nonempty(row['role']) or not nonempty(row['locator']):
            raise ValueError('GRAPH_ROLE_AND_LOCATOR_REQUIRED')
        dependencies=ids(row['internal_dependencies'],'internal_dependencies')
        for field in ('external_dependencies','information_ownership','execution_dependencies'):
            if field in row:
                ids(row[field],field)
        if not set(row.get('execution_dependencies',[])).issubset(dependencies):
            raise ValueError('GRAPH_EXECUTION_EDGE_NOT_INTERNAL')
        if purity:
            jobs=ids(row['jobs'],'jobs')
            if not jobs or not nonempty(row['job_evidence']):
                raise ValueError('GRAPH_JOB_IDENTITIES_AND_SOURCE_LOCATOR_REQUIRED')
    def analyze(target,contract):
        present={x['id'] for x in target}
        dependencies={x['id']:x['internal_dependencies'] for x in target}
        consumers={u:sorted(v for v,vs in dependencies.items() if u in vs) for u in sorted(present)}
        issues={'missing':sorted(expected-present),'extra':sorted(present-expected),
                'dangling':sorted((u,v) for u,vs in dependencies.items() for v in vs if v not in present)}
        execution={x['id']:x.get('execution_dependencies',[]) for x in target}
        owners=defaultdict(list)
        for row in target:
            for key in row.get('information_ownership',[]):
                owners[key].append(row['id'])
        candidates={
            'internal_cycles':_cyclic_components(dependencies),
            'declared_execution_cycles':_cyclic_components(execution),
            'multiple_declared_owners':{k:sorted(v) for k,v in sorted(owners.items()) if len(v)>1},
        }
        result=dict(ArchClass='EXPLICIT_SOURCE_GRAPH',Violations=issues,
            LocalizationFamilies=[k for k,v in issues.items() if v],DependencyState=dependencies,
            InteractionState={'internal_consumers':consumers,'declared_external_dependencies':{x['id']:x.get('external_dependencies',[]) for x in target},
                              'declared_execution_dependencies':execution,'diagnostic_candidates':candidates},
            TransformationFrontier=[],SuccessorFrontier=[],
            Coverage={'scope':'declared static graph only','roles':{x['id']:x['role'] for x in target},
                      'declared_information_ownership':{x['id']:x.get('information_ownership',[]) for x in target},
                      'execution_edge_coverage_declared':sorted(x['id'] for x in target if 'execution_dependencies' in x),
                      'unit_job_purity_requested':purity},
            OpenConflictBlocked={'OPEN':['semantic ownership and dynamic/external coverage not established',
                                        'cycle and ownership candidates require semantic interpretation']},
            Provenance={x['id']:{'source':x['source'],'sha':x['sha'],'locator':x['locator']} for x in target})
        if purity:
            result.update(UnitJobState={x['id']:x['jobs'] for x in target},
                          UnitJobEvidence={x['id']:{'source':x['source'],'sha':x['sha'],'locator':x['job_evidence']} for x in target})
        return result
    def invoke(current,plan):
        from architecture_analysis import run_architecture_analysis, UNIT_JOB_PURITY
        out=run_architecture_analysis(rows,{'expected':sorted(expected),'ExpectedUnitIds':sorted(expected)},
            analyze_architecture=analyze,protected_constraints=(UNIT_JOB_PURITY,) if purity else ())
        return {'status':out['status'],'execution_truth':'IMPLEMENTATION_EXECUTED','result':out,
                'material_delta':False,'evidence':['native:architecture_analysis.run_architecture_analysis',f'packet:{digest(packet)}',*['git-blob:'+s for s in admitted.values()]],
                'blocker':out.get('blocker','FULL_SEMANTIC_COVERAGE_OPEN'),'scope':'BOUNDED_DECLARED_GRAPH; NO_FULL_SEMANTIC_COVERAGE'}
    return invoke


# V. Exact-quotation ASSERT provider.
def _quote_adapter(packet, sources):
    """Verify exact text correspondence, not the truth or implication of a quotation."""
    def nonempty(value):
        return isinstance(value,str) and bool(value.strip())
    def blob_hash(text, reference):
        raw=text.encode('utf-8')
        return hashlib.new('sha1' if len(reference)==40 else 'sha256',
                           f'blob {len(raw)}\0'.encode()+raw).hexdigest()
    admitted={}
    for source in sources:
        path,sha=source['path'],source['sha']
        if not nonempty(path) or path in admitted or not _git_blob_sha(sha):
            raise ValueError('QUOTE_UNIQUE_SOURCE_PATH_AND_BLOB_REQUIRED')
        latest=source.get('latest_sha')
        if latest is not None and (not _git_blob_sha(latest) or len(latest)!=len(sha)):
            raise ValueError('QUOTE_LATEST_BLOB_INVALID')
        for field in ('text','refetched_text'):
            if source.get(field) is not None and not isinstance(source[field],str):
                raise ValueError('QUOTE_SOURCE_TEXT_REQUIRED')
        admitted[path]=source
    spec=packet['assert_quotes']
    if not isinstance(spec,dict) or not isinstance(spec.get('claims'),list):
        raise ValueError('QUOTE_CLAIMS_LIST_REQUIRED')
    claims={}
    if not spec['claims']:
        raise KeyError('assert_quotes.claims')
    for claim in spec['claims']:
        if not isinstance(claim,dict):
            raise ValueError('QUOTE_CLAIM_OBJECT_REQUIRED')
        ident=claim['id']
        if not nonempty(ident) or ident in claims or not nonempty(claim['source']) or not nonempty(claim['quote']):
            raise ValueError('QUOTE_UNIQUE_ID_SOURCE_AND_NONEMPTY_TEXT_REQUIRED')
        claims[ident]={k:claim[k] for k in ('id','source','quote')}
    def check(claim,second):
        source=admitted.get(claim['source'],{})
        frozen=source.get('sha')
        text=source.get('text')
        if frozen is None or text is None or blob_hash(text,frozen)!=frozen:
            return 'UNKNOWN'
        if not second:
            return 'TRUE' if claim['quote'] in text else 'FALSE'
        latest=source.get('latest_sha')
        refetch=source.get('refetched_text')
        if latest is not None and latest!=frozen:
            return 'CONFLICT'
        if latest is None or refetch is None:
            return 'UNKNOWN'
        if blob_hash(refetch,latest)!=latest:
            return 'CONFLICT'
        return 'TRUE' if refetch.encode('utf-8').find(claim['quote'].encode('utf-8'))>=0 else 'FALSE'
    def invoke(current,plan):
        from assert_compound import AssertState, AssertStages, run_to_fixed_point
        def assert_stage(s): return replace(s,assertions=claims,here={})
        def compare_stage(s): return replace(s,comparisons={k:check(c,bool(s.here)) for k,c in s.assertions.items()})
        def resolve_stage(s): return replace(s,resolutions=s.comparisons)
        def here_stage(s): return replace(s,here={'refetch_comparison':True})
        def inquire_stage(s): return replace(s,inquiries=tuple(k for k,v in s.comparisons.items() if v!='TRUE' or v!=s.resolutions[k]))
        def reassert_stage(s): return replace(s,world={k:(v if v==s.resolutions[k] or v=='CONFLICT' else 'UNKNOWN') for k,v in s.comparisons.items()})
        out=run_to_fixed_point(AssertState(),AssertStages(assert_stage,compare_stage,resolve_stage,here_stage,inquire_stage,reassert_stage),
            closure_gate=lambda s:bool(s.world) and all(v=='TRUE' for v in s.world.values()) and not s.inquiries,max_rounds=4)
        return {'status':'EXECUTED' if out.status=='CLOSED' else 'OPEN','result':asdict(out),
                'execution_truth':'IMPLEMENTATION_EXECUTED','material_delta':False,
                'evidence':['native:assert_compound.run_to_fixed_point',f'packet:{digest(packet)}'],
                'scope':'EXACT_UTF8_QUOTE_CORRESPONDENCE; NO_SEMANTIC_ENTAILMENT_OR_FULL_COVERAGE'}
    return invoke


# VI. Source and finite-model admission. Only requested model groups are validated.
def _admit_sources(packet, tool):
    sources=packet['sources']
    if not sources:
        raise KeyError('sources')
    if not isinstance(sources,list) or any(not isinstance(x,dict) for x in sources):
        raise ValueError('SOURCE_LIST_REQUIRED')
    source_ids=tuple(x['sha'] for x in sources)
    paths=tuple(x['path'] for x in sources)
    if any(not _git_blob_sha(s) for s in source_ids):
        raise ValueError('SOURCE_BLOB_SHA_INVALID')
    if any(not isinstance(p,str) or not p.strip() for p in paths) or len(set(paths))!=len(paths):
        raise ValueError('SOURCE_PATH_UNIQUE_NONEMPTY_REQUIRED')
    if tool=='CurrentnessAudit':
        for source in sources:
            path=source['path']
            if not isinstance(path,str) or not path.strip():
                raise ValueError('SOURCE_PATH_REQUIRED')
            if not _git_blob_sha(source['sha']):
                raise ValueError('SOURCE_BLOB_SHA_INVALID')
            latest=source.get('latest_sha')
            if latest is not None and latest != '' and not _git_blob_sha(latest):
                raise ValueError('LATEST_SOURCE_BLOB_SHA_INVALID')
    return sources, source_ids


def _admit_matrix(packet, tool):
    matrix=packet['matrix']
    if fnv(matrix['raw']) != matrix['transfer_fnv']:
        raise ValueError('CONNECTOR_PACKET_TRANSFER_MISMATCH')
    axes=tuple(matrix['axes'])
    rows=tuple(tuple(line.split()) for line in matrix['raw'].splitlines())
    if any(len(r)!=len(axes)+1 for r in rows) or len(set(r[0] for r in rows))!=len(rows):
        raise ValueError('MALFORMED_OR_DUPLICATE_MATRIX_ROW')
    expected = expected_counts = None
    # MultiObject uses only the row identities and labels, not declared counts.
    if tool!='MultiObject':
        expected=tuple(packet['expected_ids'])
    if tool in ('GDOS','Architecture'):
        expected_counts=matrix['declared_counts']
    if tool=='Architecture' and matrix['exclusive_axis'] not in axes:
        raise ValueError('MATRIX_EXCLUSIVE_AXIS_NOT_FOUND')
    return matrix, axes, rows, expected, expected_counts


def _admit_threshold(packet, tool):
    t=packet['threshold']
    thresholds=tuple(t['values'])
    lower,upper=t['lower'],t['upper']
    if (not thresholds or any(type(v) is not int for v in thresholds)
            or len(set(thresholds))!=len(thresholds)):
        raise ValueError('THRESHOLD_VALUES_NONEMPTY_UNIQUE_INTEGERS_REQUIRED')
    if type(lower) is not int or type(upper) is not int or lower>upper:
        raise ValueError('THRESHOLD_BOUNDS_INVALID')
    qs=tuple(range(lower,upper+1))
    if fnv(t['proof'])!=t['proof_fnv']:
        raise ValueError('PROOF_TRANSFER_MISMATCH')
    if tool in ('MT','GOAL','RTC'):
        probes=tuple(t['baseline_probes'])
        if any(type(q) is not int or not lower<=q<=upper for q in probes) or len(set(probes))!=len(probes):
            raise ValueError('THRESHOLD_BASELINE_PROBES_INVALID')
    if tool in ('MT','GOAL','ASSERT','Reconciler'):
        count=t['declared_pair_count']
        if type(count) is not int or count<0:
            raise ValueError('THRESHOLD_DECLARED_PAIR_COUNT_INVALID')
    return t, thresholds, qs


# VII. Shared bounded execution receipt and model routing.
# Relocation candidate (not moved): compare result-envelope construction with
# execute_tool_packet.py and the runtime configured bridge; preserve the distinct
# host provenance, native result and configured recurrence responsibilities.
def _bounded_result(packet, source_ids, entry,out,status='EXECUTED',blocker=None):
    return {'status':status,'execution_truth':'IMPLEMENTATION_EXECUTED' if status=='EXECUTED' else status,
            'result':out,'material_delta':False,'evidence':[f'native:{entry}',f'packet:{digest(packet)}',*['git-blob:'+s for s in source_ids]],
            'blocker':blocker,'scope':'BOUNDED_EXPLICIT_INPUT; NO_FULL_SEMANTIC_COVERAGE'}


def _admit_tool_models(packet,tool,groups,sources):
    """Admit only the selected model; keep this independent of native execution."""
    structured=None
    structured_key={'Diagnosis':'diagnosis','RTC':'rtc'}.get(tool)
    if structured_key is not None and structured_key in packet:
        if 'threshold' in packet:
            raise ValueError(f'{tool}:AMBIGUOUS_STRUCTURED_AND_THRESHOLD_INPUT')
        structured=_structured_inputs(packet,tool,sources)
        groups=()
    matrix_data=_admit_matrix(packet,tool) if 'matrix' in groups else None
    threshold_data=_admit_threshold(packet,tool) if 'threshold' in groups else None
    return structured,matrix_data,threshold_data


# VIII. Independent finite-matrix MultiObject provider; admits no unrelated model fields.
def _matrix_multiobject_adapter(packet, axes, rows, source_ids):
    from multiobject import (FrozenObject, RelationFinding, RouteResult, ResidualJudgment,
                             ReconciledFinding, run_multiobject)
    def envelope(entry,out,status='EXECUTED',blocker=None):
        return _bounded_result(packet, source_ids, entry, out, status, blocker)
    class MatrixProvider:
        # Joint groups are computed directly by inverted membership, independently of pair routes.
        def __init__(self,objects): self.ids=tuple(o.object_id for o in objects)
        def joint(self,objects,*,route_id):
            groups=defaultdict(list)
            for o in objects:
                for tag in o.primitives: groups[tag].append(o.object_id)
            findings=tuple(RelationFinding('GROUP:'+tag,tuple(ids),'SHARED_CODE_GROUP',(tag,),source_ids) for tag,ids in sorted(groups.items()) if len(ids)>1)
            return RouteResult(route_id,'FULL_JOINT',self.ids,findings,isolation_receipt='direct-inverted-index:'+digest([(o.object_id,o.primitives) for o in objects]))
        def pair(self,left,right,*,route_id):
            ids=(left.object_id,right.object_id)
            shared=sorted(set(left.primitives)&set(right.primitives))
            findings=tuple(RelationFinding(route_id+':'+tag,ids,'SHARED_CODE',(tag,),source_ids) for tag in shared)
            return RouteResult(route_id,'PAIR',ids,findings,isolation_receipt='pair-only:'+digest([(left.object_id,left.primitives),(right.object_id,right.primitives)]))
        def synthesize_pairs(self,pair_routes):
            return RouteResult('PAIR-UNION','PAIR_SYNTHESIS',self.ids,tuple(f for p in pair_routes for f in p.findings),isolation_receipt='pair-only-union:'+digest([p.route_id for p in pair_routes]))
        def challenge_reducibility(self,joint_route,pair_routes,pair_synthesis):
            edges=defaultdict(set)
            for f in pair_synthesis.findings: edges[f.grounds[0]].add(frozenset(f.support))
            out=[]
            for f in joint_route.findings:
                required={frozenset(x) for x in combinations(f.support,2)}
                got=edges[f.grounds[0]]
                out.append(ResidualJudgment(f.finding_id,'PAIRWISE_RECOVERABLE' if required==got else 'CONFLICT',('exact shared-code clique comparison',)))
            return tuple(out)
        def triggered_views(self,*args): return ()
        def analyze_view(self,*args): raise ValueError('NO_TRIGGERED_VIEW')
        def reconcile(self,pair_routes,pair_synthesis,joint_route,residuals,view_results):
            return tuple(ReconciledFinding(f.finding_id,'PAIRWISE_ONLY',('shared assignment, not semantic entailment',)) for f in pair_synthesis.findings)+tuple(ReconciledFinding(r.finding_id,'CONVERGENT' if r.status=='PAIRWISE_RECOVERABLE' else 'CONFLICT',r.grounds) for r in residuals)
    def mo(current,plan):
        objects=tuple(FrozenObject(r[0],'CLASSIFICATION_RECORD','EXPLICIT_MATRIX','shared codes',tuple(f'{a}:{k}' for i,a in enumerate(axes) for k in r[i+1].split('/'))) for r in rows)
        out=run_multiobject(objects,MatrixProvider(objects))
        return envelope('multiobject.run_multiobject',asdict(out),'EXECUTED' if out.status=='CLOSED_RELATIVE' else out.status,out.blocker)
    return mo


# Shared configured MT prerequisite for both GOAL input routes.
# Relocation candidate (not moved): compare receipt mapping with runtime/goal.py;
# actual gateway dispatch remains an integration responsibility.
def _configured_mt_prerequisite(packet,mt):
    from goal import GoalMTReceipt
    from direct_tool_command_gateway import execute_direct_tool_commands
    pre=execute_direct_tool_commands('run MT',state={'packet':digest(packet)},adapters={'MT':mt})
    receipt=None
    if pre.executions:
        e=pre.executions[0]
        if e.tool_id=='MT' and e.result and e.binding.get('invocation_profile')=='FULL_CONFIGURED_HF2_V1':
            raw=e.result
            receipt=GoalMTReceipt(status=raw['status'],evidence=e.evidence,open_objects=tuple(raw['open_objects']))
    return pre,receipt


# IX. Source-bound document observation provider for MT and GOAL.
# Host interpretations
# are explicit evidence inputs, never independent semantic certification.
def _document_mt_goal(packet, tool, sources):
    from difflib import SequenceMatcher
    spec=packet['document_observations']
    if not isinstance(spec,dict):
        raise ValueError('DOCUMENT_OBSERVATIONS_MAPPING_REQUIRED')
    by_path={s['path']:s for s in sources}
    target=spec['target']
    if not isinstance(target,str) or target not in by_path:
        raise ValueError('DOCUMENT_TARGET_NOT_ADMITTED')
    def checked_text(value, sha):
        if not isinstance(value,str):
            raise ValueError('DOCUMENT_UTF8_TEXT_REQUIRED')
        raw=value.encode('utf-8')
        if hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()!=sha:
            raise ValueError('DOCUMENT_BLOB_MISMATCH')
        return value
    def nonempty(value):
        return isinstance(value,str) and bool(value.strip())
    def source_text(path):
        if path not in by_path:
            raise ValueError('DOCUMENT_EVIDENCE_SOURCE_NOT_ADMITTED')
        source=by_path[path]
        if source.get('latest_sha')!=source['sha']:
            raise KeyError('CURRENT_DOCUMENT_SOURCE_REVISION')
        return checked_text(source['text'],source['sha'])
    current_text=source_text(target)
    rows=spec['observations']
    if not isinstance(rows,list) or not rows:
        raise KeyError('document_observations.observations')
    observations={}
    for row in rows:
        if not isinstance(row,dict):
            raise ValueError('DOCUMENT_OBSERVATION_MAPPING_REQUIRED')
        ident,source,quote,meaning=(row[k] for k in ('id','source','quote','interpretation'))
        if not all(nonempty(v) for v in (ident,source,quote,meaning)) or ident in observations:
            raise ValueError('DOCUMENT_OBSERVATION_ID_OR_EVIDENCE_INVALID')
        body=source_text(source)
        if quote not in body:
            raise ValueError('DOCUMENT_OBSERVATION_QUOTE_MISSING')
        observations[ident]={'source':source,'sha':by_path[source]['sha'],
            'quote':quote,'first_line':body[:body.index(quote)].count('\n')+1,
            'host_interpretation':meaning}
    if not any(row['source']==target for row in observations.values()):
        raise ValueError('DOCUMENT_TARGET_OBSERVATION_REQUIRED')
    change={'status':'NO_PREVIOUS_REVISION_SUPPLIED'}
    if 'previous' in spec:
        prev=spec['previous']
        if not isinstance(prev,dict):
            raise ValueError('DOCUMENT_PREVIOUS_MAPPING_REQUIRED')
        if prev['path']!=target:
            raise ValueError('DOCUMENT_PREVIOUS_TARGET_MISMATCH')
        before=checked_text(prev['text'],prev['sha'])
        a,b=before.splitlines(keepends=True),current_text.splitlines(keepends=True)
        change={'status':'EXACT_TEXT_COMPARISON','previous_sha':prev['sha'],
                'current_sha':by_path[target]['sha'],
                'changed_spans':[{'operation':op,'before':[i,j],'after':[k,l]}
                    for op,i,j,k,l in SequenceMatcher(None,a,b,autojunk=False).get_opcodes() if op!='equal']}
    declared_open=packet.get('open_coordinates',[])
    if not isinstance(declared_open,list) or any(not nonempty(v) for v in declared_open):
        raise ValueError('DOCUMENT_OPEN_COORDINATES_INVALID')
    # This provider checks bytes and explicit evidence only. It cannot certify
    # arbitrary prose semantics or run an unbound black-box resolution stage.
    unresolved=tuple(dict.fromkeys([*declared_open,'FULL_DOCUMENT_SEMANTIC_COVERAGE_OPEN']))
    candidates=[]
    if tool=='GOAL':
        from goal import GoalObject, GoalCandidate
        raw=packet['goal_candidates']
        if not isinstance(raw,list) or not raw:
            raise KeyError('goal_candidates')
        for row in raw:
            if not isinstance(row,dict):
                raise ValueError('DOCUMENT_GOAL_CANDIDATE_MAPPING_REQUIRED')
            ids=row['evidence']
            if not isinstance(ids,list) or not ids or any(not isinstance(x,str) or x not in observations for x in ids):
                raise ValueError('DOCUMENT_GOAL_EVIDENCE_NOT_ADMITTED')
            if not all(type(row[k]) is bool for k in ('grounded','authority_typed','determinate_enough')):
                raise ValueError('DOCUMENT_GOAL_FLAGS_INVALID')
            if not nonempty(row['id']) or not nonempty(row['authority_basis']) or not nonempty(row['determination_basis']):
                raise ValueError('DOCUMENT_GOAL_HOST_BASIS_REQUIRED')
            goal=row['goal']; constraints=row['constraints']
            if not isinstance(goal,dict) or set(goal)!={'X','T','I','Sigma'} or any(not nonempty(v) for v in goal.values()):
                raise ValueError('DOCUMENT_GOAL_OBJECT_INVALID')
            if not isinstance(constraints,list) or any(not nonempty(v) for v in constraints):
                raise ValueError('DOCUMENT_GOAL_CONSTRAINTS_INVALID')
            evidence=tuple(f"{observations[x]['source']}@{observations[x]['sha']}:L{observations[x]['first_line']}:{x}" for x in ids)
            evidence+=('HOST_AUTHORITY_BASIS:'+row['authority_basis'],'HOST_DETERMINATION_BASIS:'+row['determination_basis'])
            candidates.append(GoalCandidate(row['id'],GoalObject(**goal),tuple(constraints),evidence,
                row['grounded'],row['authority_typed'],row['determinate_enough']))
    source_ids=tuple(s['sha'] for s in sources)
    def mt(current,plan):
        from mt_semantic_return_gate import run_mt_with_before_return_gate
        def observe(state):
            return state,{'target':target,'source_observations':observations,'change':change,
                          'unresolved':unresolved,'scope':'EXACT_DOCUMENT_EVIDENCE_AND_HOST_INTERPRETATION'}
        out=run_mt_with_before_return_gate({'packet':digest(packet)},run_mt=observe,
            detect_black_boxes=lambda st,res:res['unresolved'],
            execute_stage=lambda tool_id,object_id,state:(state,'OPEN',False))
        return _bounded_result(packet,source_ids,'mt_semantic_return_gate.run_mt_with_before_return_gate',
            asdict(out),'OPEN','FULL_DOCUMENT_SEMANTIC_COVERAGE_OPEN')
    def goal(current,plan):
        from goal import recover_goal_configured
        pre,receipt=_configured_mt_prerequisite(packet,mt)
        out=recover_goal_configured(tuple(candidates),receipt)
        return _bounded_result(packet,source_ids,'goal.recover_goal_configured',
            {'native':asdict(out),'mt_preflight':asdict(pre),'host_candidate_evidence':observations},
            'EXECUTED' if out.status=='CLOSED_RELATIVE' else out.status,out.blocker)
    return {'MT':mt,'GOAL':goal}[tool]


# X. Legacy finite-model and structured provider dispatch.
# Relocation candidates (not moved): tool-neutral finite matrix/threshold
# algorithms need an existing owner review; do not move bounded model semantics
# into general native tool cores or treat them as document-semantic coverage.
def _bind_admitted_adapters(packet, tool, groups):
    # Admit only the evidence used by this invocation. No input validation
    # failure may prevent an independent binding from being constructed.
    sources, source_ids = _admit_sources(packet, tool)
    if tool in ('MT','GOAL') and 'document_observations' in packet:
        if 'matrix' in packet or 'threshold' in packet:
            raise ValueError('AMBIGUOUS_DOCUMENT_MT_GOAL_INPUT')
        return {tool:_document_mt_goal(packet,tool,sources)}
    if tool=='Architecture' and 'architecture_graph' in packet:
        if 'matrix' in packet:
            raise ValueError('AMBIGUOUS_ARCHITECTURE_INPUT')
        return {tool:_graph_adapter(packet,sources)}
    if tool=='ASSERT' and 'assert_quotes' in packet:
        if 'matrix' in packet or 'threshold' in packet:
            raise ValueError('AMBIGUOUS_ASSERT_INPUT')
        return {tool:_quote_adapter(packet,sources)}
    structured,matrix_data,threshold_data=_admit_tool_models(packet,tool,groups,sources)
    if tool == 'MultiObject':
        _, axes, rows, _, _ = matrix_data
        return {tool:_matrix_multiobject_adapter(packet, axes, rows, source_ids)}
    if matrix_data is not None:
        matrix, axes, rows, expected, expected_counts=matrix_data
    if threshold_data is not None:
        t, thresholds, qs=threshold_data
    def counts(rs):
        return {a:dict(sorted(Counter(k for r in rs for k in r[i+1].split('/')).items())) for i,a in enumerate(axes)}
    def coverage(rs):
        ids={r[0] for r in rs}
        return {'missing':sorted(set(expected)-ids),'unexpected':sorted(ids-set(expected)),'rows':len(rs)}
    def signature(qs_, threshold):
        return tuple(int(q>=threshold) for q in qs_)
    def discriminate():
        from discriminator import run_discriminator
        return run_discriminator(tuple(combinations(qs,2)),lambda p:len({signature(p,k) for k in thresholds})==len(thresholds))
    def envelope(entry,out,status='EXECUTED',blocker=None):
        return _bounded_result(packet, source_ids, entry, out, status, blocker)

    # Finite classification-matrix providers.
    def gdos(current,plan):
        from gdos import run_gdos
        out=run_gdos(rows,observers=(coverage,counts),reconcile_fn=lambda obs:{'coverage':obs[0],'counts':obs[1],'declared_counts_match':obs[1]==expected_counts})
        return envelope('gdos.run_gdos',out,out['status'])

    def bias(current,plan):
        from bias_perturbation import run_bias_perturbation
        out=run_bias_perturbation(rows,(tuple(reversed(rows)),tuple(sorted(rows,key=lambda r:r[2] if len(r)>2 else r[1:]))),
              runner=lambda r:(coverage(r),counts(r)),semantics_equivalent=lambda a,b:Counter(a)==Counter(b),result_equivalent=lambda a,b:a==b)
        return envelope('bias_perturbation.run_bias_perturbation',out,'EXECUTED' if out['status']=='ACCEPT' else 'OPEN')

    def architecture(current,plan):
        from architecture_analysis import run_architecture_analysis
        def analyze(target,contract):
            violations=[]
            cov=coverage(target)
            if cov['missing'] or cov['unexpected']: violations.append('CASE_COVERAGE')
            if counts(target)!=expected_counts: violations.append('COUNT_MISMATCH')
            if any('/' in row[axes.index(matrix['exclusive_axis'])+1] for row in target): violations.append('EXCLUSIVE_AXIS_MULTIPLICITY')
            return dict(ArchClass='MATRIX_SCHEMA',Violations=violations,LocalizationFamilies=violations,
                DependencyState={'case_index_ids':len(expected)},InteractionState={'axes':axes},TransformationFrontier=[],SuccessorFrontier=[],Coverage=cov,
                OpenConflictBlocked=['OPEN'] if violations else [],Provenance=source_ids)
        out=run_architecture_analysis(rows,{'axes':axes,'expected_ids':expected},analyze_architecture=analyze)
        return envelope('architecture_analysis.run_architecture_analysis',out,'EXECUTED' if out['status']=='RELATIVE_CLOSE' else out['status'])

    # Finite threshold-model providers.
    def disc(current,plan):
        out=discriminate()
        return envelope('discriminator.run_discriminator',out,'OPEN' if out['status']=='OPEN' else 'EXECUTED')

    def reconciler(current,plan):
        from reconcile import ReconcileResult, reconcile
        a=discriminate(); b=[(x,y) for x in qs for y in qs if x<y and all(signature((x,y),u)!=signature((x,y),v) for u,v in combinations(thresholds,2))]
        def resolver(state,admitted):
            left,right=admitted
            diff=sorted(set(left)^set(right))
            return ReconcileResult({'enumerated_pairs':len(left),'pairwise_check':len(right),'declared_count':t['declared_pair_count']},conflicts=tuple(diff),open_coordinates=() if len(left)==t['declared_pair_count'] else ('DECLARED_COUNT_MISMATCH',))
        out=reconcile({},(tuple(a['survivors']),tuple(b)),resolver)
        return envelope('reconcile.reconcile',asdict(out),'OPEN' if out.conflicts or out.open_coordinates else 'EXECUTED')

    # Joint matrix/threshold MT, GOAL and ASSERT providers.
    def mt(current,plan):
        from mt_semantic_return_gate import run_mt_with_before_return_gate
        # Actual observation pass over admitted data; unresolved source and semantic
        # objects reach the native gate but cannot be resolved by a missing worker.
        def observe(state):
            result={'target':'explicit matrix and threshold model',
                    'coverage':coverage(rows),'counts':counts(rows),
                    'distinct_outcome_signatures':{str(k):signature(tuple(t['baseline_probes']),k) for k in thresholds},
                    'declared_pair_count':t['declared_pair_count'],
                    'unresolved':tuple(packet.get('open_coordinates',()))}
            return state,result
        def resolve_stage(tool_id,object_id,state):
            return state,'OPEN',False
        out=run_mt_with_before_return_gate({'packet':digest(packet)},run_mt=observe,
                detect_black_boxes=lambda st,res:res['unresolved'],execute_stage=resolve_stage)
        return envelope('mt_semantic_return_gate.run_mt_with_before_return_gate',asdict(out),'EXECUTED' if out.status=='CLOSED_RELATIVE' else out.status,
                        'SEMANTIC_BLACK_BOXES_OPEN' if out.open_objects else None)

    def goal(current,plan):
        from goal import GoalObject, GoalCandidate, recover_goal_configured
        candidates=tuple(GoalCandidate(x['id'],GoalObject(**x['goal']),tuple(x['constraints']),tuple(x['evidence']),x['grounded'],x['authority_typed'],x['determinate_enough']) for x in packet.get('goal_candidates',[]))
        pre,receipt=_configured_mt_prerequisite(packet,mt)
        out=recover_goal_configured(candidates,receipt)
        return envelope('goal.recover_goal_configured',{'native':asdict(out),'mt_preflight':asdict(pre)},'EXECUTED' if out.status=='CLOSED_RELATIVE' else out.status,out.blocker)

    def assertion(current,plan):
        from assert_compound import AssertState, AssertStages, run_to_fixed_point
        targets={'matrix_coverage':len(expected),'probe_pair_count':t['declared_pair_count']}
        def assert_stage(s): return replace(s,assertions=targets)
        def compare_stage(s):
            n=(len(discriminate()['survivors']) if not s.here else sum(all(signature((x,y),u)!=signature((x,y),v) for u,v in combinations(thresholds,2)) for x,y in combinations(qs,2)))
            actual={'matrix_coverage':len(set(r[0] for r in rows)&set(expected)),'probe_pair_count':n}
            return replace(s,comparisons=actual)
        def resolve_stage(s): return replace(s,resolutions={k:'TRUE' if s.comparisons[k]==v else 'FALSE' for k,v in s.assertions.items()})
        def here_stage(s): return replace(s,here={'source_blobs':source_ids,'second_algorithm':True})
        def inquire_stage(s): return replace(s,inquiries=tuple(packet.get('open_coordinates',())))
        def reassert_stage(s): return replace(s,world={'claim_test_status':{k:'TRUE' if s.comparisons[k]==v else 'FALSE' for k,v in s.assertions.items()}})
        out=run_to_fixed_point(AssertState(),AssertStages(assert_stage,compare_stage,resolve_stage,here_stage,inquire_stage,reassert_stage),closure_gate=lambda s:bool(s.world.get('claim_test_status')) and all(v=='TRUE' for v in s.world['claim_test_status'].values()) and not s.inquiries,max_rounds=4)
        return envelope('assert_compound.run_to_fixed_point',asdict(out),'EXECUTED' if out.status=='CLOSED' else 'OPEN')

    # Structured or finite-model Diagnosis and RTC providers.
    def diagnosis(current,plan):
        from diagnosis import diagnose
        if structured is not None:
            out=diagnose({'failures':structured['failures']})
            result=envelope('diagnosis.diagnose',out,'EXECUTED' if out['status']=='ACCEPT' else 'OPEN',
                            'DIAGNOSTIC_MECHANISM_UNRESOLVED' if out['status']=='OPEN' else None)
            result.update(input_route='STRUCTURED_DOCUMENT_EVIDENCE',inventory_evidence=structured['inventory_evidence'])
            return result
        fails=[{'id':str(q),'mechanism':'noninjective outcome signature over fixed candidate set','material':True}
               for q in qs if len({signature((q,),k) for k in thresholds})<len(thresholds)]
        out=diagnose({'failures':fails})
        return envelope('diagnosis.diagnose',out,'EXECUTED' if out['status']=='ACCEPT' else 'OPEN')

    def rtc(current,plan):
        from raise_the_ceiling import raise_the_ceiling
        if structured is not None:
            out=raise_the_ceiling({'candidates':structured['candidates']})
            pending=out['status']=='OPEN' or bool(out.get('unresolved'))
            result=envelope('raise_the_ceiling.raise_the_ceiling',out,'OPEN' if pending else 'EXECUTED',
                            'STRICT_GAIN_OR_PRESERVATION_UNRESOLVED' if pending else None)
            result.update(input_route='STRUCTURED_DOCUMENT_EVIDENCE',inventory_evidence=structured['inventory_evidence'])
            return result
        base=tuple(t['baseline_probes'])
        n=len({signature(base,k) for k in thresholds})
        candidates=[{'id':str(q),'strict_gain':len({signature(base+(q,),k) for k in thresholds})>n,
                     'preserves':True} for q in qs if q not in base]
        out=raise_the_ceiling({'candidates':candidates})
        return envelope('raise_the_ceiling.raise_the_ceiling',out,'EXECUTED' if out['status'] in ('ACCEPT','NOOP') else 'OPEN')

    # Source currentness and consequence tracking providers.
    def currentness(current,plan):
        from currentness_audit import assess, audit_complete
        receipts=tuple(assess(component=s['path'],object_identity=s['path'],built_generation=s['sha'],latest_generation=s.get('latest_sha',''),built_basis='connector blob',latest_basis='connector blob',identity_verified=bool(s.get('latest_sha')),evidence=(s['sha'],s.get('latest_sha',''))) for s in packet['sources'])
        return envelope('currentness_audit.assess',{'receipts':[asdict(r) for r in receipts],'complete':audit_complete(receipts)},'EXECUTED' if audit_complete(receipts) else 'OPEN')

    def trc(current,plan):
        from tool_run_closure import Consequence, Disposition, run_tool_run_closure
        cons=tuple(Consequence(x,'RESEARCH_VERIFICATION','verified','read-only',source_ids[0],'SOURCE_SEMANTICS') for x in packet.get('open_coordinates',()))
        out=run_tool_run_closure(tool_result={'open':len(cons)},pre_state={},post_state={},
            harvest_fn=lambda *_:cons,disposition_fn=lambda *_:Disposition.OPEN,
            realize_fn=lambda c,s:s,verify_fn=lambda c,s:s,consume_fn=lambda c,s:s,
            harvest_basis='explicit packet open coordinates',harvest_complete=False)
        return envelope('tool_run_closure.run_tool_run_closure',asdict(out),'OPEN','UNRESOLVED_SEMANTIC_OBLIGATIONS')
    return {'GDOS':gdos,'Discriminator':disc,'BiasPerturbation':bias,'Architecture':architecture,'GOAL':goal,'CurrentnessAudit':currentness,'Reconciler':reconciler,'MT':mt,'Diagnosis':diagnosis,'RTC':rtc,'ASSERT':assertion,'TRC':trc}
