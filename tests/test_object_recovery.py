from object_recovery import recover_object_space,IdentificationStatus

def test_plural_object_space_preserves_rivals_and_common_math():
    evidence={"seen":{"a","b"}}
    candidates=(
        {"id":"x","features":{"a","b","c"},"inv":{"i1","shared"}},
        {"id":"y","features":{"a","b","d"},"inv":{"i2","shared"}},
    )
    r=recover_object_space(
        evidence,candidates,
        fit=lambda x,e:e["seen"]<=x["features"],
        equivalent=lambda a,b:a["id"]==b["id"],
        invariants=lambda x:x["inv"],
        model=lambda x:x["id"],
    )
    assert r.status==IdentificationStatus.PLURAL
    assert r.common_invariants==frozenset({"shared"})
    assert r.rival_models==("x","y")

def test_identified_only_when_one_equivalence_class_survives():
    candidates=({"id":"x","kind":"k","inv":{"s"}},{"id":"x2","kind":"k","inv":{"s","t"}})
    r=recover_object_space(
        {},candidates,
        fit=lambda x,e:True,
        equivalent=lambda a,b:a["kind"]==b["kind"],
        invariants=lambda x:x["inv"],
    )
    assert r.status==IdentificationStatus.IDENTIFIED
    assert r.common_invariants==frozenset({"s"})

def test_empty_universe_is_open_and_no_fit_is_blocked():
    assert recover_object_space({},(),fit=lambda x,e:True,equivalent=lambda a,b:a==b,invariants=lambda x:()).status==IdentificationStatus.OPEN
    assert recover_object_space({},(1,),fit=lambda x,e:False,equivalent=lambda a,b:a==b,invariants=lambda x:()).status==IdentificationStatus.BLOCKED
