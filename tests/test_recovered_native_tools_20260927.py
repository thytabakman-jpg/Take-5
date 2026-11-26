import sys
sys.path.insert(0,"runtime")

from bias_perturbation import run_bias_perturbation
from diagnosis import diagnose
from discriminator import run_discriminator
from gdos import run_gdos
from raise_the_ceiling import raise_the_ceiling


def test_discriminator_preserves_unique_plural_and_open():
    assert run_discriminator((1,2,3),lambda x:x==2)["status"]=="UNIQUE"
    assert run_discriminator((1,2,3),lambda x:x>1)["status"]=="PLURAL"
    assert run_discriminator((1,2,3),lambda x:x>9)["status"]=="OPEN"


def test_diagnosis_is_c17_failure_mechanism_specialization():
    ok=diagnose({"failures":[{"id":"f","mechanism":"stale binding"}]})
    assert ok["status"]=="ACCEPT"
    open_result=diagnose({"failures":[{"id":"f"}]})
    assert open_result["status"]=="OPEN"


def test_raise_the_ceiling_is_c48_strict_gain_specialization():
    out=raise_the_ceiling({
        "candidates":[
            {"id":"x","strict_gain":True,"preserves":True},
            {"id":"y","strict_gain":False,"preserves":True},
        ]
    })
    assert out["status"]=="ACCEPT"
    assert [x["id"] for x in out["strict_gain_or_failure"]]==["x"]


def test_bias_perturbation_never_calls_unlicensed_difference_bias():
    out=run_bias_perturbation(
        {"meaning":"same","cue":"A"},
        (
            {"meaning":"same","cue":"B"},
            {"meaning":"different","cue":"A"},
        ),
        runner=lambda x:x["cue"],
        semantics_equivalent=lambda a,b:a["meaning"]==b["meaning"],
        result_equivalent=lambda a,b:a==b,
    )
    assert out["status"]=="OPEN"
    assert len(out["bias_sensitive"])==1
    assert len(out["unlicensed_or_unresolved"])==1


def test_gdos_freezes_and_isolates_observers_before_reconcile():
    target={"x":[1]}
    def first(x):
        x["x"].append(2)
        return {"first":tuple(x["x"])}
    def second(x):
        return {"second":tuple(x["x"])}
    out=run_gdos(
        target,
        observers=(first,second),
        reconcile_fn=lambda rows:rows,
    )
    assert out["status"]=="EXECUTED"
    assert target=={"x":[1]}
    assert out["observations"][0]["first"]==(1,2)
    assert out["observations"][1]["second"]==(1,)


def test_pd_audit_preserves_one_shot_cases_for_secondary_audit():
    from pd_audit import run_pd_audit
    out=run_pd_audit(
        iter((1,2)),rho=lambda x:x,approx=lambda a,b:a==b,
        representations={"identity":lambda x:(x,)},
        kappa_cases=lambda cases:tuple(cases),
    )
    assert out["status"]=="RELATIVE_CLOSE"
    assert out["result"]["kappa_A"]==(1,2)


def test_diagnosis_distinguishes_missing_empty_and_unresolved_inventory():
    assert diagnose({})["status"]=="OPEN"
    assert diagnose({"failures":[]})["status"]=="ACCEPT"
    for mechanism in ("UNKNOWN"," OPEN ","FAILED","",None,False):
        row={"id":"f","mechanism":mechanism}
        out=diagnose({"failures":[row]})
        assert out["status"]=="OPEN" and out["unresolved"]==[row]
    assert diagnose({"failures":[{"mechanism":"stale binding"}]})["status"]=="ACCEPT"


def test_rtc_requires_boolean_gain_and_preservation():
    assert raise_the_ceiling({})["status"]=="OPEN"
    assert raise_the_ceiling({"candidates":[]})["status"]=="NOOP"
    for gain,preserves in (("OPEN","FALSE"),("TRUE",True),(True,"FALSE"),(1,True),(True,None)):
        out=raise_the_ceiling({"candidates":[{"strict_gain":gain,"preserves":preserves}]})
        assert out["status"]=="OPEN"
    assert raise_the_ceiling({"candidates":[{"strict_gain":False,"preserves":True}]})["status"]=="NOOP"
    out=raise_the_ceiling({"candidates":[{"strict_gain":True,"preserves":True},{"strict_gain":"OPEN","preserves":True}]})
    assert out["status"]=="ACCEPT" and len(out["unresolved"])==1
