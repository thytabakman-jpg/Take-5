from result_path_registry import PATHS,default_result_path,result_path

def test_exactly_one_default_result_path():
    assert default_result_path().name=="math_first"
    assert sum(p.authority=="DEFAULT_RESULT_AUTHORITY" for p in PATHS)==1

def test_legacy_facades_are_comparators_not_default_result_authority():
    assert result_path("recursive_episode").role=="COMPARATOR"
    assert result_path("inquiry_session").role=="COMPARATOR"
