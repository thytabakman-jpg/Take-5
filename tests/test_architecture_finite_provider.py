import copy
import sys
sys.path.insert(0,'runtime')
import pytest
from architecture_finite_provider import prepare_finite_architecture, invoke_finite_architecture


def packet():
    sources=[{'path':'doc.md','sha':'a'*40}]
    evidence={'source_path':'doc.md','source_sha':'a'*40,'locator':'L1','basis':'host observation'}
    spec={'components':['A'],'obligations':['q'],'baseline_ids':['base'],'authority':evidence,
          'observations':[{'id':i,'context':'ctx','state':[v],'satisfied':s,'protected':['stable'],'evidence':evidence}
                          for i,v,s in [('base','0',[]),('changed','1',['q'])]],
          'candidates':[{'id':'candidate','observation_ids':['changed']}]}
    return spec,sources


def test_source_bound_native_invocation_retains_open():
    spec,sources=packet()
    out=invoke_finite_architecture(prepare_finite_architecture(spec,sources))
    assert out['status']=='OPEN'
    assert out['result']['SuccessorFrontier']==('candidate',)
    assert ('A','q','base','changed') in out['result']['DependencyState']
    assert 'doc.md@'+'a'*40 in out['result']['Provenance']['observations']['base']


def test_missing_evidence_or_bad_candidate_is_rejected():
    spec,sources=packet()
    spec['observations'][0]['evidence']=dict(spec['authority'],source_sha='b'*40)
    with pytest.raises(ValueError,match='SOURCE_NOT_ADMITTED'):
        prepare_finite_architecture(spec,sources)
    spec,sources=packet()
    spec['candidates'][0]['observation_ids']=['unknown']
    with pytest.raises(ValueError,match='OBSERVATION_UNKNOWN'):
        prepare_finite_architecture(spec,sources)


def test_conflicting_observations_remain_conflict():
    spec,sources=packet()
    other=copy.deepcopy(spec['observations'][1])
    other.update(id='conflict',satisfied=[])
    spec['observations'].append(other)
    out=invoke_finite_architecture(prepare_finite_architecture(spec,sources))
    assert out['status']=='CONFLICT'
    assert out['result'] is None


def test_opt_in_observed_candidate_generation():
    spec,sources=packet()
    spec['candidates']=[]
    spec['generate_observed_candidates']=True
    out=invoke_finite_architecture(prepare_finite_architecture(spec,sources))
    assert out['status']=='OPEN'
    assert out['result']['SuccessorFrontier']==('observed:1',)
    witnesses=out['result']['TransformationFrontier']['generated_observed_candidates']
    assert witnesses['observed:1']['observation_ids']==('changed',)
    spec['generate_observed_candidates']=1
    with pytest.raises(ValueError,match='GENERATION_FLAG_INVALID'):
        prepare_finite_architecture(spec,sources)
    spec['generate_observed_candidates']=True
    spec['candidates']=[{'id':'candidate','observation_ids':['changed']}]
    with pytest.raises(ValueError,match='MIXED_CANDIDATE_MODES'):
        prepare_finite_architecture(spec,sources)
