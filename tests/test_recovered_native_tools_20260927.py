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
