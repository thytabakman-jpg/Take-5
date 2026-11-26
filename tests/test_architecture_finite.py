import sys
sys.path.insert(0,'runtime')
from architecture_finite import Observation, FiniteContract, run_finite_architecture
import pytest


def frame():
    rows=tuple(Observation(name,'ctx',state,frozenset(q),('stable',),name)
        for name,state,q in [('base',('0','0'),()),('a',('1','0'),('a',)),
        ('b',('0','1'),('b',)),('ab',('1','1'),('a','b','joint'))])
    c=FiniteContract(('A','B'),frozenset(('a','b','joint')),('base',),'test-contract',
        (('a',('a',)),('b',('b',)),('ab',('ab',))))
    return rows,c


def test_witnessed_dependency_interaction_and_dominance():
    rows,c=frame()
    out=run_finite_architecture(rows,c)
    assert out['status']=='OPEN'
    r=out['result']
    assert ('A','a','base','a') in r['DependencyState']
    assert r['InteractionState']==(('base','ab',('a','b','joint'),('a','b')),)
    assert r['SuccessorFrontier']==('ab',)
    assert r['LocalizationFamilies']['joint']


def test_missing_subintervention_does_not_claim_joint_residual():
    from dataclasses import replace
    rows,c=frame()
    out=run_finite_architecture((rows[0],rows[1],rows[3]),replace(c,candidates=()))
    assert not out['result']['InteractionState']
    assert out['status']=='OPEN'


def test_preservation_and_conflicting_state():
    from dataclasses import replace
    rows,c=frame()
    changed=(*rows[:-1],replace(rows[-1],protected=('regressed',)))
    r=run_finite_architecture(changed,c)['result']
    assert r['TransformationFrontier']['rejected']['ab']=='PROTECTED_REGRESSION'
    assert r['SuccessorFrontier']==('a','b')
    with pytest.raises(ValueError,match='OBSERVATION_CONFLICT'):
        run_finite_architecture((*rows,replace(rows[-1],identity='conflict',protected=('other',))),c)


def test_native_generation_groups_exact_observed_edits_and_retains_open():
    from dataclasses import replace
    rows=tuple(Observation(i,c,s,frozenset(q),p,i) for i,c,s,q,p in [
        ('b1','1',('0','0'),(),('P',)),('b2','2',('0','0'),(),('P',)),
        ('a1','1',('1','0'),('x',),('P',)),('a2','2',('1','0'),('x',),('P',)),
        ('c1','1',('0','1'),('y',),('P',)),('c2','2',('0','1'),('y',),('R',)),
        ('j1','1',('1','1'),('x','y'),('P',)),('dup','1',('1','0'),('x',),('P',))])
    c=FiniteContract(('A','B'),frozenset('xy'),('b1','b2'),'basis',
                     generate_observed_candidates=True)
    out=run_finite_architecture(rows,c)
    assert out['status']=='OPEN'
    result=out['result']
    f=result['TransformationFrontier']
    w=f['generated_observed_candidates']
    ids={tuple(v['edits']):k for k,v in w.items()}
    aa=ids[(('A','0','1'),)]
    bb=ids[(('B','0','1'),)]
    jj=ids[(('A','0','1'),('B','0','1'))]
    assert result['SuccessorFrontier']==(aa,)
    assert f['rejected']=={jj:'OPEN_CONTEXT_COVERAGE',bb:'PROTECTED_REGRESSION'}
    assert w[aa]['observation_ids']==('a1','a2')
    assert run_finite_architecture(tuple(reversed(rows)),c)['result']['TransformationFrontier']==f
    assert not run_finite_architecture(rows,replace(c,generate_observed_candidates=False))['result']['SuccessorFrontier']
    with pytest.raises(ValueError,match='MIXED_CANDIDATE_MODES'):
        run_finite_architecture(rows,replace(c,candidates=(('x',('a1','a2')),)))
    with pytest.raises(ValueError,match='GENERATION_FLAG_INVALID'):
        run_finite_architecture(rows,replace(c,generate_observed_candidates=1))
