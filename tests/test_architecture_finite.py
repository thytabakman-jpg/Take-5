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
