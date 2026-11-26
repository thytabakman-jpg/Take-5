"""Read-only Take-5 host adapters for explicitly admitted finite or structured document evidence.
No network, hidden model, private-repository writes or automatic semantic PASS.
All closures are relative to the packet; no full D36/Q22 semantic coverage claim.
"""
from collections import Counter, defaultdict
from dataclasses import asdict, replace
from itertools import combinations
import hashlib
import json
from gdos import run_gdos
from discriminator import run_discriminator
from bias_perturbation import run_bias_perturbation
from architecture_analysis import run_architecture_analysis
from multiobject import (FrozenObject, RelationFinding, RouteResult, ResidualJudgment,
                         ReconciledFinding, run_multiobject)
from goal import GoalObject, GoalCandidate, GoalMTReceipt, recover_goal_configured
from mt_semantic_return_gate import run_mt_with_before_return_gate
from direct_tool_command_gateway import execute_direct_tool_commands
from diagnosis import diagnose
from raise_the_ceiling import raise_the_ceiling
from tool_run_closure import Consequence, Disposition, run_tool_run_closure
from currentness_audit import assess, audit_complete
from reconcile import ReconcileResult, reconcile
from assert_compound import AssertState, AssertStages, run_to_fixed_point


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
                        'scope':'BOUNDED_EXPLICIT_INPUT; NO_NATIVE_INVOCATION'}
            except (ValueError, TypeError, IndexError) as exc:
                return {'status':'BLOCKED','execution_truth':'BLOCKED',
                        'blocker':f'DOCUMENT_INPUT_INVALID:{exc}',
                        'material_delta':False,'evidence':[f'packet:{digest(packet)}'],
                        'scope':'BOUNDED_EXPLICIT_INPUT; NO_NATIVE_INVOCATION'}
            return admitted[tool](current, plan)
        return invoke
    return {tool:binding(tool, groups) for tool, groups in _INPUT_GROUPS.items()}


def _structured_inputs(packet, tool, sources):
    """Validate the host's declared evidence, not the truth of its interpretation."""
    key, inventory = ('diagnosis','failures') if tool=='Diagnosis' else ('rtc','candidates')
    spec=packet[key]
    if not isinstance(spec,dict):
        raise ValueError(f'{key}:EXPECTED_OBJECT')
    admitted=set()
    for source in sources:
        path,sha=source['path'],source['sha']
        if not isinstance(path,str) or not path.strip() or not isinstance(sha,str) or len(sha) not in (40,64) or any(c not in '0123456789abcdef' for c in sha):
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


def _bind_admitted_adapters(packet, tool, groups):
    # Admit only the evidence used by this invocation. No input validation
    # failure may prevent an independent binding from being constructed.
    sources=packet['sources']
    if not sources:
        raise KeyError('sources')
    source_ids=tuple(x['sha'] for x in sources)
    if any(not isinstance(s,str) or not s for s in source_ids):
        raise ValueError('SOURCE_ID_REQUIRED')
    if tool=='CurrentnessAudit':
        for source in sources:
            if not source['path']:
                raise ValueError('SOURCE_PATH_REQUIRED')
    structured=None
    structured_key={'Diagnosis':'diagnosis','RTC':'rtc'}.get(tool)
    if structured_key is not None and structured_key in packet:
        if 'threshold' in packet:
            raise ValueError(f'{tool}:AMBIGUOUS_STRUCTURED_AND_THRESHOLD_INPUT')
        structured=_structured_inputs(packet,tool,sources)
        groups=()
    if 'matrix' in groups:
        matrix=packet['matrix']
        if fnv(matrix['raw']) != matrix['transfer_fnv']:
            raise ValueError('CONNECTOR_PACKET_TRANSFER_MISMATCH')
        axes=tuple(matrix['axes'])
        rows=tuple(tuple(line.split()) for line in matrix['raw'].splitlines())
        if any(len(r)!=len(axes)+1 for r in rows) or len(set(r[0] for r in rows))!=len(rows):
            raise ValueError('MALFORMED_OR_DUPLICATE_MATRIX_ROW')
        # MultiObject uses only the row identities and labels, not declared counts.
        if tool!='MultiObject':
            expected=tuple(packet['expected_ids'])
        if tool in ('GDOS','Architecture'):
            expected_counts=matrix['declared_counts']
        if tool=='Architecture' and matrix['exclusive_axis'] not in axes:
            raise ValueError('MATRIX_EXCLUSIVE_AXIS_NOT_FOUND')
    if 'threshold' in groups:
        t=packet['threshold']
        thresholds=tuple(t['values'])
        qs=tuple(range(t['lower'],t['upper']+1))
        if fnv(t['proof'])!=t['proof_fnv']:
            raise ValueError('PROOF_TRANSFER_MISMATCH')
        if tool in ('MT','GOAL','RTC'):
            tuple(t['baseline_probes'])
        if tool in ('MT','GOAL','ASSERT','Reconciler'):
            t['declared_pair_count']
    def counts(rs):
        return {a:dict(sorted(Counter(k for r in rs for k in r[i+1].split('/')).items())) for i,a in enumerate(axes)}
    def coverage(rs):
        ids={r[0] for r in rs}
        return {'missing':sorted(set(expected)-ids),'unexpected':sorted(ids-set(expected)),'rows':len(rs)}
    def signature(qs_, threshold):
        return tuple(int(q>=threshold) for q in qs_)
    def discriminate():
        return run_discriminator(tuple(combinations(qs,2)),lambda p:len({signature(p,k) for k in thresholds})==len(thresholds))
    def envelope(entry,out,status='EXECUTED',blocker=None):
        return {'status':status,'execution_truth':'IMPLEMENTATION_EXECUTED' if status=='EXECUTED' else status,
                'result':out,'material_delta':False,'evidence':[f'native:{entry}',f'packet:{digest(packet)}',*['git-blob:'+s for s in source_ids]],
                'blocker':blocker,'scope':'BOUNDED_EXPLICIT_INPUT; NO_FULL_SEMANTIC_COVERAGE'}
    def gdos(current,plan):
        out=run_gdos(rows,observers=(coverage,counts),reconcile_fn=lambda obs:{'coverage':obs[0],'counts':obs[1],'declared_counts_match':obs[1]==expected_counts})
        return envelope('gdos.run_gdos',out,out['status'])
    def disc(current,plan):
        out=discriminate()
        return envelope('discriminator.run_discriminator',out,'OPEN' if out['status']=='OPEN' else 'EXECUTED')
    def bias(current,plan):
        out=run_bias_perturbation(rows,(tuple(reversed(rows)),tuple(sorted(rows,key=lambda r:r[2] if len(r)>2 else r[1:]))),
              runner=lambda r:(coverage(r),counts(r)),semantics_equivalent=lambda a,b:Counter(a)==Counter(b),result_equivalent=lambda a,b:a==b)
        return envelope('bias_perturbation.run_bias_perturbation',out,'EXECUTED' if out['status']=='ACCEPT' else 'OPEN')
    def architecture(current,plan):
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
    def mt(current,plan):
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
        candidates=tuple(GoalCandidate(x['id'],GoalObject(**x['goal']),tuple(x['constraints']),tuple(x['evidence']),x['grounded'],x['authority_typed'],x['determinate_enough']) for x in packet.get('goal_candidates',[]))
        # Derive preflight only from the real native MT invocation, not a synthetic success label.
        pre=execute_direct_tool_commands('run MT',state={'packet':digest(packet)},adapters={'MT':mt})
        receipt=None
        if pre.executions:
            e=pre.executions[0]
            if e.tool_id=='MT' and e.result and e.binding.get('invocation_profile')=='FULL_CONFIGURED_HF2_V1':
                raw=e.result
                receipt=GoalMTReceipt(status=raw['status'],evidence=e.evidence,open_objects=tuple(raw['open_objects']))
        out=recover_goal_configured(candidates,receipt)
        return envelope('goal.recover_goal_configured',{'native':asdict(out),'mt_preflight':asdict(pre)},'EXECUTED' if out.status=='CLOSED_RELATIVE' else out.status,out.blocker)
    def diagnosis(current,plan):
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
    def assertion(current,plan):
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
        out=run_to_fixed_point(AssertState(),AssertStages(assert_stage,compare_stage,resolve_stage,here_stage,inquire_stage,reassert_stage),closure_gate=lambda s:all(v=='TRUE' for v in s.world.get('claim_test_status',{}).values()),max_rounds=4)
        return envelope('assert_compound.run_to_fixed_point',asdict(out),'EXECUTED' if out.status=='CLOSED' else 'OPEN')
    def trc(current,plan):
        cons=tuple(Consequence(x,'RESEARCH_VERIFICATION','verified','read-only',source_ids[0],'SOURCE_SEMANTICS') for x in packet.get('open_coordinates',()))
        out=run_tool_run_closure(tool_result={'open':len(cons)},pre_state={},post_state={},
            harvest_fn=lambda *_:cons,disposition_fn=lambda *_:Disposition.OPEN,
            realize_fn=lambda c,s:s,verify_fn=lambda c,s:s,consume_fn=lambda c,s:s,
            harvest_basis='explicit packet open coordinates',harvest_complete=False)
        return envelope('tool_run_closure.run_tool_run_closure',asdict(out),'OPEN','UNRESOLVED_SEMANTIC_OBLIGATIONS')
    def currentness(current,plan):
        receipts=tuple(assess(component=s['path'],object_identity=s['path'],built_generation=s['sha'],latest_generation=s.get('latest_sha',''),built_basis='connector blob',latest_basis='connector refetch blob',identity_verified=bool(s.get('latest_sha')),evidence=(s['sha'],s.get('latest_sha',''))) for s in packet['sources'])
        return envelope('currentness_audit.assess',{'receipts':[asdict(r) for r in receipts],'complete':audit_complete(receipts)},'EXECUTED' if audit_complete(receipts) else 'OPEN')
    def reconciler(current,plan):
        a=discriminate(); b=[(x,y) for x in qs for y in qs if x<y and all(signature((x,y),u)!=signature((x,y),v) for u,v in combinations(thresholds,2))]
        def resolver(state,admitted):
            left,right=admitted
            diff=sorted(set(left)^set(right))
            return ReconcileResult({'enumerated_pairs':len(left),'pairwise_check':len(right),'declared_count':t['declared_pair_count']},conflicts=tuple(diff),open_coordinates=() if len(left)==t['declared_pair_count'] else ('DECLARED_COUNT_MISMATCH',))
        out=reconcile({},(tuple(a['survivors']),tuple(b)),resolver)
        return envelope('reconcile.reconcile',asdict(out),'OPEN' if out.conflicts or out.open_coordinates else 'EXECUTED')
    return {'GDOS':gdos,'Discriminator':disc,'BiasPerturbation':bias,'Architecture':architecture,'MultiObject':mo,'GOAL':goal,'CurrentnessAudit':currentness,'Reconciler':reconciler,'MT':mt,'Diagnosis':diagnosis,'RTC':rtc,'ASSERT':assertion,'TRC':trc}
